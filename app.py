import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# გვერდის პარამეტრები
st.set_page_config(page_title="DIABLO", layout="wide", initial_sidebar_state="collapsed")

# ----------------- ზუსტი მობილური CSS სტილები -----------------
st.markdown("""
<style>
    /* მთლიანი ფონი */
    .stApp {
        background-color: #0b0e11 !important;
        color: #ffffff !important;
    }
    header, footer, #MainMenu { visibility: hidden !important; }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 5.5rem !important;
        max-width: 500px !important;
        margin: 0 auto !important;
    }

    /* Top Bar - DIABLO */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0 15px 0;
        border-bottom: 1px solid #1e2329;
        margin-bottom: 15px;
    }
    .diablo-logo {
        color: #a855f7;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1.5px;
        font-family: 'Arial Black', sans-serif;
    }
    .top-icons {
        color: #848e9c;
        font-size: 18px;
        display: flex;
        gap: 15px;
    }

    /* ბარათების სტილი */
    .card-box {
        background-color: #181a20;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #2b2f36;
    }
    
    /* თანხის დახატული ბარათი */
    .purple-card {
        background: linear-gradient(135deg, #7e22ce 0%, #581c87 100%);
        border-radius: 16px;
        padding: 22px;
        color: white;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(126, 34, 206, 0.3);
        position: relative;
        overflow: hidden;
    }
    .crypto-bg-icon {
        position: absolute;
        right: -10px;
        bottom: -15px;
        font-size: 90px;
        opacity: 0.15;
    }

    /* Bottom Navigation - წერტილების/მოსანიშნების გარეშე */
    div[data-testid="stRadio"] > label { display: none !important; }
    div[data-testid="stRadio"] > div {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background-color: #181a20 !important;
        border-top: 1px solid #2b2f36 !important;
        z-index: 999999 !important;
        display: flex !important;
        justify-content: space-around !important;
        padding: 12px 0 16px 0 !important;
        margin: 0 auto !important;
        max-width: 500px !important;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stRadio"] label div[role="radio"] {
        display: none !important;
    }
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        color: #848e9c !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-align: center !important;
        margin: 0 !important;
    }
    div[data-testid="stRadio"] label[aria-checked="true"] div[data-testid="stMarkdownContainer"] p {
        color: #a855f7 !important;
        font-weight: 800 !important;
    }

    /* ღილაკები */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px;
        background-color: #2b2f36;
        color: #ffffff;
        font-size: 13px;
    }
    
    /* CALL / PUT ღილაკები */
    .call-btn button {
        background-color: #0ecb81 !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    .put-btn button {
        background-color: #f6465d !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    
    /* ფერები */
    .green-text { color: #0ecb81; font-weight: bold; }
    .red-text { color: #f6465d; font-weight: bold; }
    .sub-text { color: #848e9c; font-size: 12px; }
    .green-bg-tag {
        background-color: rgba(14, 203, 129, 0.15);
        color: #0ecb81;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- სესიის მონაცემები -----------------
if "balance" not in st.session_state:
    st.session_state.balance = 2226.72
if "used_promos" not in st.session_state:
    st.session_state.used_promos = set()

# ვალიდური პრომო-კოდების სია
VALID_PROMOS = ["2045Q13TI", "203V0FL1E", "201JFEKBI", "201CMTUUA"]

# ----------------- ტოპ ბარი -----------------
st.markdown("""
<div class="top-header">
    <div class="diablo-logo">DIABLO</div>
    <div class="top-icons">
        <span>💬</span>
        <span>👤</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- ქვედა ნავიგაცია -----------------
tabs = ["მთავარი გვერდი", "ბაზრები", "ვაჭრობა", "სისტემა", "აქტივები"]
selected_tab = st.radio("", tabs, horizontal=True)

# ----------------- 1. მთავარი გვერდი -----------------
if selected_tab == "მთავარი გვერდი":
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e1b4b 0%, #311042 100%); border-radius: 12px; padding: 18px; margin-bottom: 15px; border: 1px solid #3b0764;">
        <h2 style="color: #c084fc; margin:0; font-size: 20px;">DIABLO COIN</h2>
        <p style="color: #94a3b8; margin: 4px 0 0 0; font-size: 12px;">უსაფრთხო და სწრაფი კრიპტო ვაჭრობა</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-box" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h3 style="margin:0; font-size: 15px;">სწრაფი ვაჭრობა</h3>
            <p class="sub-text" style="margin:2px 0 0 0;">უსაფრთხო და მოსახერხებელი</p>
        </div>
        <div style="font-size: 24px;">🪙</div>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("გამოტანა")
    with c2: st.button("ჩარიცხვა")
    with c3: st.button("სწრაფი გაცვლა")
    with c4: st.button("უფრო მეტი")
        
    st.markdown("""
    <div style="display:flex; gap:15px; margin-top:20px; border-bottom: 1px solid #2b2f36; padding-bottom:8px;">
        <span style="color:#ffffff; font-weight:bold; font-size:13px; border-bottom: 2px solid #a855f7; padding-bottom:6px;">ზრდის რეიტინგი</span>
        <span style="color:#848e9c; font-size:13px;">ფასის კლება</span>
        <span style="color:#848e9c; font-size:13px;">24ს სავაჭრო ღირებულება</span>
    </div>
    """, unsafe_allow_html=True)
    
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
        st.markdown("<hr style='margin:8px 0; border-color:#1e2329;'>", unsafe_allow_html=True)

# ----------------- 2. ბაზრები -----------------
elif selected_tab == "ბაზრები":
    st.markdown("<h4 style='margin-bottom:15px; font-size:16px;'>დერივატივების კონტრაქტი</h4>", unsafe_allow_html=True)
    
    pairs = [
        {"pair": "BTC/USDT", "vol": "VOL: 254144090.43", "price": "79784.12", "change": "-0.06%", "green": False},
        {"pair": "ETH/USDT", "vol": "VOL: 217937486.54", "price": "2493.48", "change": "+0.52%", "green": True},
        {"pair": "ADA/USDT", "vol": "VOL: 7575818.91", "price": "0.2183", "change": "-0.14%", "green": False},
        {"pair": "BCH/USDT", "vol": "VOL: 3053870.7", "price": "259.43", "change": "+1.33%", "green": True},
        {"pair": "DASH/USDT", "vol": "VOL: 41411014.51", "price": "68.119", "change": "+4.00%", "green": True},
        {"pair": "DOGE/USDT", "vol": "VOL: 37503078.67", "price": "0.09067", "change": "+1.13%", "green": True},
        {"pair": "DOT/USDT", "vol": "VOL: 1715520.28", "price": "0.956", "change": "+4.60%", "green": True},
        {"pair": "FIL/USDT", "vol": "VOL: 5219958", "price": "0.7988", "change": "+1.40%", "green": True},
        {"pair": "LINK/USDT", "vol": "VOL: 9726291.9", "price": "12.192", "change": "+1.20%", "green": True},
        {"pair": "LTC/USDT", "vol": "VOL: 7164582.25", "price": "54.155", "change": "-0.97%", "green": False},
    ]
    
    for p in pairs:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.markdown(f"**{p['pair']}**<br><span class='sub-text'>{p['vol']}</span>", unsafe_allow_html=True)
        col2.markdown(f"**{p['price']}**")
        color_class = "green-text" if p["green"] else "red-text"
        col3.markdown(f"<span class='{color_class}'>{p['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:6px 0; border-color:#1e2329;'>", unsafe_allow_html=True)

# ----------------- 3. ვაჭრობა -----------------
elif selected_tab == "ვაჭრობა":
    st.markdown("<h3 style='margin:0;'>BTC / USDT <span class='red-text' style='font-size:16px;'>-0.06%</span></h3>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    cols[0].button("60s")
    cols[1].button("120s")
    cols[2].button("5min")
    cols[3].button("10min")
    
    st.markdown("""
    <div style="font-size:12px; color:#848e9c; margin: 10px 0;">
        ბრძანების დასრულების დრო: <span style="border:1px solid #0ecb81; color:#0ecb81; padding:1px 6px; border-radius:4px;">25 s</span> | <span style="border:1px solid #0ecb81; color:#0ecb81; padding:1px 6px; border-radius:4px;">12:38~12:39</span>
    </div>
    """, unsafe_allow_html=True)
    
    # იაპონური სანთლების გრაფიკი
    dates = [datetime.now() - timedelta(minutes=i) for i in range(25)][::-1]
    np.random.seed(42)
    base_price = 79784.0
    
    open_p = base_price + np.random.randn(25) * 12
    close_p = open_p + np.random.randn(25) * 18
    high_p = np.maximum(open_p, close_p) + np.abs(np.random.randn(25) * 8)
    low_p = np.minimum(open_p, close_p) - np.abs(np.random.randn(25) * 8)

    fig = go.Figure(data=[go.Candlestick(
        x=dates, open=open_p, high=high_p, low=low_p, close=close_p,
        increasing_line_color='#0ecb81', increasing_fillcolor='#0ecb81',
        decreasing_line_color='#f6465d', decreasing_fillcolor='#f6465d'
    )])

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b0e11", plot_bgcolor="#0b0e11",
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis_rangeslider_visible=False,
        height=290,
        yaxis=dict(gridcolor="#1e2329"), xaxis=dict(gridcolor="#1e2329")
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("<h4 style='margin-top:10px; font-size:14px;'>პრომო-კოდის გააქტიურება</h4>", unsafe_allow_html=True)
    promo_input = st.text_input("პრომო-კოდი", key="promo_code", label_visibility="collapsed", placeholder="შეიყვანეთ პრომო-კოდი")
    
    if st.button("დადასტურება"):
        code_clean = promo_input.strip()
        if code_clean in VALID_PROMOS:
            if code_clean not in st.session_state.used_promos:
                st.session_state.balance += 11.0
                st.session_state.used_promos.add(code_clean)
                st.success(f"პრომო-კოდი {code_clean} წარმატებით გააქტიურდა! +11 USDT")
            else:
                st.warning("ეს პრომო-კოდი უკვე გამოყენებულია!")
        else:
            st.error("არასწორი პრომო-კოდი!")

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.markdown('<div class="call-btn">', unsafe_allow_html=True)
        st.button("📈 CALL  52.56%")
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        st.markdown('<div class="put-btn">', unsafe_allow_html=True)
        st.button("📉 PUT  55.44%")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- 4. სისტემა -----------------
elif selected_tab == "სისტემა":
    st.markdown("<h3 style='margin-bottom:15px;'>სისტემა</h3>", unsafe_allow_html=True)
    
    system_menu = [
        "დახმარების ცენტრი",
        "სიახლეების ცენტრი",
        "სისტემის განცხადება",
        "ჩვენს შესახებ",
        "ონლაინ სერვისი",
        "ენა",
        "APP გადამოწერა",
        "ვერსიის ნომერი: 2.3.9"
    ]
    
    for item in system_menu:
        st.markdown(f"""
        <div class="card-box" style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:14px;">{item}</span>
            <span style="color:#848e9c; font-size:16px;">›</span>
        </div>
        """, unsafe_allow_html=True)

# ----------------- 5. აქტივები (დახატული თანხის ბარათი) -----------------
elif selected_tab == "აქტივები":
    st.markdown("<h3 style='margin-bottom:15px;'>აქტივები</h3>", unsafe_allow_html=True)
    
    # ლამაზი დახატული ბალანსის ბარათი კრიპტო იკონით
    st.markdown(f"""
    <div class="purple-card">
        <div class="crypto-bg-icon">💲</div>
        <span style="opacity:0.9; font-size:13px; font-weight:500;">ანგარიშის მთლიანი აქტივები 👁️</span>
        <h1 style="margin: 10px 0 6px 0; font-size:32px; font-weight:800; letter-spacing:0.5px;">
            {st.session_state.balance:.2f} <span style="font-size:18px; font-weight:500;">USDT</span>
        </h1>
        <small style="opacity:0.85; font-size:12px;">≈ ${st.session_state.balance:.2f} USD &nbsp;|&nbsp; დღის შემოსავალი: 0.00 🔄</small>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("ჩარიცხვა")
    with c2: st.button("გამოტანა")
    with c3: st.button("გაცვლა")
    with c4: st.button("გადარიცხვა")
    
    st.markdown("<h4 style='margin-top:20px; font-size:15px;'>ჩემი ანგარიში</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card-box">
        <small class="sub-text">სპოტ ვალუტა</small>
        <h3 style="margin:4px 0 0 0; font-size:18px;">0.00 USDT</h3>
    </div>
    <div class="card-box">
        <small class="sub-text">ვადიანი კონტრაქტები</small>
        <h3 style="margin:4px 0 0 0; font-size:18px; color:#a855f7;">{st.session_state.balance:.2f} USDT</h3>
    </div>
    <div class="card-box">
        <small class="sub-text">მუდმივი კონტრაქტები</small>
        <h3 style="margin:4px 0 0 0; font-size:18px;">0.00 USDT</h3>
    </div>
    """, unsafe_allow_html=True)
