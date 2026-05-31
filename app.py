import streamlit as st
import sys
import os
import re
from io import StringIO

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Mind | Autonomous Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (Enterprise / Professional Theme) ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Merriweather:wght@300;400;700&display=swap');

/* ── Global resets ── */
html, body, .stApp {
    font-family: 'Inter', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 3rem 4rem 5rem !important; max-width: 1200px; }

/* ── Typography & Headings ── */
.hero {
    text-align: center;
    padding: 2rem 0 3rem;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    margin-bottom: 2rem;
}
.hero h1 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 2.5rem;
    color: var(--text-color);
    margin: 0 0 0.5rem;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    color: gray;
    font-size: 1.1rem;
    font-weight: 400;
}

/* ── Pipeline steps ── */
.step-container {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin: 1.5rem 0 2.5rem 0;
}
.step-card {
    background: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-left: 4px solid rgba(128, 128, 128, 0.2);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    transition: all 0.2s ease;
}
.step-card.active {
    border-left-color: var(--primary-color);
    background: rgba(var(--primary-color-rgb), 0.05);
}
.step-card.done {
    border-left-color: #10b981; /* Professional Green */
}
.step-icon {
    font-size: 1.2rem;
    min-width: 2rem;
    text-align: center;
}
.step-info { flex: 1; }
.step-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--text-color);
    margin-bottom: 0.2rem;
}
.step-desc {
    font-size: 0.85rem;
    color: gray;
}
.step-badge {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-waiting  { background: rgba(128,128,128,0.1); color: gray; }
.badge-running  { background: rgba(var(--primary-color-rgb), 0.1); color: var(--primary-color); }
.badge-done     { background: rgba(16, 185, 129, 0.1); color: #10b981; }

/* ── Result sections ── */
.result-section {
    background: var(--background-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 8px;
    margin: 1.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    overflow: hidden;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    background: var(--secondary-background-color);
}
.result-title {
    font-weight: 600;
    font-size: 1rem;
    color: var(--text-color);
    flex: 1;
}
.result-tag {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    background: rgba(128,128,128,0.1);
    color: gray;
}

.result-body {
    padding: 1.5rem;
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--text-color);
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 450px;
    overflow-y: auto;
}

/* ── Academic Report Styling ── */
.result-body.report-text {
    font-family: 'Merriweather', serif;
    font-size: 1.05rem;
    line-height: 1.8;
    color: var(--text-color);
    max-height: none; /* Let the final report expand fully */
}

/* ── Scrollbar Polish ── */
.result-body::-webkit-scrollbar { width: 6px; }
.result-body::-webkit-scrollbar-track { background: transparent; }
.result-body::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.3); border-radius: 6px; }

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid rgba(128, 128, 128, 0.2);
    margin: 3rem 0;
}

/* ── Running pulse ── */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}
.pulsing { animation: pulse 1.5s ease-in-out infinite; }

