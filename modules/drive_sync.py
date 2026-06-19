import json, os
import streamlit as st

def _get_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        info = dict(st.secrets["gcp_service_account"])
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        return None

class DriveSync:
    def __init__(self):
        self.service = _get_service()
        try:
            self.folder_id = st.secrets.get("GOOGLE_DRIVE_FOLDER_ID","")
        except:
            self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID","")

    def is_connected(self):
        return self.service is not None and bool(self.folder_id)

    def upload_json(self, local_path, drive_filename):
        if not self.is_connected(): return False
        try:
            from googleapiclient.http import MediaFileUpload
            results = self.service.files().list(
                q=f"name='{drive_filename}' and '{self.folder_id}' in parents and trashed=false",
                fields="files(id)"
            ).execute()
            files = results.get("files",[])
            media = MediaFileUpload(local_path, mimetype="application/json")
            if files:
                self.service.files().update(fileId=files[0]["id"], media_body=media).execute()
            else:
                self.service.files().create(
                    body={"name":drive_filename,"parents":[self.folder_id]},
                    media_body=media, fields="id"
                ).execute()
            return True
        except Exception as e:
            st.error(f"Upload error: {e}")
            return False

    def download_json(self, drive_filename, local_path):
        if not self.is_connected(): return False
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io
            results = self.service.files().list(
                q=f"name='{drive_filename}' and '{self.folder_id}' in parents and trashed=false",
                fields="files(id)"
            ).execute()
            files = results.get("files",[])
            if not files: return False
            fh = io.BytesIO()
            MediaIoBaseDownload(fh, self.service.files().get_media(fileId=files[0]["id"])).next_chunk()
            with open(local_path,"wb") as f:
                f.write(fh.getvalue())
            return True
        except Exception as e:
            st.error(f"Download error: {e}")
            return False
