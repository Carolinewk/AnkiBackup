import os
from google_drive import upload, create_folder
# py autogi


# se AnkiBackup não existir, criar. tem q listar as pastas no google drive primeiro
# create_folder("AnkiBackup")

pathInEnv = os.getenv("FILE_PATH")
if pathInEnv:
    filePath = pathInEnv
else:
    appdata_roaming = os.getenv("APPDATA")
    home_dir = os.path.expanduser("~")
    local_dir = os.path.join(home_dir, ".local")
    if os.name == "nt":
        filePath = f"{appdata_roaming}/Anki2"
    elif os.name == "posix":
        filePath = f"{local_dir}/share/Anki2"

ankiUsers = os.listdir(filePath)

listOfUsers = []

for ankiUser in ankiUsers:
    try:
        checkBackup = os.listdir(f"{filePath}/{ankiUser}")
        if "backups" in checkBackup:
            listOfUsers.append(ankiUser)
    except NotADirectoryError:
        continue

getAllLastBackups = {}

for user in listOfUsers:
    filepath = os.listdir(f"{filePath}/{user}/backups")
    getAllLastBackups[user] = f"{filePath}/{user}/backups/{filepath[-1]}"

for user, backupName in getAllLastBackups.items():
    if os.name == "nt":
        lastBackup = backupName.replace("/", "\\")
    upload(
        "1tlIomPv-xuKEDInWtglioci4wtHIBra1", [lastBackup]
    )  # mudar para pegar o "AnkiBackup" folder id
