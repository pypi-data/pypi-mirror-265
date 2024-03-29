import ast
import boto3
from botocore.exceptions import NoCredentialsError as BotoNoCredentialsError
from datetime import datetime
from functools import lru_cache
import io
import json
import os
import re
import sys
import time
from typing import Any, BinaryIO, Dict, List, Optional, Tuple
import yaml

# get_env_real_url would rely on env_utils
# from dcicutils.env_utils import get_env_real_url
from dcicutils.command_utils import yes_or_no
from dcicutils.common import APP_CGAP, APP_FOURFRONT, APP_SMAHT, OrchestratedApp
from dcicutils.file_utils import search_for_file
from dcicutils.function_cache_decorator import function_cache
from dcicutils.lang_utils import conjoined_list, disjoined_list, there_are
from dcicutils.misc_utils import (
    environ_bool, is_uuid, url_path_join, ignorable, normalize_spaces, remove_prefix
)
from dcicutils.s3_utils import HealthPageKey
from dcicutils.schema_utils import EncodedSchemaConstants, JsonSchemaConstants, Schema
from dcicutils.structured_data import Portal, StructuredDataSet
from typing_extensions import Literal
from urllib.parse import urlparse
from submitr.base import DEFAULT_APP
from submitr.exceptions import PortalPermissionError
from submitr.output import PRINT, PRINT_OUTPUT, PRINT_STDOUT, SHOW, get_output_file, setup_for_output_file_option
from submitr.progress_bar import ProgressBar
from submitr.scripts.cli_utils import get_version, print_boxed
from submitr.s3_utils import upload_file_to_aws_s3
from submitr.utils import (
    format_datetime, format_size, format_path, get_file_md5, get_file_md5_like_aws_s3_etag,
    get_file_modified_datetime, get_file_size, keyword_as_title, tobool
)


DEFAULT_INGESTION_TYPE = 'metadata_bundle'
GENERIC_SCHEMA_TYPE = 'FileOther'

# Maximum amount of time (approximately) we will wait for a response from server (seconds).
PROGRESS_TIMEOUT = 60 * 5  # five minutes (note this is for both server validation and submission)
# How often we actually check the server (seconds).
PROGRESS_CHECK_SERVER_INTERVAL = 3  # xyzzy
# How often the (tqdm) progress meter updates (seconds).
PROGRESS_INTERVAL = 1  # xyzzy
# How many times the (tqdm) progress meter updates (derived from above).
PROGRESS_MAX_CHECKS = round(PROGRESS_TIMEOUT / PROGRESS_INTERVAL)


class SubmissionProtocol:
    S3 = 's3'
    UPLOAD = 'upload'


SUBMISSION_PROTOCOLS = [SubmissionProtocol.S3, SubmissionProtocol.UPLOAD]
DEFAULT_SUBMISSION_PROTOCOL = SubmissionProtocol.UPLOAD
STANDARD_HTTP_HEADERS = {"Content-type": "application/json"}
INGESTION_SUBMISSION_TYPE_NAME = "IngestionSubmission"
FILE_TYPE_NAME = "File"


# TODO: Will asks whether some of the errors in this file that are called "SyntaxError" really should be something else.
#  The thought was that they're syntax errors because they tend to reflect as a need for a change in the
#  command line argument syntax, but maybe I should raise other errors and just have them converted to syntax
#  errors in the command itself. Something to think about another day. -kmp 8-Sep-2020


SERVER_REGEXP = re.compile(
    # Note that this regular expression does NOT contain 4dnucleome.org for the same reason it requires
    # a fourfront-cgapXXX address. It is trying only to match cgap addresses, though of course it has to make an
    # exception for localhost debugging. You're on your own to make sure the right server is connected there.
    # -kmp 16-Aug-2020
    r"^(https?://localhost(:[0-9]+)?"
    r"|https?://(fourfront-cgap|cgap-|smaht-)[a-z0-9.-]*"
    r"|https?://([a-z-]+[.])*smaht[.]org"
    r"|https?://([a-z-]+[.])*cgap[.]hms[.]harvard[.]edu)/?$"
)


# TODO: Probably should simplify this to just trust what's in the key file and ignore all other servers. -kmp 2-Aug-2023
def _resolve_server(server, env):
    return  # no longer used - using dcicutils.portal_utils.Portal instead


def _get_user_record(server, auth, quiet=False):
    """
    Given a server and some auth info, gets the user record for the authorized user.

    This works by using the /me endpoint.

    :param server: a server spec
    :param auth: auth info to be used when contacting the server
    :return: the /me page in JSON format
    """

    user_url = server + "/me?format=json"
    user_record_response = Portal(auth).get(user_url)
    try:
        user_record = user_record_response.json()
    except Exception:
        user_record = {}
    try:
        if user_record_response.status_code in (401, 403) and user_record.get("Title") == "Not logged in.":
            if not quiet:
                SHOW("Server did not recognize you with the given credentials.")
    except Exception:
        pass
    if user_record_response.status_code in (401, 403):
        raise PortalPermissionError(server=server)
    user_record_response.raise_for_status()
    user_record = user_record_response.json()
    if not quiet:
        SHOW(f"Portal server recognizes you as{' (admin)' if _is_admin_user(user_record) else ''}:"
             f" {user_record['title']} ({user_record['contact_email']})")
    return user_record


def _is_admin_user(user: dict) -> bool:
    return False if os.environ.get("SMAHT_NOADMIN") else ("admin" in user.get("groups", []))


def _get_defaulted_institution(institution, user_record, portal=None, quiet=False, verbose=False):
    """
    Returns the given institution or else if none is specified, it tries to infer an institution.

    :param institution: the @id of an institution, or None
    :param user_record: the user record for the authorized user
    :return: the @id of an institution to use
    """

    if not institution:
        institution = user_record.get('user_institution', {}).get('@id', None)
        if not institution:
            raise SyntaxError("Your user profile has no institution declared,"
                              " so you must specify --institution explicitly.")
        SHOW("Using institution:", institution)
    return institution


def _get_defaulted_project(project, user_record, portal=None, quiet=False, verbose=False):
    """
    Returns the given project or else if none is specified, it tries to infer a project.

    :param project: the @id of a project, or None
    :param user_record: the user record for the authorized user
    :return: the @id of a project to use
    """

    if not project:
        # Ref: https://hms-dbmi.atlassian.net/browse/C4-371
        # The project_roles are expected to look like:
        #  [
        #    {"project": {"@id": "/projects/foo"}, "role": "developer"},
        #    {"project": {"@id": "/projects/bar"}, "role": "clinician"},
        #    {"project": {"@id": "/projects/baz"}, "role": "director"},
        #  ]
        project_roles = user_record.get('project_roles', [])
        if len(project_roles) == 0:
            raise SyntaxError("Your user profile declares no project roles.")
        elif len(project_roles) > 1:
            raise SyntaxError("You must use --project to specify which project you are submitting for"
                              " (probably one of: %s)." % ", ".join([x['project']['@id'] for x in project_roles]))
        else:
            [project_role] = project_roles
            project = project_role['project']['@id']
            SHOW("Project is: ", project)
    return project


def _get_defaulted_award(award, user_record, portal=None, error_if_none=False, quiet=False, verbose=False):
    """
    Returns the given award or else if none is specified, it tries to infer an award.

    :param award: the @id of an award, or None
    :param user_record: the user record for the authorized user
    :param error_if_none: boolean true if failure to infer an award should raise an error, and false otherwise.
    :return: the @id of an award to use
    """

    if not award:
        # The lab is expected to have awards looking like:
        #  [
        #    {"@id": "/awards/foo", ...},
        #    {"@id": "/awards/bar", ...},
        #    {"@id": "/awards/baz", ...},
        #  ]
        lab = user_record.get('lab', {})
        lab_awards = lab.get('awards', [])
        if len(lab_awards) == 0:
            if error_if_none:
                raise SyntaxError("Your user profile declares no lab with awards.")
        elif len(lab_awards) > 1:
            options = disjoined_list([award['@id'] for award in lab_awards])
            if error_if_none:
                raise SyntaxError(f"Your lab ({lab['@id']}) declares multiple awards."
                                  f" You must explicitly specify one of {options} with --award.")
        else:
            [lab_award] = lab_awards
            award = lab_award['@id']
        if not award:
            SHOW("No award was inferred.")
        else:
            SHOW("Award is (inferred):", award)
    else:
        SHOW("Award is:", award)
    return award


def _get_defaulted_lab(lab, user_record, portal=None, error_if_none=False, quiet=False, verbose=False):
    """
    Returns the given lab or else if none is specified, it tries to infer a lab.

    :param lab: the @id of a lab, or None
    :param user_record: the user record for the authorized user
    :param error_if_none: boolean true if failure to infer a lab should raise an error, and false otherwise.
    :return: the @id of a lab to use
    """

    if not lab:
        lab = user_record.get('lab', {}).get('@id', None)
        if not lab:
            if error_if_none:
                raise SyntaxError("Your user profile has no lab declared,"
                                  " so you must specify --lab explicitly.")
            SHOW("No lab was inferred.")
        else:
            SHOW("Lab is (inferred):", lab)
    else:
        SHOW("Lab is:", lab)
    return lab


def _get_defaulted_consortia(consortia, user_record, portal=None, error_if_none=False, quiet=False, verbose=False):
    """
    Returns the given consortia or else if none is specified, it tries to infer any consortia.

    :param consortia: a list of @id's of consortia, or None
    :param user_record: the user record for the authorized user
    :param error_if_none: boolean true if failure to infer any consortia should raise an error, and false otherwise.
    :return: the @id of a consortium to use (or a comma-separated list)
    """
    def show_consortia():
        nonlocal portal
        if portal:
            if consortia := _get_consortia(portal):
                SHOW("CONSORTIA SUPPORTED:")
                for consortium in consortia:
                    SHOW(f"- {consortium.get('name')} ({consortium.get('uuid')})")
    suffix = ""
    if not consortia:
        consortia = [consortium.get('@id', None) for consortium in user_record.get('consortia', [])]
        if not consortia:
            if error_if_none:
                raise SyntaxError("Your user profile has no consortium declared,"
                                  " so you must specify --consortium explicitly.")
            SHOW("ERROR: No consortium was inferred. Use the --consortium option.")
            show_consortia()
            exit(1)
        else:
            suffix = " (inferred)"
    annotated_consortia = []
    if portal:
        for consortium in consortia:
            consortium_path = f"/Consortium/{consortium}" if not consortium.startswith("/") else consortium
            if not (consortium_object := portal.get_metadata(consortium_path, raise_exception=False)):
                SHOW(f"ERROR: Consortium not found: {consortium}")
                show_consortia()
                exit(1)
            elif consortium_name := consortium_object.get("identifier"):
                consortium_uuid = consortium_object.get("uuid")
                if verbose:
                    annotated_consortia.append(f"{consortium_name} ({consortium_uuid})")
                else:
                    annotated_consortia.append(f"{consortium_name}")
    if annotated_consortia:
        if not quiet:
            SHOW(f"Consortium is{suffix}:", ", ".join(annotated_consortia))
    else:
        if not quiet:
            SHOW(f"Consortium is{suffix}:", ", ".join(consortia))
    return consortia


def _get_defaulted_submission_centers(submission_centers, user_record, portal=None,
                                      error_if_none=False, quiet=False, verbose=False):
    """
    Returns the given submission center or else if none is specified, it tries to infer a submission center.

    :param submission_centers: the @id of a submission center, or None
    :param user_record: the user record for the authorized user
    :param error_if_none: boolean true if failure to infer a submission center should raise an error,
        and false otherwise.
    :return: the @id of a submission center to use
    """
    def show_submission_centers():
        nonlocal portal
        if portal:
            if submission_centers := _get_submission_centers(portal):
                SHOW("SUBMISSION CENTERS SUPPORTED:")
                for submission_center in submission_centers:
                    SHOW(f"- {submission_center.get('name')} ({submission_center.get('uuid')})")
    suffix = ""
    if not submission_centers:
        submits_for = [sc.get('@id', None) for sc in user_record.get('submits_for', [])]
        submission_centers = [sc.get('@id', None) for sc in user_record.get('submission_centers', [])]
        submission_centers = list(set(submits_for + submission_centers))
        if not submission_centers:
            if error_if_none:
                raise SyntaxError("Your user profile has no submission center declared,"
                                  " so you must specify --submission-center explicitly.")
            SHOW("ERROR: No submission center was inferred. Use the --submission-center option.")
            show_submission_centers()
            exit(1)
        else:
            suffix = " (inferred)"
    annotated_submission_centers = []
    if portal:
        for submission_center in submission_centers:
            submission_center_path = (
                f"/SubmissionCenter/{submission_center}"
                if not submission_center.startswith("/") else submission_center)
            if not (submission_center_object := portal.get_metadata(submission_center_path, raise_exception=False)):
                SHOW(f"ERROR: Submission center not found: {submission_center}")
                show_submission_centers()
                exit(1)
            elif submission_center_name := submission_center_object.get("identifier"):
                submission_center_uuid = submission_center_object.get("uuid")
                if verbose:
                    annotated_submission_centers.append(f"{submission_center_name} ({submission_center_uuid})")
                else:
                    annotated_submission_centers.append(f"{submission_center_name}")
    if annotated_submission_centers:
        if not quiet:
            SHOW(f"Submission center is{suffix}:", ", ".join(annotated_submission_centers))
    else:
        if not quiet:
            SHOW(f"Submission center is{suffix}:", ", ".join(submission_centers))
    return submission_centers


APP_ARG_DEFAULTERS = {
    'institution': _get_defaulted_institution,
    'project': _get_defaulted_project,
    'lab': _get_defaulted_lab,
    'award': _get_defaulted_award,
    'consortia': _get_defaulted_consortia,
    'submission_centers': _get_defaulted_submission_centers,
}


def _do_app_arg_defaulting(app_args, user_record, portal=None, quiet=False, verbose=False):
    for arg in list(app_args.keys()):
        val = app_args[arg]
        defaulter = APP_ARG_DEFAULTERS.get(arg)
        if defaulter:
            val = defaulter(val, user_record, portal, quiet=quiet, verbose=verbose)
            if val:
                app_args[arg] = val
            elif val is None:
                del app_args[arg]


PROGRESS_CHECK_INTERVAL = 7  # seconds
ATTEMPTS_BEFORE_TIMEOUT = 100
ATTEMPTS_BEFORE_TIMEOUT = 4


def _get_section(res, section):
    """
    Given a description of an ingestion submission, returns a section name within that ingestion.

    :param res: the description of an ingestion submission as a python dictionary that represents JSON data
    :param section: the name of a section to find either in the toplevel or in additional_data.
    :return: the section's content
    """

    return res.get(section) or res.get('additional_data', {}).get(section)


