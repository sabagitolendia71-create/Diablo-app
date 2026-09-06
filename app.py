import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="DIABLO", layout="wide", initial_sidebar_state="collapsed")

# ----------------- SESSION STATE -----------------
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Trade"
if "balance" not in st.session_state:
    st.session_state.balance = 2226.72
if "used_promos" not in st.session_state:
    st.session_state.used_promos = set()

VALID_PROMOS = ["2045Q13TI", "203V0FL1E", "201JFEKBI", "201CMTUUA"]

# ----------------- STYLES -----------------
st.markdown("""
<style>
    /* Streamlit-ის ნაგულისხმევი ელემენტების დამალვა */
    header, footer, #MainMenu { visibility: hidden !important; height: 0 !important; }
    div[data-testid="stStatusWidget"], .viewerBadge_container__163eb { display: none !important; }

    .stApp {
        background-color: #0b0e14 !important;
        color: #ffffff !important;
    }

    /* ძირითადი კონტეინერის დაშორება ქვედა მენიუსგან */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 120px !important; 
        max-width: 480px !important;
        margin: 0 auto !important;
    }

    /* Top Header */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0 12px 0;
    }
    .brand-box {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .logo-d {
        background-color: #00dc82;
        color: #0b0e14;
        font-weight: 900;
        font-size: 18px;
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .diablo-title {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    /* Banner & Announcement */
    .hero-banner {
        background: linear-gradient(180deg, #111827 0%, #0b0e14 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px 20px;
        margin-bottom: 15px;
    }
    .hero-sub { color: #00dc82; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 6px; }
    .hero-title { color: #ffffff; font-size: 22px; font-weight: 800; margin: 0; }

    .announcement-bar {
        background-color: #111827;
        border-radius: 10px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 12px;
        color: #94a3b8;
        margin-bottom: 20px;
        border: 1px solid #1e293b;
    }

    /* Quick Cards */
    .quick-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 20px 0;
    }
    .quick-card {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 14px 8px;
        text-align: center;
    }
    .quick-label { color: #e2e8f0; font-size: 12px; margin-top: 6px; }

    .green-card {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        border-radius: 16px;
        padding: 22px;
        color: white;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px;
        background-color: #1e293b;
        color: #ffffff;
    }
    
    .call-btn button { background-color: #00dc82 !important; color: #0b0e14 !important; font-size: 15px !important; font-weight: bold !important; padding: 12px !important; }
    .put-btn button { background-color: #ef4444 !important; color: white !important; font-size: 15px !important; font-weight: bold !important; padding: 12px !important; }

    /* CUSTOM BOTTOM NAVIGATION CONTAINER */
    .nav-spacer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 70px;
        background-color: #090d16;
        border-top: 1px solid #1e293b;
        z-index: 999990;
        max-width: 480px;
        margin: 0 auto;
    }
    
    /* Streamlit-ის სვეტების გასწორება ქვედა ნავიგაციისთვის */
    div[data-testid="stHorizontalBlock"]:has(button[key^="nav_"]) {
        position: fixed !important;
        bottom: 12px !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999999 !important;
        max-width: 460px !important;
        margin: 0 auto !important;
        background-color: transparent !important;
    }

    /* Custom Navigation Buttons */
    button[key^="nav_"] {
        background-color: transparent !important;
        border: none !important;
        color: #64748b !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        padding: 4px 0 !important;
        box-shadow: none !important;
    }

    button[key^="nav_"]:hover {
        color: #00dc82 !important;
    }

    .green-text { color: #00dc82; font-weight: bold; }
    .red-text { color: #ef4444; font-weight: bold; }
    .sub-text { color: #64748b; font-size: 12px; }
    .green-bg-tag { background-color: rgba(0, 220, 130, 0.15); color: #00dc82; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ----------------- TOP HEADER -----------------
st.markdown("""
<div class="top-header">
    <div class="brand-box">
        <div class="logo-d">D</div>
        <div class="diablo-title">DIABLO</div>
    </div>
    <div style="color: #94a3b8; display: flex; gap: 16px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2"><path d="M5 8l6 6M4 14l6-6 2 2M2 5h12M9 2v3M15 11l6 9M21 11l-6 9"/></svg>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- PAGES CONTENT -----------------
tab = st.session_state.active_tab

if tab == "Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-sub">TRADE SMARTER</div>
        <div class="hero-title">The future starts here</div>
    </div>
    
    <div class="announcement-bar">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>
        <span>Welcome to DIABLO – your digital asset trading...</span>
    </div>
    
    <div class="quick-grid">
        <div class="quick-card">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg>
            <div class="quick-label">Deposit</div>
        </div>
        <div class="quick-card">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
            <div class="quick-label">Markets</div>
        </div>
        <div class="quick-card">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            <div class="quick-label">News</div>
        </div>
        <div class="quick-card">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
            <div class="quick-label">Service</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("<h4 style='font-size:15px; margin-bottom:12px;'>LIVE MARKET</h4>", unsafe_allow_html=True)
    
    market_data = [
        {"pair": "DASH / USDT", "price": "68.162", "change": "+4.07%"},
        {"pair": "DOT / USDT", "price": "0.946", "change": "+3.50%"},
        {"pair": "BCH / USDT", "price": "259.47", "change": "+1.34%"},
    ]
    
    for item in market_data:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.markdown(f"**{item['pair']}**")
        col2.markdown(f"<span style='color:#e2e8f0;'>{item['price']}</span>", unsafe_allow_html=True)
        col3.markdown(f"<span class='green-bg-tag'>{item['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:8px 0; border-color:#1e293b;'>", unsafe_allow_html=True)

elif tab == "Market":
    st.markdown("<h4 style='margin-bottom:15px; font-size:16px;'>Derivatives Market</h4>", unsafe_allow_html=True)
    
    pairs = [
        {"pair": "BTC/USDT", "vol": "VOL: 254144090.43", "price": "79784.12", "change": "-0.06%", "green": False},
        {"pair": "ETH/USDT", "vol": "VOL: 217937486.54", "price": "2493.48", "change": "+0.52%", "green": True},
        {"pair": "ADA/USDT", "vol": "VOL: 7575818.91", "price": "0.2183", "change": "-0.14%", "green": False},
        {"pair": "BCH/USDT", "vol": "VOL: 3053870.7", "price": "259.43", "change": "+1.33%", "green": True},
        {"pair": "DASH/USDT", "vol": "VOL: 41411014.51", "price": "68.119", "change": "+4.00%", "green": True},
    ]
    
    for p in pairs:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.markdown(f"**{p['pair']}**<br><span class='sub-text'>{p['vol']}</span>", unsafe_allow_html=True)
        col2.markdown(f"**{p['price']}**")
        color_class = "green-text" if p["green"] else "red-text"
        col3.markdown(f"<span class='{color_class}'>{p['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:6px 0; border-color:#1e293b;'>", unsafe_allow_html=True)

elif tab == "Trade":
    st.markdown("<h3 style='margin:0;'>BTC / USDT <span class='red-text' style='font-size:16px;'>-0.06%</span></h3>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    cols[0].button("60s")
    cols[1].button("120s")
    cols[2].button("5min")
    cols[3].button("10min")
    
    st.markdown("""
    <div style="font-size:12px; color:#64748b; margin: 10px 0;">
        Order expiration time: <span style="border:1px solid #00dc82; color:#00dc82; padding:1px 6px; border-radius:4px;">25 s</span>
    </div>
    """, unsafe_allow_html=True)
    
    dates = [datetime.now() - timedelta(minutes=i) for i in range(25)][::-1]
    np.random.seed(42)
    base_price = 79784.0
    
    open_p = base_price + np.random.randn(25) * 12
    close_p = open_p + np.random.randn(25) * 18
    high_p = np.maximum(open_p, close_p) + np.abs(np.random.randn(25) * 8)
    low_p = np.minimum(open_p, close_p) - np.abs(np.random.randn(25) * 8)

    fig = go.Figure(data=[go.Candlestick(
        x=dates, open=open_p, high=high_p, low=low_p, close=close_p,
        increasing_line_color='#00dc82', increasing_fillcolor='#00dc82',
        decreasing_line_color='#ef4444', decreasing_fillcolor='#ef4444'
    )])

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0e14", plot_bgcolor="#0b0e14",
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis_rangeslider_visible=False,
        height=230,
        yaxis=dict(gridcolor="#1e293b"), xaxis=dict(gridcolor="#1e293b")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<h4 style='margin-top:5px; font-size:14px;'>Promo Code Activation</h4>", unsafe_allow_html=True)
    promo_input = st.text_input("Promo Code", key="promo_code", label_visibility="collapsed", placeholder="Enter Promo Code")
    
    if st.button("Activate Code"):
        code_clean = promo_input.strip()
        if code_clean in VALID_PROMOS:
            if code_clean not in st.session_state.used_promos:
                st.session_state.balance += 11.0
                st.session_state.used_promos.add(code_clean)
                st.success(f"Code {code_clean} applied! +11 USDT")
            else:
                st.warning("This code is already used!")
        else:
            st.error("Invalid Promo Code!")

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.markdown('<div class="call-btn">', unsafe_allow_html=True)
        st.button("📈 CALL 52.56%")
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        st.markdown('<div class="put-btn">', unsafe_allow_html=True)
        st.button("📉 PUT 55.44%")
        st.markdown('</div>', unsafe_allow_html=True)

elif tab == "Assets":
    st.markdown("<h3 style='margin-bottom:15px;'>Assets Overview</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="green-card">
        <span style="opacity:0.9; font-size:13px; font-weight:500;">Total Assets</span>
        <h1 style="margin: 8px 0 6px 0; font-size:32px; font-weight:800;">
            {st.session_state.balance:.2f} <span style="font-size:18px; font-weight:500;">USDT</span>
        </h1>
        <small style="opacity:0.85; font-size:12px;">≈ ${st.session_state.balance:.2f} USD</small>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("Deposit")
    with c2: st.button("Withdraw")
    with c3: st.button("Swap")
    with c4: st.button("Transfer")

elif tab == "Mine":
    st.markdown("<h3 style='margin-bottom:15px;'>Profile & System</h3>", unsafe_allow_html=True)
    
    system_menu = ["Help Center", "News Center", "System Announcement", "About Us", "Online Service", "Version: 2.3.9"]
    for item in system_menu:
        st.markdown(f"""
        <div style="background-color:#111827; border-radius:12px; padding:16px; margin-bottom:12px; border:1px solid #1e293b; display:flex; justify-content:space-between;">
            <span style="font-size:14px;">{item}</span>
            <span style="color:#64748b;">›</span>
        </div>
        """, unsafe_allow_html=True)

# ----------------- CUSTOM BOTTOM NAVIGATION (NO COVERING) -----------------
st.markdown('<div class="nav-spacer"></div>', unsafe_allow_html=True)

nav_cols = st.columns(5)

items = [
    ("Home", "🏠"),
    ("Market", "📈"),
    ("Trade", "🔄"),
    ("Assets", "💼"),
    ("Mine", "👤")
]

for idx, (name, icon) in enumerate(items):
    with nav_cols[idx]:
        is_active = (st.session_state.active_tab == name)
        label = f"{'🟢' if is_active else icon}\n{name}"
        if st.button(label, key=f"nav_{name}"):
            st.session_state.active_tab = name
            st.rerun()
