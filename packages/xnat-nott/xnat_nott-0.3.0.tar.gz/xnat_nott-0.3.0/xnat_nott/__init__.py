"""
XNAT_NOTT: Simple XNAT library

Local functions for XNAT containers developed to work with XNAT instances
at Nottingham or used by Nottingham researchers
"""
import csv
import getpass
import io
import json
import logging
import os
import sys
import tempfile
import urllib
import urllib3
import zipfile

import xmltodict
import requests

from ._version import __version__

LOG = logging.getLogger(__name__)

# Hacks to disable CA verification which breaks many servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["CURL_CA_BUNDLE"] = ""

def setup_logging(options, **kwargs):
    format = kwargs.get("format", "%(levelname)s: %(message)s")
    if options.debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=format)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=format)

def get_version(options):
    try:
        with open("version.txt") as f:
            options.version = f.read().strip()
    except IOError:
        options.version = "(unknown)"

def convert_dicoms(options, dicomdir, niftidir):
    LOG.info("Doing NIFTI conversion")
    dcm2niix_args = getattr(options, "dcm2niix_args", "-d 9 -m n -f %d_%q -z y -b y")
    os.makedirs(niftidir, exist_ok=True, mode=0o777)
    cmd = f'dcm2niix -o "{niftidir}" {dcm2niix_args} "{dicomdir}"'
    LOG.info(cmd)
    retval = os.system(cmd + f" 2>&1 1>>{niftidir}/dcm2niix.log")
    if retval != 0:
        LOG.warning(f"DICOM->NIFTI conversion returned error status {retval}")
    return retval

def get_host_url(options):
    """
    Get the 'real' URL for XNAT, since it may be subject to redirects and these mess up POST/PUT requests
    """
    if not getattr(options, "host", None):
        options.host = os.environ.get("XNAT_HOST", None)
    if not options.host:
        raise RuntimeError("XNAT host not specified and not in environment")
    LOG.info(f"Checking host URL: {options.host}")
    options.host = options.host.rstrip("/")
    r = requests.get(options.host + "/", verify=False, allow_redirects=False)
    if r.status_code in (301, 302):
        new_host = r.headers['Location']
        LOG.info(f" - Redirect detected: {new_host}")
        # Sometimes gets redirected to login page - don't want this!
        if "/app/" in new_host:
            new_host = new_host[:new_host.index("/app/")]
        options.host = new_host
    options.host = options.host.rstrip("/")

def get_credentials(options):
    get_host_url(options)
    if not getattr(options, "user", None):
        options.user = os.environ.get("XNAT_USER", None)
    if not options.user:
        options.user = input("XNAT username: ")
    options.password = os.environ.get("XNAT_PASS", None)
    if not options.password:
        options.password = getpass.getpass()
    LOG.info(f"Using XNAT server at: {options.host} with username: {options.user}")

def get_projects(options):
    """
    Get project details
    """
    LOG.debug("Getting projects")
    try:
        params = {"format" : "csv"}
        csvdata = xnat_get(options, "data/projects/", params=params)
        return list(csv.DictReader(io.StringIO(csvdata)))
    except Exception:
        LOG.exception("Error getting projects")
        return []

def get_project(options, project_identifier):
    """
    Get project details from specified project name/ID

    :param project_identifier: Case insensitive identifier, may be ID or name
    """
    project_identifier = project_identifier.lower()
    projects = get_projects(options)
    for p in projects:
        if p["ID"].lower() == project_identifier or p["name"].lower() == project_identifier:
            return p

    project_names = [p["name"] for p in projects]
    raise RuntimeError(f"Project not found: {project_identifier} - known project: {project_names}")

def get_subjects(options, project):
    """
    Get subject details for specified project
    """
    project_id = project["ID"]
    LOG.debug(f"Getting subjects for prject {project_id}")
    params = {"format" : "csv"}
    csvdata = xnat_get(options, f"data/projects/{project_id}/subjects/", params=params)
    subjects = list(csv.DictReader(io.StringIO(csvdata)))
    return subjects

def get_subject(options, project, subject_identifier):
    """
    Get subject details from specified project and subject label/ID

    :param subject_identifier: Case insensitive identifier, may be ID or label
    """
    subject_identifier = subject_identifier.lower()
    subjects = get_subjects(options, project)
    for s in subjects:
        if s["ID"].lower() == subject_identifier or s["label"].lower() == subject_identifier:
            return s

    raise RuntimeError(f"Subject not found: {subject_identifier}")

