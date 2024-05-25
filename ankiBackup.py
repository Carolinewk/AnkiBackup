import os
from google_drive import (
    create_folder,
    list_folders,
    rename,
    upload,
    verify_anki_backup_folder,
)
from pathlib import Path
from googleapiclient.errors import HttpError
# py autogi


pathInEnv = os.getenv("FILE_PATH")
if pathInEnv:
    filePath = pathInEnv
else:
    if os.name == "nt":
        appdata = Path(os.getenv("APPDATA"))
        filePath = appdata / "Anki2"
    elif os.name == "posix":
        home_dir = os.path.expanduser("~")
        local_dir = Path(os.path.join(home_dir, ".local"))
        filePath = local_dir / "share" / "Anki2"

ankiUsers = os.listdir(filePath)

listOfUsers = []

for ankiUser in ankiUsers:
    try:
        userPath = filePath / ankiUser  # type: ignore
        checkBackup = os.listdir(userPath)
        if "backups" in checkBackup:
            listOfUsers.append(ankiUser)
    except NotADirectoryError:
        continue

folders = list_folders()
folderId = verify_anki_backup_folder(folders)

if folderId is None:
    folderId = create_folder("ankiBackup")

ankiBackUpFolders = list_folders(folderId)

users_in_backup_folder = {}

for file in ankiBackUpFolders["files"]:
    users_in_backup_folder[file["name"]] = file["id"]

getAllLastBackups = {}
usersFolderId = {}

for user in listOfUsers:
    userPathBackup = filePath / user / "backups"
    listBackups = os.listdir(userPathBackup)
    getAllLastBackups[user] = userPathBackup / listBackups[-1]
    if user not in users_in_backup_folder:
        userFolder = create_folder(user, folderId)
        usersFolderId[user] = userFolder
    else:
        usersFolderId[user] = users_in_backup_folder[user]


for user, backupName in getAllLastBackups.items():
    folderId = usersFolderId[user]
    fileName = os.path.basename(backupName)
    try:
        fileId = upload(folderId, [str(backupName)])
        rename(fileId["id"], fileName)
    except HttpError as e:
        print(e)
        continue