def _show_section(res, section, caveat_outcome=None, portal=None):
    """
    Shows a given named section from a description of an ingestion submission.

    The caveat is used when there has been an error and should be a phrase that describes the fact that output
    shown is only up to the point of the caveat situation. Instead of a "My Heading" header the output will be
    "My Heading (prior to <caveat>)."

    :param res: the description of an ingestion submission as a python dictionary that represents JSON data
    :param section: the name of a section to find either in the toplevel or in additional_data.
    :param caveat_outcome: a phrase describing some caveat on the output
    """

    section_data = _get_section(res, section)
    if caveat_outcome and not section_data:
        # In the case of non-success, be brief unless there's data to show.
        return
    if caveat_outcome:
        caveat = " (prior to %s)" % caveat_outcome
    else:
        caveat = ""
    if not section_data:
        return
    SHOW("\n----- %s%s -----" % (keyword_as_title(section), caveat))
    if isinstance(section_data, dict):
        if file := section_data.get("file"):
            PRINT(f"File: {file}")
        if s3_file := section_data.get("s3_file"):
            PRINT(f"S3 File: {s3_file}")
        if details := section_data.get("details"):
            PRINT(f"Details: {details}")
        for item in section_data:
            if isinstance(section_data[item], list) and section_data[item]:
                issue_prefix = ""
                if item == "reader":
                    PRINT(f"Parser Warnings:")
                    issue_prefix = "WARNING: "
                elif item == "validation":
                    PRINT(f"Validation Errors:")
                    issue_prefix = "ERROR: "
                elif item == "ref":
                    PRINT(f"Reference (linkTo) Errors:")
                    issue_prefix = "ERROR: "
                elif item == "errors":
                    PRINT(f"Other Errors:")
                    issue_prefix = "ERROR: "
                else:
                    continue
                for issue in section_data[item]:
                    if isinstance(issue, dict):
                        PRINT(f"- {issue_prefix}{_format_issue(issue, file)}")
                    elif isinstance(issue, str):
                        PRINT(f"- {issue_prefix}{issue}")
    elif isinstance(section_data, list):
        if section == "upload_info":
            for info in section_data:
                if isinstance(info, dict) and info.get("filename") and (uuid := info.get("uuid")):
                    upload_file_accession_name, upload_file_type = _get_upload_file_info(portal, uuid)
                    info["target"] = upload_file_accession_name
                    info["type"] = upload_file_type
            PRINT(yaml.dump(section_data))
        else:
            [SHOW(line) for line in section_data]
    else:  # We don't expect this, but such should be shown as-is, mostly to see what it is.
        SHOW(section_data)


def _ingestion_submission_item_url(server, uuid):
    return url_path_join(server, "ingestion-submissions", uuid) + "?format=json"


# TRY_OLD_PROTOCOL = True
DEBUG_PROTOCOL = environ_bool("DEBUG_PROTOCOL", default=False)


def _initiate_server_ingestion_process(
        portal: Portal,
        ingestion_filename: str,
        consortia: Optional[List[str]] = None,
        submission_centers: Optional[List[str]] = None,
        is_server_validation: bool = False,
        is_resume_submission: bool = False,
        validation_ingestion_submission_object: Optional[dict] = None,
        post_only: bool = False,
        patch_only: bool = False,
        autoadd: Optional[dict] = None,
        datafile_size: Optional[Any] = None,
        datafile_md5: Optional[Any] = None,
        debug: bool = False) -> str:

    if isinstance(validation_ingestion_submission_object, dict):
        # This ingestion action is for a submission (rather than for a validation),
        # and we were given an associated validation UUID (i.e. from a previous client
        # initiated server validation); so we record this validation UUID in the actual
        # submission IngestionSubmission object (to be created just below); and we will
        # do the converse below, after the submission IngestionSubmission object creation.
        validation_ingestion_submission_uuid = validation_ingestion_submission_object.get("uuid", None)
        if not (isinstance(validation_parameters := validation_ingestion_submission_object.get("parameters"), dict)):
            validation_parameters = None
    else:
        validation_ingestion_submission_object = None
        validation_ingestion_submission_uuid = None
        validation_parameters = None

    submission_post_data = {
        "validate_only": is_server_validation,
        "post_only": post_only,
        "patch_only": patch_only,
        "ref_nocache": False,  # Do not do this server-side at all; only client-side for testing.
        "autoadd": json.dumps(autoadd),
        "ingestion_directory": os.path.dirname(ingestion_filename) if ingestion_filename else None,
        "datafile_size": datafile_size or get_file_size(ingestion_filename),
        "datafile_md5": datafile_md5 or get_file_md5(ingestion_filename)
    }

    if validation_ingestion_submission_uuid:
        submission_post_data["validation_uuid"] = validation_ingestion_submission_uuid

    if is_resume_submission and validation_ingestion_submission_object:
        if validation_parameters := validation_ingestion_submission_object.get("parameters"):
            submission_post_data["validation_datafile"] = validation_parameters.get("datafile")
            submission_post_data["ingestion_directory"] = validation_parameters.get("ingestion_directory")

    response = _post_submission(portal=portal,
                                is_resume_submission=is_resume_submission,
                                ingestion_filename=ingestion_filename,
                                consortia=consortia,
                                submission_centers=submission_centers,
                                submission_post_data=submission_post_data,
                                is_server_validation=is_server_validation, debug=debug)
    submission_uuid = response["submission_id"]

    if validation_ingestion_submission_uuid and validation_parameters:
        # This ingestion action is for a submission (rather than for a validation),
        # and we were given an associated validation UUID (i.e. from a previous client
        # initiated server validation); so we record the associated submission UUID,
        # created just above, in the validation IngestionSubmission object (via PATCH).
        validation_parameters["submission_uuid"] = submission_uuid
        validation_parameters = {"parameters": validation_parameters}
        portal.patch_metadata(object_id=validation_ingestion_submission_uuid, data=validation_parameters)

    return submission_uuid


def _post_submission(portal: Portal,
                     ingestion_filename: str,
                     consortia: List[str],
                     submission_centers: List[str],
                     submission_post_data: dict,
                     ingestion_type: str = DEFAULT_INGESTION_TYPE,
                     submission_protocol: str = DEFAULT_SUBMISSION_PROTOCOL,
                     is_server_validation: bool = False,
                     is_resume_submission: bool = False,
                     debug: bool = False):
    creation_post_data = {
        "ingestion_type": ingestion_type,
        "processing_status": {"state": "submitted"},
        "consortia": consortia,
        "submission_centers": submission_centers
    }
    if is_server_validation:
        creation_post_data["parameters"] = {"validate_only": True}
    # This creates the IngestionSubmission object.
    creation_post_url = url_path_join(portal.server, INGESTION_SUBMISSION_TYPE_NAME)
    creation_response = portal.post(creation_post_url, json=creation_post_data, raise_for_status=True)
    [submission] = creation_response.json()['@graph']
    submission_id = submission['@id']
    if debug:
        PRINT(f"DEBUG: Created ingestion submission object: {submission_id}")
    # This actually kicks off the ingestion process and updates the IngestionSubmission object created above.
    new_style_submission_url = url_path_join(portal.server, submission_id, "submit_for_ingestion")
    if debug:
        if is_server_validation:
            PRINT(f"DEBUG: Initiating server validation process.")
        elif is_resume_submission:
            PRINT(f"DEBUG: Initiating server submission process after server validation timeout.")
        else:
            PRINT(f"DEBUG: Initiating server submission process.")
    if is_resume_submission:
        # Dummy /dev/null file when "resuming" submission after server validation timed out.
        file_post_data = _post_files_data(submission_protocol=submission_protocol, ingestion_filename=None)
    else:
        file_post_data = _post_files_data(submission_protocol=submission_protocol,
                                          ingestion_filename=ingestion_filename)
    response = portal.post(new_style_submission_url,
                           data=submission_post_data,
                           files=file_post_data,
                           headers=None, raise_for_status=True)
    if debug:
        PRINT(f"DEBUG: Initiated server {'validation' if is_server_validation else 'submission'} process.")
    return response.json()


def _post_files_data(submission_protocol, ingestion_filename) -> Dict[Literal['datafile'], Optional[BinaryIO]]:
    """
    This composes a dictionary of the form {'datafile': <maybe-stream>}.

    If the submission protocol is SubmissionProtocol.UPLOAD (i.e., 'upload'), the given ingestion filename is opened
    and used as the datafile value in the dictionary. If it is something else, no file is opened and None is used.

    :param submission_protocol:
    :param ingestion_filename:
    :return: a dictionary with key 'datafile' whose value is either an open binary input stream or None
    """
    if submission_protocol == SubmissionProtocol.UPLOAD:
        if ingestion_filename:
            return {"datafile": io.open(ingestion_filename, 'rb')}
        else:
            return {"datafile": io.open("/dev/null", "rb")}
    else:
        return {"datafile": None}


def _resolve_app_args(institution, project, lab, award, app, consortium, submission_center):

    app_args = {}
    if app == APP_CGAP:
        required_args = {'institution': institution, 'project': project}
        unwanted_args = {'lab': lab, 'award': award,
                         'consortium': consortium, 'submission_center': submission_center}
    elif app == APP_FOURFRONT:
        required_args = {'lab': lab, 'award': award}
        unwanted_args = {'institution': institution, 'project': project,
                         'consortium': consortium, 'submission_center': submission_center}
    elif app == APP_SMAHT:

        def splitter(x):
            return None if x is None else [y for y in [x.strip() for x in x.split(',')] if y]

        consortia = None if consortium is None else splitter(consortium)
        submission_centers = None if submission_center is None else splitter(submission_center)
        required_args = {'consortia': consortia, 'submission_centers': submission_centers}
        unwanted_args = {'institution': institution, 'project': project,
                         'lab': lab, 'award': award}
    else:
        raise ValueError(f"Unknown application: {app}")

    for argname, argvalue in required_args.items():
        app_args[argname] = argvalue

    extra_keys = []
    for argname, argvalue in unwanted_args.items():
        if argvalue:
            # We use '-', not '_' in the user interface for argument names,
            # so --submission_center will need --submission-center
            ui_argname = argname.replace('_', '-')
            extra_keys.append(f"--{ui_argname}")

    if extra_keys:
        raise ValueError(there_are(extra_keys, kind="inappropriate argument", joiner=conjoined_list, punctuate=True))

    return app_args


def submit_any_ingestion(ingestion_filename, *,
                         ingestion_type,
                         server,
                         env,
                         institution=None,
                         project=None,
                         lab=None,
                         award=None,
                         consortium=None,
                         submission_center=None,
                         app: OrchestratedApp = None,
                         upload_folder=None,
                         no_query=False,
                         subfolders=False,
                         submission_protocol=DEFAULT_SUBMISSION_PROTOCOL,
                         submit=False,
                         validate_local_only=False,
                         validate_remote_only=False,
                         validate_local_skip=False,
                         validate_remote_skip=False,
                         post_only=False,
                         patch_only=False,
                         keys_file=None,
                         show_details=False,
                         noanalyze=False,
                         json_only=False,
                         ref_nocache=False,
                         verbose_json=False,
                         verbose=False,
                         noprogress=False,
                         output_file=None,
                         env_from_env=False,
                         timeout=None,
                         debug=False,
                         debug_sleep=None):

    """
    Does the core action of submitting a metadata bundle.

    :param ingestion_filename: the name of the main data file to be ingested
    :param ingestion_type: the type of ingestion to be performed (an ingestion_type in the IngestionSubmission schema)
    :param server: the server to upload to
    :param env: the portal environment to upload to
    :param validate_remote_only: whether to do stop after validation instead of proceeding to post metadata
    :param app: an orchestrated app name
    :param institution: the @id of the institution for which the submission is being done (when app='cgap')
    :param project: the @id of the project for which the submission is being done (when app='cgap')
    :param lab: the @id of the lab for which the submission is being done (when app='fourfront')
    :param award: the @id of the award for which the submission is being done (when app='fourfront')
    :param consortium: the @id of the consortium for which the submission is being done (when app='smaht')
    :param submission_center: the @id of the submission_center for which the submission is being done (when app='smaht')
    :param upload_folder: folder in which to find files to upload (default: same as bundle_filename)
    :param no_query: bool to suppress requests for user input
    :param subfolders: bool to search subdirectories within upload_folder for files
    :param submission_protocol: which submission protocol to use (default: 's3')
    :param show_details: bool controls whether to show the details from the results file in S3.
    """

    """
    if app is None:  # Better to pass explicitly, but some legacy situations might require this to default
        app = DEFAULT_APP
        app_default = True
    else:
        app_default = False
        PRINT(f"App name is: {app}")
    """
    validation = not submit

    # Setup for output to specified output file, in addition to stdout),
    # except in this case we will not output large amounts of output to stdout.
    if output_file:
        global PRINT, PRINT_OUTPUT, PRINT_STDOUT, SHOW
        PRINT, PRINT_OUTPUT, PRINT_STDOUT, SHOW = setup_for_output_file_option(output_file)

    portal = _define_portal(env=env, env_from_env=env_from_env, server=server, app=app,
                            keys_file=keys_file, report=not json_only or verbose, verbose=verbose,
                            note="Metadata Validation" if validation else "Metadata Submission")

    app_args = _resolve_app_args(institution=institution, project=project, lab=lab, award=award, app=portal.app,
                                 consortium=consortium, submission_center=submission_center)

    if not portal.ping():
        SHOW(f"Portal credentials do not seem to work: {portal.keys_file} ({env})")
        exit(1)

    user_record = _get_user_record(portal.server, auth=portal.key_pair, quiet=json_only and not verbose)
    # Nevermind: Too confusing for both testing and general usage
    # to have different behaviours for admin and non-admin users.
    # is_admin_user = _is_admin_user(user_record)
    exit_immediately_on_errors = True
    if validate_local_only or validate_remote_skip:
        if validate_remote_only or validate_local_skip:
            PRINT("WARNING: Skipping all validation is definitely not recommended.")
        else:
            PRINT("WARNING: Skipping remote (server) validation is not recommended.")
    elif validate_remote_only or validate_local_skip:
        PRINT("WARNING: Skipping local (client) validation is not recommended.")

    if debug:
        PRINT(f"DEBUG: submit = {submit}")
        PRINT(f"DEBUG: validation = {validation}")
        PRINT(f"DEBUG: validate_local_only = {validate_local_only}")
        PRINT(f"DEBUG: validate_remote_only = {validate_remote_only}")
        PRINT(f"DEBUG: validate_local_skip = {validate_local_skip}")
        PRINT(f"DEBUG: validate_remote_skip = {validate_remote_skip}")

    metadata_bundles_bucket = get_metadata_bundles_bucket_from_health_path(key=portal.key)
    if not _do_app_arg_defaulting(app_args, user_record, portal, quiet=json_only and not verbose, verbose=verbose):
        pass
    if not json_only:
        PRINT(f"Submission file to {'validate' if validation else 'ingest'}: {format_path(ingestion_filename)}")

    autoadd = None
    if app_args and isinstance(submission_centers := app_args.get("submission_centers"), list):
        if len(submission_centers) == 1:
            def extract_identifying_value_from_path(path: str) -> str:
                if path.endswith("/"):
                    path = path[:-1]
                parts = path.split("/")
                return parts[-1] if parts else ""
            autoadd = {"submission_centers": [extract_identifying_value_from_path(submission_centers[0])]}
        elif len(submission_centers) > 1:
            PRINT(f"Multiple submission centers: {', '.join(submission_centers)}")
            PRINT(f"You must specify onely one submission center using the --submission-center option.")
            exit(1)
    if verbose:
        SHOW(f"Metadata bundle upload bucket: {metadata_bundles_bucket}")

    if not validate_remote_only and not validate_local_skip:
        structured_data = _validate_locally(ingestion_filename, portal,
                                            validation=validation,
                                            validate_local_only=validate_local_only,
                                            autoadd=autoadd, upload_folder=upload_folder, subfolders=subfolders,
                                            exit_immediately_on_errors=exit_immediately_on_errors,
                                            ref_nocache=ref_nocache, output_file=output_file, noprogress=noprogress,
                                            noanalyze=noanalyze, json_only=json_only, verbose_json=verbose_json,
                                            verbose=verbose, debug=debug, debug_sleep=debug_sleep)
        if validate_local_only:
            # We actually do exit from _validate_locally if validate_local_only is True.
            # This return is just emphasize that fact.
            return
    else:
        PRINT(f"Skipping local (client) validation (as requested via"
              f" {'--validate-remote-only' if validate_remote_only else '--validate-local-skip'}).")

    # Nevermind: Too confusing for both testing and general usage
    # to have different behaviours for admin and non-admin users.
    # if is_admin_user and not no_query:
    #     # More feedback/points-of-contact for admin users; more automatic for non-admin.
    #     if not yes_or_no(f"Continue with server {'validation' if validation else 'submission'}"
    #                      f" against {portal.server}?"):
    #         SHOW("Aborting before server validation.")
    #         exit(1)

    # Server validation.

    if not validate_local_only and not validate_remote_skip:

        SHOW(f"Continuing with additional (server) validation: {portal.server}")

        validation_uuid = _initiate_server_ingestion_process(
            portal=portal,
            ingestion_filename=ingestion_filename,
            is_server_validation=True,
            consortia=app_args.get("consortia"),
            submission_centers=app_args.get("submission_centers"),
            post_only=post_only,
            patch_only=patch_only,
            autoadd=autoadd,
            debug=debug)

        SHOW(f"Validation tracking ID: {validation_uuid}")

        server_validation_done, server_validation_status, server_validation_response = _monitor_ingestion_process(
                validation_uuid, portal.server, portal.env, app=portal.app, keys_file=portal.keys_file,
                show_details=show_details, report=False, messages=True,
                validation=True,
                nofiles=True, noprogress=noprogress, timeout=timeout,
                verbose=verbose, debug=debug, debug_sleep=debug_sleep)

        if server_validation_status != "success":
            exit(1)

        PRINT("Validation results (server): OK")

    else:
        server_validation_response = None
        PRINT("Skipping remote (server) validation (as requested via"
              f" {'--validate-local-only' if validate_local_only else '--validate-remote-skip'}).")

    if validation:
        exit(0)

    # Server submission.

    SHOW(f"Ready to submit your metadata to {portal.server}: {format_path(ingestion_filename)}")
    if not yes_or_no("Continue on with the actual submission?"):
        exit(0)

    submission_uuid = _initiate_server_ingestion_process(
        portal=portal,
        ingestion_filename=ingestion_filename,
        is_server_validation=False,
        validation_ingestion_submission_object=server_validation_response,
        consortia=app_args.get("consortia"),
        submission_centers=app_args.get("submission_centers"),
        post_only=post_only,
        patch_only=patch_only,
        autoadd=autoadd,
        debug=debug)

    SHOW(f"Submission tracking ID: {submission_uuid}")

    submission_done, submission_status, submission_response = _monitor_ingestion_process(
            submission_uuid, portal.server, portal.env, app=portal.app, keys_file=portal.keys_file,
            show_details=show_details, report=False, messages=True,
            validation=False,
            nofiles=True, noprogress=noprogress, timeout=timeout,
            verbose=verbose, debug=debug, debug_sleep=debug_sleep)

    if submission_status != "success":
        exit(1)

    PRINT("Submission complete!")

    # Now that submission has successfully complete, review the files to upload and then do it.

    _review_upload_files(structured_data, ingestion_filename,
                         validation=validation, directory=upload_folder, recursive=subfolders)

    do_any_uploads(submission_response, keydict=portal.key, ingestion_filename=ingestion_filename,
                   upload_folder=upload_folder, no_query=no_query,
                   subfolders=subfolders, portal=portal)


