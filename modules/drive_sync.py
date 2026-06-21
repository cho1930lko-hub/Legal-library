import json, os, io
import streamlit as st


def _get_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        info = dict(st.secrets["gcp_service_account"])
        
        # अपने personal Gmail को delegate करें
        # Streamlit Secrets में GOOGLE_DELEGATED_EMAIL डालें
        try:
            delegated_email = st.secrets.get("GOOGLE_DELEGATED_EMAIL", "cho1930lko@gmail.com")
        except:
            delegated_email = os.getenv("GOOGLE_DELEGATED_EMAIL", "cho1930lko@gmail.com")

        scopes = ["https://www.googleapis.com/auth/drive"]
        
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=scopes
        )
        
        # अगर delegated email है तो उससे काम करो
        if delegated_email:
            creds = creds.with_subject(delegated_email)
        
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        return None


class DriveSync:
    def __init__(self):
        self.service = _get_service()
        try:
            self.folder_id = st.secrets.get("GOOGLE_DRIVE_FOLDER_ID", "cho1930lko@gmail.com")
        except:
            self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "cho1930lko@gmail.com")

    def is_connected(self):
        return self.service is not None and bool(self.folder_id)

    def upload_json(self, local_path, drive_filename):
        if not self.is_connected():
            return False
        try:
            from googleapiclient.http import MediaFileUpload

            # File exist करती है?
            results = self.service.files().list(
                q=f"name='{drive_filename}' and '{self.folder_id}' in parents and trashed=false",
                fields="files(id)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            files = results.get("files", [])

            media = MediaFileUpload(local_path, mimetype="application/json", resumable=False)

            if files:
                # Update existing
                self.service.files().update(
                    fileId=files[0]["id"],
                    media_body=media,
                    supportsAllDrives=True
                ).execute()
            else:
                # Create new
                self.service.files().create(
                    body={"name": drive_filename, "parents": [self.folder_id]},
                    media_body=media,
                    fields="id",
                    supportsAllDrives=True
                ).execute()
            return True
        except Exception as e:
            st.error(f"Upload error: {e}")
            return False

    def download_json(self, drive_filename, local_path):
        if not self.is_connected():
            return False
        try:
            results = self.service.files().list(
                q=f"name='{drive_filename}' and '{self.folder_id}' in parents and trashed=false",
                fields="files(id)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            files = results.get("files", [])
            if not files:
                return False

            fh = io.BytesIO()
            request = self.service.files().get_media(
                fileId=files[0]["id"],
                supportsAllDrives=True
            )
            from googleapiclient.http import MediaIoBaseDownload
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

            with open(local_path, "wb") as f:
                f.write(fh.getvalue())
            return True
        except Exception as e:
            st.error(f"Download error: {e}")
            return False
