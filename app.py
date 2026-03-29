import streamlit as st
import base64
import os

# Sayfa Yapılandırması
st.set_page_config(page_title="🍽️ Şefin Mutfağı | Akıllı Yemek Önerici", layout="centered")

# -----------------------------
# GÖRSEL TASARIM (CSS)
# -----------------------------
def set_bg():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
        url("https://images.unsplash.com/photo-1556910103-1c02745aae4d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
    }}
    .block-container {{
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(15px);
        padding: 3rem;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-top: 2rem;
    }}
    h1, h2, h3, p, span, label, div {{ color: white !important; }}
    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
        height: 3rem;
    }}
    .recipe-card {{
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()

# -----------------------------
# 1. VERİ SETİ
# -----------------------------
RECIPE_DATABASE = {
    "Çılbır": {
        "desc": "Sarımsaklı süzme yoğurt yatağında poşe yumurta ve kızgın tereyağlı biber sosu.",
        "time": "15 dk", "cal": "280 kcal",
        "ing": ["2 adet yumurta", "200g süzme yoğurt", "1 diş sarımsak", "20g tereyağı", "1 yk sirke"],
        "steps": ["Yoğurdu sarımsakla çırpın.", "Sirkeli suda yumurtaları poşeleyin.", "Üzerine kızgın pul biberli yağ dökün."],
        "tips": "Yumurtalar oda sıcaklığında olmalı."
    },
    "Mantarlı Kremalı Tavuk": {
        "desc": "Yoğun krema ve mantarla sotelenmiş tavuk.",
        "time": "25 dk", "cal": "450 kcal",
        "ing": ["400g tavuk", "200g mantar", "200ml krema"],
        "steps": ["Tavukları mühürle.", "Mantar ekle.", "Krema ile pişir."],
        "tips": "Kremayı fazla kaynatma."
    }
}

# --- TÜM EKLEMELER ---
# (senin attığın tüm bloklar eklendi)
RECIPE_DATABASE.update(TRADITIONAL_VEGGIE)  # :contentReference[oaicite:0]{index=0}
RECIPE_DATABASE.update(STREET_FIT_PROTEIN) # :contentReference[oaicite:1]{index=1}
RECIPE_DATABASE.update(EXOTIC_HOME_DESSERT) # :contentReference[oaicite:2]{index=2}
RECIPE_DATABASE.update(FINAL_PACK) # :contentReference[oaicite:3]{index=3}

# -----------------------------
# 2. YEMEK HAVUZU
# -----------------------------
meals = [
    {"name":"Çılbır","cat":"Kahvaltı","time":"<15 dk","tags":["Sağlıklı","Pratik"]},
    {"name":"Mantarlı Kremalı Tavuk","cat":"Akşam","time":"15-30 dk","tags":["Tavuk","Doyurucu"]},
]

# --- TÜM EKLEMELER ---
meals.extend(TRADITIONAL_MEALS)
meals.extend(STREET_FIT_MEALS)
meals.extend(EXOTIC_MEALS)
meals.extend(FINAL_MEALS)

# -----------------------------
# STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

questions = [
    ("Hangi öğün için hazırlık yapıyoruz?", "radio", ["Kahvaltı", "Öğle", "Akşam"]),
    ("Mutfakta ne kadar zamanın var?", "radio", ["<15 dk", "15-30 dk", "30+ dk"]),
    ("Beslenme tercihin nedir?", "multi", ["Et ağırlıklı","Tavuk","Sebze ağırlıklı","Vegan","Düşük kalorili"]),
    ("Nasıl bir tabak hayal ediyorsun?", "multi", ["Hafif","Doyurucu","Sağlıklı","Kaçamak"]),
    ("Uğraş seviyesi ne olsun?", "radio", ["Pratik","Orta","Detaylı"])
]

# -----------------------------
# UI
# -----------------------------
st.title("👨‍🍳 Şefin Akıllı Mutfağı")

if st.session_state.step < len(questions):
    q, typ, opts = questions[st.session_state.step]
    st.subheader(q)
    
    choice = st.radio("", opts) if typ=="radio" else st.multiselect("", opts)

    if st.button("Sonraki Adım"):
        if choice:
            st.session_state.answers[q] = choice
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Lütfen bir seçim yapın!")

else:
    ans = st.session_state.answers

    def calculate_score(m):
        score = 0
        if m["cat"] == ans["Hangi öğün için hazırlık yapıyoruz?"]: score += 10
        if m["time"] == ans["Mutfakta ne kadar zamanın var?"]: score += 5
        for user_tag in ans["Beslenme tercihin nedir?"] + ans["Nasıl bir tabak hayal ediyorsun?"]:
            if user_tag in m["tags"]: score += 3
        return score

    recommended_list = sorted(meals, key=calculate_score, reverse=True)

    if recommended_list:
        best_meal = recommended_list[0]
        recipe_data = RECIPE_DATABASE.get(best_meal["name"])

        if recipe_data:
            st.balloons()
            st.markdown(f"## 🎯 Bugünün Önerisi: **{best_meal['name']}**")

            col1, col2, col3 = st.columns(3)
            col1.metric("Süre", recipe_data['time'])
            col2.metric("Kalori", recipe_data['cal'])
            col3.info(f"Kategori: {best_meal['cat']}")

            st.write(f"_{recipe_data['desc']}_")

            st.divider()

            tab1, tab2, tab3 = st.tabs(["🛒 Malzemeler", "👨‍🍳 Hazırlanışı", "💡 Şefin İpucu"])

            with tab1:
                for item in recipe_data["ing"]:
                    st.write(f"✅ {item}")

            with tab2:
                for i, step in enumerate(recipe_data["steps"], 1):
                    st.write(f"{i}. {step}")

            with tab3:
                st.warning(recipe_data["tips"])

    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