def get_sessions(options, project, subject):
    """
    Get session details for specified project and subject
    """
    project_id = project["ID"]
    subject_id = subject["ID"]
    LOG.debug(f"Getting sessions for project {project_id}, subject {subject_id}")
    sessions = []

    params = {"xsiType": "xnat:mrSessionData", "format" : "csv"}
    csvdata = xnat_get(options, f"data/projects/{project_id}/subjects/{subject_id}/experiments/", params=params)
    for session in list(csv.DictReader(io.StringIO(csvdata))):
        session["subject"] = subject_id
        session["subject_label"] = subject['label']
        sessions.append(session)
    return sessions

def get_session(options, project, subject, session_identifier):
    """
    Get session details from specified project, subject and session label/ID

    :param session_identifier: Case insensitive identifier, may be ID or name
    """
    session_identifier = session_identifier.lower()
    sessions = get_sessions(options, project, subject)
    for s in sessions:
        if s["ID"].lower() == session_identifier or s["label"].lower() == session_identifier:
            return s

    raise RuntimeError(f"Session not found: {session_identifier}")

def get_all_from_session_id(options, session_id):
    """
    Get project, subject and session details from a session ID
    """
    LOG.debug(f"Getting session {session_id}")

    params = {"xsiType": "xnat:mrSessionData", "format" : "xml"}
    xmldata = xnat_get(options, f"data/experiments/{session_id}", params=params)
    try:
        session = xmltodict.parse(xmldata)["xnat:MRSession"]
    except KeyError:
        raise RuntimeError(f"Session not found: {session_id}")

    project_id = session['@project']
    project = get_project(options, project_id)
    subject_id = session['xnat:subject_ID']
    subject = get_subject(options, project, subject_id)
    session = get_session(options, project, subject, session_id)

    return project, subject, session

def get_all_sessions(options, project):
    """
    Get session details for all subjects in specified project
    """
    project_id = project["ID"]
    LOG.debug(f"Getting all sessions for project {project_id}")

    subjects = get_subjects(options, project)
    sessions = []
    for subject in subjects:
        sessions += get_sessions(options, project, subject)
    return sessions

def get_scans(options, session):
    """
    Get scan metadata for a session
    """
    session_id = session["ID"]
    LOG.debug(f"Getting scans for session {session_id}")
    params = {"format" : "csv"}
    csvdata = xnat_get(options, f"data/experiments/{session_id}/scans/", params=params)
    return list(csv.DictReader(io.StringIO(csvdata)))

def get_assessors(options, session, assessor_xsitype):
    """
    Get assessors for a session

    :return: List of assessor dictionaries
    """
    session_id = session["ID"]
    LOG.debug(f"Getting assessors for session {session_id}")
    params = {"format" : "csv", "xsiType" : assessor_xsitype, "columns" : "ID"}
    csvdata = xnat_get(options, f"data/experiments/{session_id}/assessors/", params=params)
    assessors = []
    for row in csv.DictReader(io.StringIO(csvdata), skipinitialspace=True):
        assessor_id = row['ID']
        assessor_xml = xnat_get(options, f"data/experiments/{session_id}/assessors/{assessor_id}", params={"format" : "xml"})
        assessor = xmltodict.parse(assessor_xml)[assessor_xsitype]
        assessor["ID"] = assessor_id
        assessors.append(assessor)

    return assessors

def add_assessor(options, xml, assessor_name):
    """
    Upload new assessor to XNAT
    """
    with tempfile.NamedTemporaryFile("w") as f:
        f.write(xml)
        LOG.info(f"Uploading assessor to {options.host}")
        LOG.debug(xml)
        url = f"data/projects/{options.project}/subjects/{options.subject}/experiments/{options.session}/assessors/"
        xnat_upload(options, url, f.name, replace_name=assessor_name)

def get_project_config_file(options, folder, fname, local_fname=None):
    """
    Get project-level configuration file
    """
    LOG.info(f"Downloading project level config {folder}/{fname} from XNAT")
    url = f"/data/projects/{options.project}/resources/{folder}/files/{fname}"
    if not local_fname:
        local_fname = fname
    xnat_download(options, url, local_fname=local_fname)

def get_command(options, project, command_name):
    project_id = project["ID"]
    LOG.info(f"Getting commands for project {project_id}")
    params = {"project" : project_id, "xsiType" : "xnat:mrSessionData"}
    jsondata = xnat_get(options, "/xapi/commands/available", params=params)
    commands = json.loads(jsondata)
    command = [c for c in commands if c["command-name"] == command_name]
    if not command:
        known_commands = [c["command-name"] for c in commands]
        raise RuntimeError(f"Unable to find command {options.command} - known commands: {known_commands}")
    if len(command) > 1:
        LOG.warn("Multiple commands found - returning first")
    return command[0]

