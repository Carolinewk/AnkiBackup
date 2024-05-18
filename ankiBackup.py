import os
from google_drive import upload
# py autogi

appdata_roaming = os.getenv("APPDATA")
home_dir = os.path.expanduser("~")
local_dir = os.path.join(home_dir, ".local")

pathInEnv = os.getenv("FILE_PATH")
if pathInEnv:
    filePath = pathInEnv
else:
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
    except:
        continue

getAllLastBackups = {}

for user in listOfUsers:
    filepath = os.listdir(f"{filePath}/{user}/backups")
    getAllLastBackups[user] = f"{filePath}/{user}/backups/{filepath[-1]}"

for user, backupName in getAllLastBackups.items():
    upload("1DKJl8bjN7nZaB-8-nrxMZciFg_D_zfT2", [backupName])
