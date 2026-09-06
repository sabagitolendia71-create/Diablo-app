import streamlit as st
import pandas as pd
import numpy as np

# გვერდის კონფიგურაცია DIABLO-ს სახელით
st.set_page_config(page_title="DIABLO", layout="wide", initial_sidebar_state="collapsed")

# სტილები - ზუსტი მუქი დიზაინი და იისფერი აქცენტები
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e11;
        color: #ffffff;
    }
    header, footer, #MainMenu {visibility: hidden;}
    
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

    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 16px;
    }
    
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button {
        background-color: #0ecb81 !important;
        color: white !important;
    }
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button {
        background-color: #f6465d !important;
        color: white !important;
    }
    
    .green-text { color: #0ecb81; font-weight: bold; }
    .red-text { color: #f6465d; font-weight: bold; }
    .sub-text { color: #848e9c; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# სესიის მონაცემები
if "balance" not in st.session_state:
    st.session_state.balance = 2226.72
if "used_promo" not in st.session_state:
    st.session_state.used_promo = False
if "tab" not in st.session_state:
    st.session_state.tab = "მთავარი გვერდი"

st.title("DIABLO")

# ქვედა ნავიგაცია (5 სექცია)
tabs = ["მთავარი გვერდი", "ბაზრები", "ვაჭრობა", "სისტემა", "აქტივები"]
selected_tab = st.radio("", tabs, index=tabs.index(st.session_state.tab), horizontal=True)
st.session_state.tab = selected_tab

st.markdown("---")

# 1. მთავარი გვერდი
if st.session_state.tab == "მთავარი გვერდი":
    st.markdown("""
    <div class="card-box">
        <h2 style="margin:0;">სწრაფი ვაჭრობა</h2>
        <p class="sub-text">უსაფრთხო და მოსახერხებელი</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.button("🔄 გამოტანა")
    with col2: st.button("📥 ჩარიცხვა")
    with col3: st.button("⚡ სწრაფი გაცვლა")
    with col4: st.button("📱 უფრო მეტი")
        
    st.markdown("### ზრდის რეიტინგი")
    
    market_data = [
        {"pair": "DASH / USDT", "price": "68.162", "change": "+4.07%"},
        {"pair": "DOT / USDT", "price": "0.946", "change": "+3.50%"},
        {"pair": "BCH / USDT", "price": "259.47", "change": "+1.34%"},
    ]
    
    for item in market_data:
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.write(f"**{item['pair']}**")
        c2.write(item['price'])
        c3.markdown(f"<span class='green-text'>{item['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:5px 0; border-color:#2b2f36;'>", unsafe_allow_html=True)

# 2. ბაზრები
elif st.session_state.tab == "ბაზრები":
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
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.markdown(f"**{p['pair']}**<br><span class='sub-text'>{p['vol']}</span>", unsafe_allow_html=True)
        c2.write(f"**{p['price']}**")
        color_class = "green-text" if p["green"] else "red-text"
        c3.markdown(f"<span class='{color_class}'>{p['change']}</span>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:5px 0; border-color:#2b2f36;'>", unsafe_allow_html=True)

# 3. ვაჭრობა
elif st.session_state.tab == "ვაჭრობა":
    st.markdown("### BTC / USDT `-0.06%`")
    
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
        st.button("📈 CALL  52.56%")
    with btn_col2:
        st.button("📉 PUT  55.44%")

# 4. სისტემა
elif st.session_state.tab == "სისტემა":
    st.markdown("### სისტემა")
    
    system_menu = [
        "❓ დახმარების ცენტრი",
        "📰 სიახლეების ცენტრი",
        "📢 სისტემის განცხადება",
        "ℹ️ ჩვენს შესახებ",
        "💬 ონლაინ სერვისი",
        "🌐 ენა",
        "☁️ APP გადამოწერა",
        "🔢 ვერსიის ნომერი: 2.3.9"
    ]
    
    for item in system_menu:
        st.markdown(f"""
        <div class="card-box" style="display:flex; justify-content:space-between;">
            <span>{item}</span>
            <span>></span>
        </div>
        """, unsafe_allow_html=True)

# 5. აქტივები
elif st.session_state.tab == "აქტივები":
    st.markdown("### აქტივები")
    
    st.markdown(f"""
    <div class="purple-card">
        <span style="opacity:0.8;">ანგარიშის მთლიანი აქტივები 👁️</span>
        <h1 style="margin: 5px 0;">{st.session_state.balance:.2f} USDT</h1>
        <small>დღის შემოსავალი: 0 🔄</small>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.button("📥 ჩარიცხვა")
    c2.button("🔄 გამოტანა")
    c3.button("⚡ სწრაფი გაცვლა")
    c4.button("➡️ გადარიცხვა")
    
    st.markdown("#### ჩემი ანგარიში")
    
    st.markdown(f"""
    <div class="card-box">
        <small class="sub-text">სპოტ ვალუტა</small>
        <h3 style="margin:0;">0.00</h3>
    </div>
    <div class="card-box">
        <small class="sub-text">ვადიანი კონტრაქტები</small>
        <h3 style="margin:0;">{st.session_state.balance:.2f}</h3>
    </div>
    <div class="card-box">
        <small class="sub-text">მუდმივი კონტრაქტები</small>
        <h3 style="margin:0;">0.00</h3>
    </div>
    """, unsafe_allow_html=True)
