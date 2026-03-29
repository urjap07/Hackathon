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
    st.markdown("---")
    st.markdown("Switch the AcmeCorp Sovereign Portal theme between our classic Amethyst Dark Mode and our Crisp Light Mode.")

# --- Dynamic Theme Generator ---
if is_light_mode:
    theme_css = """
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); color: #0f172a; }
    [data-testid="stHeader"] { background-color: #f8fafc !important; }
    .hero-header { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border: 2px solid #a855f7; box-shadow: 0 0 20px rgba(168, 85, 247, 0.5); padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2.5rem; text-align: center; }
    .hero-header h1 { color: #1e1b4b; font-weight: 900; font-size: 3rem; text-shadow: 0 2px 10px rgba(168, 85, 247, 0.2); }
    .content-box { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.4); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05); color: #0f172a; }
    .content-blocked-wrapper { border: 3px solid #dc2626; background-color: rgba(239, 68, 68, 0.05); position: relative; overflow: hidden; }
    .violation-card { background: rgba(255, 255, 255, 0.9); padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 6px solid #dc2626; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .violation-title { font-weight: 800; color: #dc2626; font-size: 1.2rem; }
    .recommendation-box { background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.5); border-radius: 12px; padding: 1.5rem; margin-top: 2.5rem; }
    """
else:
    theme_css = """
    .stApp { background: radial-gradient(circle at top left, #1e1332 0%, #05010a 100%); }
    .hero-header { background: rgba(23, 11, 36, 0.5); backdrop-filter: blur(15px); border: 2px solid #a855f7; box-shadow: 0 0 20px rgba(168, 85, 247, 0.5); padding: 3rem 2rem; border-radius: 16px; margin-bottom: 2.5rem; text-align: center; }
    .hero-header h1 { color: #f8fafc; font-weight: 800; font-size: 3rem; text-shadow: 0 2px 10px rgba(168, 85, 247, 0.8); }
    .content-box { background: rgba(23, 11, 36, 0.5); backdrop-filter: blur(15px); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(168, 85, 247, 0.4); }
    .content-blocked-wrapper { border: 3px solid #ef4444; background-color: rgba(239, 68, 68, 0.08); position: relative; overflow: hidden; }
    .violation-card { background: rgba(23, 11, 36, 0.5); padding: 20px; border-left: 6px solid #ef4444; border-radius: 8px; margin-bottom: 15px; }
    .violation-title { font-weight: 800; color: #fca5a5; font-size: 1.2rem; }
    .recommendation-box { background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.5); padding: 1.5rem; border-radius: 12px; }
    """

# Common CSS
theme_css += """
.violation-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px;}
.violation-points { background: rgba(220, 38, 38, 0.1); color: #ef4444; padding: 4px 10px; border-radius: 12px; font-weight: 800; border: 1px solid #ef4444;}
.do-not-publish-tag { position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; justify-content: center; align-items: center; color: rgba(220, 38, 38, 0.12); font-size: 4.5rem; font-weight: 900; transform: rotate(-15deg); pointer-events: none; white-space: nowrap; }
"""

st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="hero-header"><h1>AcmeCorp AI Portal</h1><p>Sovereign AI Gateway for Enterprise Content</p></div>', unsafe_allow_html=True)

# --- How to Use Section ---
st.markdown("### 💡 About & Help")
col_help1, col_help2, col_help3 = st.columns(3)
with col_help1:
    with st.expander("1. Define Intent"):
        st.write("Select Dept & Content Type to route requests.")
with col_help2:
    with st.expander("2. Agentic Processing"):
        st.write("The Architect drafts while the Referee scores.")
with col_help3:
    with st.expander("3. Verify & Export"):
        st.write("Review Compliance and use the 1-click Copy tool.")

st.divider()

# --- Input Section ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    department = st.selectbox("Department", ["HR", "Sales", "Marketing", "Operations"])
with col_in2:
    content_type = st.selectbox("Content Type", ["LinkedIn Post","Poster", "Social Media Post", "Internal Memo", "Email Campaign"])

