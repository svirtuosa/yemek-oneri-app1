import streamlit as st
import base64
import os

st.set_page_config(page_title="🍽️ Akıllı Yemek Önerici", layout="centered")

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
            background: rgba(0,0,0,0.65);
            padding: 2rem;
            border-radius: 15px;
            max-width: 750px;
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
    ("Hangi öğün?", "radio", ["Kahvaltı", "Öğle", "Akşam"]),
    ("Ne kadar zamanın var?", "radio", ["<15 dk", "15-30 dk", "30+ dk"]),
    ("Beslenme tercihin?", "multi", ["Et ağırlıklı", "Tavuk", "Sebze ağırlıklı", "Vegan", "Yüksek protein", "Düşük kalorili"]),
    ("Nasıl bir yemek istersin?", "multi", ["Hafif", "Doyurucu", "Sağlıklı", "Kaçamak"]),
    ("Evde ne var?", "multi", ["Tavuk", "Et", "Sebze", "Makarna", "Yumurta"]),
    ("Uğraş seviyesi?", "radio", ["Pratik", "Orta", "Detaylı"])
]

# -----------------------------
# YEMEK HAVUZU
# -----------------------------
meals = [
    {"name": "Tavuk Sote", "type": "Tavuk", "time": "15-30 dk", "cal": 400},
    {"name": "Izgara Tavuk Salata", "type": "Tavuk", "time": "<15 dk", "cal": 320},
    {"name": "Sebze Sote", "type": "Sebze ağırlıklı", "time": "15-30 dk", "cal": 250},
    {"name": "Kıymalı Makarna", "type": "Et ağırlıklı", "time": "30+ dk", "cal": 650},
    {"name": "Yulaf Bowl", "type": "Düşük kalorili", "time": "<15 dk", "cal": 250},
    {"name": "Granola Yoğurt", "type": "Düşük kalorili", "time": "<15 dk", "cal": 300},
    {"name": "Omlet", "type": "Yüksek protein", "time": "<15 dk", "cal": 300},
    {"name": "Izgara Somon", "type": "Yüksek protein", "time": "15-30 dk", "cal": 500},
    {"name": "Pizza", "type": "Doyurucu", "time": "30+ dk", "cal": 800},
    {"name": "Tost", "type": "Kaçamak", "time": "<15 dk", "cal": 350},
]

# -----------------------------
# SKOR
# -----------------------------
def score(meal, answers):
    s = 0

    if meal["type"] in answers["Beslenme tercihin?"]:
        s += 3

    if meal["time"] == answers["Ne kadar zamanın var?"]:
        s += 2

    if meal["type"] in answers["Evde ne var?"]:
        s += 1

    return s

# -----------------------------
# GERÇEK TARİF SİSTEMİ
# -----------------------------
def generate_recipe(meal):

    if meal["name"] == "Tavuk Sote":
        return """
## 🍽️ Tavuk Sote

**Açıklama:** Pratik ve dengeli bir protein yemeği.

**Süre:** 20 dk  
**Kalori:** 400 kcal  

### 🛒 Malzemeler:
- 300g tavuk göğsü  
- 1 adet soğan  
- 1 adet biber  
- 2 yemek kaşığı zeytinyağı  
- Tuz, karabiber  

### 👨‍🍳 Yapılışı:
1. Tavukları küp doğra  
2. Tavayı ısıt ve yağı ekle  
3. Tavukları mühürle  
4. Sebzeleri ekle  
5. 10 dk pişir  

### 💡 İpuçları:
- Yüksek ateş kullan  
"""

    if "Salata" in meal["name"]:
        return f"""
## 🥗 {meal['name']}

**Açıklama:** Hafif ve sağlıklı bir seçenek.

**Süre:** {meal['time']}  
**Kalori:** {meal['cal']} kcal  

### 🛒 Malzemeler:
- Marul  
- Domates  
- Salatalık  
- Zeytinyağı  

### 👨‍🍳 Yapılışı:
Karıştır ve servis et
"""

    if "Makarna" in meal["name"]:
        return f"""
## 🍝 {meal['name']}

**Açıklama:** Doyurucu klasik makarna.

**Süre:** {meal['time']}  
**Kalori:** {meal['cal']} kcal  

### 🛒 Malzemeler:
- 100g makarna  
- Sos  

### 👨‍🍳 Yapılışı:
Haşla ve sosla karıştır
"""

    return f"""
## 🍽️ {meal['name']}

**Süre:** {meal['time']}  
**Kalori:** {meal['cal']} kcal  

Pratik bir yemek önerisi.
"""

# -----------------------------
# UI
# -----------------------------
st.title("🍽️ Akıllı Yemek Önerici")

if st.session_state.step < len(questions):
    q, qtype, opts = questions[st.session_state.step]

    st.subheader(q)

    if qtype == "radio":
        choice = st.radio("", opts)
    else:
        choice = st.multiselect("", opts)

    if st.button("Devam"):
        if choice:
            st.session_state.answers[q] = choice
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Seçim yap")

if st.session_state.step >= len(questions):

    st.markdown("## 🎯 Senin İçin Önerimiz")

    scored = sorted(meals, key=lambda m: score(m, st.session_state.answers), reverse=True)

    main = scored[0]
    alt1 = scored[1]
    alt2 = scored[2]

    st.markdown("### ⭐ Ana Yemek")
    st.markdown(generate_recipe(main))

    st.markdown("### 🔁 Alternatifler")
    col1, col2 = st.columns(2)
    col1.write(alt1["name"])
    col2.write(alt2["name"])

    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
