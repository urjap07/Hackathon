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

# --- High Fidelity CSS Injection ---
st.markdown("""
<style>
    /* Navy Header Styling */
    .navy-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        border-bottom: 3px solid #3b82f6;
    }
    .navy-header h1 { color: #f8fafc; font-weight: 800; font-size: 2.5rem; margin-bottom: 0.5rem; padding: 0; }
    .navy-header p { font-size: 1.2rem; color: #94a3b8; margin: 0; }

    /* Score Styling */
    .score-green { color: #22c55e; text-shadow: 0 0 10px rgba(34, 197, 94, 0.4); }
    .score-yellow { color: #eab308; text-shadow: 0 0 10px rgba(234, 179, 8, 0.4); }
    .score-red { color: #ef4444; text-shadow: 0 0 10px rgba(239, 68, 68, 0.4); }
    
    .score-number { font-size: 3.5rem; font-weight: 800; line-height: 1; margin: 0;}
    .score-label { font-size: 1rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;}
    
    /* Verdict Badge */
    .verdict-badge {
        font-size: 1.5rem;
        font-weight: 800;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
    }
    .verdict-approved { background-color: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e; color: #22c55e; }
    .verdict-blocked { background-color: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #ef4444; }

    /* Generated Content Box (Blocked State) */
    .content-blocked-wrapper {
        border: 2px solid #ef4444;
        border-radius: 8px;
        padding: 1.5rem 1rem 1rem 1rem;
        position: relative;
        background-color: rgba(239, 68, 68, 0.05);
        margin-top: 1.5rem;
    }
    .do-not-publish-tag {
        position: absolute;
        top: -12px;
        left: 15px;
        background: #ef4444;
        color: white;
        font-weight: 800;
        padding: 2px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        letter-spacing: 1px;
    }
    
    /* Red Flag Violation Cards */
    .violation-card {
        background-color: #1e1e1e;
        border-left: 5px solid #ef4444;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .violation-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;}
    .violation-title { font-weight: 700; color: #fca5a5; font-size: 1.1rem; margin:0;}
    .violation-points { background: rgba(239, 68, 68, 0.2); color: #fca5a5; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: 800; }
    .violation-text { font-style: italic; color: #e2e8f0; margin: 0 0 8px 0; background: rgba(255,255,255,0.05); padding: 8px; border-radius: 4px; border-left: 2px solid #64748b;}
    .violation-ref { font-size: 0.85rem; color: #94a3b8; margin: 0; font-weight: 600;}

    /* Amber Recommendation Box */
    .recommendation-box {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 2rem;
    }
    .amber-title { color: #fbbf24; font-weight: 800; font-size: 1.2rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;}
    .amber-title::before { content: '💡'; }
    .amber-text { color: #fef3c7; margin: 0; line-height: 1.5;}
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
<div class="navy-header">
    <h1>AcmeCorp AI Portal</h1>
    <p>Sovereign AI Gateway for Enterprise Content</p>
</div>
""", unsafe_allow_html=True)

# --- Input Section ---
st.markdown("### Prepare Your Request")
col1, col2 = st.columns(2)

with col1:
    department = st.selectbox("Department", ["Marketing", "HR", "Sales", "Legal", "Executive"])
with col2:
    content_type = st.selectbox("Content Type", ["Social Media Post", "Internal Memo", "Press Release", "Email Campaign"])

user_prompt = st.text_area("What do you need help with?", placeholder="e.g., Draft a tweet about our upcoming Q4 financial results...", height=120)

if st.button("Generate & Verify", type="primary", use_container_width=True):
    if not user_prompt.strip():
        st.warning("Please provide a prompt.")
        st.stop()

    with st.spinner("AcmeCorp AI is generating and validating your content..."):
        payload = {
            "department": department,
            "content_type": content_type,
            "user_prompt": user_prompt
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # Unwrap array if n8n passes back a list of objects
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
                
            st.divider()
            
            # --- Extract Expected JSON Keys safely ---
            score = int(result.get("score", 0))
            verdict = str(result.get("verdict", "BLOCKED")).upper()
            content = result.get("content", "Error: No content generated.")
            violations = result.get("violations", [])
            recommendation = result.get("recommendation", "No recommendation provided.")
            
            # Determine Score Color Logic
            if score >= 80:
                score_class = "score-green"
            elif score >= 50:
                score_class = "score-yellow"
            else:
                score_class = "score-red"
                
            # Determine Verdict Badge Styling
            badge_class = "verdict-approved" if verdict == "APPROVED" else "verdict-blocked"
            badge_icon = "✅" if verdict == "APPROVED" else "🚫"

            # --- Evaluation Dashboard ---
            st.markdown("### Compliance Verification Report")
            c1, c2 = st.columns([1, 2])
            
            with c1:
                # Scorecard
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                    <p class="score-label">Policy Match Score</p>
                    <p class="score-number {score_class}">{score}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with c2:
                # Verdict Badge
                st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 1rem;">
                    <p style="margin:0; color:#94a3b8; font-weight:600; text-transform:uppercase; font-size:0.9rem;">Final Decision</p>
                    <div class="verdict-badge {badge_class}">{badge_icon} {verdict}</div>
                </div>
                """, unsafe_allow_html=True)

            # --- Generated Content Box ---
            st.markdown("### Generated Output")
            if verdict == "APPROVED":
                st.success("This content has passed all governance checks. You may safely publish it.")
                st.code(content, language="markdown") # Uses Streamlit's native copy button
            else:
                # Blocked render state with red border wrapper
                st.markdown(f"""
                <div class="content-blocked-wrapper">
                    <div class="do-not-publish-tag">DO NOT PUBLISH</div>
                </div>
                """, unsafe_allow_html=True)
                st.code(content, language="markdown")

            # --- Violations Panel ---
            if verdict == "BLOCKED" and violations:
                st.markdown("<h3 style='color: #ef4444; margin-top:2rem;'>🚩 Identified Policy Violations</h3>", unsafe_allow_html=True)
                
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

            # --- Recommendation Panel ---
            if verdict == "BLOCKED" and recommendation:
                st.markdown(f"""
                <div class="recommendation-box">
                    <p class="amber-title">How to fix this</p>
                    <p class="amber-text">{recommendation}</p>
                </div>
                """, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error("❌ Webhook Connection Failed. Ensure your n8n test webhook is listening before generating!")
        except Exception as e:
            st.error(f"❌ Failed to parse backend validation payload. Ensure n8n returns the exact schema (score, verdict, content, violations, recommendation). Error: {e}")
            st.code(response.text) # Dump what n8n actually sent for debugging
