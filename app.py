"""
app.py — Legal Library Main App
⚖️ विधिक पुस्तकालय — BNS 2023
"""

import os
import json
import streamlit as st
from pathlib import Path

from config import (
    APP_TITLE, APP_SUBTITLE, APP_VERSION,
    BNS_JSON, CASE_LAWS_JSON, UPLOADS_DIR, AI_PROVIDERS
)

# ── Page config ───────────────────────────────────────
st.set_page_config(
    page_title="विधिक पुस्तकालय",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans Devanagari', sans-serif; }
    .main-header { background: linear-gradient(135deg, #1a1d27, #21253a);
        padding: 1rem 1.5rem; border-radius: 10px; border-left: 4px solid #f4a623;
        margin-bottom: 1.5rem; }
    .main-header h1 { color: #f4a623; margin: 0; font-size: 1.6rem; }
    .main-header p  { color: #8890b5; margin: 0.2rem 0 0; font-size: 0.85rem; }
    .stat-card { background: #1a1d27; border: 1px solid #2e3250;
        border-radius: 8px; padding: 1rem; text-align: center; }
    .stat-card .num { font-size: 2rem; font-weight: 700; color: #4ecdc4; }
    .stat-card .lbl { font-size: 0.78rem; color: #8890b5; }
    .section-badge { background: #f4a623; color: #000; font-weight: 700;
        padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; }
    .new-badge { background: #27ae60; color: #fff; font-size: 0.7rem;
        padding: 1px 5px; border-radius: 3px; margin-left: 4px; }
    .ai-provider { background: #21253a; border: 1px solid #2e3250;
        border-radius: 6px; padding: 0.4rem 0.8rem; font-size: 0.8rem;
        color: #4ecdc4; display: inline-block; margin-bottom: 0.5rem; }
    div[data-testid="stExpander"] { border: 1px solid #2e3250; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Helper: load JSON data ────────────────────────────
@st.cache_data
def load_bns_data():
    try:
        for p in [BNS_JSON, Path(__file__).parent/"data"/"bns_sections.json"]:
            if Path(p).exists():
                with open(p, encoding="utf-8") as f:
                    return json.load(f)
    except Exception:
        pass
    return []

@st.cache_data
def load_case_laws():
    if not Path(CASE_LAWS_JSON).exists():
        return []
    with open(CASE_LAWS_JSON, encoding="utf-8") as f:
        return json.load(f)

def save_case_laws(data: list):
    with open(CASE_LAWS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    load_case_laws.clear()

def active_ai_providers():
    return [p for p in AI_PROVIDERS if p["key_env"] and not p["key_env"].startswith("your_")]

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.markdown(f"## ⚖️ विधिक पुस्तकालय")
    st.markdown(f"*{APP_SUBTITLE}*")
    st.divider()

    page = st.radio(
        "📌 Menu",
        options=[
            "🏠 Dashboard",
            "🔍 धारा खोज",
            "📚 Case Law Library",
            "⚡ जमानत विरोध आख्या",
            "📝 RTI सहायक",
            "📋 विभागीय जाँच",
            "📥 Google Drive Sync",
            "⚙️ Settings & API Keys",
        ],
        label_visibility="collapsed"
    )

    st.divider()

    # AI Status
    providers = active_ai_providers()
    if providers:
        st.markdown("**🤖 AI Providers Active:**")
        for p in providers:
            st.markdown(f"✅ {p['name']} — `{p['model']}`")
    else:
        st.warning("⚠️ कोई API key नहीं\nSettings में डालें")

    st.divider()
    st.caption(f"v{APP_VERSION} | UP Police Legal Ref.")

# ══════════════════════════════════════════════════════
# PAGE: Dashboard
# ══════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ विधिक पुस्तकालय — BNS 2023</h1>
        <p>भारतीय न्याय संहिता | UP Police Legal Reference System | लागू: 1 जुलाई 2024</p>
    </div>
    """, unsafe_allow_html=True)

    bns_data  = load_bns_data()
    case_laws = load_case_laws()

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-card">
            <div class="num">{len(bns_data)}</div>
            <div class="lbl">BNS धाराएं</div></div>""", unsafe_allow_html=True)
    with c2:
        new_count = sum(1 for r in bns_data if r.get("is_new"))
        st.markdown(f"""<div class="stat-card">
            <div class="num" style="color:#e05c5c">{new_count}</div>
            <div class="lbl">नई धाराएं ★</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card">
            <div class="num" style="color:#f4a623">{len(case_laws)}</div>
            <div class="lbl">Case Laws</div></div>""", unsafe_allow_html=True)
    with c4:
        ai_count = len(active_ai_providers())
        st.markdown(f"""<div class="stat-card">
            <div class="num" style="color:#27ae60">{ai_count}/4</div>
            <div class="lbl">AI Providers</div></div>""", unsafe_allow_html=True)

    st.divider()

    # Quick links
    st.markdown("### ⚡ Quick Actions")
    qa1, qa2, qa3 = st.columns(3)
    with qa1:
        if st.button("🔍 धारा खोजें", use_container_width=True):
            st.session_state["goto"] = "🔍 धारा खोज"
            st.rerun()
    with qa2:
        if st.button("⚡ जमानत विरोध बनाएं", use_container_width=True):
            st.session_state["goto"] = "⚡ जमानत विरोध आख्या"
            st.rerun()
    with qa3:
        if st.button("📚 Case Law जोड़ें", use_container_width=True):
            st.session_state["goto"] = "📚 Case Law Library"
            st.rerun()

    st.divider()
    st.markdown("### 📋 BNS 2023 — Chapter Overview")
    chapters = {
        "जीवन के विरुद्ध अपराध": ("S.100–S.113", "#e05c5c"),
        "चोट/हमला": ("S.114–S.146", "#f4a623"),
        "महिला/बच्चों के विरुद्ध": ("S.63–S.99", "#e91e8c"),
        "राज्य के विरुद्ध": ("S.147–S.158", "#3f8ef5"),
        "संपत्ति अपराध": ("S.303–S.334", "#27ae60"),
        "जालसाजी/साक्ष्य": ("S.227–S.250, S.335–S.346", "#9b59b6"),
        "लोक व्यवस्था": ("S.189–S.226, S.351–S.358", "#4ecdc4"),
    }
    for ch, (sections, color) in chapters.items():
        st.markdown(
            f'<div style="padding:6px 12px;margin:4px 0;border-left:3px solid {color};'
            f'background:#1a1d27;border-radius:4px;">'
            f'<b style="color:{color}">{ch}</b> &nbsp; '
            f'<span style="color:#8890b5;font-size:0.82rem">{sections}</span></div>',
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════
# PAGE: धारा खोज
# ══════════════════════════════════════════════════════
elif page == "🔍 धारा खोज":
    st.header("🔍 धारा खोज")

    bns_data = load_bns_data()

    col1, col2 = st.columns([3, 2])
    with col1:
        query = st.text_input("🔍 BNS धारा / अपराध / हिंदी में खोजें",
                              placeholder="जैसे: हत्या, S.103, murder, 304...")
    with col2:
        ipc_query = st.text_input("📌 पुरानी IPC डालें → नई BNS देखें",
                                  placeholder="जैसे: 302, 376, 420...")

    # Filters
    f1, f2, f3 = st.columns(3)
    with f1:
        chunk_filter = st.multiselect("Chapter", options=[
            "जीवन अपराध", "चोट/हमला", "महिला/बच्चे",
            "राज्य के विरुद्ध", "संपत्ति अपराध", "जालसाजी/साक्ष्य", "लोक व्यवस्था"
        ])
    with f2:
        bail_filter = st.selectbox("जमानत", ["सभी", "जमानती", "गैर-जमानती"])
    with f3:
        only_new = st.checkbox("केवल नई धाराएं ★")

    if bns_data:
        results = bns_data
        q = query.strip().lower()
        iq = ipc_query.strip().lower().replace("ipc", "").strip()

        if q:
            results = [r for r in results if
                       q in r.get("bns","").lower() or
                       q in r.get("offence","").lower() or
                       q in r.get("offence_hi","").lower() or
                       q in r.get("punishment","").lower()]
        if iq:
            results = [r for r in results if iq in r.get("ipc","").lower().replace("ipc","").strip()]
        if chunk_filter:
            results = [r for r in results if r.get("chapter") in chunk_filter]
        if only_new:
            results = [r for r in results if r.get("is_new")]
        if bail_filter == "जमानती":
            results = [r for r in results if r.get("bailable")]
        elif bail_filter == "गैर-जमानती":
            results = [r for r in results if not r.get("bailable")]

        st.caption(f"🔎 {len(results)} धाराएं मिलीं")

        for row in results:
            with st.expander(
                f"{'🆕 ' if row.get('is_new') else ''}"
                f"**{row['bns']}** — {row.get('offence_hi', row.get('offence',''))}"
            ):
                c1, c2, c3 = st.columns(3)
                c1.metric("IPC (पुरानी)", row.get("ipc", "—"))
                c2.metric("सज़ा", row.get("punishment_short", "देखें"))
                c3.metric("जमानत", "✅ जमानती" if row.get("bailable") else "❌ गैर-जमानती")

                st.markdown(f"**सज़ा का विवरण:** {row.get('punishment','—')}")

                if row.get("case_laws"):
                    st.markdown("**📚 संबंधित Case Law:**")
                    for cl in row["case_laws"]:
                        st.markdown(f"- {cl}")

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"🤖 AI से विस्तार", key=f"exp_{row['bns']}"):
                        from modules.ai_engine import explain_section
                        with st.spinner("AI समझा रहा है..."):
                            res = explain_section(row["bns"], row.get("offence","") + " — " + row.get("punishment",""))
                        if res["success"]:
                            st.markdown(f'<div class="ai-provider">🤖 {res["provider"]}</div>', unsafe_allow_html=True)
                            st.markdown(res["text"])
                        else:
                            st.error(f"AI Error: {res['error']}")
                with btn_col2:
                    if st.button(f"⚡ जमानत विरोध", key=f"bail_{row['bns']}"):
                        st.session_state["bail_section"] = row["bns"]
                        st.session_state["goto"] = "⚡ जमानत विरोध आख्या"
                        st.rerun()
    else:
        st.info("📂 BNS data अभी load नहीं हुआ। Settings → Data Management से JSON load करें।")

# ══════════════════════════════════════════════════════
# PAGE: Case Law Library
# ══════════════════════════════════════════════════════
elif page == "📚 Case Law Library":
    st.header("📚 Case Law Library")

    case_laws = load_case_laws()

    tab1, tab2, tab3 = st.tabs(["📋 देखें", "➕ नया जोड़ें", "📄 PDF से Extract"])

    with tab1:
        search_cl = st.text_input("🔍 Case law खोजें", placeholder="धारा, case name, keyword...")
        results = case_laws
        if search_cl:
            q = search_cl.lower()
            results = [c for c in case_laws if
                       q in c.get("title","").lower() or
                       q in c.get("sections","").lower() or
                       q in c.get("ratio","").lower() or
                       q in c.get("citation","").lower()]

        st.caption(f"{len(results)} case laws")
        for cl in results:
            with st.expander(f"**{cl.get('title','—')}** | {cl.get('citation','—')}"):
                st.markdown(f"**धाराएं:** {cl.get('sections','—')}")
                st.markdown(f"**Ratio Decidendi:** {cl.get('ratio','—')}")
                if cl.get("prosecution_points"):
                    st.markdown("**अभियोजन के लिए उपयोगी बिंदु:**")
                    for pt in cl["prosecution_points"]:
                        st.markdown(f"• {pt}")
                if cl.get("full_text"):
                    st.text_area("पूरा text", cl["full_text"], height=150, key=f"ft_{cl.get('id','')}")

    with tab2:
        st.markdown("### ➕ नया Case Law मैनुअल जोड़ें")
        with st.form("add_case_law"):
            t1, t2 = st.columns(2)
            title    = t1.text_input("Case Name *", placeholder="State vs. Ram Kumar 2019")
            citation = t2.text_input("Citation *", placeholder="2019 SCC 123 / 2019 (3) ADJ 45")
            sections = st.text_input("धाराएं *", placeholder="BNS S.103, S.111 / IPC 302")
            court    = st.text_input("Court", placeholder="Allahabad High Court / Supreme Court")
            ratio    = st.text_area("Ratio Decidendi (मुख्य निर्णय हिंदी में) *", height=100)
            pros_pts = st.text_area("अभियोजन के लिए उपयोगी बिंदु (एक लाइन = एक बिंदु)")
            full_txt = st.text_area("पूरा Judgment Text (optional)", height=150)

            submitted = st.form_submit_button("✅ Case Law जोड़ें", use_container_width=True)
            if submitted:
                if not (title and citation and sections and ratio):
                    st.error("⚠️ * वाले fields जरूरी हैं")
                else:
                    new_cl = {
                        "id": f"cl_{len(case_laws)+1:04d}",
                        "title": title, "citation": citation,
                        "sections": sections, "court": court,
                        "ratio": ratio,
                        "prosecution_points": [p.strip() for p in pros_pts.split("\n") if p.strip()],
                        "full_text": full_txt,
                    }
                    case_laws.append(new_cl)
                    save_case_laws(case_laws)
                    st.success(f"✅ '{title}' जोड़ा गया!")

    with tab3:
        st.markdown("### 📄 PDF/Text से Case Law Extract करें")
        uploaded = st.file_uploader("Judgment PDF या Text file upload करें",
                                    type=["pdf","txt"])
        if uploaded:
            raw_text = ""
            if uploaded.type == "application/pdf":
                try:
                    import pdfplumber
                    import io
                    with pdfplumber.open(io.BytesIO(uploaded.read())) as pdf:
                        raw_text = "\n".join(p.extract_text() or "" for p in pdf.pages)
                except Exception as e:
                    st.error(f"PDF read error: {e}")
            else:
                raw_text = uploaded.read().decode("utf-8", errors="ignore")

            if raw_text:
                st.text_area("Extracted Text (preview)", raw_text[:1500], height=200)
                if st.button("🤖 AI से Case Law Extract करें"):
                    from modules.ai_engine import extract_case_law
                    with st.spinner("AI extract कर रहा है..."):
                        res = extract_case_law(raw_text)
                    if res["success"]:
                        st.markdown(f'<div class="ai-provider">🤖 {res["provider"]}</div>', unsafe_allow_html=True)
                        st.markdown("**Extracted Data:**")
                        st.code(res["text"], language="json")
                        st.info("ऊपर 'नया जोड़ें' tab में copy करके save करें")
                    else:
                        st.error(res["error"])

# ══════════════════════════════════════════════════════
# PAGE: जमानत विरोध आख्या
# ══════════════════════════════════════════════════════
elif page == "⚡ जमानत विरोध आख्या":
    st.header("⚡ जमानत विरोध आख्या")
    st.caption("जमानत प्रार्थनापत्र upload करें → AI बिंदुवार विरोध आख्या तैयार करेगा")

    if not active_ai_providers():
        st.error("⚠️ कोई AI API key नहीं है। Settings में डालें।")
        st.stop()

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown("### 📄 Step 1: जमानत प्रार्थनापत्र")
        bail_file = st.file_uploader("PDF/DOCX upload करें", type=["pdf","docx","txt"], key="bail_up")
        bail_text_manual = st.text_area("या सीधे text paste करें", height=200,
                                         placeholder="जमानत प्रार्थनापत्र का content यहाँ paste करें...")

    with col2:
        st.markdown("### 📝 Step 2: FIR व अभियोजन की जानकारी")
        fir_details = st.text_area("FIR नंबर, धारा, घटना का विवरण", height=120,
                                   placeholder="FIR No. 123/2024, थाना: कोतवाली, धारा: BNS S.103(1)...")
        extra_points = st.text_area("विरोध के अतिरिक्त बिंदु", height=120,
                                    placeholder="• आरोपी फरार रहा है\n• पीड़ित परिवार को धमकी\n• गवाह प्रभावित हो सकते हैं...")

    # Extract bail text from file
    bail_text = bail_text_manual
    if bail_file and not bail_text_manual:
        try:
            if bail_file.type == "application/pdf":
                import pdfplumber, io
                with pdfplumber.open(io.BytesIO(bail_file.read())) as pdf:
                    bail_text = "\n".join(p.extract_text() or "" for p in pdf.pages)
            elif "word" in bail_file.type or bail_file.name.endswith(".docx"):
                from docx import Document
                import io
                doc = Document(io.BytesIO(bail_file.read()))
                bail_text = "\n".join(p.text for p in doc.paragraphs)
            else:
                bail_text = bail_file.read().decode("utf-8", errors="ignore")
        except Exception as e:
            st.error(f"File read error: {e}")

    st.divider()

    # Pre-fill section if coming from search
    if "bail_section" in st.session_state:
        st.info(f"धारा {st.session_state['bail_section']} के लिए आख्या")

    generate_btn = st.button("⚡ जमानत विरोध आख्या तैयार करें",
                             use_container_width=True, type="primary")

    if generate_btn:
        if not bail_text and not fir_details:
            st.error("⚠️ जमानत प्रार्थनापत्र या FIR details जरूरी हैं")
        else:
            with st.spinner("🤖 AI आख्या तैयार कर रहा है..."):
                from modules.ai_engine import generate_bail_opposition
                res = generate_bail_opposition(
                    bail_text or "प्रार्थनापत्र उपलब्ध नहीं",
                    fir_details,
                    extra_points
                )

            if res["success"]:
                st.markdown(f'<div class="ai-provider">🤖 {res["provider"]} द्वारा तैयार</div>',
                            unsafe_allow_html=True)
                st.markdown("---")
                akhya_text = res["text"]
                st.markdown(akhya_text)
                st.markdown("---")

                # DOCX Download
                try:
                    from modules.docx_export import create_akhya_docx
                    import io
                    docx_bytes = create_akhya_docx(akhya_text, fir_details)
                    st.download_button(
                        label="📥 DOCX Download करें",
                        data=docx_bytes,
                        file_name="jamant_virodh_akhya.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )
                except Exception as e:
                    st.warning(f"DOCX export error: {e}")
                    st.text_area("Text copy करें", akhya_text, height=300)
            else:
                st.error(f"❌ AI Error: {res['error']}")

# ══════════════════════════════════════════════════════
# PAGE: 📝 RTI सहायक
# ══════════════════════════════════════════════════════
elif page == "📝 RTI सहायक":
    st.header("📝 RTI सहायक — सूचना का अधिकार अधिनियम 2005")

    import json
    from pathlib import Path

    rti_path = Path(__file__).parent / "data" / "rti_sections.json"
    try:
        with open(rti_path, encoding="utf-8") as f:
            rti_data = json.load(f)
    except:
        rti_data = []

    tab1, tab2, tab3 = st.tabs(["🔍 धारा खोजें", "✍️ RTI आवेदन बनाएं", "📤 अपील बनाएं"])

    with tab1:
        q = st.text_input("🔍 खोजें", placeholder="जैसे: अपील, दंड, 30 दिन, छूट...")
        only_imp = st.checkbox("केवल महत्वपूर्ण धाराएं")
        results = rti_data
        if q:
            results = [r for r in rti_data if
                q.lower() in r["title"].lower() or
                q.lower() in r["description"].lower() or
                any(q.lower() in s.lower() for s in r["subsections"])]
        if only_imp:
            results = [r for r in results if r.get("important")]
        st.caption(f"{len(results)} धाराएं मिलीं")
        for r in results:
            with st.expander(f"**धारा {r['section_no']}** — {r['title']} {'⭐' if r.get('important') else ''}"):
                st.markdown(f"*{r['chapter']}*")
                st.markdown(f"**सार:** {r['description']}")
                st.markdown("**विवरण:**")
                for s in r["subsections"]:
                    st.markdown(f"• {s}")
                if st.button(f"🤖 AI से विस्तार", key=f"rti_{r['section_no']}"):
                    from modules.ai_engine import ask_ai
                    with st.spinner("AI समझा रहा है..."):
                        res = ask_ai(
                            "आप RTI विशेषज्ञ हैं। धारा को UP Police के संदर्भ में सरल हिंदी में समझाएं।",
                            f"धारा {r['section_no']} — {r['title']}: {r['description']}"
                        )
                    if res["success"]:
                        st.markdown(f"`🤖 {res['provider']}`")
                        st.markdown(res["text"])

    with tab2:
        st.markdown("### ✍️ RTI आवेदन तैयार करें")
        c1, c2 = st.columns(2)
        with c1:
            applicant_name = st.text_input("आवेदक का नाम")
            applicant_address = st.text_area("पता", height=80)
            department = st.text_input("विभाग/कार्यालय", placeholder="जैसे: पुलिस अधीक्षक कार्यालय, श्रावस्ती")
        with c2:
            pio_name = st.text_input("लोक सूचना अधिकारी", placeholder="जैसे: जनपद पुलिस अधीक्षक")
            info_needed = st.text_area("मांगी गई सूचना का विवरण *", height=120,
                placeholder="जैसे:\n1. दिनांक xx से xx तक की ACR प्रतियाँ\n2. विभागीय जाँच के आदेश की प्रति")
            purpose = st.text_input("उद्देश्य (optional)", placeholder="जैसे: व्यक्तिगत जानकारी हेतु")

        if st.button("⚡ RTI आवेदन तैयार करें", type="primary", use_container_width=True):
            if not (applicant_name and department and info_needed):
                st.error("⚠️ नाम, विभाग और सूचना का विवरण जरूरी है")
            else:
                from modules.ai_engine import ask_ai
                with st.spinner("AI आवेदन तैयार कर रहा है..."):
                    res = ask_ai(
                        """आप RTI विशेषज्ञ हैं। UP Police के लिए औपचारिक RTI आवेदन हिंदी में तैयार करें।
Format: सेवा में..., विषय:..., महोदय, अनुच्छेद 1,2,3... में सूचना मांगें, धारा 6(1) RTI Act 2005 का हवाला दें, अंत में प्रार्थना।""",
                        f"""आवेदक: {applicant_name}
पता: {applicant_address}
विभाग: {department}
PIO: {pio_name}
मांगी गई सूचना: {info_needed}
उद्देश्य: {purpose}"""
                    )
                if res["success"]:
                    st.markdown(f"`🤖 {res['provider']}`")
                    st.markdown("---")
                    st.markdown(res["text"])
                    try:
                        from modules.docx_export import create_akhya_docx
                        docx_bytes = create_akhya_docx(res["text"], f"RTI आवेदन — {department}")
                        st.download_button("📥 DOCX Download", data=docx_bytes,
                            file_name="rti_avedan.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True)
                    except Exception as e:
                        st.warning(f"DOCX: {e}")

    with tab3:
        st.markdown("### 📤 प्रथम/द्वितीय अपील तैयार करें")
        appeal_type = st.radio("अपील का प्रकार", ["प्रथम अपील (धारा 19(1))", "द्वितीय अपील (धारा 19(3))"])
        c1, c2 = st.columns(2)
        with c1:
            app_name = st.text_input("आवेदक का नाम", key="app_name2")
            rti_date = st.text_input("RTI आवेदन की तारीख", placeholder="जैसे: 01/01/2025")
            rti_subject = st.text_area("RTI में मांगी गई सूचना", height=80)
        with c2:
            reply_received = st.radio("जवाब मिला?", ["नहीं मिला", "अधूरा मिला", "गलत मिला", "मना किया"])
            grievance = st.text_area("शिकायत/आधार", height=80,
                placeholder="जैसे: 30 दिन बीत गए, कोई जवाब नहीं मिला")

        if st.button("⚡ अपील तैयार करें", type="primary", use_container_width=True):
            if not (app_name and rti_subject):
                st.error("⚠️ जरूरी fields भरें")
            else:
                from modules.ai_engine import ask_ai
                appeal_no = "19(1)" if "प्रथम" in appeal_type else "19(3)"
                with st.spinner("AI अपील तैयार कर रहा है..."):
                    res = ask_ai(
                        f"""आप RTI विशेषज्ञ हैं। RTI Act 2005 की धारा {appeal_no} के अंतर्गत औपचारिक अपील हिंदी में तैयार करें।
Format: सेवा में..., विषय:..., महोदय, पृष्ठभूमि, अपील के आधार बिंदुवार, प्रार्थना।""",
                        f"""आवेदक: {app_name}
RTI आवेदन तारीख: {rti_date}
मांगी गई सूचना: {rti_subject}
स्थिति: {reply_received}
शिकायत: {grievance}
अपील प्रकार: {appeal_type}"""
                    )
                if res["success"]:
                    st.markdown(f"`🤖 {res['provider']}`")
                    st.markdown("---")
                    st.markdown(res["text"])
                    try:
                        from modules.docx_export import create_akhya_docx
                        docx_bytes = create_akhya_docx(res["text"], f"{appeal_type}")
                        st.download_button("📥 DOCX Download", data=docx_bytes,
                            file_name="rti_appeal.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True)
                    except Exception as e:
                        st.warning(f"DOCX: {e}")

# ══════════════════════════════════════════════════════
# PAGE: 📋 विभागीय जाँच
# ══════════════════════════════════════════════════════
elif page == "📋 विभागीय जाँच":
    st.header("📋 विभागीय जाँच सहायक")
    st.info("🚧 यह module अगले update में आएगा। इसमें होगा:\n\n• आरोप पत्र upload → AI जवाब\n• CCA Rules UP reference\n• DOCX export")

# ══════════════════════════════════════════════════════
# PAGE: Google Drive Sync
# ══════════════════════════════════════════════════════
elif page == "📥 Google Drive Sync":
    st.header("📥 Google Drive Sync")
    st.info("यह feature अगले update में पूरी तरह तैयार होगा। नीचे setup guide देखें।")

    with st.expander("📋 Google Drive Setup कैसे करें?"):
        st.markdown("""
1. [Google Cloud Console](https://console.cloud.google.com) खोलें
2. नया project बनाएं → **Google Drive API** enable करें
3. **OAuth 2.0 Credentials** create करें (Desktop App)
4. `credentials.json` download करें → project folder में रखें
5. `.env` में `GOOGLE_DRIVE_FOLDER_ID` डालें
6. पहली बार run करने पर browser में login होगा → `token.json` बन जाएगा
        """)

    try:
        from modules.drive_sync import DriveSync
        ds = DriveSync()
        if ds.is_connected():
            st.success("✅ Google Drive Connected")
            if st.button("📤 Case Laws Drive पर Upload करें"):
                with st.spinner("Upload हो रहा है..."):
                    ds.upload_json(CASE_LAWS_JSON, "case_laws.json")
                st.success("✅ Upload complete!")
            if st.button("📥 Drive से Case Laws Download करें"):
                with st.spinner("Download हो रहा है..."):
                    ds.download_json("case_laws.json", CASE_LAWS_JSON)
                load_case_laws.clear()
                st.success("✅ Download complete! Page refresh करें।")
        else:
            st.warning("Drive connect नहीं है। credentials.json setup करें।")
    except Exception as e:
        st.warning(f"Drive module: {e}")

# ══════════════════════════════════════════════════════
# PAGE: Settings
# ══════════════════════════════════════════════════════
elif page == "⚙️ Settings & API Keys":
    st.header("⚙️ Settings & API Keys")

    tab1, tab2 = st.tabs(["🔑 API Keys", "📂 Data Management"])

    with tab1:
        st.markdown("### API Keys Status")
        st.info("Keys `.env` file में डालें (नीचे देखें) — Streamlit Cloud पर Secrets में डालें।")

        for p in AI_PROVIDERS:
            key = p["key_env"]
            status = "✅ Active" if (key and not key.startswith("your_")) else "❌ Not Set"
            col1, col2 = st.columns([2,1])
            col1.markdown(f"**{p['name']}** — `{p['model']}`")
            col2.markdown(status)

        st.divider()
        st.markdown("### `.env` file format:")
        st.code("""GROQ_API_KEY=gsk_xxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxxxx
OPENROUTER_API_KEY=sk-or-xxxxxxxxxx
GOOGLE_DRIVE_FOLDER_ID=1xxxxxxxxxxxxxxxxxxx""", language="bash")

        st.markdown("""
**Free API Keys कहाँ से लें:**
- [Groq](https://console.groq.com) — सबसे fast, 6000 req/day free
- [Gemini](https://aistudio.google.com) — PDF analysis के लिए best
- [DeepSeek](https://platform.deepseek.com) — Legal reasoning
- [OpenRouter](https://openrouter.ai) — Multiple models, $1 free credit
        """)

    with tab2:
        st.markdown("### 📂 Data Management")
        bns_data  = load_bns_data()
        case_laws = load_case_laws()

        st.metric("BNS Sections loaded", len(bns_data))
        st.metric("Case Laws", len(case_laws))

        if st.button("🔄 Cache Clear करें"):
            load_bns_data.clear()
            load_case_laws.clear()
            st.success("Cache cleared!")

        st.divider()
        st.markdown("### BNS Data Import")
        bns_upload = st.file_uploader("BNS sections JSON upload करें", type=["json"])
        if bns_upload:
            try:
                new_data = json.load(bns_upload)
                with open(BNS_JSON, "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)
                load_bns_data.clear()
                st.success(f"✅ {len(new_data)} sections import हुए!")
            except Exception as e:
                st.error(f"Import error: {e}")

        st.divider()
        st.markdown("### Case Laws Export/Import")
        cl_col1, cl_col2 = st.columns(2)
        with cl_col1:
            if case_laws:
                st.download_button(
                    "📥 Case Laws Export (JSON)",
                    data=json.dumps(case_laws, ensure_ascii=False, indent=2),
                    file_name="case_laws_backup.json",
                    mime="application/json"
                )
        with cl_col2:
            cl_upload = st.file_uploader("Case Laws JSON Import", type=["json"], key="cl_imp")
            if cl_upload:
                try:
                    imported = json.load(cl_upload)
                    save_case_laws(imported)
                    st.success(f"✅ {len(imported)} case laws import हुए!")
                except Exception as e:
                    st.error(f"Import error: {e}")
