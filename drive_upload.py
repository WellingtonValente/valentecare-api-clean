
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def upload_file_to_drive(filepath, pasta="ValenteCareUploads"):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # Procurar ou criar pasta da empresa
    folder_id = None
    file_list = drive.ListFile({'q': f"title='{pasta}' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    if file_list:
        folder_id = file_list[0]['id']
    else:
        folder_metadata = {
            'title': pasta,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        folder_id = folder['id']

    # Upload do arquivo para a pasta
    arquivo = drive.CreateFile({'title': os.path.basename(filepath), 'parents': [{'id': folder_id}]})
    arquivo.SetContentFile(filepath)
    arquivo.Upload()
    print(f"Arquivo '{filepath}' enviado com sucesso ao Google Drive na pasta '{pasta}'.")
