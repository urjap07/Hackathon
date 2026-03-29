import streamlit as st
import requests

# --- Constants ---
N8N_WEBHOOK_URL = "https://hriday.datachef.in/webhook-test/41ff8937-9d4f-4128-b786-52ab925f1062"

# --- Page Configuration ---
st.set_page_config(
    page_title="AcmeCorp AI Portal",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Sidebar Theme Toggle ---
with st.sidebar:
    st.markdown("## ⚙️ Portal Settings")
    is_light_mode = st.toggle("🌞 Enable Light Mode", value=False)

# --- Theme CSS ---
if is_light_mode:
    theme_css = """
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); color: #0f172a; }
    .hero-header { padding: 3rem; border-radius:16px; text-align:center; }
    .content-box { background:white; padding:20px; border-radius:12px; }
    .violation-card { background:#fff5f5; padding:20px; border-left:6px solid #dc2626; border-radius:8px; margin-bottom:15px;}
    .recommendation-box { background:#fffbeb; padding:20px; border-radius:12px; }
    """
else:
    theme_css = """
    .stApp { background: radial-gradient(circle at top left, #1e1332 0%, #05010a 100%); }
    .hero-header { padding: 3rem; border-radius:16px; text-align:center; }
    .content-box { background: rgba(23,11,36,0.6); padding:20px; border-radius:12px; }
    .violation-card { background: rgba(23,11,36,0.6); padding:20px; border-left:6px solid #ef4444; border-radius:8px; margin-bottom:15px;}
    .recommendation-box { background: rgba(245,158,11,0.15); padding:20px; border-radius:12px;}
    """

st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    '<div class="hero-header"><h1>AcmeCorp AI Portal</h1><p>Sovereign AI Gateway for Enterprise Content</p></div>',
    unsafe_allow_html=True
)

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    department = st.selectbox(
        "Department",
        ["HR", "Sales", "Marketing", "Operations"]
    )

with col2:
    content_type = st.selectbox(
        "Content Type",
        ["LinkedIn Post","Poster","Social Media Post","Internal Memo","Email Campaign"]
    )

user_prompt = st.text_area(
    "What do you need help with?",
    placeholder="Give me a poster for a shoes business...",
    height=120
)

# --- Generate Button ---
if st.button("Generate & Verify", type="primary", use_container_width=True):

    if not user_prompt.strip():
        st.warning("Please provide a prompt.")
        st.stop()

    with st.status("AcmeCorp AI is orchestrating agents...", expanded=True) as status:

        payload = {
            "department": department,
            "content_type": content_type,
            "user_prompt": user_prompt
        }

        try:

            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=120)
            response.raise_for_status()

            result = response.json()

            if isinstance(result, list):
                result = result[0]

            status.update(label="Validation Complete", state="complete")

            # --- Extract Data ---
            score = int(result.get("score", 0))
            verdict = str(result.get("verdict", "BLOCKED")).upper()
            content = result.get("content", "No content generated.")
            violations = result.get("violations", [])
            recommendation = result.get("recommendation", "")

            st.divider()

            # ==================================================
            # 📝 GENERATED CONTENT
            # ==================================================
            st.markdown("## 📝 Generated Content")

            if verdict == "APPROVED":
                st.success("Governance Passed: Safe for Publication")
            else:
                st.error("Governance Blocked: Fix Required")

            st.markdown('<div class="content-box">', unsafe_allow_html=True)
            st.write(content)
            st.markdown('</div>', unsafe_allow_html=True)

            st.divider()

            # ==================================================
            # 📊 COMPLIANCE SCORE
            # ==================================================
            st.markdown("## 📊 Compliance Score")

            st.progress(score / 100)

            colA, colB = st.columns(2)

            with colA:
                st.metric("Compliance Score", f"{score}/100")

            with colB:
                st.metric("Verdict", verdict)

            st.divider()

            # ==================================================
            # ⚠️ VIOLATIONS
            # ==================================================
            st.markdown("## ⚠️ Policy Violations")

            if not violations:
                st.success("No violations detected 🎉")

            else:
                for v in violations:

                    title = v.get("title", "Violation")
                    desc = v.get("description", "")
                    points = v.get("points", "")

                    st.markdown(
                        f"""
                        <div class="violation-card">
                        <b>{title}</b> ({points} pts)
                        <br>{desc}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            st.divider()

            # ==================================================
            # 💡 RECOMMENDATIONS
            # ==================================================
            st.markdown("## 💡 Suggested Fixes")

            st.markdown(
                f"""
                <div class="recommendation-box">
                {recommendation}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error connecting to workflow: {e}")
