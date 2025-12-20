import feedparser
import pandas as pd
from datetime import datetime
import os
import json

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

# ---------------- CONFIG ----------------
RSS_FEEDS = {
    "Dairy_Industry": "https://www.google.com/alerts/feeds/13661428012330067824/14912746933511886095",
}

# ---------------- FETCH GOOGLE ALERTS ----------------
all_entries = []

for topic, url in RSS_FEEDS.items():
    feed = feedparser.parse(url)

    for entry in feed.entries:
        all_entries.append({
            "Topic": topic,
            "Title": entry.title,
            "Link": entry.link,
            "Published": entry.get("published", ""),
            "Fetched_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# Convert to DataFrame
df = pd.DataFrame(all_entries)

# Save CSV
filename = f"google_alerts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
df.to_csv(filename, index=False)
print("CSV created:", filename)

# ---------------- GOOGLE DRIVE AUTH (SERVICE ACCOUNT) ----------------

# Load credentials JSON from GitHub Secret
creds_json = json.loads(os.environ["GDRIVE_CREDENTIALS"])

with open("credentials.json", "w") as f:
    json.dump(creds_json, f)

# Setup GoogleAuth
gauth = GoogleAuth()

scope = ["https://www.googleapis.com/auth/drive"]
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

# Create Drive object
drive = GoogleDrive(gauth)

# ---------------- UPLOAD TO GOOGLE DRIVE ----------------
file = drive.CreateFile({
    "title": filename
})
file.SetContentFile(filename)
file.Upload()

print("Uploaded to Google Drive successfully")
