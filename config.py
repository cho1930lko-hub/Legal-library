import os
import streamlit as st

def _get(key, default=""):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

GROQ_API_KEY       = _get("GROQ_API_KEY")
GEMINI_API_KEY     = _get("GEMINI_API_KEY")
DEEPSEEK_API_KEY   = _get("DEEPSEEK_API_KEY")
OPENROUTER_API_KEY = _get("OPENROUTER_API_KEY")

GOOGLE_CREDENTIALS_PATH = _get("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_DRIVE_FOLDER_ID  = _get("GOOGLE_DRIVE_FOLDER_ID", "")

AI_PROVIDERS = [
    {"name":"Groq","key_env":GROQ_API_KEY,"model":"llama-3.3-70b-versatile","type":"groq"},
    {"name":"Gemini","key_env":GEMINI_API_KEY,"model":"gemini-1.5-flash","type":"gemini"},
    {"name":"DeepSeek","key_env":DEEPSEEK_API_KEY,"model":"deepseek-chat","type":"openai_compat","base_url":"https://api.deepseek.com/v1"},
    {"name":"OpenRouter","key_env":OPENROUTER_API_KEY,"model":"mistralai/mixtral-8x7b-instruct","type":"openai_compat","base_url":"https://openrouter.ai/api/v1"},
]

import os
DATA_DIR       = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
UPLOADS_DIR    = os.path.join(DATA_DIR, "uploads")
BNS_JSON       = os.path.join(DATA_DIR, "bns_sections.json")
CASE_LAWS_JSON = os.path.join(DATA_DIR, "case_laws.json")
TEMPLATES_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

APP_TITLE    = "⚖️ विधिक पुस्तकालय — BNS 2023"
APP_SUBTITLE = "भारतीय न्याय संहिता | UP Police Legal Reference System"
APP_VERSION  = "1.0.0"
