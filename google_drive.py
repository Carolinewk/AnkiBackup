import os
import pickle
from googleapiclient import discovery
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow, InstalledAppFlow


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


# "client_secret"

# nebuzoka
#CLIENT_SECRET_FILE = "client_secret_566868905417-g3difppfkga03a99hdvofmnguokj4hgn.apps.googleusercontent.com.json"
CLIENT_SECRET_FILE= "client_secret_860763931823-ormt3p4dh5r6gfs2fb9pgq9186ocmnms.apps.googleusercontent.com.json"

API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]


service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def upload(
    folder_id: str,
    file_names: list[str],
    mime_types=["application / vnd.google - apps.file"],
):
    """Upload files to a folder in Gdrive"""

    for file_name, mime_type in zip(file_names, mime_types):
        file_metadata = {"name": file_name, "parents": [folder_id]}

    media = MediaFileUpload("{0}".format(file_name), mimetype=mime_type)

    service.files().create(body=file_metadata, media_body=media, fields="id").execute()


def create_folder(folder_name):

    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder['id']
