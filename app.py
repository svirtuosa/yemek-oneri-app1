import streamlit as st
import base64
import os
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="🍽️ AI Yemek Önerici", layout="centered")

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# BACKGROUND
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
            max-width: 650px;
            margin: auto;
        }}
        h1,h2,h3,h4,p,div {{
            color:white !important;
            text-align:center;
        }}
        </style>
        """, unsafe_allow_html=True)

set_bg()

# -----------------------------
# STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------
# SORULAR (7 adet)
# -----------------------------
questions = [
    {"q": "Hangi öğün?", "options": ["Kahvaltı", "Öğle", "Akşam"]},
    {"q": "Ne kadar zamanın var?", "options": ["<15 dk", "15-30 dk", "30+ dk"]},
    {"q": "Beslenme tercihin?", "options": ["Et", "Tavuk", "Sebze", "Vegan"]},
    {"q": "Nasıl bir yemek?", "options": ["Hafif", "Doyurucu", "Sağlıklı"]},
    {"q": "Ruh halin?", "options": ["Yorgun", "Stresli", "Mutlu"]},
    {"q": "Evde ne var?", "options": ["Tavuk", "Et", "Sebze", "Makarna"]},
    {"q": "Uğraş seviyesi?", "options": ["Pratik", "Orta", "Detaylı"]}
]

# -----------------------------
# UI
# -----------------------------
st.title("🍽️ AI Yemek Önerici")

if st.session_state.step < len(questions):
    q = questions[st.session_state.step]

    st.subheader(q["q"])
    choice = st.multiselect("", q["options"])

    if st.button("Devam"):
        if choice:
            st.session_state.answers[q["q"]] = choice
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Lütfen seçim yap")

# -----------------------------
# AI TARİF
# -----------------------------
def generate_recipe(answers):
    prompt = f"""
    Kullanıcı tercihleri:
    {answers}

    Buna göre:
    - 1 ana yemek
    - 2 alternatif yemek öner

    Her yemek için:
    - İsim
    - Neden uygun
    - Tahmini süre
    - Kalori
    - Malzemeler (liste halinde)
    - Adım adım tarif

    Türkçe yaz, düzenli ve okunabilir olsun.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# -----------------------------
# SONUÇ
# -----------------------------
else:
    st.subheader("🤖 AI senin için en iyi yemekleri seçiyor...")

    if "result" not in st.session_state:
        with st.spinner("AI düşünüyor..."):
            st.session_state.result = generate_recipe(st.session_state.answers)

    st.markdown(st.session_state.result)

    st.divider()

    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.result = None
        st.rerun()
        