def _get_recent_submissions(portal: Portal, count: int = 30, name: Optional[str] = None) -> List[dict]:
    url = f"/search/?type=IngestionSubmission&sort=-date_created&from=0&limit={count}"
    if name:
        # TODO: Does not seem to return the same stuff; of not great consequence yet.
        url += f"&q={name}"
    if submissions := portal.get_metadata(url):
        if submissions := submissions.get("@graph"):
            return submissions
    return []


def _print_recent_submissions(portal: Portal, count: int = 30, message: Optional[str] = None,
                              details: bool = False, verbose: bool = False,
                              mine: bool = False, user: Optional[str] = None) -> bool:
    user_name = None
    if mine:
        try:
            user_record = _get_user_record(portal.server, auth=portal.key_pair, quiet=True)
            user_name = user_record.get("display_title")
        except Exception:
            PRINT(f"Cannot find your user info.")
            exit(1)
    elif user:
        if "@" in user or is_uuid(user):
            try:
                user_record = portal.get_metadata(f"/users/{user.lower()}")
                user_name = user_record.get("display_title")
            except Exception:
                PRINT(f"Cannot find user info: {user}")
                exit(1)
        else:
            user_name = user

    lines = []
    if submissions := _get_recent_submissions(portal, count, name=user_name):
        if message:
            PRINT(message)
        lines.append("===")
        lines.append("Recent Submissions [COUNT]")
        lines.append("===")
        index = 0
        for submission in submissions:
            if details and (index > 0):
                lines.append("===")
            if verbose:
                PRINT()
                _print_submission_summary(portal, submission)
                continue
            submission_uuid = submission.get("uuid")
            submission_created = submission.get("date_created")
            line = f"{submission_uuid}: {_format_portal_object_datetime(submission_created)}"
            if tobool(submission.get("parameters", {}).get("validate_only")):
                line += f" (V)"
            else:
                line += f" (S)"
            if submission.get("processing_status", {}).get("outcome") == "success":
                line += f" ▶ OK"
            lines.append(line)
            if details:
                line_detail = ""
                if submitted_by := submission.get("submitted_by", {}).get("display_title"):
                    if line_detail:
                        line_detail += " | "
                    line_detail += f"{submitted_by}"
                if ((submission_params := submission.get("parameters")) and
                    (submission_file := submission_params.get("datafile"))):  # noqa
                    if submission_file == "null":
                        if validation_datafile := submission_params.get("validation_datafile"):
                            # was_server_validation_timeout = True
                            submission_file = f"{validation_datafile} (ω)"
                    if line_detail:
                        line_detail += " | "
                    line_detail += f"{submission_file}"
                if line_detail:
                    lines.append(line_detail)
            index += 1
        if not verbose:
            lines.append("===")
            print_boxed(lines, right_justified_macro=("[COUNT]", lambda: f"Showing: {len(submissions)}"))
        return True
    return False


def _monitor_ingestion_process(uuid: str, server: str, env: str, keys_file: Optional[str] = None,
                               app: Optional[OrchestratedApp] = None,
                               show_details: bool = False,
                               validation: bool = False,
                               env_from_env: bool = False,
                               report: bool = True, messages: bool = False,
                               nofiles: bool = False, noprogress: bool = False,
                               check_submission_script: bool = False,
                               upload_directory: Optional[str] = None,
                               upload_directory_recursive: bool = False,
                               timeout: Optional[int] = None,
                               verbose: bool = False, debug: bool = False,
                               note: Optional[str] = None,
                               debug_sleep: Optional[int] = None) -> Tuple[bool, str, dict]:

    if timeout:
        global PROGRESS_TIMEOUT, PROGRESS_MAX_CHECKS
        PROGRESS_TIMEOUT = timeout
        PROGRESS_MAX_CHECKS = max(round(PROGRESS_TIMEOUT / PROGRESS_INTERVAL), 1)

    def define_progress_callback(max_checks: int, title: str, include_status: bool = False) -> None:
        bar = ProgressBar(max_checks, "Calculating", interrupt_exit=True)
        nchecks = 0
        nchecks_server = 0
        check_status = "Unknown"
        next_check = 0
        # From (new/2024-03-25) /ingestion-status/{submission_uuid} call.
        ingestion_total = 0
        ingestion_started = 0
        ingestion_started_second_round = 0
        def progress_report(status: dict) -> None:  # noqa
            nonlocal bar, max_checks, nchecks, nchecks_server, next_check, check_status, noprogress, validation
            nonlocal ingestion_total, ingestion_started, ingestion_started_second_round, verbose
            if noprogress:
                return
            # This are from the (new/2024-03-25) /ingestion-status/{submission_uuid} call.
            # These key name come ultimately from snovault.loadxl.PROGRESS (minus "ingestion_" prefix).
            ingestion_total = ingestion_status.get("ingestion_total", 0)
            ingestion_started = ingestion_status.get("ingestion_start", 0)
            ingestion_item = ingestion_status.get("ingestion_item", 0)
            ingestion_started_second_round = ingestion_status.get("ingestion_start_second_round", 0)
            ingestion_item_second_round = ingestion_status.get("ingestion_item_second_round", 0)
            ingestion_done = status.get("ingestion_done", 0) > 0
            # This string is from the /ingestion-status endpoint, really as a convenience/courtesey
            # so we don't have to cobble together our own string; but we could also build the
            # message ourselves manually here from the counts contained in the same response.
            ingestion_message = (status.get("ingestion_message_verbose", "")
                                 if verbose else status.get("ingestion_message", ""))
            # Phases: 0 means waiting for server response; 1 means loadxl round one; 2 means loadxl round two.
            ingestion_phase = 2 if ingestion_started_second_round > 0 else (1 if ingestion_started > 0 else 0)
            done = False
            if status.get("finish") or nchecks >= max_checks:
                check_status = status.get("status")
                if ingestion_phase == 0:
                    bar.increment_progress(max_checks - nchecks)
                done = True
            elif status.get("check_server"):
                check_status = status.get("status")
                nchecks_server += 1
            elif status.get("check"):
                if (next_check := status.get("next")) is not None:
                    next_check = round(status.get("next") or 0)
                nchecks += 1
                if ingestion_phase == 0:
                    bar.increment_progress(1)
            message = f"▶ {title} Pings: {nchecks_server}"
            if ingestion_started == 0:
                message += f" | Waiting on server"
            else:
                if ingestion_done:
                    bar.set_total(ingestion_total)
                    bar.set_progress(ingestion_total)
                elif ingestion_phase == 2:
                    bar.set_total(ingestion_total)
                    bar.set_progress(ingestion_item_second_round)
                elif ingestion_phase == 1:
                    bar.set_total(ingestion_total)
                    bar.set_progress(ingestion_item)
                if ingestion_message:
                    message += " | " + ingestion_message
            if include_status:
                message += f" | Status: {check_status}"
            # message += f" | Next: {'Now' if next_check == 0 else str(next_check) + 's'} ‖ Progress"
            bar.set_description(message)
            if done:
                bar.done()
        return progress_report

    portal = _define_portal(env=env, server=server, app=app or DEFAULT_APP,
                            env_from_env=env_from_env, report=report, note=note)

    if not (uuid_metadata := portal.get_metadata(uuid)):
        message = f"Submission ID not found: {uuid}" if uuid != "dummy" else "No submission ID specified."
        if _print_recent_submissions(portal, message=message):
            return
        raise Exception(f"Cannot find object given uuid: {uuid}")
    if not portal.is_schema_type(uuid_metadata, INGESTION_SUBMISSION_TYPE_NAME):
        undesired_type = portal.get_schema_type(uuid_metadata)
        raise Exception(f"Given ID is not for a submission or validation: {uuid} ({undesired_type})"
                        f" | Accession: {uuid_metadata.get('accession')}")
    if tobool(uuid_metadata.get("parameters", {}).get("validate_only")):
        validation = True

    action = "validation" if validation else "ingestion"
    if validation:
        SHOW(f"Waiting (up to about {PROGRESS_TIMEOUT}s) for server validation results.")
    else:
        SHOW(f"Waiting (up to about {PROGRESS_TIMEOUT}s) for submission results.")
        # SHOW(f"Checking {action} for submission ID: %s ..." % uuid)

    started = time.time()
    progress = define_progress_callback(PROGRESS_MAX_CHECKS,
                                        title="Validation" if validation else "Submission",
                                        include_status=False)  # include_status=not validation
    most_recent_server_check_time = None
    check_submission_script_initial_check_ran = False
    check_done = False
    check_status = None
    check_response = None
    ingestion_status = {}
    for n in range(PROGRESS_MAX_CHECKS):
        if ((most_recent_server_check_time is None) or
            ((time.time() - most_recent_server_check_time) >= PROGRESS_CHECK_SERVER_INTERVAL)):  # noqa
            if most_recent_server_check_time is None:
                progress({"start": True, **ingestion_status})
            else:
                progress({"check_server": True, "status": (check_status or "unknown").title(), **ingestion_status})
            # Do the actual portal check here (i.e by fetching the IngestionSubmission object)..
            [check_done, check_status, check_response] = (
                _check_ingestion_progress(uuid, keypair=portal.key_pair, server=portal.server))
            # Do the (new/2024-03-25) portal ingestion-status check here which reads
            # from Redis where the ingester is (now/2024-03-25) writing.
            ingestion_status = portal.get(f"/ingestion-status/{uuid}").json()
            ingestion_status = {"ingestion_" + key: value for key, value in ingestion_status.items()}
            if check_done:
                break
            if check_submission_script:
                if not check_submission_script_initial_check_ran:
                    check_submission_script_initial_check_ran = True
                    PRINT(f"This ID is for a server validation that had not yet completed; waiting for completion.")
                    PRINT(f"Details for this server validation ({uuid}) below:")
                    _print_submission_summary(portal, check_response, nofiles=nofiles,
                                              check_submission_script=True, verbose=verbose, debug=debug)
            most_recent_server_check_time = time.time()
        progress({"check": True,
                  "next": PROGRESS_CHECK_SERVER_INTERVAL - (time.time() - most_recent_server_check_time),
                  **ingestion_status})
        time.sleep(PROGRESS_INTERVAL)
    if check_done:
        progress({"finish": True, "done": True,
                  "status": (check_status or "unknown").title(), "response": check_response, **ingestion_status})
    else:
        progress({"finish": True, **ingestion_status})

    if not check_done:
        command_summary = _summarize_submission(uuid=uuid, server=server, env=env, app=portal.app)
        SHOW(f"Timed out (after {round(time.time() - started)}s) WAITING for {action}.")
        SHOW(f"Your {'validation' if validation else 'submission'} is still running on the server.")
        SHOW(f"Use this command to check its status: {command_summary}")
        exit(1)

    if (check_submission_script and check_response and
        (check_parameters := check_response.get("parameters", {})) and
        tobool(check_parameters.get("validate_only")) and
        not check_parameters.get("submission_uuid")):  # noqa
        # This is the check-submission script waiting for a VALIDATION (not a submission)
        # to complete, i.e. the server validation part of submit-metadata-bundle had timed
        # out previously. And this which server validation is now complete. We now want
        # to give the user the opportunity to continue with the submission process,
        # ala submit_any_ingestion; see around line 830 of that function.
        if not check_submission_script_initial_check_ran:
            check_submission_script_initial_check_ran = True
            PRINT(f"This ID is for a server validation that had not yet completed but now is.")
            PRINT(f"Details for this server validation ({uuid}) below:")
            _print_submission_summary(portal, check_response, nofiles=nofiles,
                                      check_submission_script=True, include_errors=True,
                                      verbose=verbose, debug=debug)
        validation_info = check_response.get("additional_data", {}).get("validation_output")
        # TODO: Cleanup/unify error structure from client and server!
        if isinstance(validation_info, list):
            validation_errors = [item for item in validation_info if item.lower().startswith("errored")]
            if validation_errors:
                PRINT("\nServer validation errors were encountered for this metadata.")
                PRINT("You will need to correct any errors and resubmit via submit-metadata-bundle.")
                exit(1)
        elif isinstance(validation_info, dict):
            if validation_info.get("ref") or validation_info.get("validation"):
                PRINT("\nServer validation errors were encountered for this metadata.")
                PRINT("You will need to correct any errors and resubmit via submit-metadata-bundle.")
                exit(1)
        PRINT("Validation results (server): OK")
        if not yes_or_no("Do you want to now continue with the submission for this metadata?"):
            PRINT("Exiting with no action.")
            exit(0)
        # Get parameters for this submission from the validation IngestionSubmission object.
        consortia = None
        submission_centers = None
        if consortium := check_parameters.get("consortium"):
            consortia = [consortium]
        if submission_center := check_parameters.get("submission_center"):
            submission_centers = [submission_center]
        if debug:
            PRINT("DEBUG: Continuing with submission process after a previous server validation timeout.")
        submission_uuid = _initiate_server_ingestion_process(
            portal=portal,
            ingestion_filename=None,
            is_server_validation=False,
            is_resume_submission=True,
            validation_ingestion_submission_object=check_response,
            consortia=consortia,
            submission_centers=submission_centers,
            autoadd=check_parameters.get("autoadd"),
            datafile_size=check_parameters.get("datafile_size"),
            datafile_md5=check_parameters.get("datafile_md5"))
        SHOW(f"Submission tracking ID: {submission_uuid}")
        submission_done, submission_status, submission_response = _monitor_ingestion_process(
                submission_uuid, portal.server, portal.env, app=portal.app, keys_file=portal.keys_file,
                show_details=show_details, report=False, messages=True,
                validation=False,
                nofiles=True, noprogress=noprogress, timeout=timeout,
                verbose=verbose, debug=debug, debug_sleep=debug_sleep)
        if submission_status != "success":
            exit(1)
        PRINT("Submission complete!")
        do_any_uploads(submission_response, keydict=portal.key,
                       upload_folder=upload_directory, subfolders=upload_directory_recursive, portal=portal)
        return

    if check_submission_script or debug or not validation:
        _print_submission_summary(portal, check_response,
                                  nofiles=nofiles, check_submission_script=check_submission_script,
                                  verbose=verbose, debug=debug)

    # If not sucessful then output any validation/submission results.
    if check_status != "success":
        PRINT(f"{'Validation' if validation else 'Submission'} results (server): ERROR"
              f"{f' ({check_status})' if check_status not in ['failure', 'error'] else ''}")
        printed_newline = False
        if check_response and (additional_data := check_response.get("additional_data")):
            if (validation_info := additional_data.get("validation_output")):
                if isinstance(validation_info, list):
                    if errors := [info for info in validation_info if info.lower().startswith("error:")]:
                        if not printed_newline:
                            PRINT_OUTPUT()
                            printed_newline = True
                        for error in errors:
                            PRINT_OUTPUT(f"- {_format_server_error(error, indent=2)}")
                elif isinstance(validation_info, dict):
                    if ((validation_errors := validation_info.get("validation")) and
                        isinstance(validation_errors, list) and validation_errors):  # noqa
                        if not printed_newline:
                            PRINT_OUTPUT()
                            printed_newline = True
                        PRINT_OUTPUT(f"- Data errors: {len(validation_errors)}")
                        for validation_error in validation_errors:
                            PRINT_OUTPUT(f"    - {_format_issue(validation_error)}")
                    if debug:
                        ref_errors = validation_info.get("ref")
                    elif not (ref_errors := validation_info.get("ref_grouped")):
                        ref_errors = validation_info.get("ref")
                    if ref_errors and (ref_errors := _validate_references(ref_errors, None, debug=debug)):
                        if not printed_newline:
                            PRINT_OUTPUT()
                            printed_newline = True
                        _print_reference_errors(ref_errors, verbose=verbose, debug=debug)
        if check_response and isinstance(other_errors := check_response.get("errors"), list) and other_errors:
            if not printed_newline:
                PRINT_OUTPUT()
                printed_newline = True
            for error in other_errors:
                PRINT_OUTPUT("- " + error)
        if output_file := get_output_file():
            PRINT_STDOUT(f"Exiting with server validation errors; see your output file: {output_file}")
        else:
            PRINT_STDOUT("\nExiting with no action with server validation errors.")
            PRINT_STDOUT("Use the --output FILE option to write errors to a file.")
        exit(1)

    return check_done, check_status, check_response


