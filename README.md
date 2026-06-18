# ⚖️ विधिक पुस्तकालय — BNS 2023
### Legal Reference System for UP Police

> भारतीय न्याय संहिता 2023 (BNS) | लागू: 1 जुलाई 2024

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔍 **धारा खोज** | BNS धारा / IPC नंबर / हिंदी keyword से खोजें |
| 📚 **Case Law Library** | धाराओं से जुड़े judgments store और search करें |
| ⚡ **जमानत विरोध आख्या** | AI से बिंदुवार, प्रस्तरवार आख्या तैयार करें |
| 📥 **DOCX Export** | आख्या/report सीधे Word file में download करें |
| ☁️ **Google Drive Sync** | अपनी library Drive पर sync रखें |
| 🤖 **Multi-AI** | Groq → Gemini → DeepSeek → OpenRouter (auto-rotation) |

---

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/legal-library
cd legal-library
pip install -r requirements.txt
cp .env.example .env
# .env में API keys डालें
streamlit run app.py
```

---

## 🔑 API Keys (Free)

| Provider | Link | Free Limit |
|----------|------|-----------|
| Groq | https://console.groq.com | 6000 req/day |
| Gemini | https://aistudio.google.com | 1500 req/day |
| DeepSeek | https://platform.deepseek.com | ~500 req/day |
| OpenRouter | https://openrouter.ai | $1 free credit |

---

## ☁️ Streamlit Cloud Deploy

1. GitHub पर push करें
2. [share.streamlit.io](https://share.streamlit.io) पर जाएं
3. Repo connect करें
4. **Secrets** में API keys डालें:
```toml
GROQ_API_KEY = "gsk_xxxx"
GEMINI_API_KEY = "AIzaSyxxxx"
DEEPSEEK_API_KEY = "sk-xxxx"
OPENROUTER_API_KEY = "sk-or-xxxx"
GOOGLE_DRIVE_FOLDER_ID = "1xxxx"
```

---

## 📁 Project Structure

```
legal-library/
├── app.py              # Main Streamlit app
├── config.py           # Settings & API config
├── requirements.txt
├── .env.example        # API keys template
├── data/
│   ├── bns_sections.json   # BNS 2023 data
│   └── case_laws.json      # Case laws database
└── modules/
    ├── ai_engine.py    # Multi-API AI engine
    ├── docx_export.py  # DOCX generation
    └── drive_sync.py   # Google Drive sync
```

---

## 📋 Roadmap

- [x] BNS 2023 search (IPC → BNS mapping)
- [x] Multi-AI engine (auto-rotation)
- [x] Bail opposition generator
- [x] DOCX export
- [x] Google Drive sync
- [ ] BNSS (CrPC replacement) sections
- [ ] BSA (Evidence Act) sections
- [ ] Offline mode
- [ ] Mobile PWA

---

*Developed for UP Police Legal Reference | v1.0.0*
