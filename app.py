import streamlit as st
import pandas as pd
import numpy as np

# 1. გვერდის ძირითადი პარამეტრები
st.set_page_config(page_title="DIABLO", layout="wide", initial_sidebar_state="collapsed")

# 2. დიზაინი (HTML/CSS) - ზუსტი მუქი თემა, Radio მარკერების დამალვა
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e11;
        color: #ffffff;
    }
    header, footer, #MainMenu {visibility: hidden;}

    /* Radio ღილაკების წერტილების/მარკერების დამალვა */
    div[data-testid="stRadio"] > div {
        display: flex;
        justify-content: space-around;
        background-color: #181a20;
        padding: 8px;
        border-radius: 12px;
        border: 1px solid #2b2f36;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        padding: 6px 12px !important;
        cursor: pointer;
    }
    div[data-testid="stRadio"] label div[role="radio"] {
        display: none !important;
    }
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        color: #848e9c;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* ბარათების სტილი */
    .card-box {
        background-color: #181a20;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #2b2f36;
    }
    
    .purple-card {
        background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);
        border-radius: 14px;
        padding: 20px;
        color: white;
        margin-bottom: 15px;
    }

    /* ღილაკები */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 16px;
        background-color: #2b2f36;
        color: #ffffff;
    }
    
    /* CALL / PUT სავაჭრო ღილაკები */
    .call-btn button { background-color: #0ecb81 !important; color: white !important; }
    .put-btn button { background-color: #f6465d !important; color: white !important; }
    
    .green-text { color: #0ecb81; font-weight: bold; }
    .red-text { color: #f6465d; font-weight: bold; }
    .sub-text { color: #848e9c; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# 3. სესიის მდგომარეობა
if "balance" not in st.session_state:
    st.session_state.balance = 2226.72
if "used_promo" not in st.session_state:
    st.session_state.used_promo = False

# 4. ზედა ჰედერი
st.markdown("<h2 style='text-align: center; color: #a855f7;'>DIABLO</h2>", unsafe_allow_html=True)

# 5. ქვედა ნავიგაციის ჩანართები (მარკერების გარეშე)
tabs = ["მთავარი გვერდი", "ბაზრები", "ვაჭრობა", "სისტემა", "აქტივები"]
selected_tab = st.radio("", tabs, horizontal=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- 1. მთავარი გვერდი -----------------
if selected_tab == "მთავარი გვერდი":
    st.markdown("""
    <div class="card-box">
        <h3 style="margin:0;">სწრაფი ვაჭრობა</h3>
        <p class="sub-text">უსაფრთხო და მოსახერხებელი</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("გამოტანა")
    with c2: st.button("ჩარიცხვა")
    with c3: st.button("სწრაფი გაცვლა")
    with c4: st.button("უფრო მეტი")
        
    st.markdown("<h4 style='margin-top:20px;'>ზრდის რეიტინგი</h4>", unsafe_allow_html=True)
    
    market_data = [
        {"pair": "DASH / USDT", "price": "68.162", "change": "+4.07%"},
        {"pair": "DOT / USDT", "price": "0.946", "change": "+3.50%"},
        {"pair": "BCH / USDT", "price": "259.47", "change": "+1.34%"},
    ]
    
    for item in market_data:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**{item['pair']}**")
        col2.write(item['price'])
        col3.markdown(f"<span class='green-text'>{item['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:5px 0; border-color:#2b2f36;'>", unsafe_allow_html=True)

# ----------------- 2. ბაზრები -----------------
elif selected_tab == "ბაზრები":
    st.markdown("### დერივატივების კონტრაქტი")
    
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
        col2.write(f"**{p['price']}**")
        color_class = "green-text" if p["green"] else "red-text"
        col3.markdown(f"<span class='{color_class}'>{p['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:5px 0; border-color:#2b2f36;'>", unsafe_allow_html=True)

# ----------------- 3. ვაჭრობა -----------------
elif selected_tab == "ვაჭრობა":
    st.markdown("### BTC / USDT <span class='red-text'>-0.06%</span>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    cols[0].button("60s")
    cols[1].button("120s")
    cols[2].button("5min")
    cols[3].button("10min")
    
    st.markdown("**ბრძანების დასრულების დრო:** `25 s` | `12:38~12:39`")
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 1) + 79784.45,
        columns=['Price']
    )
    st.line_chart(chart_data)
    
    st.markdown("#### პრომო-კოდის გააქტიურება")
    promo_input = st.text_input("შეიყვანეთ პრომო-კოდი", key="promo_code")
    if st.button("დადასტურება"):
        if promo_input == "2045Q13TI" and not st.session_state.used_promo:
            st.session_state.balance += 11
            st.session_state.used_promo = True
            st.success("პრომო-კოდი გააქტიურდა! +11 USDT დაგერიცხათ.")
        elif st.session_state.used_promo:
            st.warning("ეს პრომო-კოდი უკვე გამოყენებულია!")
        else:
            st.error("არასწორი პრომო-კოდი!")

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.markdown('<div class="call-btn">', unsafe_allow_html=True)
        st.button("CALL 52.56%")
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        st.markdown('<div class="put-btn">', unsafe_allow_html=True)
        st.button("PUT 55.44%")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- 4. სისტემა -----------------
elif selected_tab == "სისტემა":
    st.markdown("### სისტემა")
    
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
            <span>{item}</span>
            <span style="color:#848e9c;">></span>
        </div>
        """, unsafe_allow_html=True)

# ----------------- 5. აქტივები -----------------
elif selected_tab == "აქტივები":
    st.markdown("### აქტივები")
    
    st.markdown(f"""
    <div class="purple-card">
        <span style="opacity:0.8; font-size:13px;">ანგარიშის მთლიანი აქტივები</span>
        <h1 style="margin: 8px 0;">{st.session_state.balance:.2f} USDT</h1>
        <small style="opacity:0.8;">დღის შემოსავალი: 0</small>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("ჩარიცხვა")
    with c2: st.button("გამოტანა")
    with c3: st.button("სწრაფი გაცვლა")
    with c4: st.button("გადარიცხვა")
    
    st.markdown("<h4 style='margin-top:20px;'>ჩემი ანგარიში</h4>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="card-box">
        <small class="sub-text">სპოტ ვალუტა</small>
        <h3 style="margin:4px 0 0 0;">0.00</h3>
    </div>
    <div class="card-box">
        <small class="sub-text">ვადიანი კონტრაქტები</small>
        <h3 style="margin:4px 0 0 0;">{st.session_state.balance:.2f}</h3>
    </div>
    <div class="card-box">
        <small class="sub-text">მუდმივი კონტრაქტები</small>
        <h3 style="margin:4px 0 0 0;">0.00</h3>
    </div>
    """, unsafe_allow_html=True)