def _format_server_error(error: str, indent: int = 0) -> str:
    """
    Make an attempt at parsing and formatting a server (validation/submission) error.
    If we can't do it then just return the string as given. Here for example is what
    we hope a "typical" server error message looks like:
    'Error: /Software/DAX_SOFTWARE_VEPX Exception encountered on VirtualAppURL: /Software?skip_indexing=true&check_only=true&skip_links=trueBODY: {\'submitted_id\': \'DAX_SOFTWARE_VEPX\', \'category\': [\'Variant Annotation\'], \'title\': \'VEP\', \'version\': \'1.0.1\', \'consortia\': [\'smaht\'], \'submission_centers\': [\'9626d82e-8110-4213-ac75-0a50adf890ff\']}MSG: HTTP POST failed.Raw Exception: Bad response: 422 Unprocessable Entity (not 200 OK or 3xx redirect for http://localhost/Software?skip_indexing=true&check_only=true&skip_links=true)b\'{"@type": ["ValidationFailure", "Error"], "status": "error", "code": 422, "title": "Unprocessable Entity", "description": "Failed validation", "errors": [{"location": "submitted_id", "name": "Submission Code Mismatch", "description": "Submitted ID DAX_SOFTWARE_VEPX start (DAX) does not match options for given submission centers: [\\\'DAC\\\']."}]}\''  # noqa
    """

    def load_json_fuzzy(value: str) -> Optional[dict]:
        if isinstance(value, str):
            if (value := normalize_spaces(value)).endswith("'"):
                value = value[:-1]
            try:
                value = json.loads(value)
            except Exception:
                try:
                    value = ast.literal_eval(value)
                except Exception:
                    try:
                        value = json.loads(value := value.replace("\\", ""))
                    except Exception:
                        try:
                            value = json.loads(value := value.replace("'", '"'))
                        except Exception:
                            pass
            if isinstance(value, dict):
                value.pop("@type", None)
                return value

    def format_json_with_indent(value: dict, indent: int = 0) -> Optional[str]:
        if isinstance(value, dict):
            result = json.dumps(value, indent=4)
            if indent > 0:
                result = f"{indent * ' '}{result}"
                result = result.replace("\n", f"\n{indent * ' '}")
            return result

    pattern = r"\s*Error:\s*(.+?)\s*Exception.*BODY:\s*({.*})MSG:\s*(.*?)Raw Exception.*({\"@type\":.*)"
    match = re.match(pattern, error)
    if match and len(match.groups()) == 4:
        path = match.group(1)
        body = match.group(2)
        message = match.group(3)
        if message.endswith("."):
            message = message[:-1]
        error = match.group(4)
        body = load_json_fuzzy(body)
        error = load_json_fuzzy(error)
        if path and message and error and body:
            result = f"ERROR: {message} ▶ {path}"
            result += f"\n{format_json_with_indent(error, indent=indent)}"
            result += f"\n{format_json_with_indent(body, indent=indent)}"
            return result
    return error.replace("Error:", "ERROR:")


def _check_ingestion_progress(uuid, *, keypair, server) -> Tuple[bool, str, dict]:
    """
    Calls endpoint to get this status of the IngestionSubmission uuid (in outer scope);
    this is used as an argument to check_repeatedly below to call over and over.
    Returns tuple with: done-indicator (True or False), short-status (str), full-response (dict)
    From outer scope: server, keypair, uuid (of IngestionSubmission)
    """
    tracking_url = _ingestion_submission_item_url(server=server, uuid=uuid)
    response = Portal(keypair).get(tracking_url)
    response_status_code = response.status_code
    response = response.json()
    if response_status_code == 404:
        return True, f"Not found - {uuid}", response
    # FYI this processing_status and its state, progress, outcome properties were ultimately set
    # from within the ingester process, from within types.ingestion.SubmissionFolio.processing_status.
    status = response.get("processing_status", {})
    if status.get("state") == "done":
        outcome = status.get("outcome")
        return True, outcome, response
    else:
        progress = status.get("progress")
        return False, progress, response


def _summarize_submission(uuid: str, app: str, server: Optional[str] = None, env: Optional[str] = None):
    if env:
        command_summary = f"check-submission --env {env} {uuid}"
    elif server:
        command_summary = f"check-submission --server {server} {uuid}"
    else:  # unsatisfying, but not worth raising an error
        command_summary = f"check-submission {uuid}"
    return command_summary


def compute_s3_submission_post_data(ingestion_filename, ingestion_post_result, **other_args):
    uuid = ingestion_post_result['uuid']
    at_id = ingestion_post_result['@id']
    accession = ingestion_post_result.get('accession')  # maybe not always there?
    upload_credentials = ingestion_post_result['upload_credentials']
    upload_urlstring = upload_credentials['upload_url']
    upload_url = urlparse(upload_urlstring)
    upload_key = upload_credentials['key']
    upload_bucket = upload_url.netloc
    # Possible sanity check, probably not needed...
    # check_true(upload_key == remove_prefix('/', upload_url.path, required=True),
    #            message=f"The upload_key, {upload_key!r}, did not match path of {upload_url}.")
    submission_post_data = {
        'datafile_uuid': uuid,
        'datafile_accession': accession,
        'datafile_@id': at_id,
        'datafile_url': upload_urlstring,
        'datafile_bucket': upload_bucket,
        'datafile_key': upload_key,
        'datafile_source_filename': os.path.basename(ingestion_filename),
        **other_args  # validate_remote_only, and any of institution, project, lab, or award that caller gave us
    }
    return submission_post_data


def _print_submission_summary(portal: Portal, result: dict,
                              nofiles: bool = False,
                              check_submission_script: bool = False,
                              include_errors: bool = False,
                              verbose: bool = False, debug: bool = False) -> None:
    if not result:
        return
    def is_admin_user(user_record: Optional[dict]) -> bool:  # noqa
        nonlocal portal, check_submission_script
        if not check_submission_script or not user_record or not (user_uuid := user_record.get("uuid")):
            return None
        try:
            user_record = portal.get_metadata(user_uuid)
            return "admin" in user_record.get("groups", [])
        except Exception:
            return None
    lines = []
    errors = []
    validation_info = None
    submission_type = "Submission"
    validation = None
    was_server_validation_timeout = False
    if submission_parameters := result.get("parameters", {}):
        if validation := tobool(submission_parameters.get("validate_only")):
            submission_type = "Validation"
        if submission_file := submission_parameters.get("datafile"):
            if submission_file == "null":
                # This submission was a continuance via check-submission of a
                # server validation (via submit-metadata-bundle) which timed out;
                # we will note this fact very subtly in the output.
                if validation_datafile := submission_parameters.get("validation_datafile"):
                    submission_file = validation_datafile
                    was_server_validation_timeout = True
            lines.append(f"Submission File: {submission_file}")
    if submission_uuid := result.get("uuid"):
        lines.append(f"{submission_type} ID: {submission_uuid}")
    if date_created := _format_portal_object_datetime(result.get("date_created"), True):
        lines.append(f"{submission_type} Time: {date_created}")
    if submission_parameters:
        extra_file_info = ""
        if (datafile_size := submission_parameters.get("datafile_size", None)) is not None:
            if not isinstance(datafile_size, int) and isinstance(datafile_size, str) and datafile_size.isdigit():
                datafile_size = int(datafile_size)
            if isinstance(datafile_size, int):
                extra_file_info += f"{format_size(datafile_size)}"
        if datafile_md5 := submission_parameters.get("datafile_md5"):
            if extra_file_info:
                extra_file_info += " | "
            extra_file_info += f"MD5: {datafile_md5}"
        if extra_file_info:
            lines.append(f"Submission File Info: {extra_file_info}")
    if validation:
        lines.append(f"Validation Only: Yes ◀ ◀ ◀")
        if submission_parameters and (associated_submission_uuid := submission_parameters.get("submission_uuid")):
            lines.append(f"Associated Submission ID: {associated_submission_uuid}")
    elif submission_parameters and (associated_validation_uuid := submission_parameters.get("validation_uuid")):
        lines.append(f"Associated Validation ID:"
                     f" {associated_validation_uuid}{' (ω)' if was_server_validation_timeout else ''}")
    if submitted_by := result.get("submitted_by", {}).get("display_title"):
        consortia = None
        submission_center = None
        if consortia := result.get("consortia", []):
            consortium = consortia[0].get("display_title")
        if submission_centers := result.get("submission_centers", []):
            submission_center = submission_centers[0].get("display_title")
        if consortia:
            if submission_center:
                lines.append(f"Submitted By: {submitted_by} ({consortium} | {submission_center})")
            else:
                lines.append(f"Submitted By: {submitted_by} ({consortia})")
        elif submission_center:
            lines.append(f"Submitted By: {submitted_by} ({submission_center})")
        else:
            lines.append(f"Submitted By: {submitted_by}")
        if is_admin_user(result.get("submitted_by")) is True:
            lines[len(lines) - 1] += " ▶ Admin"
    if additional_data := result.get("additional_data"):
        if (validation_info := additional_data.get("validation_output")) and isinstance(validation_info, dict):
            # TODO: Cleanup/unify error structure from client and server!
            if ref_errors := _validate_references(validation_info.get("ref"), None):
                errors.extend(_format_reference_errors(ref_errors, verbose=verbose, debug=debug))
            if validation_errors := validation_info.get("validation"):
                errors.append(f"- Validation errors: {len(validation_errors)}")
                for validation_error in validation_errors:
                    errors.append(f"  - {_format_issue(validation_error)}")
    if processing_status := result.get("processing_status"):
        summary_lines = []
        if additional_data := result.get("additional_data"):
            if (validation_info := additional_data.get("validation_output")) and isinstance(validation_info, list):
                if status := [info for info in validation_info if info.lower().startswith("status:")]:
                    summary_lines.append(status[0])
        if state := processing_status.get("state"):
            summary_lines.append(f"State: {state.title()}")
        if progress := processing_status.get("progress"):
            summary_lines.append(f"Progress: {progress.title()}")
        if outcome := processing_status.get("outcome"):
            summary_lines.append(f"Outcome: {outcome.title()}")
        if main_status := result.get("status"):
            summary_lines.append(f"{main_status.title()}")
        if summary := " | ".join(summary_lines):
            lines.append("===")
            lines.append(summary)
    if additional_data := result.get("additional_data"):
        if (validation_info := additional_data.get("validation_output")) and isinstance(validation_info, list):
            summary_lines = []
            if types := [info for info in validation_info if info.lower().startswith("types")]:
                summary_lines.append(types[0])
            if created := [info for info in validation_info if info.lower().startswith("created")]:
                summary_lines.append(created[0])
            if updated := [info for info in validation_info if info.lower().startswith("updated")]:
                summary_lines.append(updated[0])
            if skipped := [info for info in validation_info if info.lower().startswith("skipped")]:
                summary_lines.append(skipped[0])
            if checked := [info for info in validation_info if info.lower().startswith("checked")]:
                summary_lines.append(checked[0])
            if errored := [info for info in validation_info if info.lower().startswith("errored")]:
                summary_lines.append(errored[0].replace("Errored", "Errors"))
            if errors := [info for info in validation_info if info.lower().startswith("error:")]:
                pass
            if total := [info for info in validation_info if info.lower().startswith("total")]:
                summary_lines.append(total[0])
            if summary := " | ".join(summary_lines):
                lines.append("===")
                lines.append(summary)
    if validation_info:
        summary_lines = []
        if s3_data_file := [info for info in validation_info if info.lower().startswith("s3 file: ")]:
            s3_data_file = s3_data_file[0][9:]
            if (rindex := s3_data_file.rfind("/")) > 0:
                s3_data_bucket = s3_data_file[5:rindex] if s3_data_file.startswith("s3://") else ""
                s3_data_file = s3_data_file[rindex + 1:]
                if s3_data_bucket:
                    summary_lines.append(f"S3: {s3_data_bucket}")
                summary_lines.append(f"S3 Data: {s3_data_file}")
        if s3_details_file := [info for info in validation_info if info.lower().startswith("details: ")]:
            s3_details_file = s3_details_file[0][9:]
            if (rindex := s3_details_file.rfind("/")) > 0:
                s3_details_bucket = s3_details_file[5:rindex] if s3_details_file.startswith("s3://") else ""
                s3_details_file = s3_details_file[rindex + 1:]
                if s3_details_bucket != s3_data_bucket:
                    summary_lines.append(f"S3 Bucket: {s3_details_bucket}")
                summary_lines.append(f"S3 Details: {s3_details_file}")
        if summary_lines:
            lines.append("===")
            lines += summary_lines
    if additional_data and not nofiles:
        if upload_files := additional_data.get("upload_info"):
            lines.append("===")
            lines.append(f"Upload Files: {len(upload_files)} ...")
            for upload_file in upload_files:
                upload_file_uuid = upload_file.get("uuid")
                upload_file_name = upload_file.get("filename")
                upload_file_accession_name, upload_file_type = _get_upload_file_info(portal, upload_file_uuid)
                lines.append("===")
                lines.append(f"Upload File: {upload_file_name}")
                lines.append(f"Upload File ID: {upload_file_uuid}")
                if upload_file_accession_name:
                    lines.append(f"Upload File Accession Name: {upload_file_accession_name}")
                if upload_file_type:
                    lines.append(f"Upload File Type: {upload_file_type}")
    if lines:
        lines = ["===", f"SMaHT {'Validation' if validation else 'Submission'} Summary [UUID]", "==="] + lines + ["==="]
        if errors and include_errors:
            lines += ["ERRORS ITEMIZED BELOW ...", "==="]
        print_boxed(lines, right_justified_macro=("[UUID]", lambda: submission_uuid))
        if errors and include_errors:
            for error in errors:
                PRINT(_format_server_error(error))


