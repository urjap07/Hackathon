import streamlit as st
import requests
import json
import time
import math

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vivek-Kavach | AI Content Governance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

/* ── Root Variables ── */
:root {
  --cream:     #FAF8F4;
  --paper:     #F3F0EA;
  --warm-grey: #E8E4DC;
  --sand:      #D4CFC4;
  --muted:     #9B9589;
  --ink:       #2A2520;
  --ink-light: #4A4540;
  --ink-muted: #6B6560;
  --accent:    #C84B31;
  --accent-soft: #F2DDD8;
  --safe:      #2E7D52;
  --safe-soft: #D6EDE0;
  --warn:      #B85C00;
  --warn-soft: #FDE8CC;
  --border:    rgba(42,37,32,0.10);
  --shadow-sm: 0 2px 8px rgba(42,37,32,0.06);
  --shadow-md: 0 6px 24px rgba(42,37,32,0.10);
  --shadow-lg: 0 16px 48px rgba(42,37,32,0.14);
  --radius:    14px;
  --radius-sm: 8px;
}

/* ── Global ── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
  background-color: var(--cream);
  color: var(--ink);
}

.stApp { background: var(--cream); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: var(--paper) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
  font-family: 'DM Serif Display', serif;
  color: var(--ink);
}

/* ── Nav Pills (radio buttons as tabs) ── */
[data-testid="stSidebar"] .stRadio > div {
  gap: 6px;
}
[data-testid="stSidebar"] .stRadio label {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  color: var(--ink-muted);
  width: 100%;
  display: block;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: var(--warm-grey);
  color: var(--ink);
}

/* ── Hide default streamlit header ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Input box ── */
.stTextArea textarea {
  background: #FFFFFF;
  border: 1.5px solid var(--warm-grey);
  border-radius: var(--radius);
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: var(--ink);
  padding: 14px 18px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  box-shadow: var(--shadow-sm);
}
.stTextArea textarea:focus {
  border-color: var(--ink);
  box-shadow: 0 0 0 3px rgba(42,37,32,0.08);
}

/* ── Select boxes ── */
.stSelectbox select, div[data-baseweb="select"] {
  background: #FFFFFF;
  border: 1.5px solid var(--warm-grey) !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'DM Sans', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--ink) !important;
  color: #FAF8F4 !important;
  border: none !important;
  border-radius: var(--radius-sm) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-weight: 600 !important;
  font-size: 15px !important;
  padding: 12px 32px !important;
  letter-spacing: 0.3px;
  transition: all 0.2s ease !important;
  box-shadow: var(--shadow-sm) !important;
}
.stButton > button:hover {
  background: #3D3530 !important;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--ink) !important; }

/* ── Card component ── */
.vk-card {
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 28px;
  box-shadow: var(--shadow-sm);
  margin-bottom: 18px;
  animation: fadeUp 0.4s ease both;
}

/* ── Verdict badge ── */
.vk-verdict {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 22px;
  border-radius: 100px;
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.vk-verdict.approved {
  background: var(--safe-soft);
  color: var(--safe);
  border: 1.5px solid rgba(46,125,82,0.25);
}
.vk-verdict.blocked {
  background: var(--accent-soft);
  color: var(--accent);
  border: 1.5px solid rgba(200,75,49,0.25);
}

/* ── Score gauge wrapper ── */
.gauge-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

/* ── Violation row ── */
.vk-violation {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid var(--warm-grey);
  animation: fadeUp 0.35s ease both;
}
.vk-violation:last-child { border-bottom: none; }
.vk-deduct {
  min-width: 52px;
  text-align: center;
  background: var(--accent-soft);
  color: var(--accent);
  border-radius: 6px;
  padding: 4px 0;
  font-weight: 700;
  font-size: 13px;
}
.vk-flag-text {
  font-size: 13.5px;
  color: var(--ink-light);
  line-height: 1.5;
}
.vk-flag-name {
  font-weight: 600;
  color: var(--ink);
  font-size: 14px;
  margin-bottom: 2px;
}

/* ── Meta tag ── */
.vk-meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 5px 14px;
  font-size: 13px;
  color: var(--ink-muted);
  font-weight: 500;
}
.vk-meta-tag span { color: var(--ink); font-weight: 600; }

/* ── Section label ── */
.vk-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 10px;
}

