import os
import pickle

import pathlib
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def create_service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = scopes[0]  # [scopes for scope in scopes]

    cred = None
    pickle_file = f"token_{API_SERVICE_NAME}_{API_VERSION}.pickle"

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, "wb") as token:
            pickle.dump(cred, token)

    try:
        service = discovery.build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, "service created successfully")
        return service
    except Exception as e:
        print("Unable to connect.")
        print(e)
        return None


API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# lista pasta atual e encontra arquivo client secret
CLIENT_SECRET_FILE = ""
homeDir = pathlib.Path(__file__).parent.resolve()
filesInHomeDir = os.listdir(homeDir)
for file in filesInHomeDir:
    if "client_secret" in file:
        CLIENT_SECRET_FILE = file
        break

if not CLIENT_SECRET_FILE:
    CLIENT_SECRET_FILE = input(
        "Credenciais não encontradas. Indique o caminho para o arquivo: "
    )

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def upload(
    folder_id: str,
    file_names: list[str],
    mime_types=["application / vnd.google - apps.file"],
):
    """Upload files to a folder in Gdrive"""

    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {
            "name": file_name,
            "parents": [folder_id],
        }

    media = MediaFileUpload("{0}".format(file_name), mimetype=mime_type)

    assert service is not None
    file_id = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    return file_id


def rename(file_id, file_name):
    body = {"name": file_name}

    assert service is not None
    service.files().update(fileId=file_id, body=body, fields="id, name").execute()


def create_folder(folder_name, anki_backup_id=None):
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [anki_backup_id],
    }

    assert service is not None
    folder = service.files().create(body=file_metadata, fields="id").execute()
    return folder["id"]


def list_folders(folder_id=None):
    assert service is not None

    if not folder_id:
        query = "'root' in parents and trashed = False"
    else:
        query = f"parents = '{folder_id}'"

    results = (
        service.files()
        .list(
            q=query,
            spaces="drive",
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    return results


def verify_anki_backup_folder(results):
    for folder in results["files"]:
        if "ankiBackup" in folder["name"]:
            return folder.get("id")