def _show_upload_info(uuid, server=None, env=None, keydict=None, app: str = None,
                      show_primary_result=True,
                      show_validation_output=True,
                      show_processing_status=True,
                      show_datafile_url=True,
                      show_details=True):
    """
    Uploads the files associated with a given ingestion submission. This is useful if you answered "no" to the query
    about uploading your data and then later are ready to do that upload.

    :param uuid: a string guid that identifies the ingestion submission
    :param server: the server to upload to
    :param env: the portal environment to upload to
    :param keydict: keydict-style auth, a dictionary of 'key', 'secret', and 'server'
    :param app: the name of the app to use
        e.g., affects whether to expect --lab, --award, --institution, --project, --consortium or --submission_center
        and whether to use .fourfront-keys.json, .cgap-keys.json, or .smaht-keys.json
    :param show_primary_result: bool controls whether the primary result is shown
    :param show_validation_output: bool controls whether to show output resulting from validation checks
    :param show_processing_status: bool controls whether to show the current processing status
    :param show_datafile_url: bool controls whether to show the datafile_url parameter from the parameters.
    :param show_details: bool controls whether to show the details from the results file in S3.
    """

    if app is None:  # Better to pass explicitly, but some legacy situations might require this to default
        app = DEFAULT_APP

    portal = _define_portal(key=keydict, env=env, server=server, app=app, report=True)

    if not (uuid_metadata := portal.get_metadata(uuid)):
        raise Exception(f"Cannot find object given uuid: {uuid}")

    if not portal.is_schema_type(uuid_metadata, INGESTION_SUBMISSION_TYPE_NAME):
        undesired_type = portal.get_schema_type(uuid_metadata)
        raise Exception(f"Given ID is not an {INGESTION_SUBMISSION_TYPE_NAME} type: {uuid} ({undesired_type})")

    url = _ingestion_submission_item_url(portal.server, uuid)
    response = portal.get(url)
    response.raise_for_status()
    res = response.json()
    _show_upload_result(res,
                        show_primary_result=show_primary_result,
                        show_validation_output=show_validation_output,
                        show_processing_status=show_processing_status,
                        show_datafile_url=show_datafile_url,
                        show_details=show_details,
                        portal=portal)
    if show_details:
        metadata_bundles_bucket = get_metadata_bundles_bucket_from_health_path(key=portal.key)
        _show_detailed_results(uuid, metadata_bundles_bucket)

    if not _pytesting():
        PRINT("")
        _print_submission_summary(portal, res)


@lru_cache(maxsize=256)
def _get_upload_file_info(portal: Portal, uuid: str) -> Tuple[Optional[str], Optional[str]]:
    try:
        upload_file_info = portal.get(f"/{uuid}").json()
        upload_file_accession_based_name = upload_file_info.get("display_title")
        if upload_file_type := upload_file_info.get("data_type"):
            if isinstance(upload_file_type, list) and len(upload_file_type) > 0:
                upload_file_type = upload_file_type[0]
            elif not isinstance(upload_file_type, str):
                upload_file_type = None
            if upload_file_type:
                upload_file_type = Schema.type_name(upload_file_type)
        return upload_file_accession_based_name, upload_file_type
    except Exception:
        return None


def _show_upload_result(result,
                        show_primary_result=True,
                        show_validation_output=True,
                        show_processing_status=True,
                        show_datafile_url=True,
                        show_details=True,
                        portal=None):

    if show_primary_result:
        if _get_section(result, 'upload_info'):
            _show_section(result, 'upload_info', portal=portal)
        else:
            SHOW("Uploads: None")

    # New March 2023 ...

    if show_validation_output and _get_section(result, 'validation_output'):
        _show_section(result, 'validation_output')

    if show_processing_status and result.get('processing_status'):
        SHOW("\n----- Processing Status -----")
        state = result['processing_status'].get('state')
        if state:
            SHOW(f"State: {state.title()}")
        outcome = result['processing_status'].get('outcome')
        if outcome:
            SHOW(f"Outcome: {outcome.title()}")
        progress = result['processing_status'].get('progress')
        if progress:
            SHOW(f"Progress: {progress.title()}")

    if show_datafile_url and result.get('parameters'):
        datafile_url = result['parameters'].get('datafile_url')
        if datafile_url:
            SHOW("----- DataFile URL -----")
            SHOW(datafile_url)


def do_any_uploads(res, keydict, upload_folder=None, ingestion_filename=None,
                   no_query=False, subfolders=False, portal=None):

    def display_file_info(upload_file_info: dict) -> None:
        nonlocal upload_folder, subfolders
        file = upload_file_info.get("filename")
        file_uuid = upload_file_info.get("uuid")
        if file:
            if file_paths := search_for_file(file, location=upload_folder, recursive=subfolders):
                if len(file_paths) == 1:
                    PRINT(f"File to upload to AWS S3: {format_path(file_paths[0])}"
                          f" ({format_size(get_file_size(file_paths[0]))})")
                    return True
                else:
                    PRINT(f"No upload attempted for file {file} because multiple"
                          f" copies were found in folder {upload_folder}: {', '.join(file_paths)}.")
                    return False
            PRINT(f"WARNING: Cannot find file to upload to AWS S3: {format_path(file)} ({file_uuid})")
        return False

    upload_info = _get_section(res, 'upload_info')
    if not upload_folder:
        if ingestion_directory := res.get("parameters", {}).get("ingestion_directory"):
            if os.path.isdir(ingestion_directory):
                upload_folder = ingestion_directory
    if not upload_folder and ingestion_filename:
        if ingestion_directory := os.path.dirname(ingestion_filename):
            upload_folder = ingestion_directory
    resume_upload_commands = []
    resume_upload_commands_missing = []
    noupload = False
    if upload_info:
        files_to_upload = []
        for upload_file_info in upload_info:
            if display_file_info(upload_file_info):
                files_to_upload.append(upload_file_info)
                if portal:
                    resume_upload_commands.append(f"resume-uploads --env {portal.env} {upload_file_info.get('uuid')}")
            elif portal:
                resume_upload_commands_missing.append(
                    f"resume-uploads --env {portal.env} {upload_file_info.get('uuid')}")
        if len(files_to_upload) == 0:
            return
        if no_query:
            do_uploads(files_to_upload, auth=keydict, no_query=no_query, folder=upload_folder,
                       subfolders=subfolders)
        else:
            message = ("Upload this file?" if len(files_to_upload) == 1
                       else f"Upload these {len(files_to_upload)} files?")
            if yes_or_no(message):
                do_uploads(files_to_upload, auth=keydict,
                           no_query=no_query, folder=upload_folder,
                           subfolders=subfolders)
            else:
                noupload = True
                SHOW("No uploads attempted.")
                if resume_upload_commands:
                    resume_upload_commands += resume_upload_commands_missing
                    nresume_upload_commands = len(resume_upload_commands)
                    if yes_or_no(f"Do you want to see the resume-uploads"
                                 f" command{'s' if nresume_upload_commands != 1 else ''} to use to"
                                 f" upload {'these' if nresume_upload_commands != 1 else 'this'} separately?"):
                        for resume_upload_command in resume_upload_commands:
                            PRINT(f"▶ {resume_upload_command}")
    if not noupload and resume_upload_commands_missing:
        nresume_upload_commands_missing = len(resume_upload_commands_missing)
        PRINT(f"There {'were' if nresume_upload_commands_missing != 1 else 'was'}"
              f" {nresume_upload_commands_missing} missing"
              f" file{'s' if nresume_upload_commands_missing != 1 else ''} as mentioned above.")
        if yes_or_no(f"Do you want to see the resume-uploads"
                     f" command{'s' if nresume_upload_commands_missing != 1 else ''}"
                     f" to use to upload {'these' if nresume_upload_commands_missing != 1 else 'this'} separately?"):
            for resume_upload_command_missing in resume_upload_commands_missing:
                PRINT(f"▶ {resume_upload_command_missing}")


def resume_uploads(uuid, server=None, env=None, bundle_filename=None, keydict=None,
                   upload_folder=None, no_query=False, subfolders=False,
                   output_file=None, app=None, keys_file=None, env_from_env=False):
    """
    Uploads the files associated with a given ingestion submission. This is useful if you answered "no" to the query
    about uploading your data and then later are ready to do that upload.

    :param uuid: a string guid that identifies the ingestion submission
    :param server: the server to upload to
    :param env: the portal environment to upload to
    :param bundle_filename: the bundle file to be uploaded
    :param keydict: keydict-style auth, a dictionary of 'key', 'secret', and 'server'
    :param upload_folder: folder in which to find files to upload (default: same as ingestion_filename)
    :param no_query: bool to suppress requests for user input
    :param subfolders: bool to search subdirectories within upload_folder for files
    """

    if output_file:
        global PRINT, PRINT_OUTPUT, PRINT_STDOUT, SHOW
        PRINT, PRINT_OUTPUT, PRINT_STDOUT, SHOW = setup_for_output_file_option(output_file)

    portal = _define_portal(key=keydict, keys_file=keys_file, env=env,
                            server=server, app=app, env_from_env=env_from_env,
                            report=True, note="Resuming File Upload")

    if not (response := portal.get_metadata(uuid, raise_exception=False)):
        if accession_id := _extract_accession_id(uuid):
            if not (response := portal.get_metadata(accession_id)):
                raise Exception(f"Given accession ID not found: {accession_id}")
            if (display_title := response.get("display_title")) and not (uuid == display_title):
                raise Exception(f"Accession ID found but wrong filename: {accession_id} vs {uuid}")
            uuid = accession_id
        else:
            raise Exception(f"Given ID not found: {uuid}")

    if not portal.is_schema_type(response, INGESTION_SUBMISSION_TYPE_NAME):

        # Subsume function of upload-item-data into resume-uploads for convenience.
        if portal.is_schema_type(response, FILE_TYPE_NAME):
            _upload_item_data(item_filename=uuid, uuid=None, server=portal.server,
                              env=portal.env, directory=upload_folder, recursive=subfolders,
                              no_query=no_query, app=app, report=False)
            return

        undesired_type = portal.get_schema_type(response)
        raise Exception(f"Given ID is not an {INGESTION_SUBMISSION_TYPE_NAME} type: {uuid} ({undesired_type})")

    if submission_parameters := response.get("parameters", {}):
        if tobool(submission_parameters.get("validate_only")):
            PRINT(f"This submission ID ({uuid}) is for a validation not an actual submission.")
            exit(1)

    do_any_uploads(response,
                   keydict=portal.key,
                   ingestion_filename=bundle_filename,
                   upload_folder=upload_folder,
                   no_query=no_query,
                   subfolders=subfolders,
                   portal=portal)


@function_cache(serialize_key=True)
def _get_health_page(key: dict) -> dict:
    return Portal(key).get_health().json()


def get_metadata_bundles_bucket_from_health_path(key: dict) -> str:
    return _get_health_page(key=key).get("metadata_bundles_bucket")


def get_s3_encrypt_key_id_from_health_page(auth):
    try:
        return _get_health_page(key=auth).get(HealthPageKey.S3_ENCRYPT_KEY_ID)
    except Exception:  # pragma: no cover
        # We don't actually unit test this section because _get_health_page realistically always returns
        # a dictionary, and so health.get(...) always succeeds, possibly returning None, which should
        # already be tested. Returning None here amounts to the same and needs no extra unit testing.
        # The presence of this error clause is largely pro forma and probably not really needed.
        return None


def get_s3_encrypt_key_id(*, upload_credentials, auth):
    if 's3_encrypt_key_id' in upload_credentials:
        s3_encrypt_key_id = upload_credentials.get('s3_encrypt_key_id')
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"Extracted s3_encrypt_key_id from upload_credentials: {s3_encrypt_key_id}")
    else:
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"No s3_encrypt_key_id entry found in upload_credentials.")
            PRINT(f"Fetching s3_encrypt_key_id from health page.")
        s3_encrypt_key_id = get_s3_encrypt_key_id_from_health_page(auth)
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f" =id=> {s3_encrypt_key_id!r}")
    return s3_encrypt_key_id


def execute_prearranged_upload(path, upload_credentials, auth=None):
    """
    This performs a file upload using special credentials received from ff_utils.patch_metadata.

    :param path: the name of a local file to upload
    :param upload_credentials: a dictionary of credentials to be used for the upload,
        containing the keys 'AccessKeyId', 'SecretAccessKey', 'SessionToken', and 'upload_url'.
    :param auth: auth info in the form of a dictionary containing 'key', 'secret', and 'server',
        and possibly other useful information such as an encryption key id.
    """

    if DEBUG_PROTOCOL:  # pragma: no cover
        PRINT(f"Upload credentials contain {conjoined_list(list(upload_credentials.keys()))}.")
    try:
        s3_uri = upload_credentials["upload_url"]
        aws_credentials = {
            "AWS_ACCESS_KEY_ID": upload_credentials["AccessKeyId"],
            "AWS_SECRET_ACCESS_KEY": upload_credentials["SecretAccessKey"],
            "AWS_SECURITY_TOKEN": upload_credentials["SessionToken"]
        }
        aws_kms_key_id = get_s3_encrypt_key_id(upload_credentials=upload_credentials, auth=auth)
    except Exception as e:
        raise ValueError("Upload specification is not in good form. %s: %s" % (e.__class__.__name__, e))

    upload_file_to_aws_s3(file=path,
                          s3_uri=s3_uri,
                          aws_credentials=aws_credentials,
                          aws_kms_key_id=aws_kms_key_id,
                          print_progress=True,
                          print_function=PRINT,
                          verify_upload=True,
                          catch_interrupt=True)


