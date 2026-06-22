import json, os, base64
import streamlit as st


def _get_config():
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        repo  = st.secrets.get("GITHUB_REPO", "")
    except:
        token = os.getenv("GITHUB_TOKEN", "")
        repo  = os.getenv("GITHUB_REPO", "")
    return token, repo


class DriveSync:
    """
    GitHub API को database की तरह use करता है।
    case_laws.json, cca_rules.json आदि GitHub repo के data/ folder में save होती हैं।
    """

    def __init__(self):
        self.token, self.repo = _get_config()
        self.api_base = f"https://api.github.com/repos/{self.repo}/contents/data"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def is_connected(self):
        return bool(self.token) and bool(self.repo)

    def _get_file_sha(self, filename):
        """GitHub पर file का SHA लो — update के लिए जरूरी है"""
        import requests
        url = f"{self.api_base}/{filename}"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json().get("sha")
        return None

    def upload_json(self, local_path, drive_filename):
        """Local JSON file को GitHub repo के data/ folder में save करो"""
        if not self.is_connected():
            return False
        try:
            import requests

            # File का content पढ़ो
            with open(local_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Base64 encode करो
            encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

            # पहले SHA लो (file exist करती है?)
            sha = self._get_file_sha(drive_filename)

            url = f"{self.api_base}/{drive_filename}"
            payload = {
                "message": f"Update {drive_filename} via Legal Library App",
                "content": encoded,
                "branch": "main"
            }
            if sha:
                payload["sha"] = sha  # Update के लिए SHA जरूरी

            r = requests.put(url, headers=self.headers, json=payload)

            if r.status_code in [200, 201]:
                return True
            else:
                st.error(f"GitHub upload error: {r.status_code} — {r.json().get('message','')}")
                return False

        except Exception as e:
            st.error(f"Upload error: {e}")
            return False

    def download_json(self, drive_filename, local_path):
        """GitHub repo के data/ folder से JSON file download करो"""
        if not self.is_connected():
            return False
        try:
            import requests

            url = f"{self.api_base}/{drive_filename}"
            r = requests.get(url, headers=self.headers)

            if r.status_code == 200:
                content = base64.b64decode(r.json()["content"]).decode("utf-8")
                with open(local_path, "w", encoding="utf-8") as f:
                    f.write(content)
                return True
            else:
                st.error(f"GitHub download error: {r.status_code}")
                return False

        except Exception as e:
            st.error(f"Download error: {e}")
            return False

    def sync_all(self):
        """सभी data files GitHub से download करो"""
        files = ["case_laws.json", "bns_sections.json", "rti_sections.json", "cca_rules.json"]
        results = {}
        for f in files:
            import os
            local = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", f)
            results[f] = self.download_json(f, local)
        return results
