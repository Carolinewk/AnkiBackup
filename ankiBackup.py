import os
from google_drive import upload, createFolder, verifyAnkiBackupFolder, listFolders
from pathlib import Path
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

folders = listFolders()
folderId = verifyAnkiBackupFolder(folders)

if folderId is None:
    folderId = createFolder("ankiBackup")

ankiBackUpFolders = listFolders(folderId)

users_in_backup_folder = []

for file in ankiBackUpFolders['files']:
    users_in_backup_folder.append(file['name'])

getAllLastBackups = {}
usersFolderId = {}

for user in listOfUsers:
    userPathBackup = filePath / user / "backups"
    listBackups = os.listdir(userPathBackup)
    getAllLastBackups[user] = userPathBackup / listBackups[-1]
    if user not in users_in_backup_folder:
        userFolder = createFolder(user, folderId)
        usersFolderId[user] = userFolder


for user, backupName in getAllLastBackups.items():
    folderId = getAllLastBackups['folderId']
    upload(folderId, [str(backupName)])
