import time, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _get_providers():
    try:
        import streamlit as st
        from config import AI_PROVIDERS
        return AI_PROVIDERS
    except:
        return []

def ask_ai(system_prompt, user_prompt, task_label=""):
    import streamlit as st
    errors = []
    for p in _get_providers():
        key = p["key_env"]
        name = p["name"]
        if not key or key.startswith("your_"):
            errors.append(f"{name}: key नहीं")
            continue
        try:
            st.toast(f"🤖 {name}...", icon="⏳")
            if p["type"] == "groq":
                from groq import Groq
                r = Groq(api_key=key).chat.completions.create(
                    model=p["model"],
                    messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
                    temperature=0.3, max_tokens=4096)
                return {"success":True,"text":r.choices[0].message.content,"provider":name,"error":None}
            elif p["type"] == "gemini":
                import google.generativeai as genai
                genai.configure(api_key=key)
                m = genai.GenerativeModel(p["model"], system_instruction=system_prompt)
                r = m.generate_content(user_prompt)
                return {"success":True,"text":r.text,"provider":name,"error":None}
            else:
                from openai import OpenAI
                r = OpenAI(api_key=key, base_url=p.get("base_url")).chat.completions.create(
                    model=p["model"],
                    messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
                    temperature=0.3, max_tokens=4096)
                return {"success":True,"text":r.choices[0].message.content,"provider":name,"error":None}
        except Exception as e:
            errors.append(f"{name}: {str(e)[:80]}")
            time.sleep(1)
    return {"success":False,"text":"","provider":None,"error":" | ".join(errors)}

BAIL_SYS = "आप वरिष्ठ लोक अभियोजक हैं। जमानत विरोध आख्या शुद्ध हिंदी में बिंदुवार प्रस्तरवार लिखें। अंत में: अतः जमानत निरस्त की जाए।"
SEC_SYS = "आप BNS 2023 विशेषज्ञ हैं। धारा सरल हिंदी में: सार, तत्व, सज़ा, जमानत, केस law।"
CASE_SYS = "text से case law JSON निकालें: title, citation, sections, ratio, prosecution_points"

def generate_bail_opposition(bail_text, fir_details, extra_points):
    u = f"जमानत:\n{bail_text}\nFIR:\n{fir_details}\nबिंदु:\n{extra_points}"
    return ask_ai(BAIL_SYS, u, "आख्या")

def explain_section(s, t):
    return ask_ai(SEC_SYS, f"धारा {s}: {t}", s)

def extract_case_law(t):
    return ask_ai(CASE_SYS, t[:6000], "Case Law")
