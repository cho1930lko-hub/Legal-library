import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st

def _get_providers():
    try:
        from config import AI_PROVIDERS
        return AI_PROVIDERS
    except:
        return []

def _call_groq(provider, system, user):
    from groq import Groq
    client = Groq(api_key=provider["key_env"])
    resp = client.chat.completions.create(
        model=provider["model"],
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.3, max_tokens=4096,
    )
    return resp.choices[0].message.content

def _call_gemini(provider, system, user):
    from google import genai
    client = genai.Client(api_key=provider["key_env"])
    resp = client.models.generate_content(
        model=provider["model"],
        contents=f"{system}\n\n{user}",
    )
    return resp.text

def _call_openai_compat(provider, system, user):
    from openai import OpenAI
    client = OpenAI(api_key=provider["key_env"], base_url=provider.get("base_url"))
    resp = client.chat.completions.create(
        model=provider["model"],
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.3, max_tokens=4096,
    )
    return resp.choices[0].message.content

def ask_ai(system_prompt, user_prompt, task_label=""):
    errors = []
    for provider in _get_providers():
        key = provider["key_env"]
        name = provider["name"]
        if not key or key.startswith("your_"):
            errors.append(f"{name}: key नहीं")
            continue
        try:
            if task_label:
                st.toast(f"🤖 {name} से {task_label}...", icon="⏳")
            ptype = provider["type"]
            if ptype == "groq":
                text = _call_groq(provider, system_prompt, user_prompt)
            elif ptype == "gemini":
                text = _call_gemini(provider, system_prompt, user_prompt)
            else:
                text = _call_openai_compat(provider, system_prompt, user_prompt)
            return {"success":True,"text":text,"provider":name,"error":None}
        except Exception as e:
            errors.append(f"{name}: {str(e)[:100]}")
            time.sleep(1)
    return {"success":False,"text":"","provider":None,"error":" | ".join(errors)}

SYSTEM_BAIL = """आप एक वरिष्ठ लोक अभियोजक हैं। जमानत प्रार्थनापत्र के विरुद्ध बिंदुवार, प्रस्तरवार आख्या हिंदी में लिखें।
नियम: शुद्ध कानूनी हिंदी | प्रस्तर 1, 2, 3... format | अंत में "अतः जमानत निरस्त की जाए" """

SYSTEM_SECTION = """आप BNS 2023 विशेषज्ञ हैं। धारा को सरल हिंदी में समझाएं।
Format: सार → तत्व → सज़ा → जमानत → केस law"""

SYSTEM_CASE = """PDF/text से case law निकालें। JSON में दें: title, citation, sections, ratio, prosecution_points"""

def generate_bail_opposition(bail_text, fir_details, extra_points):
    user = f"जमानत प्रार्थनापत्र:\n{bail_text}\n\nFIR:\n{fir_details}\n\nविरोध बिंदु:\n{extra_points}"
    return ask_ai(SYSTEM_BAIL, user, "जमा
