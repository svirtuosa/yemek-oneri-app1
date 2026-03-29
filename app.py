import streamlit as st
import base64
import os
from openai import OpenAI

st.set_page_config(page_title="🍽️ AI Yemek Önerici", layout="centered")

# -----------------------------
# API
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# BACKGROUND
# -----------------------------
def set_bg():
    if os.path.exists("bg.PNG"):
        with open("bg.PNG", "rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
        }}
        .block-container {{
            background: rgba(0,0,0,0.6);
            padding: 2rem;
            border-radius: 15px;
            max-width: 600px;
            margin: auto;
        }}
        h1,h2,h3,h4,p,div {{ color:white !important; text-align:center; }}
        </style>
        """, unsafe_allow_html=True)

set_bg()

# -----------------------------
# STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "result" not in st.session_state:
    st.session_state.result = None

# -----------------------------
# SORULAR
# -----------------------------
questions = [
    "Hangi öğün?",
    "Ne kadar zamanın var?",
    "Beslenme tercihin?",
    "Nasıl bir yemek?",
    "Ruh halin?",
    "Evde ne var?",
    "Uğraş seviyesi?"
]

options = [
    ["Kahvaltı", "Öğle", "Akşam"],
    ["<15 dk", "15-30 dk", "30+ dk"],
    ["Et", "Tavuk", "Sebze", "Vegan"],
    ["Hafif", "Doyurucu", "Sağlıklı"],
    ["Yorgun", "Stresli", "Mutlu"],
    ["Tavuk", "Et", "Sebze", "Makarna"],
    ["Pratik", "Orta", "Detaylı"]
]

# -----------------------------
# UI
# -----------------------------
st.title("🍽️ AI Yemek Önerici")

if st.session_state.step < len(questions):

    q = questions[st.session_state.step]
    opts = options[st.session_state.step]

    st.subheader(q)
    choice = st.multiselect("", opts, key=st.session_state.step)

    if st.button("Devam"):
        if choice:
            st.session_state.answers[q] = choice
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Seçim yap")

# -----------------------------
# AI FONKSİYON
# -----------------------------
def generate_recipe(answers):
    prompt = f"""
    Kullanıcı tercihleri:
    {answers}

    1 ana yemek ve 2 alternatif öner.

    Her biri için:
    - İsim
    - Neden uygun
    - Süre
    - Kalori
    - Malzemeler
    - Tarif

    Türkçe yaz.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# -----------------------------
# SONUÇ
# -----------------------------
if st.session_state.step >= len(questions):

    st.subheader("🤖 AI öneri hazırlıyor...")

    if st.session_state.result is None:
        with st.spinner("AI düşünüyor..."):
            st.session_state.result = generate_recipe(st.session_state.answers)

    st.markdown(st.session_state.result)

    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.session_state.result = None
        st.rerun()
