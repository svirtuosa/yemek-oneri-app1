import streamlit as st
import base64
import os

st.set_page_config(page_title="🍽️ Yemek Önerici", layout="centered")

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
if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------------
# SORULAR
# -----------------------------
questions = [
    "Hangi öğün?",
    "Ne kadar zamanın var?",
    "Beslenme tercihin?",
    "Nasıl bir yemek?",
    "Evde ne var?",
    "Uğraş seviyesi?"
]

options = [
    ["Kahvaltı", "Öğle", "Akşam"],
    ["<15 dk", "15-30 dk", "30+ dk"],
    ["Et", "Tavuk", "Sebze", "Vegan"],
    ["Hafif", "Doyurucu", "Sağlıklı"],
    ["Tavuk", "Et", "Sebze", "Makarna"],
    ["Pratik", "Orta", "Detaylı"]
]

# -----------------------------
# YEMEK HAVUZU
# -----------------------------
meals = [
    {"name": "Tavuk Sote", "type": "Tavuk", "time": "<15 dk", "cal": 400},
    {"name": "Izgara Tavuk Salata", "type": "Tavuk", "time": "<15 dk", "cal": 300},
    {"name": "Sebze Sote", "type": "Sebze", "time": "15-30 dk", "cal": 250},
    {"name": "Kıymalı Makarna", "type": "Et", "time": "30+ dk", "cal": 650},
]

# -----------------------------
# SORU AKIŞI
# -----------------------------
st.title("🍽️ Yemek Önerici")

if st.session_state.step < len(questions):

    q = questions[st.session_state.step]
    opts = options[st.session_state.step]

    st.subheader(q)
    choice = st.multiselect("", opts)

    if st.button("Devam"):
        if choice:
            st.session_state.answers[q] = choice
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Seçim yap")

# -----------------------------
# PUANLAMA
# -----------------------------
def score(meal, answers):
    s = 0

    if meal["type"] in answers["Beslenme tercihin?"]:
        s += 3

    if meal["time"] == answers["Ne kadar zamanın var?"][0]:
        s += 2

    if meal["type"] in answers["Evde ne var?"]:
        s += 2

    return s

# -----------------------------
# TARİF OLUŞTURMA (FAKE AI)
# -----------------------------
def generate_recipe(meal, answers):
    return f"""
## 🍽️ {meal['name']}

**Neden önerildi:** Tercihlerinle uyumlu, pratik ve uygun bir seçenek.

**Süre:** {meal['time']}  
**Kalori:** {meal['cal']} kcal  

### 🛒 Malzemeler:
- Ana malzeme (seçimine göre)
- Soğan  
- Yağ  
- Baharatlar  

### 👨‍🍳 Tarif:
1. Malzemeleri doğra  
2. Tavayı ısıt  
3. Ana malzemeyi ekle  
4. Baharat ekle  
5. 10-20 dk pişir  

👉 Basit, hızlı ve tam senlik.
"""

# -----------------------------
# SONUÇ
# -----------------------------
if st.session_state.step >= len(questions):

    st.subheader("🎯 Senin için öneri")

    scored = sorted(meals, key=lambda m: score(m, st.session_state.answers), reverse=True)

    main = scored[0]
    alt1 = scored[1]
    alt2 = scored[2]

    st.markdown(generate_recipe(main, st.session_state.answers))

    st.markdown("### 🔁 Alternatifler")
    st.write(alt1["name"])
    st.write(alt2["name"])

    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