/* ── Error box ── */
.error-box {
    background: rgba(239, 68, 68, 0.1);
    border-left: 4px solid #ef4444;
    padding: 1rem 1.5rem;
    border-radius: 4px;
    color: #b91c1c;
    font-size: 0.9rem;
    font-weight: 500;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ─────────────────────────────────────────────
def step_card(icon, title, desc, status="waiting"):
    badge_class = f"badge-{status}"
    card_class  = "active" if status == "running" else ("done" if status == "done" else "")
    pulse_class = "pulsing" if status == "running" else ""
    label = {"waiting": "Waiting", "running": "Running...", "done": "Complete"}[status]
    st.markdown(f"""
    <div class="step-card {card_class}">
        <div class="step-icon {pulse_class}">{icon}</div>
        <div class="step-info">
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        <span class="step-badge {badge_class}">{label}</span>
    </div>
    """, unsafe_allow_html=True)


def result_block(icon, title, tag, tag_class, content, body_class=""):
    st.markdown(f"""
    <div class="result-section">
        <div class="result-header">
            <span style="font-size: 1.1rem;">{icon}</span>
            <span class="result-title">{title}</span>
            <span class="result-tag">{tag}</span>
        </div>
        <div class="result-body {body_class}">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Research Raccoon 🦝</h1>
    <p class="hero-sub">Digging through the internet so you don't have to | Search • Read • Write • Critique</p>
            
</div>
""", unsafe_allow_html=True)

# ── Input Area ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input("Research Topic", placeholder="e.g. Recent advances in quantum error correction", label_visibility="collapsed")
with col2:
    run_btn = st.button("Run Pipeline", type="primary", use_container_width=True)

# ── Pipeline step indicators ──────────────────────────────────────────────────
STEPS = [
    ("🔍", "Search Agent",   "Queries the web for recent, reliable sources"),
    ("📄", "Reader Agent",   "Picks the best URL and scrapes deep content"),
    ("✍️", "Writer Chain",   "Drafts a structured research report"),
    ("🧐", "Critic Chain",   "Reviews the report and provides feedback"),
]

# Session state
if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None
if "step_statuses" not in st.session_state:
    st.session_state.step_statuses = ["waiting"] * 4

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.result = None
        st.session_state.error  = None

        step_box = st.empty()

        def render_steps(statuses):
            with step_box.container():
                st.markdown('<div class="step-container">', unsafe_allow_html=True)
                for i, (icon, title, desc) in enumerate(STEPS):
                    step_card(icon, title, desc, statuses[i])
                st.markdown('</div>', unsafe_allow_html=True)

        statuses = ["waiting"] * 4
        render_steps(statuses)

        try:
            # ── Redirect stdout so pipeline prints don't clutter the UI ──
            old_stdout = sys.stdout
            sys.stdout  = StringIO()

            from pipeline import run_research_pipeline

            # Step 1
            statuses[0] = "running";  render_steps(statuses)
            from agents import build_search_agent
            search_agent  = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state = {}
            state["search_results"] = search_result["messages"][-1].content
            statuses[0] = "done";     render_steps(statuses)

            # Step 2
            statuses[1] = "running";  render_steps(statuses)
            from agents import build_reader_agent
            reader_agent  = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            statuses[1] = "done";     render_steps(statuses)

            # Step 3
            statuses[2] = "running";  render_steps(statuses)
            from agents import writer_chain
            research_combined = (
                f"SEARCH RESULT :\n {state['search_results']}\n\n"
                f"SCRAPED RESULT :\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            statuses[2] = "done";     render_steps(statuses)

            # Step 4
            statuses[3] = "running";  render_steps(statuses)
            from agents import critic_chain
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            statuses[3] = "done";     render_steps(statuses)

            sys.stdout = old_stdout
            st.session_state.result = state

        except Exception as e:
            sys.stdout = old_stdout
            statuses = [s if s != "running" else "waiting" for s in statuses]
            render_steps(statuses)
            st.session_state.error = str(e)

# ── Show results ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f'<div class="error-box">⚠️ Error: {st.session_state.error}</div>', unsafe_allow_html=True)

if st.session_state.result:
    r = st.session_state.result
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-weight: 600; font-size: 1.25rem; margin-bottom: 1rem; color: var(--text-color);">
        Execution Log & Results
    </div>
    """, unsafe_allow_html=True)

    # 1. Final Research Report
    result_block("✍️", "Final Research Report",  "Report",   "tag-report",
                 r.get("report",          "—"), body_class="report-text")
    
    # 2. Critic Evaluation
    result_block("🧐", "Critic Evaluation",  "Critique", "tag-critic",
                 r.get("feedback",        "—"))
    
    # 3. Background Logs
    with st.expander("View Raw Agent Data (Search & Scrape Logs)"):
        result_block("🔍", "Search Engine Results",   "Search",   "tag-search",
                    r.get("search_results",  "—"))
        result_block("📄", "Raw Scraped Content",  "Scrape",   "tag-scrape",
                    r.get("scraped_content", "—"))

    # Download button
    st.markdown("<div style='margin-top:2rem;'>", unsafe_allow_html=True)
    full_text = (
        f"TOPIC: {topic}\n\n"
        f"{'='*60}\nRESEARCH REPORT\n{'='*60}\n{r.get('report','')}\n\n"
        f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n{r.get('feedback','')}\n\n"
        f"{'='*60}\nSEARCH RESULTS (RAW)\n{'='*60}\n{r.get('search_results','')}\n\n"
        f"{'='*60}\nSCRAPED CONTENT (RAW)\n{'='*60}\n{r.get('scraped_content','')}\n"
    )
    st.download_button(
        label="📄 Download Complete Report Context (.txt)",
        data=full_text,
        file_name=f"ResearchMind_{topic[:30].replace(' ','_')}.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Empty state hint ──────────────────────────────────────────────────────────
if not run_btn and st.session_state.result is None and st.session_state.error is None:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 0; color: gray;">
        <div style="font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.5;">🧠</div>
        <div style="font-size: 1rem;">
            Awaiting instructions. Enter a topic above to initiate the research pipeline.
        </div>
    </div>
    """, unsafe_allow_html=True)