def _running_on_windows_native():
    return os.name == 'nt'


def compute_file_post_data(filename, context_attributes):
    file_basename = os.path.basename(filename)
    _, ext = os.path.splitext(file_basename)  # could probably get a nicer error message if file in bad format
    file_format = remove_prefix('.', ext, required=True)
    return {
        'filename': file_basename,
        'file_format': file_format,
        **{attr: val for attr, val in context_attributes.items() if val}
    }


def upload_file_to_new_uuid(filename, schema_name, auth, **context_attributes):
    """
    Upload file to a target environment.

    :param filename: the name of a file to upload.
    :param schema_name: the schema_name to use when creating a new file item whose content is to be uploaded.
    :param auth: auth info in the form of a dictionary containing 'key', 'secret', and 'server'.
    :returns: item metadata dict or None
    """

    post_item = compute_file_post_data(filename=filename, context_attributes=context_attributes)

    if DEBUG_PROTOCOL:  # pragma: no cover
        SHOW("Creating FileOther type object ...")
    response = Portal(auth).post_metadata(object_type=schema_name, data=post_item)
    if DEBUG_PROTOCOL:  # pragma: no cover
        type_object_message = f" {response.get('@graph', [{'uuid': 'not-found'}])[0].get('uuid', 'not-found')}"
        SHOW(f"Created FileOther type object: {type_object_message}")

    metadata, upload_credentials = extract_metadata_and_upload_credentials(response,
                                                                           method='POST', schema_name=schema_name,
                                                                           filename=filename, payload_data=post_item)

    execute_prearranged_upload(filename, upload_credentials=upload_credentials, auth=auth)

    return metadata


def upload_file_to_uuid(filename, uuid, auth):
    """
    Upload file to a target environment.

    :param filename: the name of a file to upload.
    :param uuid: the item into which the filename is to be uploaded.
    :param auth: auth info in the form of a dictionary containing 'key', 'secret', and 'server'.
    :returns: item metadata dict or None
    """
    metadata = None
    ignorable(metadata)  # PyCharm might need this if it worries it isn't set below

    # filename here should not include path
    patch_data = {'filename': os.path.basename(filename)}

    response = Portal(auth).patch_metadata(object_id=uuid, data=patch_data)

    metadata, upload_credentials = extract_metadata_and_upload_credentials(response,
                                                                           method='PATCH', uuid=uuid,
                                                                           filename=filename, payload_data=patch_data)

    execute_prearranged_upload(filename, upload_credentials=upload_credentials, auth=auth)

    return metadata


def extract_metadata_and_upload_credentials(response, filename, method, payload_data, uuid=None, schema_name=None):
    try:
        [metadata] = response['@graph']
        upload_credentials = metadata['upload_credentials']
    except Exception as e:
        if DEBUG_PROTOCOL:  # pragma: no cover
            PRINT(f"Problem trying to {method} to get upload credentials.")
            PRINT(f" payload_data={payload_data}")
            if uuid:
                PRINT(f" uuid={uuid}")
            if schema_name:
                PRINT(f" schema_name={schema_name}")
            PRINT(f" response={response}")
            PRINT(f"Got error {type(e)}: {e}")
        raise RuntimeError(f"Unable to obtain upload credentials for file {filename}.")
    return metadata, upload_credentials


# This can be set to True in unusual situations, but normally will be False to avoid unnecessary querying.
SUBMITR_SELECTIVE_UPLOADS = environ_bool("SUBMITR_SELECTIVE_UPLOADS")


def do_uploads(upload_spec_list, auth, folder=None, no_query=False, subfolders=False):
    """
    Uploads the files mentioned in the give upload_spec_list.

    If any files have associated extra files, upload those as well.

    :param upload_spec_list: a list of upload_spec dictionaries, each of the form {'filename': ..., 'uuid': ...},
        representing uploads to be formed.
    :param auth: a dictionary-form auth spec, of the form {'key': ..., 'secret': ..., 'server': ...}
        representing destination and credentials.
    :param folder: a string naming a folder in which to find the filenames to be uploaded.
    :param no_query: bool to suppress requests for user input
    :param subfolders: bool to search subdirectories within upload_folder for files
    :return: None
    """
    folder = folder or os.path.curdir
    if subfolders:
        folder = os.path.join(folder, '**')
    for upload_spec in upload_spec_list:
        file_name = upload_spec["filename"]
        if not (file_paths := search_for_file(file_name, location=folder, recursive=subfolders)) or len(file_paths) > 1:
            if len(file_paths) > 1:
                SHOW(f"No upload attempted for file {file_name} because multiple copies"
                     f" were found in folder {folder}: {', '.join(file_paths)}.")
            else:
                SHOW(f"Upload file not found: {file_name}")
            continue
        file_path = file_paths[0]
        uuid = upload_spec['uuid']
        uploader_wrapper = UploadMessageWrapper(uuid, no_query=no_query)
        wrapped_upload_file_to_uuid = uploader_wrapper.wrap_upload_function(
            upload_file_to_uuid, file_path
        )
        file_metadata = wrapped_upload_file_to_uuid(
            filename=file_path, uuid=uuid, auth=auth
        )
        if file_metadata:
            extra_files_credentials = file_metadata.get("extra_files_creds", [])
            if extra_files_credentials:
                _upload_extra_files(
                    extra_files_credentials,
                    uploader_wrapper,
                    folder,
                    auth,
                    recursive=subfolders,
                )


class UploadMessageWrapper:
    """Class to provide consistent queries/messages to user when
    uploading file(s) to given File UUID.
    """

    def __init__(self, uuid, no_query=False):
        """Initialize instance for given UUID

        :param uuid: UUID of File item for uploads
        :param no_query: Whether to suppress asking for user
            confirmation prior to upload
        """
        self.uuid = uuid
        self.no_query = no_query

    def wrap_upload_function(self, function, file_name):
        """Wrap upload given function with messages conerning upload.

        :param function: Upload function to wrap
        :param file_name: File to upload
        :returns: Wrapped function
        """
        def wrapper(*args, **kwargs):
            result = None
            perform_upload = True
            if not self.no_query:
                if (
                    SUBMITR_SELECTIVE_UPLOADS
                    and not yes_or_no(f"Upload {file_name}?")
                ):
                    SHOW("OK, not uploading it.")
                    perform_upload = False
            if perform_upload:
                try:
                    result = function(*args, **kwargs)
                except Exception as e:
                    SHOW("%s: %s" % (e.__class__.__name__, e))
            return result
        return wrapper


def _upload_extra_files(
    credentials, uploader_wrapper, folder, auth, recursive=False
):
    """Attempt upload of all extra files.

    Similar to "do_uploads", search for each file and then call a
    wrapped upload function. Here, since extra files do not correspond
    to Items on the portal, no need to PATCH an Item to retrieve AWS
    credentials; they are directly passed in from the parent File's
    metadata.

    :param credentials: AWS credentials dictionary
    :param uploader_wrapper: UploadMessageWrapper instance
    :param folder: Directory to search for files
    :param auth: a portal authorization tuple
    :param recursive: Whether to search subdirectories for file
    """
    for extra_file_item in credentials:
        extra_file_name = extra_file_item.get("filename")
        extra_file_credentials = extra_file_item.get("upload_credentials")
        if not extra_file_name or not extra_file_credentials:
            continue
        if (not (extra_file_paths := search_for_file(extra_file_name, location=folder,
                                                     recursive=recursive)) or len(extra_file_paths) > 1):
            if len(extra_file_paths) > 1:
                SHOW(f"No upload attempted for file {extra_file_name} because multiple"
                     f" copies were found in folder {folder}: {', '.join(extra_file_paths)}.")
            else:
                SHOW(f"Upload file not found: {extra_file_name}")
            continue
        extra_file_path = extra_file_paths[0]
        wrapped_execute_prearranged_upload = uploader_wrapper.wrap_upload_function(
            execute_prearranged_upload, extra_file_path
        )
        wrapped_execute_prearranged_upload(extra_file_path, extra_file_credentials, auth=auth)


def _upload_item_data(item_filename, uuid, server, env, directory=None, recursive=False,
                      no_query=False, app=None, report=True):
    """
    Given a part_filename, uploads that filename to the Item specified by uuid on the given server.

    Only one of server or env may be specified.

    :param item_filename: the name of a file to be uploaded
    :param uuid: the UUID of the Item with which the uploaded data is to be associated
    :param server: the server to upload to (where the Item is defined)
    :param env: the portal environment to upload to (where the Item is defined)
    :param no_query: bool to suppress requests for user input
    :return:
    """

    # Allow the given "file name" to be uuid for submitted File object, or associated accession
    # ID (e.g. SMAFIP2PIEDG), or the (S3) accession ID based file name (e.g. SMAFIP2PIEDG.fastq).
    if not uuid:
        if is_uuid(item_filename) or _is_accession_id(item_filename):
            uuid = item_filename
            item_filename = None
        elif accession_id := _extract_accession_id(item_filename):
            uuid = accession_id
            item_filename = None

    portal = _define_portal(env=env, server=server, app=app, report=report)

    if not (uuid_metadata := portal.get_metadata(uuid)):
        raise Exception(f"Cannot find object given uuid: {uuid}")

    if not portal.is_schema_type(uuid_metadata, FILE_TYPE_NAME):
        undesired_type = portal.get_schema_type(uuid_metadata)
        raise Exception(f"Given uuid is not a file type: {uuid} ({undesired_type})")

    if not item_filename:
        if not (item_filename := uuid_metadata.get("filename")):
            raise Exception(f"Cannot determine file name: {uuid}")

    if not (item_filename_found := search_for_file(item_filename, location=directory,
                                                   recursive=recursive, single=True)):
        raise Exception(f"File not found: {item_filename}")
    else:
        PRINT(f"File to upload to AWS S3: {format_path(item_filename_found)}")
        item_filename = item_filename_found

    if not no_query:
        file_size = format_size(get_file_size(item_filename))
        if not yes_or_no(f"Upload {format_path(item_filename)} ({file_size}) to {server}?"):
            SHOW("Aborting submission.")
            exit(1)

    upload_file_to_uuid(filename=item_filename, uuid=uuid, auth=portal.key)


def _show_detailed_results(uuid: str, metadata_bundles_bucket: str) -> None:

    PRINT(f"----- Detailed Info -----")

    submission_results_location, submission_results = _fetch_submission_results(metadata_bundles_bucket, uuid)
    exception_results_location, exception_results = _fetch_exception_results(metadata_bundles_bucket, uuid)

    if not submission_results and not exception_results:
        PRINT(f"Neither submission nor exception results found!")
        PRINT(f"-> {submission_results_location}")
        PRINT(f"-> {exception_results_location}")
        return

    if submission_results:
        PRINT(f"From: {submission_results_location}")
        PRINT(yaml.dump(submission_results))

    if exception_results:
        PRINT("Exception during schema ingestion processing:")
        PRINT(f"From: {exception_results_location}")
        PRINT(exception_results)


def _fetch_submission_results(metadata_bundles_bucket: str, uuid: str) -> Optional[Tuple[str, dict]]:
    return _fetch_results(metadata_bundles_bucket, uuid, "submission.json")


def _fetch_exception_results(metadata_bundles_bucket: str, uuid: str) -> Optional[Tuple[str, str]]:
    return _fetch_results(metadata_bundles_bucket, uuid, "traceback.txt")


def _fetch_results(metadata_bundles_bucket: str, uuid: str, file: str) -> Optional[Tuple[str, str]]:
    results_key = f"{uuid}/{file}"
    results_location = f"s3://{metadata_bundles_bucket}/{results_key}"
    try:
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=metadata_bundles_bucket, Key=f"{uuid}/{file}")
        results = response['Body'].read().decode('utf-8')
        if file.endswith(".json"):
            results = json.loads(results)
        return (results_location, results)
    except BotoNoCredentialsError:
        PRINT(f"No credentials found for fetching: {results_location}")
    except Exception as e:
        if hasattr(e, "response") and e.response.get("Error", {}).get("Code", "").lower() == "accessdenied":
            PRINT(f"Access denied fetching: {results_location}")
        return (results_location, None)


