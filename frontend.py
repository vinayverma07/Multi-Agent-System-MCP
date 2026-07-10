import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from project import app
from auth import create_user, verify_user, get_history, save_history, init_db

st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #080d14;
}
/* ── Hero ── */
.hero-wrapper {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 2rem;
    min-height: 40vh;
    max-height: 520px;
}
.hero-bg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: block;
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    filter: brightness(0.6);
}
.hero-bg::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(11,31,60,0.5), rgba(17,43,85,0.45), rgba(27,59,111,0.45), rgba(12,29,50,0.5));
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
    pointer-events: none;
}
.hero-bg::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 20% 30%, rgba(72, 127, 214, 0.12), transparent 28%),
                radial-gradient(circle at 80% 20%, rgba(255, 184, 108, 0.10), transparent 24%),
                radial-gradient(circle at 50% 80%, rgba(129, 86, 255, 0.10), transparent 30%);
    pointer-events: none;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: clamp(1rem, 3vw, 2.5rem);
    max-width: 1100px;
    margin: 0 auto;
}
.hero-badge {
    background: rgba(58,123,213,0.25);
    border: 1px solid rgba(58,123,213,0.5);
    color: #7ab8f5 !important;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    margin-bottom: 0.9rem;
    display: inline-block;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.6rem;
    line-height: 1.2;
}
.hero-sub {
    color: #ffffff;
    font-size: 1rem;
    max-width: 560px;
}
.auth-card {
    background: rgba(8, 18, 34, 0.96);
    border: 1px solid rgba(58, 123, 213, 0.4);
    border-radius: 24px;
    padding: 2rem;
    max-width: 520px;
    margin: 2rem auto 1.5rem;
    box-shadow: 0 28px 64px rgba(0, 0, 0, 0.28);
}
.auth-shell {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 1.2rem;
    margin: 1rem 0 1.6rem;
    align-items: stretch;
}
.auth-hero-card {
    background: linear-gradient(135deg, rgba(7, 20, 38, 0.97), rgba(20, 45, 82, 0.95));
    border: 1px solid rgba(58, 123, 213, 0.45);
    border-radius: 24px;
    padding: 1.6rem;
    min-height: 100%;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.26);
}
.auth-badge {
    display: inline-block;
    background: rgba(58, 123, 213, 0.22);
    color: #8ac2fb;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.auth-title {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}
.auth-subtitle {
    color: #a4c5f8;
    margin-bottom: 1.3rem;
    line-height: 1.5;
}
.auth-feature-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1rem;
}
.auth-feature-pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e6f2ff;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    font-size: 0.85rem;
}
.auth-form-card {
    background: rgba(8, 18, 34, 0.96);
    border: 1px solid rgba(58, 123, 213, 0.4);
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.24);
}
.auth-form-title {
    color: #ffffff;
    font-size: 1.45rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}
