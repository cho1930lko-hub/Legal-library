"""
modules/drive_sync.py
Google Drive Sync — JSON files upload/download
"""

import os
import json
from config import GOOGLE_CREDENTIALS_PATH, GOOGLE_DRIVE_FOLDER_ID


class DriveSync:
    def __init__(self):
        self.service = None
        self._connect()

    def _connect(self):
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build

            SCOPES = ["https://www.googleapis.com/auth/drive.file"]
            creds = None

            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                elif os.path.exists(GOOGLE_CREDENTIALS_PATH):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        GOOGLE_CREDENTIALS_PATH, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    with open("token.json", "w") as token:
                        token.write(creds.to_json())
                else:
                    return  # credentials.json नहीं है

            self.service = build("drive", "v3", credentials=creds)
        except Exception:
            self.service = None

    def is_connected(self) -> bool:
        return self.service is not None

    def upload_json(self, local_path: str, drive_filename: str) -> bool:
        if not self.is_connected():
            return False
        try:
            from googleapiclient.http import MediaFileUpload

            # पहले देखें file already है?
            results = self.service.files().list(
                q=f"name='{drive_filename}' and '{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false",
                fields="files(id)"
            ).execute()
            files = results.get("files", [])

            media = MediaFileUpload(local_path, mimetype="application/json")

            if files:
                # Update existing
                self.service.files().update(
                    fileId=files[0]["id"], media_body=media
                ).execute()
            else:
                # Create new
                meta = {"name": drive_filename, "parents": [GOOGLE_DRIVE_FOLDER_ID]}
                self.service.files().create(
                    body=meta, media_body=media, fields="id"
                ).execute()
            return True
        except Exception as e:
            print(f"Drive upload error: {e}")
            return False

    def download_json(self, drive_filename: str, local_path: str) -> bool:
        if not self.is_connected():
            return False
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io

            results = self.service.files().list(
                q=f"name='{drive_filename}' and '{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false",
                fields="files(id)"
            ).execute()
            files = results.get("files", [])

            if not files:
                return False

            request = self.service.files().get_media(fileId=files[0]["id"])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

            with open(local_path, "wb") as f:
                f.write(fh.getvalue())
            return True
        except Exception as e:
            print(f"Drive download error: {e}")
            return False