def _validate_locally(ingestion_filename: str, portal: Portal, autoadd: Optional[dict] = None,
                      validation: bool = False, validate_local_only: bool = False,
                      upload_folder: Optional[str] = None,
                      subfolders: bool = False, exit_immediately_on_errors: bool = False,
                      ref_nocache: bool = False, output_file: Optional[str] = None,
                      noanalyze: bool = False, json_only: bool = False, noprogress: bool = False,
                      verbose_json: bool = False, verbose: bool = False, quiet: bool = False,
                      debug: bool = False, debug_sleep: Optional[str] = None) -> StructuredDataSet:

    if json_only:
        noprogress = True

    # N.B. This same bit of code is in smaht-portal; not sure best way to share;
    # It really should not go in dcicutils (structured_data) as this know pretty
    # specific details about our (SMaHT) schemas, namely, submitted_id and accession.
    def ref_lookup_strategy(type_name: str, schema: dict, value: str) -> (int, Optional[str]):
        #
        # FYI: Note this situation WRT object lookups ...
        #
        # /{submitted_id}                # NOT FOUND
        # /UnalignedReads/{submitted_id} # OK
        # /SubmittedFile/{submitted_id}  # OK
        # /File/{submitted_id}           # NOT FOUND
        #
        # /{accession}                   # OK
        # /UnalignedReads/{accession}    # NOT FOUND
        # /SubmittedFile/{accession}     # NOT FOUND
        # /File/{accession}              # OK
        #
        def ref_validator(schema: Optional[dict],
                          property_name: Optional[str], property_value: Optional[str]) -> Optional[bool]:
            """
            Returns False iff the type represented by the given schema, can NOT be referenced by
            the given property name with the given property value, otherwise returns None.

            For example, if the schema is for the UnalignedReads type and the property name
            is accession, then we will return False iff the given property value is NOT a properly
            formatted accession ID. Otherwise, we will return None, which indicates that the
            caller (in dcicutils.structured_data.Portal.ref_exists) will continue executing
            its default behavior, which is to check other ways in which the given type can NOT
            be referenced by the given value, i.e. it checks other identifying properties for
            the type and makes sure any patterns (e.g. for submitted_id or uuid) are ahered to.

            The goal (in structured_data) being to detect if a type is being referenced in such
            a way that cannot possibly be allowed, i.e. because none of its identifying types
            are in the required form (if indeed there any requirements). Note that it is guaranteed
            that the given property name is indeed an identifying property for the given type.
            """
            if property_format := schema.get("properties", {}).get(property_name, {}).get("format"):
                if (property_format == "accession") and (property_name == "accession"):
                    if not _is_accession_id(property_value):
                        return False
            return None

        if not schema and value:
            nonlocal portal
            if not (schema := portal.get_schema(type_name)):
                return Portal.LOOKUP_DEFAULT, ref_validator
        if value and (schema_properties := schema.get("properties")):
            if schema_properties.get("accession") and _is_accession_id(value):
                # Case: lookup by accession (only by root).
                return Portal.LOOKUP_ROOT, ref_validator
            elif schema_property_info_submitted_id := schema_properties.get("submitted_id"):
                if schema_property_pattern_submitted_id := schema_property_info_submitted_id.get("pattern"):
                    if re.match(schema_property_pattern_submitted_id, value):
                        # Case: lookup by submitted_id (only by specified type).
                        return Portal.LOOKUP_SPECIFIED_TYPE, ref_validator
        return Portal.LOOKUP_DEFAULT, ref_validator

    structured_data = None  # TEMPORARY WORKAROUND FOR DCICUTILS BUG

    def define_progress_callback(debug: bool = False) -> None:
        nsheets = 0
        nrows = 0
        nrows_processed = 0
        nrefs_total = 0
        nrefs_resolved = 0
        nrefs_unresolved = 0
        nrefs_lookup = 0
        nrefs_exists_cache_hit = 0
        nrefs_lookup_cache_hit = 0
        nrefs_invalid = 0
        bar = ProgressBar(nrows, "Calculating", interrupt_exit=True)

        def progress_report(status: dict) -> None:  # noqa
            nonlocal bar, nsheets, nrows, nrows_processed, verbose, noprogress
            nonlocal nrefs_total, nrefs_resolved, nrefs_unresolved, nrefs_lookup
            nonlocal nrefs_exists_cache_hit, nrefs_lookup_cache_hit, nrefs_invalid
            if noprogress:
                return
            increment = 1
            if status.get("start"):
                nsheets = status.get("sheets") or 0
                nrows = status.get("rows") or 0
                if nrows > 0:
                    bar.set_total(nrows)
                    if nsheets > 0:
                        PRINT(
                            f"Parsing submission file which has{' only' if nsheets == 1 else ''}"
                            f" {nsheets} sheet{'s' if nsheets != 1 else ''} and a total of {nrows} rows.")
                    else:
                        PRINT(f"Parsing submission file which has a total of {nrows} row{'s' if nrows != 1 else ''}.")
                elif nsheets > 0:
                    PRINT(f"Parsing submission file which has {nsheets} sheet{'s' if nsheets != 1 else ''}.")
                else:
                    PRINT(f"Parsing submission file which has a total of {nrows} row{'s' if nrows != 1 else ''}.")
                return
            elif status.get("parse") or status.get("finish"):
                if not status.get("finish"):
                    nrows_processed += increment
                nrefs_total = status.get("refs") or 0
                nrefs_resolved = status.get("refs_found") or 0
                nrefs_unresolved = status.get("refs_not_found") or 0
                nrefs_lookup = status.get("refs_lookup") or 0
                nrefs_exists_cache_hit = status.get("refs_exists_cache_hit") or 0
                nrefs_lookup_cache_hit = status.get("refs_lookup_cache_hit") or 0
                nrefs_invalid = status.get("refs_invalid") or 0
                if not status.get("finish"):
                    bar.increment_progress(increment)
            elif not status.get("finish"):
                bar.increment_progress(increment)
            message = f"▶ Rows: {nrows} | Parsed: {nrows_processed}"
            if nrefs_total > 0:
                message += f" ‖ Refs: {nrefs_total}"
                if nrefs_unresolved > 0:
                    message += f" | Unresolved: {nrefs_unresolved}"
                if nrefs_lookup > 0:
                    message += f" | Lookups: {nrefs_lookup}"
                if nrefs_invalid > 0:
                    message += f" | Invalid: {nrefs_invalid}"
                if (verbose or debug) and (nrefs_exists_cache_hit > 0):
                    message += f" | Hits: {nrefs_exists_cache_hit}"
                    if debug:
                        message += f" [{nrefs_lookup_cache_hit}]"
            bar.set_description(message)
            if status.get("finish"):
                bar.done()

        return progress_report

    if debug:
        PRINT("DEBUG: Starting client validation.")

    structured_data = StructuredDataSet(None, portal, autoadd=autoadd,
                                        ref_lookup_strategy=ref_lookup_strategy,
                                        ref_lookup_nocache=ref_nocache,
                                        progress=None if noprogress else define_progress_callback(debug=debug),
                                        debug_sleep=debug_sleep)
    structured_data.load_file(ingestion_filename)

    if debug:
        PRINT("DEBUG: Finished client validation.")

    if debug:
        PRINT_OUTPUT(f"DEBUG: Reference total count: {structured_data.ref_total_count}")
        PRINT_OUTPUT(f"DEBUG: Reference total found count: {structured_data.ref_total_found_count}")
        PRINT_OUTPUT(f"DEBUG: Reference total not found count: {structured_data.ref_total_notfound_count}")
        PRINT_OUTPUT(f"DEBUG: Reference exists cache hit count: {structured_data.ref_exists_cache_hit_count}")
        PRINT_OUTPUT(f"DEBUG: Reference exists cache miss count: {structured_data.ref_exists_cache_miss_count}")
        PRINT_OUTPUT(f"DEBUG: Reference exists internal count: {structured_data.ref_exists_internal_count}")
        PRINT_OUTPUT(f"DEBUG: Reference exists external count: {structured_data.ref_exists_external_count}")
        PRINT_OUTPUT(f"DEBUG: Reference lookup cache hit count: {structured_data.ref_lookup_cache_hit_count}")
        PRINT_OUTPUT(f"DEBUG: Reference lookup cache miss count: {structured_data.ref_lookup_cache_miss_count}")
        PRINT_OUTPUT(f"DEBUG: Reference lookup count: {structured_data.ref_lookup_count}")
        PRINT_OUTPUT(f"DEBUG: Reference lookup found count: {structured_data.ref_lookup_found_count}")
        PRINT_OUTPUT(f"DEBUG: Reference lookup not found count: {structured_data.ref_lookup_notfound_count}")
        PRINT_OUTPUT(f"DEBUG: Reference lookup error count: {structured_data.ref_lookup_error_count}")
        PRINT_OUTPUT(f"DEBUG: Reference invalid identifying property count:"
                     f" {structured_data.ref_invalid_identifying_property_count}")
    if json_only:
        PRINT_OUTPUT(json.dumps(structured_data.data, indent=4))
        exit(1)
    if verbose_json:
        PRINT_OUTPUT(f"Parsed JSON:")
        PRINT_OUTPUT(json.dumps(structured_data.data, indent=4))
    validation_okay = _validate_data(structured_data, portal, ingestion_filename,
                                     upload_folder, recursive=subfolders, verbose=verbose, debug=debug)
    if validation_okay:
        PRINT("Validation results (preliminary): OK")
    elif exit_immediately_on_errors:
        if verbose:
            _print_structured_data_verbose(portal, structured_data, ingestion_filename, upload_folder=upload_folder,
                                           recursive=subfolders, validation=validation, noanalyze=True, verbose=verbose)
        if output_file:
            PRINT_STDOUT(f"Exiting with preliminary validation errors; see your output file: {output_file}")
        else:
            if not verbose:
                PRINT_STDOUT()
            PRINT_STDOUT(f"Exiting with preliminary validation errors.")
            PRINT_STDOUT("Use the --output FILE option to write errors to a file.")
        exit(1)

    # They don't want to present upload file info on validate, only on submit.
    # _review_upload_files(structured_data, ingestion_filename,
    #                      validation=validation, directory=upload_folder, recursive=subfolders)

    if verbose:
        _print_structured_data_verbose(portal, structured_data, ingestion_filename, upload_folder=upload_folder,
                                       recursive=subfolders, validation=validation, verbose=verbose)
    elif not quiet:
        if not noanalyze:
            _print_structured_data_status(portal, structured_data, validation=validation,
                                          report_updates_only=True, noprogress=noprogress, verbose=verbose, debug=debug)
        else:
            PRINT("Skipping analysis of metadata wrt creates/updates to be done (via --noanalyze).")
    if not validation_okay:
        if not yes_or_no(f"There are some preliminary errors outlined above;"
                         f" do you want to continue with {'validation' if validation else 'submission'}?"):
            exit(1)
    if validate_local_only:
        PRINT("Terminating as requested (via --validate-local-only).")
        exit(0 if validation_okay else 1)

    return structured_data


def _review_upload_files(structured_data: StructuredDataSet, ingestion_filename: str, validation: bool = False,
                         directory: Optional[str] = None, recursive: bool = False) -> None:

    nfiles_found, file_validation_errors = _validate_files(structured_data, ingestion_filename,
                                                           upload_folder=directory, recursive=recursive)
    if file_validation_errors:
        nfiles = len(file_validation_errors)
        if nfiles == 1:
            PRINT(f"WARNING: There is one file referenced which is missing (below).")
            PRINT(f"- {file_validation_errors[0]}")
        else:
            PRINT(f"WARNING: However there are {nfiles} files referenced which are missing.")
            if yes_or_no(f"Do you want to see a list of these {nfiles} missing file{'s' if nfiles != 1 else ''}?"):
                for error in file_validation_errors:
                    PRINT(f"- {error}")
        if not validation:
            if not yes_or_no(f"Do you want to continue even with"
                             f" {'these' if nfiles != 1 else 'this'} missing file{'s' if nfiles != 1 else ''}?"):
                exit(1)
        else:
            PRINT(f"Continuing even with {'these' if nfiles != 1 else 'this'}"
                  f" missing file{'s' if nfiles != 1 else ''} as noted above.")
    if nfiles_found > 0:
        PRINT(f"Files referenced for upload (and which exist): {nfiles_found}")
    elif not file_validation_errors:
        PRINT("No files to upload were referenced.")


def _validate_data(structured_data: StructuredDataSet, portal: Portal, ingestion_filename: str,
                   upload_folder: str, recursive: bool, verbose: bool = False, debug: bool = False) -> bool:
    nerrors = 0

    if initial_validation_errors := _validate_initial(structured_data, portal):
        nerrors += len(initial_validation_errors)

    if ref_validation_errors := _validate_references(structured_data.ref_errors, ingestion_filename, debug=debug):
        nerrors += len(ref_validation_errors)

    structured_data.validate()
    if data_validation_errors := structured_data.validation_errors:
        nerrors += len(data_validation_errors)

    if nerrors > 0:
        PRINT_OUTPUT("Validation results (preliminary): ERROR")

    printed_newline = False

    if initial_validation_errors:
        if not printed_newline:
            PRINT_OUTPUT()
            printed_newline = True
        PRINT_OUTPUT(f"- Initial errors: {len(initial_validation_errors)}")
        for error in initial_validation_errors:
            PRINT_OUTPUT(f"  - ERROR: {error}")

    if data_validation_errors:
        if not printed_newline:
            PRINT_OUTPUT()
            printed_newline = True
        PRINT_OUTPUT(f"- Data errors: {len(data_validation_errors)}")
        for error in data_validation_errors:
            PRINT_OUTPUT(f"  - ERROR: {_format_issue(error, ingestion_filename)}")

    if ref_validation_errors:
        if not printed_newline:
            PRINT_OUTPUT()
            printed_newline = True
        _print_reference_errors(ref_validation_errors, verbose=verbose, debug=debug)
        # PRINT_OUTPUT(f"- Reference errors: {len(ref_validation_errors)}")
        # if debug:
        #     for error in ref_validation_errors:
        #         PRINT_OUTPUT(f"  - ERROR: {error}")
        # else:
        #     for error in ref_validation_errors:
        #         PRINT_OUTPUT(f"  - ERROR: {error['ref']} (refs: {error['count']})")

    return not (nerrors > 0)


def _validate_references(ref_errors: Optional[List[dict]], ingestion_filename: str, debug: bool = False) -> List[str]:
    def normalize(ref_errors: Optional[List[dict]]) -> None:  # noqa
        # Server sends back fill path to "file"; adjust to basename; fix on server (TODO).
        if isinstance(ref_errors, list):
            for ref_error in ref_errors:
                if isinstance(src := ref_error.get("src"), dict) and isinstance(file := src.get("file"), str):
                    src["file"] = os.path.basename(file)
    normalize(ref_errors)
    ref_validation_errors = []
    ref_validation_errors_truncated = None
    if isinstance(ref_errors, list):
        for ref_error in ref_errors:
            if debug:
                ref_validation_errors.append(f"{_format_issue(ref_error, ingestion_filename)}")
            elif ref_error.get("truncated") is True:
                ref_validation_errors_truncated = {"ref": f"{_format_issue(ref_error, ingestion_filename)}"}
            elif ref_error.get("ref"):
                # TODO: Can we actually get here?
                ref_validation_errors.append(ref_error)
            else:
                if ref := ref_error.get("error"):
                    if ref_error_existing := [r for r in ref_validation_errors if r.get("ref") == ref]:
                        ref_error_existing = ref_error_existing[0]
                        ref_error_existing["count"] += 1
                        if isinstance(src := ref_error.get("src"), dict):
                            if isinstance(ref_error_existing.get("srcs"), list):
                                ref_error_existing["srcs"].append(src)
                            else:
                                ref_error_existing["srcs"] = [src]
                    else:
                        ref_validation_error = {"ref": ref, "count": 1}
                        if isinstance(src := ref_error.get("src"), dict):
                            ref_validation_error["srcs"] = [src]
                        ref_validation_errors.append(ref_validation_error)
    if debug:
        ref_validation_errors = sorted(ref_validation_errors)
    else:
        ref_validation_errors = sorted(ref_validation_errors, key=lambda item: item.get("ref"))
    if ref_validation_errors_truncated:
        ref_validation_errors.append(ref_validation_errors_truncated)
    return ref_validation_errors


def _print_reference_errors(ref_errors: List[dict], verbose: bool = False, debug: bool = False) -> None:
    if errors := _format_reference_errors(ref_errors=ref_errors, verbose=verbose, debug=debug):
        for error in errors:
            PRINT_OUTPUT(error)


def _format_reference_errors(ref_errors: List[dict], verbose: bool = False, debug: bool = False) -> List[str]:
    errors = []
    if isinstance(ref_errors, list) and ref_errors:
        nref_errors = len([r for r in ref_errors
                           if (not isinstance(r, dict)) or (not r.get('ref', '').startswith('Truncated'))])
        errors.append(f"- Reference errors: {nref_errors}")
        if debug:
            for ref_error in ref_errors:
                errors.append(f"  - ERROR: {ref_error}")
        else:
            truncated = None
            for ref_error in ref_errors:
                if ref_error["ref"].startswith("Truncated"):
                    truncated = ref_error["ref"]
                elif isinstance(count := ref_error.get("count"), int):
                    errors.append(f"  - ERROR: {ref_error['ref']} (refs: {count})")
                    if verbose and isinstance(srcs := ref_error.get("srcs"), list):
                        for src in srcs:
                            errors.append(f"    - {_format_src(src)}")
                else:
                    errors.append(f"  - ERROR: {ref_error['ref']}")
            if truncated:
                errors.append(f"  - {truncated}")
    return errors


def _validate_files(structured_data: StructuredDataSet, ingestion_filename: str,
                    upload_folder: str, recursive: bool) -> Tuple[int, List[str]]:
    file_validation_errors = []
    if files := structured_data.upload_files_located(location=[upload_folder,
                                                               os.path.dirname(ingestion_filename) or "."],
                                                     recursive=recursive):
        if files_not_found := [file for file in files if not file.get("path")]:
            for file in sorted(files_not_found, key=lambda key: key.get("file")):
                file_validation_errors.append(f"{file.get('file')} -> File not found ({file.get('type')})")
    return len(files) - len(file_validation_errors), sorted(file_validation_errors)


