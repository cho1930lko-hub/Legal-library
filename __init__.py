# modules package
"""
modules/ai_engine.py
Multi-API AI Engine — Groq → Gemini → DeepSeek → OpenRouter
अगर एक fail हो या limit हो तो automatically अगला try करेगा
"""

import time
import streamlit as st
from config import AI_PROVIDERS


def _call_groq(provider: dict, system: str, user: str) -> str:
    from groq import Groq
    client = Groq(api_key=provider["key_env"])
    resp = client.chat.completions.create(
        model=provider["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    return resp.choices[0].message.content


def _call_gemini(provider: dict, system: str, user: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=provider["key_env"])
    model = genai.GenerativeModel(
        model_name=provider["model"],
        system_instruction=system,
    )
    resp = model.generate_content(user)
    return resp.text


def _call_openai_compat(provider: dict, system: str, user: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=provider["key_env"],
        base_url=provider.get("base_url", "https://api.openai.com/v1"),
    )
    resp = client.chat.completions.create(
        model=provider["model"],
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.3,
        max_tokens=4096,
    )
    return resp.choices[0].message.content


def ask_ai(system_prompt: str, user_prompt: str, task_label: str = "") -> dict:
    """
    Main function — सभी providers try करेगा, जो काम करे उससे answer लेगा।

    Returns:
        {
            "success": True/False,
            "text": "AI का जवाब",
            "provider": "Groq",
            "error": "अगर सब fail हों"
        }
    """
    errors = []

    for provider in AI_PROVIDERS:
        key = provider["key_env"]
        name = provider["name"]

        # API key नहीं है तो skip
        if not key or key.startswith("your_"):
            errors.append(f"{name}: API key नहीं मिली")
            continue

        try:
            if task_label:
                st.toast(f"🤖 {name} से {task_label} तैयार हो रहा है...", icon="⏳")

            ptype = provider["type"]

            if ptype == "groq":
                text = _call_groq(provider, system_prompt, user_prompt)
            elif ptype == "gemini":
                text = _call_gemini(provider, system_prompt, user_prompt)
            elif ptype == "openai_compat":
                text = _call_openai_compat(provider, system_prompt, user_prompt)
            else:
                errors.append(f"{name}: Unknown type")
                continue

            return {"success": True, "text": text, "provider": name, "error": None}

        except Exception as e:
            err_msg = str(e)
            # Rate limit? 429?
            if "429" in err_msg or "rate" in err_msg.lower() or "quota" in err_msg.lower():
                errors.append(f"{name}: Rate limit — अगला try करते हैं")
                time.sleep(1)
            else:
                errors.append(f"{name}: {err_msg[:120]}")
            continue

    # सब fail
    return {
        "success": False,
        "text": "",
        "provider": None,
        "error": " | ".join(errors),
    }


# ── Specialized prompts ───────────────────────────────────────────────────────

SYSTEM_BAIL_OPPOSITION = """आप एक वरिष्ठ लोक अभियोजक (Senior Public Prosecutor) हैं जो उत्तर प्रदेश की अदालतों में जमानत का विरोध करते हैं।
आपका काम है — जमानत प्रार्थनापत्र पढ़कर, दिए गए तथ्यों और धाराओं के आधार पर एक मजबूत, बिंदुवार, प्रस्तरवार आख्या (Opposition Report) तैयार करना।

नियम:
1. भाषा: शुद्ध हिंदी, कानूनी शैली
2. Format: प्रस्तर 1, प्रस्तर 2... (numbered paragraphs)
3. हर बिंदु में — तथ्य → धारा → केस law का संदर्भ
4. अंत में — "अतः जमानत निरस्त की जाए" के साथ समाप्त
5. अभियोजन पक्ष की भाषा में लिखें, बचाव पक्ष की नहीं"""

SYSTEM_SECTION_SUMMARY = """आप एक कानूनी विशेषज्ञ हैं जो BNS 2023 (भारतीय न्याय संहिता) की धाराओं को सरल हिंदी में समझाते हैं।
पुलिस अधिकारियों के लिए — practical, field-useful explanation दें।
Format: धारा का सार → तत्व → सज़ा → जमानत स्थिति → महत्वपूर्ण केस law"""

SYSTEM_CASE_LAW_EXTRACT = """आप एक कानूनी शोधकर्ता हैं। दिए गए PDF/text से:
1. Case name और citation निकालें
2. धारा/section identify करें
3. Ratio decidendi (मुख्य निर्णय) हिंदी में लिखें
4. Prosecution के लिए उपयोगी बिंदु अलग करें
JSON format में output दें।"""


def generate_bail_opposition(bail_text: str, fir_details: str, extra_points: str) -> dict:
    user = f"""जमानत प्रार्थनापत्र का विषय:
{bail_text}

FIR/मुकदमे की जानकारी:
{fir_details}

विरोध के अतिरिक्त बिंदु (अभियोजन पक्ष के):
{extra_points}

कृपया पूर्ण जमानत विरोध आख्या तैयार करें।"""

    return ask_ai(SYSTEM_BAIL_OPPOSITION, user, task_label="जमानत विरोध आख्या")


def explain_section(section_number: str, section_text: str) -> dict:
    user = f"धारा {section_number} को विस्तार से समझाइए:\n{section_text}"
    return ask_ai(SYSTEM_SECTION_SUMMARY, user, task_label=f"धारा {section_number} की व्याख्या")


def extract_case_law(raw_text: str) -> dict:
    user = f"निम्नलिखित text से case law की जानकारी निकालें:\n\n{raw_text[:6000]}"
    return ask_ai(SYSTEM_CASE_LAW_EXTRACT, user, task_label="Case Law Extract")
