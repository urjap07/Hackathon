import streamlit as st
import requests

# --- Constants ---
N8N_WEBHOOK_URL = "https://hriday.datachef.in/webhook-test/50e12966-853b-4891-9253-a52b8bb359e2"

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
    /* Global Overrides - Crisp Light Mode */
    .stApp { 
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        color: #0f172a;
    }
    
    /* Top Navigation Bar Fix for Light Mode */
    [data-testid="stHeader"] {
        background-color: #f8fafc !important;
    }
    [data-testid="stHeader"] * {
        color: #0f172a !important;
    }
    
    /* Hero Section */
    .hero-header {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 2px solid #a855f7;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        margin-top: 1rem;
        text-align: center;
        position: relative;
    }
    .hero-header h1 { color: #1e1b4b; font-weight: 900; font-size: 3rem; margin-bottom: 0.5rem; padding: 0; text-shadow: 0 2px 10px rgba(168, 85, 247, 0.2); }
    .hero-header p { font-size: 1.25rem; color: #475569; margin: 0; font-weight: 600; letter-spacing: 0.5px;}

    /* Force Streamlit Expander Boxes */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 2px solid #a855f7 !important;
        border-radius: 8px !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stExpander"]:hover {
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.7) !important;
    }
    [data-testid="stExpander"] summary { 
        color: #1e1b4b !important; 
        font-weight: 800 !important; 
        padding: 10px !important;
        background-color: transparent !important;
    }
    [data-testid="stExpander"] summary:hover { background-color: rgba(0,0,0,0.03) !important; }
    [data-testid="stExpander"] p { color: #334155 !important;}
    
    /* Input Labels (e.g. "Department") */
    [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }
    /* Input Boxes (Select dropdowns) */
    div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(168, 85, 247, 0.6) !important;
        border-radius: 8px !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.02) !important;
    }
    /* Force select dropdown text to be unequivocally dark */
    div[data-baseweb="select"] * { color: #0f172a !important; }
    
    /* Text Area Input */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(168, 85, 247, 0.6) !important;
        border-radius: 8px !important;
        color: #0f172a !important;
        font-weight: 500 !important;
        padding: 1rem !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.02) !important;
    }
    .stTextArea textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }
    .stTextArea textarea:focus, div[data-baseweb="select"]:focus-within > div {
        border-color: #a855f7 !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.3) !important;
        outline: none !important;
    }
    
    /* Generate Button styling for maximum legibility */
    .stButton>button { border: 2px solid #a855f7 !important; background-color: rgba(168, 85, 247, 0.1) !important; transition: all 0.3s ease; font-weight: 800 !important; letter-spacing: 0.5px; height: 3rem; color: #7e22ce !important;}
    .stButton>button:hover { background-color: #a855f7 !important; box-shadow: 0 0 20px rgba(168, 85, 247, 0.6) !important; transform: translateY(-2px); color: white !important;}

    /* Headers & Text globally (scoping to Main App Area to protect Sidebar) */
    [data-testid="stAppViewBlockContainer"] h3, 
    [data-testid="stAppViewBlockContainer"] h1, 
    [data-testid="stAppViewBlockContainer"] h2, 
    [data-testid="stAppViewBlockContainer"] p { color: #0f172a; }
    
    /* Fix Sidebar text visibility under Light Mode (Two-Tone Layout) */
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p { color: #f8fafc !important; text-shadow: none;}

    /* Score Visualizer */
    .score-green { color: #16a34a; text-shadow: 0 0 10px rgba(22, 163, 74, 0.2); }
    .score-yellow { color: #d97706; text-shadow: 0 0 10px rgba(217, 119, 6, 0.2); }
    .score-red { color: #dc2626; text-shadow: 0 0 10px rgba(220, 38, 38, 0.2); }
    
    .score-number { font-size: 4.5rem; font-weight: 900; line-height: 1; margin: 0;}
    .stat-line { font-size: 0.95rem; color: #64748b; margin-top: 8px; font-weight: 700;}
    
    /* Verdict Badge */
    .verdict-badge {
        font-size: 1.8rem;
        font-weight: 900;
        padding: 0.6rem 1.5rem;
        border-radius: 12px;
        display: inline-block;
        margin-top: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        letter-spacing: 1px;
    }
    .verdict-approved { background-color: rgba(34, 197, 94, 0.1); border: 2px solid #16a34a; color: #16a34a; }
    .verdict-blocked { background-color: rgba(239, 68, 68, 0.1); border: 2px solid #dc2626; color: #dc2626; }

    /* Generated Output Container with Glassmorphism */
    .content-box {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05);
        color: #0f172a;
    }
    .content-blocked-wrapper {
        border: 3px solid #dc2626;
        background-color: rgba(239, 68, 68, 0.05);
        position: relative;
        overflow: hidden;
    }
    .do-not-publish-tag {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        color: rgba(220, 38, 38, 0.15);
        font-size: 4.5rem;
        font-weight: 900;
        pointer-events: none;
        transform: rotate(-15deg);
        z-index: 0;
        white-space: nowrap;
        letter-spacing: 2px;
    }
    
    /* Red Flag Violation Cards with Glassmorphism */
    .violation-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid rgba(220, 38, 38, 0.2);
        border-left: 6px solid #dc2626;
    }
    .violation-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px;}
    .violation-title { font-weight: 800; color: #dc2626; font-size: 1.2rem; margin:0;}
    .violation-points { background: rgba(220, 38, 38, 0.1); color: #dc2626; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 800; border: 1px solid rgba(220, 38, 38, 0.4);}
    .violation-text { font-style: italic; color: #1e293b; margin: 0 0 10px 0; background: rgba(0,0,0,0.03); padding: 12px; border-radius: 6px; border-left: 2px solid #dc2626; font-size: 1.05rem;}
    .violation-ref { font-size: 0.9rem; color: #475569; margin: 0; font-weight: 700;}

    /* Amber Recommendation Box with Glassmorphism */
    .recommendation-box {
        background: rgba(245, 158, 11, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(245, 158, 11, 0.5);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    .amber-title { color: #d97706; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
    .amber-text { color: #78350f; margin: 0; line-height: 1.6; font-size: 1.1rem; font-weight: 600;}
    
    /* Code styling for light mode */
    code { color: #8b5cf6 !important; background-color: rgba(139, 92, 246, 0.08) !important; font-weight: 500;}
    """
else:
    theme_css = """
    /* Global Overrides - Reliable Radial Gradient */
    .stApp { 
        background: radial-gradient(circle at top left, #1e1332 0%, #05010a 100%);
    }
    
    /* Hero Section with Restored Glassmorphism */
    .hero-header {
        background: rgba(23, 11, 36, 0.5);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 2px solid #a855f7;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        margin-top: 1rem;
        text-align: center;
        position: relative;
    }
    .hero-header h1 { color: #f8fafc; font-weight: 800; font-size: 3rem; margin-bottom: 0.5rem; padding: 0; text-shadow: 0 2px 10px rgba(168, 85, 247, 0.8); }
    .hero-header p { font-size: 1.25rem; color: #cbd5e1; margin: 0; font-weight: 300; letter-spacing: 0.5px;}

    /* Force Streamlit Expander Boxes with Glassmorphism */
    [data-testid="stExpander"] {
        background: rgba(23, 11, 36, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 2px solid #a855f7 !important;
        border-radius: 8px !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5) !important;
        transition: all 0.3s ease;
    }
    [data-testid="stExpander"]:hover {
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.7) !important;
    }
    [data-testid="stExpander"] summary { color: #f8fafc; font-weight: 600; padding: 10px;}
    
    /* Input Boxes (Select Dropdowns & Text Areas) with Glassmorphism */
    div[data-baseweb="select"] > div {
        background: rgba(23, 11, 36, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 8px !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.3) !important;
    }
    .stTextArea textarea {
        background: rgba(23, 11, 36, 0.5) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(168, 85, 247, 0.4) !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
        padding: 1rem !important;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.3) !important;
    }
    .stTextArea textarea:focus, div[data-baseweb="select"]:focus-within > div {
        border-color: #a855f7 !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.5) !important;
        outline: none !important;
    }
    
    /* Buttons */
    .stButton>button { border: 1px solid #a855f7; background-color: rgba(168, 85, 247, 0.2); transition: all 0.3s ease; font-weight: 600; letter-spacing: 0.5px; height: 3rem; backdrop-filter: blur(5px);}
    .stButton>button:hover { background-color: rgba(168, 85, 247, 0.6); box-shadow: 0 0 20px rgba(168, 85, 247, 0.6); transform: translateY(-2px); color: white;}

    /* Score Visualizer */
    .score-green { color: #22c55e; text-shadow: 0 0 20px rgba(34, 197, 94, 0.6); }
    .score-yellow { color: #eab308; text-shadow: 0 0 20px rgba(234, 179, 8, 0.6); }
    .score-red { color: #ef4444; text-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }
    
    .score-number { font-size: 4.5rem; font-weight: 900; line-height: 1; margin: 0;}
    .stat-line { font-size: 0.95rem; color: #94a3b8; margin-top: 8px; font-weight: 500;}
    
    /* Verdict Badge */
    .verdict-badge {
        font-size: 1.8rem;
        font-weight: 900;
        padding: 0.6rem 1.5rem;
        border-radius: 12px;
        display: inline-block;
        margin-top: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        letter-spacing: 1px;
    }
    .verdict-approved { background-color: rgba(34, 197, 94, 0.15); border: 2px solid #22c55e; color: #22c55e; }
    .verdict-blocked { background-color: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; color: #ef4444; }

    /* Generated Output Container with Glassmorphism */
    .content-box {
        background: rgba(23, 11, 36, 0.5);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(168, 85, 247, 0.4);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    .content-blocked-wrapper {
        border: 3px solid #ef4444;
        background-color: rgba(239, 68, 68, 0.08);
        position: relative;
        overflow: hidden;
    }
    .do-not-publish-tag {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        color: rgba(239, 68, 68, 0.12);
        font-size: 4.5rem;
        font-weight: 900;
        pointer-events: none;
        transform: rotate(-15deg);
        z-index: 0;
        white-space: nowrap;
        letter-spacing: 2px;
    }
    
    /* Red Flag Violation Cards with Glassmorphism */
    .violation-card {
        background: rgba(23, 11, 36, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-left: 6px solid #ef4444;
    }
    .violation-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px;}
    .violation-title { font-weight: 800; color: #fca5a5; font-size: 1.2rem; margin:0;}
    .violation-points { background: rgba(239, 68, 68, 0.2); color: #fca5a5; padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; font-weight: 800; border: 1px solid rgba(239, 68, 68, 0.4);}
    .violation-text { font-style: italic; color: #e2e8f0; margin: 0 0 10px 0; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 6px; border-left: 2px solid #ef4444; font-size: 1.05rem;}
    .violation-ref { font-size: 0.9rem; color: #94a3b8; margin: 0; font-weight: 600;}

    /* Amber Recommendation Box with Glassmorphism */
    .recommendation-box {
        background: rgba(245, 158, 11, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(245, 158, 11, 0.5);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .amber-title { color: #fbbf24; font-weight: 800; font-size: 1.3rem; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;}
    .amber-text { color: #fef3c7; margin: 0; line-height: 1.6; font-size: 1.1rem;}
    """

# Inject Dynamic CSS
st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
<div class="hero-header">
    <h1>AcmeCorp AI Portal</h1>
    <p>Sovereign AI Gateway for Enterprise Content</p>
</div>
""", unsafe_allow_html=True)

# --- How to Use Section ---
st.markdown("### 💡 About & Help")
col_help1, col_help2, col_help3 = st.columns(3)

with col_help1:
    with st.expander("1. Define Intent"):
        st.write("Select **Dept** & **Content Type** to route requests through tailored Knowledge Bases.")

with col_help2:
    with st.expander("2. Agentic Processing"):
        st.write("The Architect drafts while the Governance Referee scores against enterprise policies.")

with col_help3:
    with st.expander("3. Verify & Export"):
        st.write("Review the Compliance Score and use the 1-click **Copy** tool safely.")

st.divider()

# --- Input Section ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    department = st.selectbox("Department", ["HR", "Sales", "Marketing", "Operations"])
with col_in2:
    content_type = st.selectbox("Content Type", ["LinkedIn Post","Poster", "Social Media Post", "Internal Memo", "Email Campaign"])
 
user_prompt = st.text_area("What do you need help with?", placeholder="e.g. Give me a poster for a Shoes Business where there is a 30% discount...", height=120)

if st.button("Generate & Verify", type="primary", use_container_width=True):
    if not user_prompt.strip():
        st.warning("Please provide a prompt.")
        st.stop()

    with st.status("AcmeCorp AI is orchestrating agents...", expanded=True) as status:
        st.write("Forwarding intent to specialized Knowledge Base...")
        payload = {
            "department": department,
            "content_type": content_type,
            "user_prompt": user_prompt
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
            response.raise_for_status()
            
            st.write("Evaluating results against Governance Constraints...")
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
                
            status.update(label="Validation Complete", state="complete", expanded=False)
            st.divider()
            
            # --- Extract Expected JSON Keys ---
            score = int(result.get("score", 0))
            verdict = str(result.get("verdict", "BLOCKED")).upper()
            content = result.get("content", "Error: No content generated.")
            violations = result.get("violations", [])
            recommendation = result.get("recommendation", "No recommendation provided.")
            
            # Score Color Logic
            if score >= 80:
                score_class = "score-green"
            elif score >= 50:
                score_class = "score-yellow"
            else:
                score_class = "score-red"
                
            # Verdict Badge Logic
            badge_class = "verdict-approved" if verdict == "APPROVED" else "verdict-blocked"
            badge_icon = "✅" if verdict == "APPROVED" else "🚫"

            # --- Evaluation Dashboard ---
            st.markdown("### Compliance Verification Report")
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.markdown(f"""
                <div style="text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
                    <p class="score-number {score_class}">{score}</p>
                    <p class="stat-line">10 policies checked</p>
                </div>
                """, unsafe_allow_html=True)
                
            with c2:
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 2rem;">
                    <p style="margin:0; color:#94a3b8; font-weight:600; text-transform:uppercase; font-size:1rem; letter-spacing: 1.5px;">Final Verdict</p>
                    <div class="verdict-badges" style="margin-top:8px;">
                        <span class="verdict-badge {badge_class}">{badge_icon} {verdict}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- Generated Content Box ---
            st.markdown("<h3 style='margin-top: 2rem;'>Generated Output</h3>", unsafe_allow_html=True)

            def render_content_smartly(c_val):
                c_clean = str(c_val).strip()
                
                # Scenario 1: n8n returned a direct URL to a generated image/flyer
                if c_clean.startswith("http") and "\n" not in c_clean and " " not in c_clean:
                    st.image(c_clean, caption=f"Generated Asset", use_container_width=True)
                    
                # Scenario 2: n8n returned Text containing embedded Markdown images or HTML images
                elif "![" in c_clean or "<img" in c_clean:
                    st.markdown(c_clean, unsafe_allow_html=True)
                    
                # Scenario 3: n8n returned a text-based post/memo. Render in the 1-click Copy Box!
                else:
                    st.code(c_val, language="markdown")

            if verdict == "APPROVED":
                st.success("This content has passed all governance checks. You may safely publish it.")
                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                render_content_smartly(content)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("This content violates corporate policies and must be rewritten.")
                st.markdown('<div class="content-box content-blocked-wrapper">', unsafe_allow_html=True)
                st.markdown('<div class="do-not-publish-tag">⚠️ DO NOT PUBLISH</div>', unsafe_allow_html=True)
                # Ensure the text is on top of watermark
                st.markdown('<div style="position:relative; z-index:1;">', unsafe_allow_html=True)
                render_content_smartly(content)
                st.markdown('</div></div>', unsafe_allow_html=True)

            # --- Violations Panel ---
            if verdict == "BLOCKED" and violations:
                st.markdown("<h3 style='color: #ef4444; margin-top:2.5rem; border-bottom: 1px solid rgba(239,68,68,0.3); padding-bottom: 10px;'>🚩 Policy Violations</h3>", unsafe_allow_html=True)
                
                for flag in violations:
                    fname = flag.get("flag_name", "Unknown Violation")
                    ftext = flag.get("violated_text", "N/A")
                    fref = flag.get("policy_ref", "General Policy")
                    fpoints = flag.get("points_deducted", 0)
                    
                    st.markdown(f"""
                    <div class="violation-card">
                        <div class="violation-header">
                            <p class="violation-title">{fname}</p>
                            <span class="violation-points">-{fpoints} Pts</span>
                        </div>
                        <p class="violation-text">"{ftext}"</p>
                        <p class="violation-ref">Ref: {fref}</p>
                    </div>
                    """, unsafe_allow_html=True)

            # --- Recommendation Box ---
            if verdict == "BLOCKED" and recommendation:
                st.markdown(f"""
                <div class="recommendation-box">
                    <p class="amber-title">💡 How to fix this</p>
                    <p class="amber-text">{recommendation}</p>
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            status.update(label="Webhook Connection Failed", state="error", expanded=True)
            st.error("❌ Ensure your n8n test webhook is listening before generating!")
        except Exception as e:
            status.update(label="Validation Error", state="error", expanded=True)
            st.error(f"❌ Failed to parse backend validation payload. Error: {e}")
