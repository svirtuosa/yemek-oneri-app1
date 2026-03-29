import streamlit as st
import base64
import os

st.set_page_config(page_title="🍽️ Yemek Önerici", layout="centered")

# -----------------------------
# BACKGROUND (HATA DAYANIKLI)
# -----------------------------
def set_bg():
    file_path = "bg.PNG"

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
        }}

        .block-container {{
            background: rgba(0,0,0,0.6);
            padding: 2rem;
            border-radius: 15px;
            max-width: 600px;
            margin: auto;
        }}

        h1, h2, h3, h4, p, div {{
            color: white !important;
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("bg.PNG bulunamadı. Aynı klasöre ekle.")

set_bg()

# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------
# SORULAR (7 ADET)
# -----------------------------
questions = [
    {"q": "Hangi öğün?", "type": "single", "options": ["Kahvaltı", "Öğle", "Akşam"]},
    {"q": "Ne kadar zamanın var?", "type": "single", "options": ["<15 dk", "15-30 dk", "30+ dk"]},
    {"q": "Beslenme tercihin?", "type": "multi", "options": ["Et", "Tavuk", "Sebze", "Vegan"]},
    {"q": "Nasıl bir yemek istersin?", "type": "single", "options": ["Hafif", "Doyurucu", "Sağlıklı"]},
    {"q": "Ruh halin?", "type": "single", "options": ["Yorgun", "Stresli", "Mutlu"]},
    {"q": "Evde ne var?", "type": "multi", "options": ["Tavuk", "Et", "Sebze", "Makarna"]},
    {"q": "Uğraş seviyesi?", "type": "single", "options": ["Pratik", "Orta", "Detaylı"]}
]

# -----------------------------
# YEMEK VERİ TABANI
# -----------------------------
meals = [
    {
        "name": "Tavuk Sote",
        "types": ["Tavuk"],
        "time": "<15 dk",
        "cal": 400,
        "tags": ["Hafif", "Pratik"],
        "ingredients": ["Tavuk"],
        "recipe": ["Tavuk doğra", "Tavada pişir", "Sebze ekle"]
    },
    {
        "name": "Izgara Tavuk Salata",
        "types": ["Tavuk"],
        "time": "<15 dk",
        "cal": 300,
        "tags": ["Sağlıklı", "Hafif"],
        "ingredients": ["Tavuk"],
        "recipe": ["Tavuk ızgara", "Salata ile karıştır"]
    },
    {
        "name": "Sebze Sote",
        "types": ["Sebze", "Vegan"],
        "time": "15-30 dk",
        "cal": 250,
        "tags": ["Hafif"],
        "ingredients": ["Sebze"],
        "recipe": ["Sebzeleri doğra", "Tavada pişir"]
    },
    {
        "name": "Kıymalı Makarna",
        "types": ["Et"],
        "time": "30+ dk",
        "cal": 650,
        "tags": ["Doyurucu"],
        "ingredients": ["Et", "Makarna"],
        "recipe": ["Kıymayı pişir", "Makarnayı haşla"]
    }
]

# -----------------------------
# SORU AKIŞI
# -----------------------------
st.title("🍽️ Yemek Önerici")

if st.session_state.step < len(questions):
    q_data = questions[st.session_state.step]

    st.subheader(q_data["q"])

    if q_data["type"] == "multi":
        selected = st.multiselect("", q_data["options"])
    else:
        selected = st.radio("", q_data["options"])

    if st.button("Devam"):
        if selected:
            st.session_state.answers[q_data["q"]] = selected
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Lütfen seçim yap")

# -----------------------------
# SKORLAMA
# -----------------------------
def score(meal, answers):
    s = 0

    if any(t in answers["Beslenme tercihin?"] for t in meal["types"]):
        s += 3

    if meal["time"] == answers["Ne kadar zamanın var?"]:
        s += 2

    if answers["Nasıl bir yemek istersin?"] in meal["tags"]:
        s += 2

    if any(i in answers["Evde ne var?"] for i in meal["ingredients"]):
        s += 2

    if answers["Uğraş seviyesi?"] == "Pratik" and meal["time"] == "<15 dk":
        s += 1

    return s

# -----------------------------
# SONUÇ
# -----------------------------
else:
    st.subheader("🎯 Öneriler")

    scored = [(m, score(m, st.session_state.answers)) for m in meals]
    scored.sort(key=lambda x: x[1], reverse=True)

    main, alt1, alt2 = scored[0][0], scored[1][0], scored[2][0]

    def show(title, meal):
        st.markdown(f"### {title}: {meal['name']}")
        st.write(f"Süre: {meal['time']}")
        st.write(f"Kalori: {meal['cal']} kcal")

    show("Ana Yemek", main)
    show("Alternatif", alt1)
    show("Alternatif", alt2)

    if st.button("Tarifini görmek ister misiniz?"):
        st.markdown(f"## 📖 {main['name']}")

        st.write("**Malzemeler:**")
        for i in main["ingredients"]:
            st.write(f"- {i}")

        st.write("**Adımlar:**")
        for step in main["recipe"]:
            st.write(f"- {step}")
