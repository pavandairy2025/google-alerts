from pydrive2.auth import ServiceAccountCredentials
from pydrive2.drive import GoogleDrive
import json

# --- GOOGLE DRIVE AUTH ---
creds_json = json.loads(os.environ["GDRIVE_CREDENTIALS"])

with open("credentials.json", "w") as f:
    json.dump(creds_json, f)

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

drive = GoogleDrive(creds)

# --- UPLOAD FILE ---
drive_file = drive.CreateFile({
    'title': os.path.basename(file_name),
    'parents': [{'id': os.environ["GDRIVE_FOLDER_ID"]}]
})
drive_file.SetContentFile(file_name)
drive_file.Upload()

print("✅ File uploaded to Google Drive")