def run_command(options, project, session, command, idx=""):
    command_name, command_id, wrapper_id = command["command-name"], command["command-id"], command["wrapper-id"]
    project_id, session_id = project["ID"], session["ID"]
    LOG.info(f"Running command {command_name} on session {idx} {session_id} : {session['label']}")

    url = f"xapi/projects/{project_id}/commands/{command_id}/wrappers/{wrapper_id}/launch/"
    params = {"session" : session_id}
    xnat_get(options, url, params=params, method="POST")
    LOG.info("Started successfully")

def get_session_dicoms(options, session_id, outdir):
    get_session_images(options, session_id, outdir, resource="DICOM")

def get_session_images(options, session_id, outdir, resource="DICOM"):
    LOG.info(f"Getting {resource}s for session {session_id}")
    data_fname = xnat_download(
        options,
        f"data/experiments/{session_id}/scans/ALL/resources/{resource}/files",
        params={"format" : "zip"}
    )
    try:
        with zipfile.ZipFile(data_fname, 'r') as z:
            z.extractall(outdir)
    finally:
        os.remove(data_fname)

def xnat_login(options):
    """
    Attempt to use the auth service to log in but fall back on HTTP basic auth if not working
    """
    url = f"{options.host}/data/services/auth"
    auth_params = {"username" : options.user, "password" : options.password}
    LOG.info(f"Attempting log in: {url} using xnat-nott v{__version__}")
    r = requests.put(url, verify=False, data=urllib.parse.urlencode(auth_params))
    LOG.debug(f"status: {r.status_code}")
    if r.status_code == 200:
        LOG.info(" - Logged in using auth service")
        options.cookies = {"JSESSIONID" : r.text}
        options.auth = None
    else:
        LOG.warn(f" - Failed to log in using auth service, status {r.status_code} - will use basic auth instead")
        LOG.warn(r.text)
        options.cookies = {}
        options.auth = (options.user, options.password)
    LOG.info("DONE login")

def xnat_get(options, url, params=None, method="GET"):
    """
    Get text content from XNAT, e.g. CSV/XML data
    """
    LOG.debug(f"Executing GET on {options.host}")
    url = url.lstrip("/")
    url = f"{options.host}/{url}"
    LOG.debug(f" - URL: {url}")
    tries = 0
    method_impl = getattr(requests, method.lower(), None)
    if not method_impl:
        raise RuntimeError(f"No such HTTP method: {method}")

    while tries < 10:
        tries += 1
        r = method_impl(url, verify=False, cookies=options.cookies, auth=options.auth, params=params)
        if r.status_code == 200:
            break
        if r.status_code == 401:
            LOG.info(" - Session expired, will re-login and retry")
            xnat_login(options)

    if r.status_code != 200:
        raise RuntimeError(f"Failed to execute {method} after 10 tries: {r.status_code} {r.text}")
    return r.text

def xnat_download(options, url, params=None, local_fname=None):
    LOG.info(f"Downloading data from {options.host}")
    url = url.lstrip("/")
    url = f"{options.host}/{url}"
    LOG.info(f" - URL: {url}")
    r = requests.get(url, verify=False, cookies=options.cookies, auth=options.auth, params=params, stream=True)
    LOG.debug(f" - status: {r.status_code}")
    if r.status_code == 401:
        LOG.info(" - Session expired, will re-login and retry")
        xnat_login(options)
        r = requests.get(url, verify=False, cookies=options.cookies, auth=options.auth, params=params, stream=True)
    r.raise_for_status()

    if not local_fname:
        local_fname = tempfile.NamedTemporaryFile(delete=False).name
    try:
        with open(local_fname, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            LOG.info(f" - Downloaded to: {local_fname}")

        stats = os.stat(local_fname)
        LOG.info(f" - Byte size: {stats.st_size}")
        return local_fname
    except Exception:
        if local_fname and os.path.exists(local_fname):
            os.remove(local_fname)
        raise

def xnat_upload(options, url, local_fname, replace_name=None):
    """
    Upload data to XNAT
    """
    LOG.info(f"Uploading data to {options.host}")
    url = url.lstrip("/")
    url = f"{options.host}/{url}"
    LOG.info(f" - URL: {url}")

    with open(local_fname, "r") as f:
        files = {'file': f}
        while True:
            LOG.info(f"Posting to {url}")
            r = requests.post(url, files=files, auth=options.auth, cookies=options.cookies, verify=False, allow_redirects=False)
            if r.status_code == 409:
                LOG.info(" - File already exists")
                if replace_name:
                    LOG.info(" - will delete and replace")
                    delete_url = url + replace_name
                    LOG.info(f" - Delete URL: {delete_url}")
                    r = requests.delete(delete_url, auth=options.auth, cookies=options.cookies, verify=False)
                    if r.status_code == 200:
                        LOG.info(" - Delete successful - re-posting")
                        f.seek(0)
                        continue

            if r.status_code != 200:
                raise RuntimeError(f"Failed to upload data: {r.status_code} {r.text}")
            break