/* ── Flagged text ── */
.vk-flagged-text {
  background: var(--warn-soft);
  border-left: 3px solid var(--warn);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 12px 16px;
  font-size: 13.5px;
  color: var(--ink-light);
  margin-bottom: 10px;
  line-height: 1.6;
}

/* ── Fix block ── */
.vk-fix {
  background: var(--safe-soft);
  border-left: 3px solid var(--safe);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 14px 18px;
  font-size: 14px;
  color: var(--ink-light);
  line-height: 1.6;
}

/* ── Hero header ── */
.vk-hero {
  padding: 10px 0 28px 0;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
}
.vk-hero h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 2.2rem;
  color: var(--ink);
  margin: 0;
  line-height: 1.15;
}
.vk-hero p {
  color: var(--ink-muted);
  font-size: 15px;
  margin: 8px 0 0 0;
}

/* ── Score ring label ── */
.score-number {
  font-family: 'DM Serif Display', serif;
  font-size: 3rem;
  color: var(--ink);
  text-align: center;
  margin-top: -8px;
}

/* ── Animations ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}
.pulse-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  display: inline-block;
  animation: pulse-dot 1.6s ease-in-out infinite;
}
.pulse-dot.safe  { background: var(--safe); }
.pulse-dot.block { background: var(--accent); }

/* ── About page ── */
.about-hero {
  background: linear-gradient(135deg, #F3F0EA 0%, #FAF8F4 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 40px 48px;
  margin-bottom: 28px;
  animation: fadeUp 0.5s ease both;
}
.about-hero h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 2.6rem;
  color: var(--ink);
  margin: 0 0 10px 0;
}
.about-hero p {
  font-size: 16px;
  color: var(--ink-muted);
  max-width: 560px;
  line-height: 1.7;
}

.feature-card {
  background: #FFFFFF;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  height: 100%;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  animation: fadeUp 0.5s ease both;
}
.feature-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.feature-icon {
  font-size: 1.8rem;
  margin-bottom: 12px;
}
.feature-card h3 {
  font-family: 'DM Serif Display', serif;
  font-size: 1.15rem;
  color: var(--ink);
  margin: 0 0 8px 0;
}
.feature-card p {
  font-size: 13.5px;
  color: var(--ink-muted);
  line-height: 1.6;
  margin: 0;
}

.stack-pill {
  display: inline-block;
  background: var(--paper);
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 5px 14px;
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-light);
  margin: 4px;
}

.scoring-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid var(--warm-grey);
  font-size: 14px;
  color: var(--ink-light);
}
.scoring-row:last-child { border-bottom: none; }
.scoring-row .pts {
  font-weight: 700;
  color: var(--accent);
}

/* ── divider ── */
hr { border-color: var(--border) !important; }

