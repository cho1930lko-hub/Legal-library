"""
config.py — Central configuration
सभी settings और constants यहाँ हैं
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────
GROQ_API_KEY       = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY   = os.getenv("DEEPSEEK_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# ── Google Drive ──────────────────────────────────────
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_DRIVE_FOLDER_ID  = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

# ── AI Models — priority order (पहले वाला पहले try होगा) ──
AI_PROVIDERS = [
    {
        "name": "Groq",
        "key_env": GROQ_API_KEY,
        "model": "llama-3.3-70b-versatile",
        "type": "groq",
    },
    {
        "name": "Gemini",
        "key_env": GEMINI_API_KEY,
        "model": "gemini-1.5-flash",
        "type": "gemini",
    },
    {
        "name": "DeepSeek",
        "key_env": DEEPSEEK_API_KEY,
        "model": "deepseek-chat",
        "type": "openai_compat",
        "base_url": "https://api.deepseek.com/v1",
    },
    {
        "name": "OpenRouter",
        "key_env": OPENROUTER_API_KEY,
        "model": "mistralai/mixtral-8x7b-instruct",
        "type": "openai_compat",
        "base_url": "https://openrouter.ai/api/v1",
    },
]

# ── Paths ─────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
UPLOADS_DIR     = os.path.join(DATA_DIR, "uploads")
BNS_JSON        = os.path.join(DATA_DIR, "bns_sections.json")
CASE_LAWS_JSON  = os.path.join(DATA_DIR, "case_laws.json")
TEMPLATES_DIR   = os.path.join(os.path.dirname(__file__), "templates")

# ── App Settings ──────────────────────────────────────
APP_TITLE    = "⚖️ विधिक पुस्तकालय — BNS 2023"
APP_SUBTITLE = "भारतीय न्याय संहिता | UP Police Legal Reference System"
APP_VERSION  = "1.0.0"
