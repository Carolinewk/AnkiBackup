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


path_in_env = os.getenv("FILE_PATH")
if path_in_env:
    file_path = path_in_env
else:
    if os.name == "nt":
        appdata = Path(os.getenv("APPDATA"))
        file_path = appdata / "Anki2"
    elif os.name == "posix":
        home_dir = os.path.expanduser("~")
        local_dir = Path(os.path.join(home_dir, ".local"))
        file_path = local_dir / "share" / "Anki2"

anki_users = os.listdir(file_path)

list_of_users = []

for anki_user in anki_users:
    try:
        user_path = file_path / anki_user  # type: ignore
        check_backup = os.listdir(user_path)
        if "backups" in check_backup:
            list_of_users.append(anki_user)
    except NotADirectoryError:
        continue

folders = list_folders()
folder_id = verify_anki_backup_folder(folders)

if folder_id is None:
    folder_id = create_folder("ankiBackup")

anki_backup_folders = list_folders(folder_id)

users_in_backup_folder = {}

for file in anki_backup_folders["files"]:
    users_in_backup_folder[file["name"]] = file["id"]

get_all_last_backups = {}
users_folder_id = {}

for user in list_of_users:
    user_path_backup = file_path / user / "backups"
    list_backups = os.listdir(user_path_backup)
    get_all_last_backups[user] = user_path_backup / list_backups[-1]
    if user not in users_in_backup_folder:
        user_folder = create_folder(user, folder_id)
        users_folder_id[user] = user_folder
    else:
        users_folder_id[user] = users_in_backup_folder[user]


for user, backup_name in get_all_last_backups.items():
    folder_id = users_folder_id[user]
    file_name = os.path.basename(backup_name)
    try:
        file_id = upload(folder_id, [str(backup_name)])
        rename(file_id["id"], file_name)
    except HttpError as e:
        print(e)
        continue
