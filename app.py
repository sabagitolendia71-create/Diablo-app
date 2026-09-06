import streamlit as st

# გვერდის ძირითადი პარამეტრები
st.set_page_config(page_title="DIABLO", page_icon="💎", layout="centered")

# Session State ცვლადების ინიციალიზაცია
if 'total_assets' not in st.session_state:
    st.session_state.total_assets = 2226.72
if 'daily_income' not in st.session_state:
    st.session_state.daily_income = 0.0
if 'use_count' not in st.session_state:
    st.session_state.use_count = 0

# CSS სტილები
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #ffffff; }
    .logo-text { font-size: 28px; font-weight: bold; color: #ffffff; padding: 10px 0; }
    .hero-banner {
        background: linear-gradient(135deg, #051329 0%, #0a2246 50%, #000000 100%);
        border-radius: 12px; padding: 25px; text-align: center; margin-bottom: 15px;
        border: 1px solid #1e293b;
    }
    .banner-title { font-size: 32px; font-weight: 800; color: #3b82f6; }
    .trade-card { background-color: #1a1a1a; border-radius: 12px; padding: 15px; margin-bottom: 20px; }
    .balance-card {
        background: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);
        border-radius: 12px; padding: 20px; color: white; margin-bottom: 20px;
    }
    .badge-green { background-color: #00c087; color: white; padding: 6px 12px; border-radius: 6px; font-weight: bold; }
    .badge-red { background-color: #ff3b30; color: white; padding: 6px 12px; border-radius: 6px; font-weight: bold; }
    .empty-state { text-align: center; color: #666666; padding: 40px 0; }
    </style>
""", unsafe_allow_html=True)

# ზედა ნავიგაცია
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.markdown('<div class="logo-text">💎 DIABLO</div>', unsafe_allow_html=True)
with col_head2:
    st.write("💬 👤")

# ქვედა მენიუ
tab_home, tab_markets, tab_trade, tab_system, tab_assets = st.tabs([
    "მთავარი გვერდი", "ბაზრები", "ვაჭრობა", "სისტემა", "აქტივები"
])

# ----------------- 1. მთავარი გვერდი -----------------
with tab_home:
    st.markdown('<div class="hero-banner"><div class="banner-title">DIABLO</div></div>', unsafe_allow_html=True)
    st.caption("📢 sa****c2@gmail.com გილოცავთ პრიზის მოგებას...")
    st.markdown('<div class="trade-card"><h3 style="margin:0;">სწრაფი ვაჭრობა</h3><p style="color: #888;">უსაფრთხო და მოსახერხებელი</p></div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.button("🔄\nგამოტანა", key="h_out", use_container_width=True)
    c2.button("📥\nჩარიცხვა", key="h_in", use_container_width=True)
    c3.button("⚡\nსწრაფი გაცვლა", key="h_ex", use_container_width=True)
    c4.button("🔲\nუფრო მეტი", key="h_more", use_container_width=True)
    
    st.markdown("---")
    st.subheader("ზრდის რეიტინგი")
    st.markdown("""
    | სავაჭრო წყვილი | ბოლო ფასი | 24ს ფასის ცვლილება |
    | :--- | :--- | :--- |
    | **DASH** / USDT | 74.518 | <span class="badge-green">+13.77%</span> |
    | **FIL** / USDT | 0.8058 | <span class="badge-green">+2.28%</span> |
    | **BCH** / USDT | 261.62 | <span class="badge-green">+2.18%</span> |
    """, unsafe_allow_html=True)

# ----------------- 2. ბაზრები -----------------
with tab_markets:
    st.subheader("დერივატივების კონტრაქტი")
    markets_data = [
        ("BTC/USDT", "79784.47", "-0.06%", False),
        ("ETH/USDT", "2507.18", "+1.08%", True),
        ("ADA/USDT", "0.2213", "+1.24%", True),
        ("BCH/USDT", "261.62", "+2.18%", True),
        ("DASH/USDT", "74.534", "+13.79%", True),
    ]
    for pair, price, change, is_pos in markets_data:
        m1, m2, m3 = st.columns([2, 2, 1])
        m1.write(f"**{pair}**")
        m2.write(f"${price}")
        m3.markdown(f'<span class="{"badge-green" if is_pos else "badge-red"}">{change}</span>', unsafe_allow_html=True)
        st.divider()

# ----------------- 3. ვაჭრობა -----------------
with tab_trade:
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "კონტრაქტის ბრძანება", "ისტორიული ბრძანებები", "მომწივიეს მე", "მოსდევი გეგმა"
    ])
    
    with sub_tab1:
        st.subheader("BTC / USDT  -0.06%")
        t1, t2, t3, t4 = st.columns(4)
        t1.button("60s", type="primary", use_container_width=True)
        t2.button("120s", use_container_width=True)
        t3.button("5min", use_container_width=True)
        t4.button("10min", use_container_width=True)
        st.metric(label="უკუთვლა", value="50 s")
    
    with sub_tab2:
        st.info("ისტორია ცარიელია")

    # 3.1 "მომწივიეს მე" სექცია - კოდის შეყვანა
    with sub_tab3:
        b1, b2 = st.columns(2)
        b1.button("➕ დაწყება მოსდევი", key="m1", type="primary", use_container_width=True)
        b2.button("📑 მოსდევი ისტორია", key="m2", use_container_width=True)
        
        st.write("")
        promo_code = st.text_input("გთხოვთ შეიყვანოთ მოსდევი კოდი:", placeholder="მაგ: 2045Q13TI")
        
        if st.button("დადასტურება", type="primary"):
            if promo_code.strip() == "2045Q13TI":
                # პროცენტის გაანგარიშება: ყოველ გამოყენებაზე ემატება +5%
                bonus_percent = st.session_state.use_count * 0.05
                added_amount = round(11 * (1 + bonus_percent), 2)
                
                st.session_state.total_assets += added_amount
                st.session_state.daily_income += added_amount
                st.session_state.use_count += 1
                
                st.success(f"კოდი წარმატებით გააქტიურდა! დაგერიცხათ: ${added_amount} (ბონუს პროცენტი: {int(bonus_percent*100)}%)")
            else:
                st.error("არასწორი კოდი!")
        
        st.markdown('<div class="empty-state">🏢<br>მონაცემები არ არის</div>', unsafe_allow_html=True)

    # 3.2 "მოსდევი გეგმა" სექცია
    with sub_tab4:
        p1, p2 = st.columns(2)
        p1.button("➕ დაწყება მოსდევი", key="p1", type="primary", use_container_width=True)
        p2.button("📑 ისტორიის გამოქვეყნება", key="p2", use_container_width=True)
        st.markdown('<div class="empty-state">🏢<br>მონაცემები არ არის</div>', unsafe_allow_html=True)

    # CALL / PUT ღილაკები
    btn_call, btn_put = st.columns(2)
    btn_call.button("📈 CALL  53.73%", use_container_width=True)
    btn_put.button("📉 PUT  54.27%", use_container_width=True)

# ----------------- 4. სისტემა -----------------
with tab_system:
    st.subheader("სისტემა")
    menu = ["❓ დახმარების ცენტრი", "📰 სიახლეების ცენტრი", "📢 სისტემის განცხადება", "ℹ️ ჩვენს შესახებ", "💬 ონლაინ სერვისი", "🌐 ენა", "☁️ APP გადმოწერა"]
    for item in menu:
        st.button(item, use_container_width=True)
    st.caption("ვერსიის ნომერი: 2.3.9")

# ----------------- 5. აქტივები -----------------
with tab_assets:
    st.markdown(f"""
        <div class="balance-card">
            <small>ანგარიშის მთლიანი აქტივები 👁️</small>
            <h1 style="margin: 5px 0;">{st.session_state.total_assets:.2f}</h1>
            <small>დღის შემოსავალი: {st.session_state.daily_income:.2f} 🔄</small>
        </div>
    """, unsafe_allow_html=True)
    
    a1, a2, a3, a4 = st.columns(4)
    a1.button("📥\nჩარიცხვა", key="a_in", use_container_width=True)
    a2.button("🔄\nგამოტანა", key="a_out", use_container_width=True)
    a3.button("⚡\nსწრაფი გაცვლა", key="a_ex", use_container_width=True)
    a4.button("📲\nგადარიცხვა", key="a_tr", use_container_width=True)
    
    st.markdown("---")
    st.write("**ჩემი ანგარიში**")
    st.info("სპოტ ვალუტა: **0.00**")
    st.success(f"ვადიანი კონტრაქტები: **{st.session_state.total_assets:.2f}**")
    st.info("მუდმივი კონტრაქტები: **0.00**")