.auth-form-subtitle {
    color: #8fb7e6;
    margin-bottom: 1rem;
    line-height: 1.45;
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
}
.input-label {
    color: #7ab8f5;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── Quick destinations ── */
.dest-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 1.2rem;
}
.dest-chip {
    background: #111b2b;
    border: 1px solid #1e3050;
    color: #f7fdf4;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
}
.dest-chip:hover { background: #1a2e47; border-color: #3a7bd5; color: #fff; }

/* ── Generate button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(26,107,191,0.35), 0 4px 15px rgba(0,0,0,0.4) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 40px rgba(26,107,191,0.6), 0 6px 20px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] {
    background: #0e1a2e !important;
    border: 1px solid #1e3050 !important;
    border-radius: 12px !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: #0e1a2e !important;
    border-radius: 12px 12px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: #0a1520 !important;
    color: #ffffff !important;
    padding: 0.25rem 0.5rem !important;
}
[data-testid="stStatusWidget"] * { color: #ffffff !important; }
[data-testid="stStatusWidget"] a { color: #4ea8f0 !important; }
[data-testid="stStatusWidget"] hr { border-color: #1e3050 !important; }

/* ── Section headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2e44;
}
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e0edf8; }

/* ── Metric bar ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #4ea8f0; }
.metric-lbl { font-size: 0.78rem; color: #5a7a96; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Final plan ── */
.final-card {
    background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3a5c;
    border-left: 4px solid #3a7bd5;
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #cce0f5;
    font-size: 0.95rem;
}

/* ── Save bar ── */
.save-bar {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #5a8ab0;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid #141f30 !important;
}
.sidebar-chip {
    background: #0e1a2b;
    border: 1px solid #1a2e44;
    border-radius: 8px;
    padding: 0.45rem 0.75rem;
    margin-bottom: 0.4rem;
    font-size: 0.83rem;
    color: #7aa8cc;
}
.sidebar-title { color: #e0edf8; font-size: 1rem; font-weight: 600; margin: 1rem 0 0.5rem; }

/* Hide branding */
#MainMenu, footer { visibility: hidden; }

/* Textarea */
.stTextArea textarea {
    background: #0a1520 !important;
    border: 1px solid #1e2e44 !important;
    border-radius: 10px !important;
    color: #e8f4ff !important;
    font-size: 0.95rem !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}
.stTextArea textarea::placeholder { color: #4a6a85 !important; }

/* Text input (sidebar User ID field) */
input[type="text"], .stTextInput input {
    background: #0e1a2b !important;
    border: 1px solid #1a2e44 !important;
    border-radius: 8px !important;
    color: #e0edf8 !important;
}
input[type="text"]:focus, .stTextInput input:focus {
    border-color: #3a7bd5 !important;
    box-shadow: 0 0 0 2px rgba(58,123,213,0.2) !important;
}
input[type="text"]::placeholder { color: #3a5570 !important; }

/* All Streamlit labels — dark bg → light text */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stNumberInput label {
    color: #7ab8f5 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
}

/* General markdown / paragraph text */
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th {
    color: #cce0f5 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #e8f4ff !important; }
.stMarkdown code {
    background: #0e1a2b !important;
    color: #7ab8f5 !important;
    padding: 0.15em 0.4em;
    border-radius: 4px;
}

/* Metric labels — was #5a7a96 (too dim on dark bg) */
.metric-lbl { color: #7aa8cc !important; }

/* Save bar — was #5a8ab0 (slightly dim) */
.save-bar { color: #8ab8d8 !important; }
.save-bar code { color: #7ab8f5 !important; background: #0a1520 !important; }

/* Streamlit warning / info / success on dark bg */
.stAlert { background: #0e1a2b !important; border-radius: 10px !important; }
.stAlert p, .stAlert div { color: #e0edf8 !important; }

/* Sidebar text & dividers */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown { color: #a0c4e0 !important; }
section[data-testid="stSidebar"] hr { border-color: #1a2e44 !important; }

/* Download button — light bg → dark text  */
div[data-testid="stDownloadButton"] > button {
    background: #1a3a5c !important;
    color: #e8f4ff !important;
    border: 1px solid #2a5080 !important;
    border-radius: 10px !important;
}

/* ── Hotel Card Styles ── */
.hotel-card {
    background: linear-gradient(135deg, #0e1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3050;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.3s ease;
}
.hotel-card:hover {
    border-color: #3a7bd5;
    box-shadow: 0 4px 12px rgba(58, 123, 213, 0.15);
}
.hotel-num {
    display: inline-block;
    background: rgba(58, 123, 213, 0.25);
    color: #7ab8f5;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 0.5rem;
}
.hotel-title {
    color: #e8f4ff;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.hotel-content {
    color: #a4c5f8;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* ── Flight Card Styles ── */
.flight-card {
    background: linear-gradient(135deg, #0e1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3050;
    border-left: 4px solid #2978d4;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}
.flight-label {
    color: #7ab8f5;
    font-weight: 700;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.flight-value {
    color: #e8f4ff;
    font-size: 1rem;
}

/* ── Weather Card Styles ── */
.weather-section {
    background: linear-gradient(135deg, #0e1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3050;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}
.weather-title {
    color: #7ab8f5;
    font-weight: 700;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e3050;
}
.weather-content {
    color: #a4c5f8;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Itinerary Styles ── */
.itinerary-container {
    background: linear-gradient(135deg, #0e1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3050;
    border-radius: 12px;
    padding: 1.5rem;
}
.itinerary-content {
    color: #a4c5f8;
    font-size: 0.95rem;
    line-height: 1.8;
}
.itinerary-content h1, .itinerary-content h2, .itinerary-content h3 {
    color: #e8f4ff;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}
.itinerary-content li, .itinerary-content ul {
    margin-left: 1.2rem;
    margin-bottom: 0.3rem;
}

/* ── Final Response Styles ── */
.final-response {
    background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3a5c;
    border-left: 4px solid #3a7bd5;
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #cce0f5;
    font-size: 0.95rem;
}
.final-response h1, .final-response h2, .final-response h3 {
    color: #e8f4ff;
    margin-top: 1.2rem;
    margin-bottom: 0.6rem;
}
.final-response ul, .final-response ol {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
}
.final-response li {
    margin-bottom: 0.4rem;
}
</style>
""", unsafe_allow_html=True)

init_db()

def format_hotel_results(hotel_text):
    """Format hotel results into nice cards."""
    if not hotel_text or not hotel_text.strip():
        return "<p style='color: #7aa8cc;'>_No hotel data returned._</p>"
    
    import html
    lines = hotel_text.strip().split('\n')
    html_output = ""
    
    for i, line in enumerate(lines, 1):
        if line.strip():
            stripped = line.strip()
            # Check if line starts with a number (like "1. ")
            if stripped and stripped[0].isdigit() and '. ' in stripped:
                parts = stripped.split('. ', 1)
                num = parts[0]
                rest = html.escape(parts[1]) if len(parts) > 1 else ""
                html_output += f'<div class="hotel-card"><span class="hotel-num">{num}</span><div class="hotel-title">{rest}</div>'
            elif line.startswith('   '):
                # This is content, add it to the current card
                content = html.escape(line.strip())
                html_output += f'<div class="hotel-content">{content}</div></div>'
            else:
                escaped_content = html.escape(stripped)
                html_output += f'<div class="hotel-content">{escaped_content}</div></div>'
    
    return html_output if html_output else "<p style='color: #7aa8cc;'>_No hotel data returned._</p>"

def format_flight_results(flight_text):
    """Format flight results into structured cards."""
    if not flight_text or not flight_text.strip():
        return "<p style='color: #7aa8cc;'>_No flight data returned._</p>"
    
    import html
    lines = flight_text.strip().split('\n')
    html_output = '<div style="display: flex; flex-direction: column; gap: 0.8rem;">'
    
    for line in lines:
        if line.strip():
            stripped = line.strip()
            # Check if line has a number followed by dot and space
            if stripped and stripped[0].isdigit() and '. ' in stripped:
                parts = stripped.split('. ', 1)
                num = parts[0]
                content = html.escape(parts[1]) if len(parts) > 1 else ""
                html_output += f'<div class="flight-card"><div class="flight-label">Point {num}</div><div class="flight-value">{content}</div></div>'
            elif stripped and not stripped[0].isdigit():
                # Regular content line
                escaped_line = html.escape(stripped)
                html_output += f'<div style="color: #a4c5f8; font-size: 0.9rem; margin: 0.5rem 0;">{escaped_line}</div>'
    
    html_output += '</div>'
    return html_output if html_output else "<p style='color: #7aa8cc;'>_No flight data returned._</p>"

def format_weather_results(weather_text):
    """Format weather results into sections."""
    if not weather_text or not weather_text.strip():
        return "<p style='color: #7aa8cc;'>_No weather data returned._</p>"
    
    import html
    html_output = ""
    sections = weather_text.strip().split('\n\n')
    
    for section in sections:
        if section.strip():
            lines = section.strip().split('\n')
            # First line might be a header
            if lines:
                first_line = lines[0].strip()
                if ':' in first_line:
                    title, _ = first_line.split(':', 1)
                    escaped_title = html.escape(title.strip())
                    html_output += f'<div class="weather-section"><div class="weather-title">{escaped_title}</div>'
                    remaining_content = '\n'.join(lines)
                    if ':' in remaining_content:
                        content = remaining_content.split(':', 1)[1].strip()
                    else:
                        content = remaining_content
                    escaped_content = html.escape(content)
                    html_output += f'<div class="weather-content">{escaped_content.replace(chr(10), "<br>")}</div></div>'
                else:
                    escaped_section = html.escape(section)
                    html_output += f'<div class="weather-section"><div class="weather-content">{escaped_section.replace(chr(10), "<br>")}</div></div>'
    
    return html_output if html_output else "<p style='color: #7aa8cc;'>_No weather data returned._</p>"

def format_itinerary_results(itinerary_text):
    """Format itinerary results with styling."""
    if not itinerary_text or not itinerary_text.strip():
        return "<div class='itinerary-container'><p style='color: #7aa8cc;'>_No itinerary generated._</p></div>"
    
    # Escape HTML and replace line breaks
    import html
    escaped_text = html.escape(itinerary_text)
    formatted_text = escaped_text.replace('\n', '<br>')
    
    return f'<div class="itinerary-container"><div class="itinerary-content">{formatted_text}</div></div>'

def format_final_response(response_text):
    """Format final response with styling."""
    if not response_text or not response_text.strip():
        return "<p style='color: #7aa8cc;'>_No final response._</p>"
    
    # Escape HTML and replace line breaks
    import html
    escaped_text = html.escape(response_text)
    formatted_text = escaped_text.replace('\n', '<br>')
    
    return f'<div class="final-response">{formatted_text}</div>'

if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "enter_user"
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "signup"
if "auth_message" not in st.session_state:
    st.session_state.auth_message = ""
if "auth_error" not in st.session_state:
    st.session_state.auth_error = ""

thread_id = st.session_state.thread_id

if not st.session_state.user_logged_in:
    st.markdown("<div class='auth-shell'>", unsafe_allow_html=True)
    auth_col1, auth_col2 = st.columns([1.05, 0.95], gap="large")

    with auth_col1:
        st.markdown(
            """
            <div class='auth-hero-card'>
                <div class='auth-badge'>✦ AI Travel Planner</div>
                <div class='auth-title'>Create your travel account</div>
                <div class='auth-subtitle'>Save your favorite destinations, reuse your best trip prompts, and let AI build polished itineraries in seconds.</div>
                <div class='auth-feature-list'>
                    <div class='auth-feature-pill'>⚡ Instant planning</div>
                    <div class='auth-feature-pill'>🧠 Smart itinerary generation</div>
                    <div class='auth-feature-pill'>✈️ Flight & hotel suggestions</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with auth_col2:
        st.markdown(
            """
            <div class='auth-form-card'>
                <div class='auth-form-title'>Welcome to AI Travel Booker</div>
                <div class='auth-form-subtitle'>Sign up to start planning your next adventure or log in to continue where you left off.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.pills(
            "Mode",
            options=["login", "signup"],
            default=st.session_state.auth_mode,
            format_func=lambda x: "Log In" if x == "login" else "Sign Up",
            selection_mode="single",
            key="auth_mode",
        )

        username = st.text_input(
            "Username",
            value=st.session_state.username,
            placeholder="Choose a username",
            key="auth_username",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="auth_password",
        )
        if st.session_state.auth_mode == "signup":
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="auth_confirm_password",
            )
        else:
            confirm_password = None

        if st.session_state.auth_mode == "signup":
            if st.button("Create Account", use_container_width=True):
                if not username or not password or not confirm_password:
                    st.session_state.auth_error = "All fields are required for sign up."
                elif password != confirm_password:
                    st.session_state.auth_error = "Passwords do not match."
                else:
                    success, result = create_user(username, password)
                    if success:
                        st.session_state.user_logged_in = True
                        st.session_state.user_id = result
                        st.session_state.username = username.strip().lower()
                        st.session_state.thread_id = result
                        st.session_state.auth_message = "Account created successfully. You are now logged in."
                        st.rerun()
                    else:
                        st.session_state.auth_error = result
        else:
            if st.button("Login", use_container_width=True):
                if not username or not password:
                    st.session_state.auth_error = "Username and password are required."
                else:
                    success, result = verify_user(username, password)
                    if success:
                        st.session_state.user_logged_in = True
                        st.session_state.user_id = result
                        st.session_state.username = username.strip().lower()
                        st.session_state.thread_id = result
                        st.session_state.auth_message = "Login successful. Redirecting..."
                        st.rerun()
                    else:
                        st.session_state.auth_error = result

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.auth_error:
        st.error(st.session_state.auth_error)
    elif st.session_state.auth_message:
        st.success(st.session_state.auth_message)

    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🌍 AI Travel Planner</div>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.user_logged_in:
        st.markdown(f"<div class='sidebar-chip'>User ID: {st.session_state.user_id}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='sidebar-chip'>Username: {st.session_state.username}</div>", unsafe_allow_html=True)
        if st.button("🔓 Logout"):
            st.session_state.user_logged_in = False
            st.session_state.user_id = ""
            st.session_state.username = ""
            st.session_state.thread_id = "enter_user"
            st.session_state.auth_message = ""
            st.session_state.auth_error = ""
            st.rerun()
    else:
        thread_id = st.text_input(
            "👤 User ID",
            value=st.session_state.thread_id,
            key="thread_id",
            help="Your session ID — keeps travel history across queries",
        )

    st.markdown("<div class='sidebar-title'>Powered by</div>", unsafe_allow_html=True)
    for tech in ["🔗 LangGraph", "🧠 Groq · LLaMA 3.3 70B", "🐘 PostgreSQL", "🔍 Tavily Search", "✈️ AviationStack"]:
        st.markdown(f"<div class='sidebar-chip'>{tech}</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>Agent Pipeline</div>", unsafe_allow_html=True)
    for step in ["① Flight Agent", "② Hotel Agent", "③ Weather Agent", "④ Itinerary Agent", "⑤ Final Agent"]:
        st.markdown(f"<div class='sidebar-chip'>{step}</div>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-bg" style="background-image: url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80');"></div>
    <div class="hero-content">
        <div class="hero-badge">✦ Multi-Agent AI System</div>
        <div class="hero-title">✈️ AI Travel Booking System</div>
        <div class="hero-sub">Four specialized agents work together — searching flights, hotels, building an itinerary, and delivering your perfect trip plan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Destination image strip ───────────────────────────────────────────────────
DESTINATIONS = [
    ("🇯🇵 Tokyo",     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris",     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok",   "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome",      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai",     "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(5)
for col, (name, img_url) in zip(cols, DESTINATIONS):
    with col:
        st.markdown(f"""
        <div style="border-radius:10px;overflow:hidden;position:relative;height:90px;cursor:pointer;">
            <img src="{img_url}" style="width:100%;height:100%;object-fit:cover;filter:brightness(0.55);" />
            <div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;
                        color:#fff;font-size:0.8rem;font-weight:600;">{name}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown("<div class='input-label'>🗺️ Describe your trip</div>", unsafe_allow_html=True)

QUICK = ["7-day Japan under ₹2L", "Paris trip for 5 days", "Dubai weekend trip", "Bali backpacking 10 days"]
qcols = st.columns(len(QUICK))
for qc, label in zip(qcols, QUICK):
    with qc:
        if st.button(label, key=f"q_{label}"):
            st.session_state.user_query = label

user_query = st.text_area(
    "",
    value=st.session_state.user_query,
    key="user_query",
    placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
    height=120,
    label_visibility="collapsed",
)

action_col, reset_col = st.columns([3, 1])
with action_col:
    generate = st.button("🚀  Generate My Travel Plan", use_container_width=True)
with reset_col:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.user_query = ""
        st.rerun()

# ── Agent pipeline ────────────────────────────────────────────────────────────
AGENT_META = {
    "flight_agent":    ("✈️", "Flight Agent"),
    "hotel_agent":     ("🏨", "Hotel Agent"),
    "weather_agent":   ("🌤️", "Weather Agent"),
    "itinerary_agent": ("🗓️", "Itinerary Agent"),
    "final_agent":     ("🧠", "Final Agent"),
}

if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {"flight_results": "", "hotel_results": "", "weather_results": "",
                     "itinerary": "", "final_response": "", "llm_calls": 0}

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline — Live</span></div>",
                    unsafe_allow_html=True)

        with st.spinner("Generating your travel plan... This may take a moment."):
            for chunk in app.stream(
                {
                    "messages": [HumanMessage(content=user_query)],
                    "user_query": user_query,
                    "flight_results": "",
                    "hotel_results": "",
                    "itinerary": "",
                    "llm_calls": 0,
                },
                config=config,
                stream_mode="updates",
            ):
                for node_name, state_update in chunk.items():
                    icon, label = AGENT_META.get(node_name, ("🔧", node_name))

                    with st.status(f"{icon}  {label}", state="complete", expanded=True):
                        if node_name == "flight_agent":
                            text = state_update.get("flight_results", "")
                            collected["flight_results"] = text
                            flight_html = format_flight_results(text)
                            st.markdown(flight_html, unsafe_allow_html=True)

                        elif node_name == "hotel_agent":
                            text = state_update.get("hotel_results", "")
                            collected["hotel_results"] = text
                            hotel_html = format_hotel_results(text)
                            st.markdown(hotel_html, unsafe_allow_html=True)

                        elif node_name == "weather_agent":
                            text = state_update.get("weather_results", "")
                            collected["weather_results"] = text
                            weather_html = format_weather_results(text)
                            st.markdown(weather_html, unsafe_allow_html=True)

                        elif node_name == "itinerary_agent":
                            text = state_update.get("itinerary", "")
                            collected["itinerary"] = text
                            itinerary_html = format_itinerary_results(text)
                            st.markdown(itinerary_html, unsafe_allow_html=True)

                        elif node_name == "final_agent":
                            msgs = state_update.get("messages", [])
                            text = msgs[-1].content if msgs else ""
                            collected["final_response"] = text
                            final_html = format_final_response(text)
                            st.markdown(final_html, unsafe_allow_html=True)

                        collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])

        # Metrics
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-val">5</div><div class="metric-lbl">Agents Run</div></div>
            <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>
            <div class="metric-box"><div class="metric-val">✅</div><div class="metric-lbl">Status</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Final plan card
        if collected["final_response"]:
            st.markdown("<div class='sec-head'><span>🧠 Final Travel Plan</span></div>",
                        unsafe_allow_html=True)
            final_html = format_final_response(collected['final_response'])
            st.markdown(final_html, unsafe_allow_html=True)

        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)

        file_content = f"""# Travel Plan
**Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

---

## ✈️ Flight Information
{collected['flight_results'] or 'N/A'}

---

## 🏨 Hotel Information
{collected['hotel_results'] or 'N/A'}

---
## 🏨 weather Information
{collected['weather_results'] or 'N/A'}

---

## 🗓️ Itinerary
{collected['itinerary'] or 'N/A'}

---

## 🧠 Final Travel Plan
{collected['final_response'] or 'N/A'}

---
*LLM Calls: {collected['llm_calls']}*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        if st.session_state.user_logged_in and collected["final_response"]:
            try:
                save_history(st.session_state.user_id, user_query, collected["final_response"])
            except Exception as exc:
                st.warning(f"Could not save history: {exc}")

        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button("⬇️ Download Plan (MD)", data=file_content,
                               file_name=filename, mime="text/markdown",
                               use_container_width=True)
            try:
                import io
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas
                from reportlab.lib.utils import simpleSplit

                def render_pdf_bytes(text: str) -> bytes:
                    buffer = io.BytesIO()
                    c = canvas.Canvas(buffer, pagesize=letter)
                    width, height = letter
                    margin = 72
                    maxw = width - 2 * margin
                    font_name = "Helvetica"
                    font_size = 10
                    c.setFont(font_name, font_size)
                    lines = simpleSplit(text, font_name, font_size, maxw)
                    y = height - margin
                    for line in lines:
                        if y < margin:
                            c.showPage()
                            c.setFont(font_name, font_size)
                            y = height - margin
                        c.drawString(margin, y, line)
                        y -= font_size + 2
                    c.save()
                    return buffer.getvalue()

                pdf_bytes = render_pdf_bytes(file_content)
                st.download_button("⬇️ Download Plan (PDF)", data=pdf_bytes,
                                   file_name=filename.replace('.md', '.pdf'),
                                   mime="application/pdf", use_container_width=True)
            except Exception:
                st.info("PDF generation requires the 'reportlab' package. Install with: `pip install reportlab`")

        with info_col:
            st.markdown(f"<div class='save-bar'>📁 Auto-saved → <code>travel_plans/{filename}</code></div>",
                        unsafe_allow_html=True)