def _validate_initial(structured_data: StructuredDataSet, portal: Portal) -> List[str]:
    # TODO: Move this more specific "pre" validation checking to dcicutils.structured_data.
    # Just for nicer more specific (non-jsonschema) error messages for common problems.
    initial_validation_errors = []
    if not (portal and structured_data and structured_data.data):
        return initial_validation_errors
    for schema_name in structured_data.data:
        if schema_data := portal.get_schema(schema_name):
            if identifying_properties := schema_data.get(EncodedSchemaConstants.IDENTIFYING_PROPERTIES):
                identifying_properties = set(identifying_properties)
                if data := structured_data.data[schema_name]:
                    data_properties = set(data[0].keys())
                    if not data_properties & identifying_properties:
                        # No identifying properties for this object.
                        initial_validation_errors.append(f"No identifying properties for type: {schema_name}")
            if required_properties := schema_data.get(JsonSchemaConstants.REQUIRED):
                required_properties = set(required_properties) - set("submission_centers")
                if data := structured_data.data[schema_name]:
                    data_properties = set(data[0].keys())
                    if (data_properties & required_properties) != required_properties:
                        if missing_required_properties := required_properties - data_properties:
                            # Missing required properties for this object.
                            for missing_required_property in missing_required_properties:
                                initial_validation_errors.append(
                                    f"Missing required property ({missing_required_property})"
                                    f" for type: {schema_name}")
    return initial_validation_errors


def _print_structured_data_verbose(portal: Portal, structured_data: StructuredDataSet, ingestion_filename: str,
                                   upload_folder: str, recursive: bool, validation: bool = False,
                                   noanalyze: bool = False, noprogress: bool = False, verbose: bool = False) -> None:
    if (reader_warnings := structured_data.reader_warnings):
        PRINT_OUTPUT(f"\n> Parser warnings:")
        for reader_warning in reader_warnings:
            PRINT_OUTPUT(f"  - {_format_issue(reader_warning, ingestion_filename)}")
    PRINT_OUTPUT(f"\n> Types submitting:")
    for type_name in sorted(structured_data.data):
        PRINT_OUTPUT(f"  - {type_name}: {len(structured_data.data[type_name])}"
                     f" object{'s' if len(structured_data.data[type_name]) != 1 else ''}")
    if resolved_refs := structured_data.resolved_refs:
        PRINT_OUTPUT(f"\n> Resolved object (linkTo) references:")
        for resolved_ref in sorted(resolved_refs):
            PRINT_OUTPUT(f"  - {resolved_ref}")
    if files := structured_data.upload_files_located(location=[upload_folder,
                                                               os.path.dirname(ingestion_filename) or "."],
                                                     recursive=recursive):
        printed_header = False
        if files_found := [file for file in files if file.get("path")]:
            for file in files_found:
                path = file.get("path")
                if not printed_header:
                    PRINT_OUTPUT(f"\n> Resolved file references:")
                    printed_header = True
                PRINT_OUTPUT(f"  - {file.get('type')}: {file.get('file')} -> {path}"
                             f" [{format_size(get_file_size(path))}]")
    PRINT_OUTPUT()
    if not noanalyze:
        _print_structured_data_status(portal, structured_data,
                                      validation=validation,
                                      report_updates_only=True, noprogress=noprogress, verbose=verbose)
    else:
        PRINT("Skipping analysis of metadata wrt creates/updates to be done (via --noanalyze).")


def _print_structured_data_status(portal: Portal, structured_data: StructuredDataSet,
                                  validation: bool = False,
                                  report_updates_only: bool = False,
                                  noprogress: bool = False, verbose: bool = False, debug: bool = False) -> None:

    if verbose:
        report_updates_only = False

    def define_progress_callback(debug: bool = False) -> None:
        ntypes = 0
        nobjects = 0
        ncreates = 0
        nupdates = 0
        nlookups = 0
        bar = ProgressBar(nobjects, "Calculating", interrupt_exit=True, interrupt_message="analysis")
        def progress_report(status: dict) -> None:  # noqa
            nonlocal bar, ntypes, nobjects, ncreates, nupdates, nlookups, noprogress
            if noprogress:
                return
            increment = 1
            if status.get("start"):
                ntypes = status.get("types")
                nobjects = status.get("objects")
                bar.set_total(nobjects)
                PRINT(f"Analyzing submission file which has {ntypes} type{'s' if ntypes != 1 else ''}"
                      f" and a total of {nobjects} object{'s' if nobjects != 1 else ''}.")
                return
            elif status.get("finish"):
                bar.done()
                return
            elif status.get("create"):
                ncreates += increment
                nlookups += status.get("lookups") or 0
                bar.increment_progress(increment)
            elif status.get("update"):
                nupdates += increment
                nlookups += status.get("lookups") or 0
                bar.increment_progress(increment)
            else:
                nlookups += status.get("lookups") or 0
                bar.increment_progress(increment)
            # duration = time.time() - started
            # nprocessed = ncreates + nupdates
            # rate = nprocessed / duration
            # nremaining = nobjects - nprocessed
            # duration_remaining = (nremaining / rate) if rate > 0 else 0
            message = (
                f"▶ Items: {nobjects} | Checked: {ncreates + nupdates}"
                f" ‖ Creates: {ncreates} | Updates: {nupdates} | Lookups: {nlookups}")
            # if debug:
            #    message += f" | Rate: {rate:.1f}%"
            # message += " | Progress" # xyzzy
            bar.set_description(message)
        return progress_report

    # TODO: Allow abort of compare by returning some value from the
    # progress callback that just breaks out of the loop in structured_data.
    diffs = structured_data.compare(progress=define_progress_callback(debug=debug))

    ncreates = 0
    nupdates = 0
    nsubstantive_updates = 0
    for object_type in diffs:
        for object_info in diffs[object_type]:
            if object_info.uuid:
                if object_info.diffs:
                    nsubstantive_updates += 1
                nupdates += 1
            else:
                ncreates += 1

    to_or_which_would = "which would" if validation else "to"

    if ncreates > 0:
        if nupdates > 0:
            message = f"Objects {to_or_which_would} be -> Created: {ncreates} | Updated: {nupdates}"
            if nsubstantive_updates == 0:
                message += " (no substantive differences)"
        else:
            message = f"Objects {to_or_which_would} be created: {ncreates}"
    elif nupdates:
        message = f"Objects {to_or_which_would} be updated: {nupdates}"
        if nsubstantive_updates == 0:
            message += " (no substantive differences)"
    else:
        message = "No objects {to_or_which_would} create or update."
        return

    if report_updates_only and nsubstantive_updates == 0:
        PRINT(f"{message}")
        return
    else:
        if report_updates_only:
            PRINT(f"{message} | Update details below ...")
        else:
            PRINT(f"{message} | Details below ...")

    will_or_would = "Would" if validation else "Will"

    nreported = 0
    printed_newline = False
    for object_type in sorted(diffs):
        printed_type = False
        for object_info in diffs[object_type]:
            if report_updates_only and (not object_info.uuid or not object_info.diffs):
                # Create or non-substantive update, and report-updates-only.
                continue
            nreported += 1
            if not printed_newline:
                PRINT()
                printed_newline = True
            if not printed_type:
                PRINT(f"  TYPE: {object_type}")
                printed_type = True
            PRINT(f"  - OBJECT: {object_info.path}")
            if not object_info.uuid:
                PRINT(f"    Does not exist -> {will_or_would} be CREATED")
            else:
                message = f"    Already exists -> {object_info.uuid} -> {will_or_would} be UPDATED"
                if not object_info.diffs:
                    message += " (no substantive diffs)"
                    PRINT(message)
                else:
                    message += " (substantive DIFFs below)"
                    PRINT(message)
                    for diff_path in object_info.diffs:
                        if (diff := object_info.diffs[diff_path]).creating_value:
                            PRINT(f"     CREATE {diff_path}: {diff.value}")
                        elif diff.updating_value:
                            PRINT(f"     UPDATE {diff_path}: {diff.updating_value} -> {diff.value}")
                        elif (diff := object_info.diffs[diff_path]).deleting_value:
                            PRINT(f"     DELETE {diff_path}: {diff.value}")
    if nreported:
        PRINT()


def _print_json_with_prefix(data, prefix):
    json_string = json.dumps(data, indent=4)
    json_string = f"\n{prefix}".join(json_string.split("\n"))
    PRINT_OUTPUT(prefix, end="")
    PRINT_OUTPUT(json_string)


def _format_issue(issue: dict, original_file: Optional[str] = None) -> str:
    issue_message = None
    if issue:
        if error := issue.get("error"):
            issue_message = error.replace("'$.", "'")
            issue_message = error.replace("Validation error at '$': ", "")
        elif warning := issue.get("warning"):
            issue_message = warning
        elif issue.get("truncated"):
            return f"Truncated result set | More: {issue.get('more')} | See: {issue.get('details')}"
    return f"{_format_src(issue)}: {issue_message}" if issue_message else ""


def _format_src(issue: dict) -> str:
    def file_without_extension(file: str) -> str:
        if isinstance(file, str):
            if file.endswith(".gz"):
                file = file[:-3]
            if (dot := file.rfind(".")) > 0:
                file = file[:dot]
        return file
    if not isinstance(issue, dict):
        return ""
    if not isinstance(issue_src := issue.get("src"), dict):
        issue_src = issue
    if src_type := issue_src.get("type"):
        src = src_type
    elif src_sheet := issue_src.get("sheet"):
        src = src_sheet
    elif src_file := file_without_extension(issue_src.get("file")):
        src = src_file
    else:
        src = ""
    if src_column := issue_src.get("column"):
        src = f"{src}.{src_column}" if src else src_column
    if (src_row := issue_src.get("row", 0)) > 0:
        src = f"{src} [{src_row}]" if src else f"[{src_row}]"
    if not src:
        if issue.get("warning"):
            src = "Warning"
        elif issue.get("error"):
            src = "Error"
        else:
            src = "Issue"
    return src


def _define_portal(key: Optional[dict] = None, env: Optional[str] = None, server: Optional[str] = None,
                   app: Optional[str] = None, keys_file: Optional[str] = None, env_from_env: bool = False,
                   report: bool = False, verbose: bool = False, note: Optional[str] = None) -> Portal:

    def get_default_keys_file():
        nonlocal app
        return os.path.expanduser(os.path.join(Portal.KEYS_FILE_DIRECTORY, f".{app.lower()}-keys.json"))

    raise_exception = True
    if not app:
        app = DEFAULT_APP
        app_default = True
    else:
        app_default = False
    portal = None
    try:
        # TODO: raise_exception does not totally work here (see portal_utils.py).
        portal = Portal(key or keys_file, env=env, server=server, app=app, raise_exception=True)
    except Exception as e:
        if "not found in keys-file" in str(e):
            PRINT(f"ERROR: Environment ({env}) not found in keys file: {keys_file or get_default_keys_file()}")
            exit(1)
    if not portal or not portal.key:
        try:
            if keys_file and not os.path.exists(keys_file):
                PRINT(f"ERROR: No keys file found: {keys_file or get_default_keys_file()}")
                exit(1)
            else:
                default_keys_file = get_default_keys_file()
                if not os.path.exists(default_keys_file):
                    PRINT(f"ERROR: No default keys file found: {default_keys_file}")
                    exit(1)
        except Exception:
            pass
        if raise_exception:
            raise Exception(
                f"No portal key defined; setup your ~/.{app or 'smaht'}-keys.json file and use the --env argument.")
    if report:
        message = f"SMaHT submitr version: {get_version()}"
        if note:
            message += f" | {note}"
        PRINT(message)
        if verbose:
            PRINT(f"Portal app name is{' (default)' if app_default else ''}: {app}")
        PRINT(f"Portal environment (in keys file) is: {portal.env}{' (from SMAHT_ENV)' if env_from_env else ''}")
        PRINT(f"Portal keys file is: {format_path(portal.keys_file)}")
        PRINT(f"Portal server is: {portal.server}")
        if portal.key_id and len(portal.key_id) > 2:
            PRINT(f"Portal key prefix is: {portal.key_id[:2]}******")
    return portal


@lru_cache(maxsize=1)
def _get_consortia(portal: Portal) -> List[str]:
    results = []
    if consortia := portal.get_metadata("/consortia"):
        consortia = sorted(consortia.get("@graph", []), key=lambda key: key.get("identifier"))
        for consortium in consortia:
            if ((consortium_name := consortium.get("identifier")) and
                (consortium_uuid := consortium.get("uuid"))):  # noqa
                results.append({"name": consortium_name, "uuid": consortium_uuid})
    return results


@lru_cache(maxsize=1)
def _get_submission_centers(portal: Portal) -> List[str]:
    results = []
    if submission_centers := portal.get_metadata("/submission-centers"):
        submission_centers = sorted(submission_centers.get("@graph", []), key=lambda key: key.get("identifier"))
        for submission_center in submission_centers:
            if ((submission_center_name := submission_center.get("identifier")) and
                (submission_center_uuid := submission_center.get("uuid"))):  # noqa
                results.append({"name": submission_center_name, "uuid": submission_center_uuid})
    return results


def _is_accession_id(value: str) -> bool:
    # See smaht-portal/.../schema_formats.py
    return isinstance(value, str) and re.match(r"^SMA[1-9A-Z]{9}$", value) is not None
    # return isinstance(value, str) and re.match(r"^[A-Z0-9]{12}$", value) is not None


def _extract_accession_id(value: str) -> Optional[str]:
    if isinstance(value, str):
        if value.endswith(".gz"):
            value = value[:-3]
        value, _ = os.path.splitext(value)
        if _is_accession_id(value):
            return value


def _format_portal_object_datetime(value: str, verbose: bool = False) -> Optional[str]:  # noqa
    return format_datetime(datetime.fromisoformat(value))


def _print_metadata_file_info(file: str) -> None:
    PRINT(f"Metadata File: {os.path.basename(file)}")
    if size := get_file_size(file):
        PRINT(f"Size: {format_size(size)} ({size})")
    if modified := get_file_modified_datetime(file):
        PRINT(f"Modified: {modified}")
    if md5 := get_file_md5(file):
        PRINT(f"MD5: {md5}")
    if etag := get_file_md5_like_aws_s3_etag(file):
        PRINT(f"S3 ETag: {etag}{' | Same as MD5' if md5 == etag else ''}")
    sheet_lines = []
    if file.endswith(".xlsx") or file.endswith(".xls"):
        from dcicutils.data_readers import Excel
        excel = Excel(file)
        nrows_total = 0
        nsheets = 0
        for sheet_name in sorted(excel.sheet_names):
            nsheets += 1
            nrows = 0
            for row in excel.sheet_reader(sheet_name):
                nrows += 1
            sheet_lines.append(f"- Sheet: {sheet_name} ▶ Rows: {nrows}")
            nrows_total += nrows
        sheet_lines = "\n" + "\n".join(sheet_lines)
        PRINT(f"Sheets: {nsheets} | Rows: {nrows_total}{sheet_lines}")


def _ping(app: str, env: str, server: str, keys_file: str,
          env_from_env: bool = False, verbose: bool = False) -> bool:
    portal = _define_portal(env=env, server=server, app=app, keys_file=keys_file,
                            env_from_env=env_from_env, report=verbose)
    return portal.ping()


def _pytesting():
    return "pytest" in sys.modules
