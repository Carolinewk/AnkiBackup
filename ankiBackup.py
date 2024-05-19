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

getAllLastBackups = {}

for user in listOfUsers:
    userPathBackup = filePath / user / "backups"
    listBackups = os.listdir(userPathBackup)
    getAllLastBackups[user] = userPathBackup / listBackups[-1]

folders = listFolders()

folderId = verifyAnkiBackupFolder(folders)

if folderId is None:
    folderId = createFolder("ankiBackup")

for user, backupName in getAllLastBackups.items():
    upload(folderId, [str(backupName)])
