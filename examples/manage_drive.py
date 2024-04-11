# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.oauth2 import service_account
# #https://drive.google.com/drive/folders/13IxgKy63UwURCnWg8XvsSpeDWiLdr2-F?usp=sharing

credentials = "googleapi_key\youtube-radio-418701-798128a6981b.json"

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Replace 'FOLDER_NAME' with the name you want to give your new folder
folder_name = 'Test Upload'


# setup google drive
credentials = service_account.Credentials.from_service_account_file(
        'googleapi_key\youtube-radio-418701-798128a6981b.json', 
        scopes=['https://www.googleapis.com/auth/drive']
    )
service = build("drive", "v3", credentials=credentials)
folder_metadata = {
    'name': folder_name,
    "parents": ['13IxgKy63UwURCnWg8XvsSpeDWiLdr2-F'],
    'mimeType': 'application/vnd.google-apps.folder'
}

# create folder 
new_folder = service.files().create(body=folder_metadata).execute()