user_prompt = st.text_area("What do you need help with?", placeholder="e.g. Give me a poster for a Shoes Business...", height=120)

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
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # Extract first object if response is a list
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
                
            status.update(label="Validation Complete", state="complete", expanded=False)
            st.divider()
            
            # --- 1. Data Extraction ---
            score = int(result.get("score", 0))
            verdict = str(result.get("verdict", "BLOCKED")).upper()
            content = result.get("content", "Error: No content generated.")
            violations = result.get("violations", [])
            recommendation = result.get("recommendation", "No recommendation provided.")
            
            # --- 2. Generated Output Section (TOP) ---
            st.markdown("### 📝 Generated Output")

            def render_content_smartly(c_val):
                c_clean = str(c_val).strip()
                # Check if output is an image URL
                if c_clean.startswith("http") and "\n" not in c_clean:
                    st.image(c_clean, use_container_width=True)
                # Check for Markdown/HTML images
                elif "![" in c_clean or "<img" in c_clean:
                    st.markdown(c_clean, unsafe_allow_html=True)
                else:
                    st.code(c_val, language="markdown")

            if verdict == "APPROVED":
                st.success("Governance Passed: Safe for publication.")
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                render_content_smartly(content)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Governance Blocked: Modification required.")
                st.markdown('<div class="content-box content-blocked-wrapper">', unsafe_allow_html=True)
                st.markdown('<div class="do-not-publish-tag">⚠️ DO NOT PUBLISH</div>', unsafe_allow_html=True)
                st.markdown('<div style="position:relative; z-index:1;">', unsafe_allow_html=True)
                render_content_smartly(content)
                st.markdown('</div></div>', unsafe_allow_html=True)

            st.divider()

            # --- 3. Compliance Gauge Section (MIDDLE) ---
            st.markdown("### 📊 Compliance Verification Gauge")
            col_gauge, col_label = st.columns([1, 1])
            
            with col_gauge:
                # Gauge Color Logic (matches your theme classes)
                color = "#ef4444" if score < 50 else "#eab308" if score < 80 else "#22c55e"
                st.markdown(f"""
                    <div style="text-align: center;">
                        <h1 style="color: {color}; font-size: 4.5rem; margin: 0;">{score}%</h1>
                        <p style="font-weight: 700; opacity: 0.8; letter-spacing: 1px;">ADHERENCE SCORE</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with col_label:
                st.write(f"**Final Status:** {verdict}")
                st.progress(score / 100)
                st.caption("Content evaluated against enterprise safety and tone benchmarks.")

            # --- 4. Violations & Reasons Section ---
            if violations:
                st.markdown("<h3 style='color: #ef4444; margin-top:2rem;'>🚩 Policy Violations</h3>", unsafe_allow_html=True)
                for flag in violations:
                    fname = flag.get("flag_name", "Policy Breach")
                    ftext = flag.get("violated_text", "N/A")
                    freason = flag.get("reason", "Violation of corporate guidelines.") # New field
                    fpoints = flag.get("points_deducted", 0)
                    
                    st.markdown(f"""
                    <div class="violation-card">
                        <div class="violation-header">
                            <p class="violation-title">{fname}</p>
                            <span class="violation-points">-{fpoints} Pts</span>
                        </div>
                        <p class="violation-text">"{ftext}"</p>
                        <p style="margin: 0; font-weight: 700; font-size: 0.9rem;">Reason for Flagging:</p>
                        <p style="opacity: 0.9; margin-bottom: 0;">{freason}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # --- 5. Suggestions Section (BOTTOM) ---
            if verdict == "BLOCKED":
                st.markdown(f"""
                <div class="recommendation-box">
                    <p class="amber-title">💡 Resolution Road-map</p>
                    <p class="amber-text">{recommendation}</p>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Failed to parse backend payload. Error: {e}")
