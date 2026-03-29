import streamlit as st
import base64

st.set_page_config(page_title="Yemek Öneri Sistemi", page_icon="🍽️", layout="centered")

# -----------------------------
# BACKGROUND EKLEME
# -----------------------------
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    .block-container {{
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 15px;
    }}

    h2, h3, h4, p, div {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg("bg.png")

# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------
# SORULAR
# -----------------------------
questions = [
    ("Hangi öğün?", ["Kahvaltı", "Öğle", "Akşam", "Atıştırmalık"]),
    ("Ne kadar zamanın var?", ["<15 dk", "15-30 dk", "30-60 dk", "60+ dk"]),
    ("Bütçen?", ["Düşük", "Orta", "Yüksek"]),
    ("Beslenme tercihin?", ["Et", "Tavuk", "Sebze", "Vegan"]),
    ("Diyet durumun?", ["Yok", "Kalori kontrolü", "Protein", "Düşük karbonhidrat"]),
    ("Nasıl bir yemek?", ["Hafif", "Doyurucu", "Sağlıklı", "Kaçamak"]),
    ("Ruh halin?", ["Yorgun", "Stresli", "Mutlu", "Enerjik"]),
    ("Deneyim?", ["Hızlı", "Konfor", "Yeni", "Klasik"]),
    ("Evde ne var?", ["Tavuk", "Et", "Sebze", "Makarna/Pilav", "Yok"]),
    ("Karbonhidrat?", ["Pilav/Makarna", "Ekmek", "Olmasın", "Fark etmez"]),
    ("Tat tercihi?", ["Acılı", "Tatlı", "Tuzlu", "Dengeli"]),
    ("Uğraş seviyesi?", ["Pratik", "Orta", "Detaylı"])
]

# -----------------------------
# YEMEK VERİ TABANI
# -----------------------------
meals = [
    {"name": "Tavuk Sote", "type": "Tavuk", "time": "15-30 dk", "cal": 400, "tags": ["Hafif", "Protein"]},
    {"name": "Izgara Tavuk Salata", "type": "Tavuk", "time": "<15 dk", "cal": 300, "tags": ["Hafif", "Kalori kontrolü"]},
    {"name": "Tavuklu Makarna", "type": "Tavuk", "time": "15-30 dk", "cal": 550, "tags": ["Doyurucu"]},
    {"name": "Sebze Sote", "type": "Sebze", "time": "15-30 dk", "cal": 250, "tags": ["Vegan", "Hafif"]},
    {"name": "Kıymalı Makarna", "type": "Et", "time": "30-60 dk", "cal": 650, "tags": ["Doyurucu"]}
]

# -----------------------------
# UI
# -----------------------------
st.markdown("<h2 style='text-align:center;'>🍽️ Yemek Öneri Sistemi</h2>", unsafe_allow_html=True)

if st.session_state.step < len(questions):
    q, options = questions[st.session_state.step]

    st.markdown(f"<h4 style='text-align:center;'>{q}</h4>", unsafe_allow_html=True)

    choice = st.radio("", options, key=st.session_state.step)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Devam"):
            st.session_state.answers[q] = choice
            st.session_state.step += 1
            st.rerun()

else:
    st.markdown("<h3 style='text-align:center;'>🍽️ Senin için en uygun yemekler</h3>", unsafe_allow_html=True)

    def score(meal, answers):
        s = 0

        if meal["type"] == answers["Beslenme tercihin?"]:
            s += 3

        if meal["time"] == answers["Ne kadar zamanın var?"]:
            s += 2

        if "Hafif" in meal["tags"] and answers["Nasıl bir yemek?"] == "Hafif":
            s += 2

        if "Doyurucu" in meal["tags"] and answers["Nasıl bir yemek?"] == "Doyurucu":
            s += 2

        if "Kalori kontrolü" in meal["tags"] and answers["Diyet durumun?"] == "Kalori kontrolü":
            s += 2

        return s

    scored = [(meal, score(meal, st.session_state.answers)) for meal in meals]
    scored.sort(key=lambda x: x[1], reverse=True)

    main = scored[0][0]
    alt1 = scored[1][0]
    alt2 = scored[2][0]

    def show_meal(title, meal):
        st.subheader(title + ": " + meal["name"])
        st.write(f"Süre: {meal['time']}")
        st.write(f"Kalori: {meal['cal']} kcal")

    show_meal("🎯 Ana Yemek", main)
    show_meal("🔁 Alternatif", alt1)
    show_meal("🔁 Alternatif", alt2)

    if st.button("Tarif göster"):
        st.markdown("### 📖 Tarif")
        st.write("""
        1. Tavukları doğra  
        2. Tavada yağ ile pişir  
        3. Sebzeleri ekle  
        4. Baharat ekle  
        5. 15 dakika pişir  
        """)