</style>
""", unsafe_allow_html=True)

# ── Webhook URL ───────────────────────────────────────────────────────────────
WEBHOOK_URL = "https://hriday.datachef.in/webhook-test/41ff8937-9d4f-4128-b786-52ab925f1062"

# ── Helper: SVG Gauge ─────────────────────────────────────────────────────────
def build_gauge_svg(score: int) -> str:
    """Build a clean semicircular gauge SVG."""
    pct = max(0, min(100, score)) / 100

    # Arc math
    cx, cy, r = 130, 120, 90
    start_angle = -180
    end_angle   = 0
    sweep        = (end_angle - start_angle) * pct
    angle_rad    = math.radians(start_angle + sweep)
    ex = cx + r * math.cos(angle_rad)
    ey = cy + r * math.sin(angle_rad)
    large_arc = 1 if sweep > 180 else 0

    # Color zones
    if score >= 80:
        track_color = "#2E7D52"
        glow        = "rgba(46,125,82,0.18)"
    elif score >= 50:
        track_color = "#B85C00"
        glow        = "rgba(184,92,0,0.15)"
    else:
        track_color = "#C84B31"
        glow        = "rgba(200,75,49,0.15)"

    return f"""
    <svg width="260" height="150" viewBox="0 0 260 150" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <linearGradient id="trackGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="{track_color}" stop-opacity="0.7"/>
          <stop offset="100%" stop-color="{track_color}" stop-opacity="1"/>
        </linearGradient>
      </defs>

      <!-- Background track -->
      <path d="M {cx-r},{cy} A {r},{r} 0 0,1 {cx+r},{cy}"
            fill="none" stroke="#E8E4DC" stroke-width="14"
            stroke-linecap="round"/>

      <!-- Zone markers -->
      <line x1="{cx + r*math.cos(math.radians(-180 + 80*1.8)):.1f}"
            y1="{cy + r*math.sin(math.radians(-180 + 80*1.8)):.1f}"
            x2="{(cx + (r+10)*math.cos(math.radians(-180 + 80*1.8))):.1f}"
            y2="{(cy + (r+10)*math.sin(math.radians(-180 + 80*1.8))):.1f}"
            stroke="#D4CFC4" stroke-width="2"/>

      <!-- Active track -->
      {f'<path d="M {cx-r},{cy} A {r},{r} 0 {large_arc},1 {ex:.2f},{ey:.2f}" fill="none" stroke="url(#trackGrad)" stroke-width="14" stroke-linecap="round" filter="url(#glow)"/>' if pct > 0 else ''}

      <!-- Needle dot -->
      {f'<circle cx="{ex:.2f}" cy="{ey:.2f}" r="7" fill="{track_color}" stroke="white" stroke-width="2.5" filter="url(#glow)"/>' if pct > 0 else f'<circle cx="{cx-r}" cy="{cy}" r="7" fill="#D4CFC4" stroke="white" stroke-width="2.5"/>'}

      <!-- Zone labels -->
      <text x="{cx - r - 4}" y="{cy + 22}" font-size="10" fill="#9B9589" text-anchor="middle" font-family="DM Sans, sans-serif">0</text>
      <text x="{cx}" y="{cy - r - 12}" font-size="10" fill="#9B9589" text-anchor="middle" font-family="DM Sans, sans-serif">50</text>
      <text x="{cx + r + 4}" y="{cy + 22}" font-size="10" fill="#9B9589" text-anchor="middle" font-family="DM Sans, sans-serif">100</text>

      <!-- Score text -->
      <text x="{cx}" y="{cy + 14}" font-size="38" fill="{track_color}" text-anchor="middle"
            font-family="DM Serif Display, serif" font-weight="400">{score}</text>
      <text x="{cx}" y="{cy + 34}" font-size="11" fill="#9B9589" text-anchor="middle"
            font-family="DM Sans, sans-serif" letter-spacing="1.5">/100</text>
    </svg>
    """

# ── Helper: Call n8n webhook ──────────────────────────────────────────────────
def call_workflow(prompt: str, department: str, content_type: str) -> dict | None:
    payload = {
        "user_prompt": prompt,
        "department": department,
        "content_type": content_type,
    }
    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=90)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        st.error("⏱ Request timed out. The workflow took too long to respond.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot reach the n8n webhook. Is your instance running?")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None

# ── Sidebar Nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 6px 0 24px 0;'>
      <div style='font-family:"DM Serif Display",serif; font-size:1.4rem; color:var(--ink); letter-spacing:-0.3px;'>
        🛡️ Vivek-Kavach
      </div>
      <div style='font-size:12px; color:var(--muted); margin-top:4px; letter-spacing:0.3px;'>
        AI Content Governance
      </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["⚡  Compliance Check", "📖  About"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='margin:18px 0;'/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:12px; color:var(--muted); line-height:1.7;'>
      <b style='color:var(--ink-light);'>Score thresholds</b><br>
      🟢 80–100 → Approved<br>
      🟡 50–79  → Review needed<br>
      🔴  0–49  → Blocked
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — COMPLIANCE CHECK
# ═══════════════════════════════════════════════════════════════════════════════
if "⚡" in page:
    st.markdown("""
    <div class='vk-hero'>
      <h1>Content Compliance Auditor</h1>
      <p>Paste or describe your content below. Our AI governance pipeline will audit it against Acme Corp policies in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Section ─────────────────────────────────────────────────────────
    c1, c2 = st.columns([2, 1])
    with c1:
        user_prompt = st.text_area(
            "Content to audit",
            placeholder="e.g. Write a social media post for our new protein supplement claiming it boosts immunity by 40% and is #1 in India...",
            height=160,
            label_visibility="collapsed",
        )
    with c2:
        department = st.selectbox(
            "Department",
            ["Sales", "Marketing", "HR", "Legal", "Finance", "Product"],
        )
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Email Campaign", "Blog Article", "Ad Copy", "Internal Memo", "Press Release"],
        )
        run_btn = st.button("🔍 Run Audit", use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Run ───────────────────────────────────────────────────────────────────
    if run_btn:
        if not user_prompt.strip():
            st.warning("Please enter some content to audit.")
            st.stop()

        with st.spinner("Routing through Retriever → Architect → Referee…"):
            data = call_workflow(user_prompt.strip(), department, content_type)

        if not data:
            st.stop()

        # Unpack fields
        score      = data.get("compliance_score", data.get("score", 0))
        compliant  = data.get("compliant", score >= 80)
        verdict    = data.get("verdict", "APPROVED" if compliant else "BLOCKED")
        final_post = data.get("final_post", data.get("final_content", ""))
        fix        = data.get("recommendation", data.get("actionable_fix", "No fixes needed."))
        meta       = data.get("meta", {})
        dept_out   = meta.get("department", department)
        type_out   = meta.get("type", content_type)
        query_out  = meta.get("query", user_prompt[:80])

        # Raw explanation / violations from score_explanation
        raw_explanation = data.get("score_explanation", "")

        # Parse violation lines from explanation string
        violations_parsed = []
        for line in raw_explanation.splitlines():
            line = line.strip()
            if line.startswith("-") and "pts:" in line:
                try:
                    pts_part, rest = line[1:].split("pts:", 1)
                    pts = abs(int(pts_part.strip().replace(" ", "")))
                    flag_detail = rest.strip()
                    if "(" in flag_detail and flag_detail.endswith(")"):
                        flag_name = flag_detail[:flag_detail.rfind("(")].strip()
                        detail    = flag_detail[flag_detail.rfind("(")+1:-1].strip()
                    else:
                        flag_name = flag_detail
                        detail    = ""
                    violations_parsed.append({"flag": flag_name, "detail": detail, "pts": pts})
                except Exception:
                    pass

        # ── 1) META BAR ───────────────────────────────────────────────────────
        st.markdown(f"""
        <div style='display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px; animation:fadeUp 0.3s ease both;'>
          <span class='vk-meta-tag'>🏢 Dept: <span>{dept_out}</span></span>
          <span class='vk-meta-tag'>📄 Type: <span>{type_out}</span></span>
          <span class='vk-meta-tag'>💬 Query: <span title="{query_out}">{query_out[:55]}{"…" if len(query_out)>55 else ""}</span></span>
        </div>
        """, unsafe_allow_html=True)

        # ── Main 2-column layout: left=scorecard, right=gauge+details ─────────
        left_col, right_col = st.columns([4, 5], gap="large")

        # ── LEFT: Verdict + Score Breakdown ──────────────────────────────────
        with left_col:
            dot_cls   = "safe" if compliant else "block"
            badge_cls = "approved" if compliant else "blocked"
            icon      = "✓" if compliant else "✕"
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:0.05s;'>
              <div class='vk-label'>Compliance Verdict</div>
              <div class='vk-verdict {badge_cls}'>
                <span class='pulse-dot {dot_cls}'></span>
                {icon} &nbsp;{verdict}
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Score breakdown card
            st.markdown("<div class='vk-card' style='animation-delay:0.1s;'>", unsafe_allow_html=True)
            st.markdown("<div class='vk-label'>Score Breakdown</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class='scoring-row'>
              <span>Base score</span>
              <span style='color:var(--ink);font-weight:600;'>100</span>
            </div>
            """, unsafe_allow_html=True)

            if violations_parsed:
                for v in violations_parsed:
                    st.markdown(f"""
                    <div class='scoring-row'>
                      <span style='font-size:13px;'>{v['flag']}</span>
                      <span class='pts'>−{v['pts']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='scoring-row'>
                  <span style='color:var(--safe); font-size:13px;'>✓ No violations found</span>
                  <span style='color:var(--safe); font-weight:600;'>−0</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center;
                        margin-top:12px; padding-top:12px; border-top:2px solid var(--border);
                        font-weight:700; font-size:15px;'>
              <span>Final Score</span>
              <span style='color:{"var(--safe)" if compliant else "var(--accent)"};
                           font-family:"DM Serif Display",serif; font-size:1.4rem;'>{score}</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── RIGHT: Gauge + Explanation + Content ─────────────────────────────
        with right_col:
            # Gauge
            st.markdown("<div class='vk-card' style='animation-delay:0.08s; text-align:center;'>", unsafe_allow_html=True)
            st.markdown("<div class='vk-label' style='text-align:left;'>Compliance Score</div>", unsafe_allow_html=True)
            st.markdown(build_gauge_svg(score), unsafe_allow_html=True)
            zone_label = "Safe to Publish" if score >= 80 else ("Needs Review" if score >= 50 else "Blocked — Do Not Publish")
            zone_color = "var(--safe)" if score >= 80 else ("var(--warn)" if score >= 50 else "var(--accent)")
            st.markdown(f"""
            <div style='font-size:13px; color:{zone_color}; font-weight:600;
                        letter-spacing:0.5px; margin-top:4px;'>{zone_label}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Explanation
            if raw_explanation:
                clean_exp = "\n".join(
                    l for l in raw_explanation.splitlines()
                    if not l.strip().startswith("-")
                ).strip()
                if clean_exp:
                    st.markdown(f"""
                    <div class='vk-card' style='animation-delay:0.15s;'>
                      <div class='vk-label'>Why this score?</div>
                      <div style='font-size:14px; color:var(--ink-light); line-height:1.7;'>{clean_exp}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Generated content
            if final_post:
                st.markdown(f"""
                <div class='vk-card' style='animation-delay:0.18s;'>
                  <div class='vk-label'>Generated Content</div>
                  <div style='font-size:14px; color:var(--ink-light); line-height:1.7; white-space:pre-wrap;'>{final_post}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # ── 5) Violated Texts & Flags ─────────────────────────────────────────
        if violations_parsed:
            st.markdown("<div class='vk-card' style='animation-delay:0.2s;'>", unsafe_allow_html=True)
            st.markdown("<div class='vk-label'>🚩 Violated Texts & Flags Raised</div>", unsafe_allow_html=True)
            for v in violations_parsed:
                st.markdown(f"""
                <div class='vk-violation'>
                  <div class='vk-deduct'>−{v['pts']}</div>
                  <div>
                    <div class='vk-flag-name'>{v['flag']}</div>
                    <div class='vk-flag-text'>{v['detail'] if v['detail'] else "Policy violation detected in submitted content."}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── 6) Actionable Fix ─────────────────────────────────────────────────
        if fix and fix.strip() and fix.lower() not in ("no fixes needed.", ""):
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:0.25s;'>
              <div class='vk-label'>🔧 Actionable Fix</div>
              <div class='vk-fix'>{fix}</div>
            </div>
            """, unsafe_allow_html=True)
        elif compliant:
            st.markdown(f"""
            <div class='vk-card' style='animation-delay:0.25s;'>
              <div class='vk-label'>🔧 Recommendation</div>
              <div class='vk-fix'>✓ Content is fully compliant. No edits required — safe to publish.</div>
            </div>
            """, unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:var(--muted); animation:fadeUp 0.5s ease both;'>
          <div style='font-size:3rem; margin-bottom:16px;'>🛡️</div>
          <div style='font-family:"DM Serif Display",serif; font-size:1.4rem; color:var(--ink-light); margin-bottom:8px;'>
            Awaiting content
          </div>
          <div style='font-size:14px; max-width:380px; margin:0 auto; line-height:1.7;'>
            Enter your content above, choose a department and content type, then hit
            <strong>Run Audit</strong> to see the compliance report.
          </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class='about-hero'>
      <h1>Vivek-Kavach</h1>
      <p>
        An enterprise AI content governance middleware — built to audit, score, and
        block non-compliant AI-generated content before it ever reaches a customer.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature grid
    cols = st.columns(3)
    features = [
        ("🔍", "Policy Retrieval", "Pinecone vector store holds all brand guidelines and legal rules. Every audit starts with a fresh policy fetch."),
        ("🤖", "Content Generation", "GPT-4o Architect generates the requested content, aware of department context and content type."),
        ("⚖️", "Compliance Refereeing", "A strict GPT-4o Referee applies a 10-point checklist and deducts points for each violation found."),
        ("📊", "Visual Scoring", "Live gauge with colour-coded zones: green (safe), amber (review), red (blocked) — instant intuition."),
        ("🚩", "Flag & Explain", "Each violation is surfaced with the exact policy reference, deducted points, and flagged text snippet."),
        ("🔧", "Actionable Fixes", "Every blocked report includes a concrete, step-by-step fix so writers can remediate immediately."),
    ]
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='feature-card' style='animation-delay:{0.05*i}s;'>
              <div class='feature-icon'>{icon}</div>
              <h3>{title}</h3>
              <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
        if (i + 1) % 3 == 0 and i != len(features) - 1:
            cols = st.columns(3)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Pipeline + Stack side by side
    pa, pb = st.columns([3, 2], gap="large")
    with pa:
        st.markdown("""
        <div class='vk-card'>
          <div class='vk-label'>Workflow Pipeline</div>
          <div style='display:flex; flex-direction:column; gap:0;'>
        """, unsafe_allow_html=True)
        steps = [
            ("Webhook", "Receives prompt, department, content type from this UI"),
            ("Retriever (Gemini)", "Searches Pinecone for relevant policies"),
            ("Parser 1", "Strips fluff, extracts structured context"),
            ("Architect (GPT-4o)", "Generates policy-aware content"),
            ("Code Parser 2", "Extracts clean generated content JSON"),
            ("Referee (GPT-4o)", "Runs 10-point compliance check"),
            ("Compliance Router", "Routes to Approved / Blocked response"),
        ]
        for i, (name, desc) in enumerate(steps):
            arrow = "↓" if i < len(steps) - 1 else ""
            st.markdown(f"""
            <div style='display:flex; gap:14px; align-items:flex-start; padding:10px 0;
                        border-bottom:1px solid var(--warm-grey);'>
              <div style='min-width:28px; height:28px; background:var(--paper); border:1px solid var(--border);
                          border-radius:50%; display:flex; align-items:center; justify-content:center;
                          font-size:12px; font-weight:700; color:var(--ink-muted);'>{i+1}</div>
              <div>
                <div style='font-weight:600; font-size:14px; color:var(--ink);'>{name}</div>
                <div style='font-size:13px; color:var(--ink-muted); margin-top:2px;'>{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with pb:
        st.markdown("""
        <div class='vk-card'>
          <div class='vk-label'>Tech Stack</div>
        """, unsafe_allow_html=True)
        stacks = {
            "Orchestration": ["n8n (self-hosted)", "GCP VM"],
            "AI Models": ["GPT-4o (OpenAI)", "Gemini 1.5 (Google)"],
            "Vector DB": ["Pinecone", "vivek-kavach assistant"],
            "Frontend": ["Streamlit", "DM Serif Display"],
        }
        for cat, items in stacks.items():
            st.markdown(f"<div style='font-size:12px; font-weight:600; color:var(--muted); letter-spacing:0.8px; text-transform:uppercase; margin:14px 0 6px 0;'>{cat}</div>", unsafe_allow_html=True)
            pills = "".join(f"<span class='stack-pill'>{item}</span>" for item in items)
            st.markdown(f"<div>{pills}</div>", unsafe_allow_html=True)

        st.markdown("""
          <div style='margin-top:20px; padding-top:16px; border-top:1px solid var(--border);'>
            <div class='vk-label'>Scoring Rules</div>
        """, unsafe_allow_html=True)
        rules = [
            ("Unverified health/product claim", "−20"),
            ("Unauthorized pricing promise", "−25"),
            ("PII / sensitive data exposure", "−30"),
            ("EU AI Act / DPDP violation", "−25"),
            ("Copyright / trademark risk", "−20"),
            ("Superlatives without proof", "−10"),
        ]
        for rule, pts in rules:
            st.markdown(f"""
            <div class='scoring-row' style='font-size:12.5px;'>
              <span>{rule}</span>
              <span class='pts'>{pts}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; color:var(--muted); font-size:12.5px; padding:20px 0; border-top:1px solid var(--border);'>
      Built for the <strong style='color:var(--ink-light);'>Enterprise AI Governance Hackathon</strong> &nbsp;·&nbsp;
      Powered by n8n, Pinecone, GPT-4o & Gemini
    </div>
    """, unsafe_allow_html=True)
