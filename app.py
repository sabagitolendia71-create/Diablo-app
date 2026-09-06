import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="DIABLO", layout="wide", initial_sidebar_state="collapsed")

# ----------------- Lovable UI CSS (ზუსტი მობილური ტაბები წერტილების გარეშე) -----------------
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14 !important;
        color: #ffffff !important;
    }
    header, footer, #MainMenu { visibility: hidden !important; }
    
    /* Streamlit-ის ქვედა ზოლისგან (Manage app) აცილება */
    div[data-testid="stStatusWidget"], .viewerBadge_container__163eb { display: none !important; }

    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 480px !important;
        margin: 0 auto !important;
    }

    /* Top Bar Header */
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
    .header-right-icons {
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    /* Banner */
    .hero-banner {
        background: linear-gradient(180deg, #111827 0%, #0b0e14 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px 20px;
        margin-bottom: 15px;
    }
    .hero-sub {
        color: #00dc82;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 6px;
    }
    .hero-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
    }

    /* Quick Grid Cards */
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
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .quick-label {
        color: #e2e8f0;
        font-size: 12px;
        margin-top: 6px;
    }

    /* ----------------- STREAMLIT RADIO-ს სრული გარდაქმნა ნამდვილ TAB BAR-ად ----------------- */
    div[data-testid="stRadio"] > label { 
        display: none !important; 
    }
    
    div[data-testid="stRadio"] > div {
        position: fixed !important;
        bottom: 0px !important;
        left: 0 !important;
        right: 0 !important;
        background-color: #090d16 !important;
        border-top: 1px solid #1e293b !important;
        z-index: 999999 !important;
        display: flex !important;
        justify-content: space-around !important;
        padding: 8px 0 14px 0 !important;
        margin: 0 auto !important;
        max-width: 480px !important;
    }
    
    /* წერტილების სრული წაშლა */
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
        cursor: pointer !important;
    }
    
    div[data-testid="stRadio"] label div[role="radio"], 
    div[data-testid="stRadio"] label input {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
    }

    /* ტექსტისა და იკონების სტილი */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        color: #64748b !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-align: center !important;
        margin: 0 !important;
    }

    /* აქტიური ტაბის ფერი (მწვანე) */
    div[data-testid="stRadio"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
        color: #00dc82 !important;
        font-weight: 700 !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 10px;
        background-color: #1e293b;
        color: #ffffff;
    }
    
    .call-btn button { background-color: #00dc82 !important; color: #0b0e14 !important; font-weight: bold !important; }
    .put-btn button { background-color: #ef4444 !important; color: white !important; font-weight: bold !important; }
    .green-bg-tag { background-color: rgba(0, 220, 130, 0.15); color: #00dc82; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ----------------- Session State -----------------
if "balance" not in st.session_state:
    st.session_state.balance = 2226.72
if "used_promos" not in st.session_state:
    st.session_state.used_promos = set()

VALID_PROMOS = ["2045Q13TI", "203V0FL1E", "201JFEKBI", "201CMTUUA"]

# Header
st.markdown("""
<div class="top-header">
    <div class="brand-box">
        <div class="logo-d">D</div>
        <div class="diablo-title">DIABLO</div>
    </div>
    <div class="header-right-icons">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2"><path d="M5 8l6 6M4 14l6-6 2 2M2 5h12M9 2v3M15 11l6 9M21 11l-6 9"/></svg>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- Bottom Navigation Bar (HTML ტექსტით და იკონებით) -----------------
tabs = [
    "Home",
    "Market",
    "Trade",
    "Assets",
    "Mine"
]
selected_tab = st.radio("", tabs, horizontal=True)

# ----------------- PAGES -----------------
if selected_tab == "Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-sub">TRADE SMARTER</div>
        <div class="hero-title">The future starts here</div>
    </div>
    
    <div class="quick-grid">
        <div class="quick-card">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg>
            <div class="quick-label">Deposit</div>
        </div>
        <div class="quick-card">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
            <div class="quick-label">Markets</div>
        </div>
        <div class="quick-card">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            <div class="quick-label">News</div>
        </div>
        <div class="quick-card">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#00dc82" stroke-width="2"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>
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

elif selected_tab == "Market":
    st.markdown("<h4>Market Data</h4>", unsafe_allow_html=True)
    st.write("BTC/USDT - 79,784.12")
    st.write("ETH/USDT - 2,493.48")

elif selected_tab == "Trade":
    st.markdown("<h3>BTC / USDT</h3>", unsafe_allow_html=True)
    promo_input = st.text_input("Promo Code", key="promo_code", placeholder="Enter Code")
    if st.button("Apply Code"):
        code = promo_input.strip()
        if code in VALID_PROMOS and code not in st.session_state.used_promos:
            st.session_state.balance += 11.0
            st.session_state.used_promos.add(code)
            st.success("Added +11 USDT!")
        else:
            st.error("Invalid or already used code!")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="call-btn">', unsafe_allow_html=True)
        st.button("CALL")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="put-btn">', unsafe_allow_html=True)
        st.button("PUT")
        st.markdown('</div>', unsafe_allow_html=True)

elif selected_tab == "Assets":
    st.markdown("<h3>Assets</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2>{st.session_state.balance:.2f} USDT</h2>", unsafe_allow_html=True)

elif selected_tab == "Mine":
    st.markdown("<h3>Profile & Settings</h3>", unsafe_allow_html=True)
