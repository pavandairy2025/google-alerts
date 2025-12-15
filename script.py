import os
import json
from datetime import datetime
from pydrive2.auth import ServiceAccountCredentials
from pydrive2.drive import GoogleDrive
import pandas as pd

# ---------- CREATE OUTPUT FILE ----------
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df = pd.DataFrame({
    "Run_Time": [now],
    "Status": ["Automation ran successfully"]
})

output_file = "output.csv"
df.to_csv(output_file, index=False)
print("CSV created")

# ---------- GOOGLE DRIVE AUTH ----------
print("Secret length:", len(os.environ["GDRIVE_CREDENTIALS"]))
creds_json = json.loads(os.environ["GDRIVE_CREDENTIALS"])

with open("credentials.json", "w") as f:
    json.dump(creds_json, f)

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

drive = GoogleDrive(creds)

# ---------- UPLOAD TO DRIVE ----------
file = drive.CreateFile({
    'title': f'output_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
    'parents': [{'id': os.environ["GDRIVE_FOLDER_ID"]}]
})

file.SetContentFile(output_file)
file.Upload()

print("Uploaded to Google Drive")
