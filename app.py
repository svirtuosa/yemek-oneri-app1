import streamlit as st
import base64
import os
import random

st.set_page_config(page_title="🍽️ Chef-Level Yemek Önerici", layout="centered")

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
            background: rgba(0,0,0,0.7);
            padding: 2rem;
            border-radius: 20px;
            max-width: 900px;
            margin: auto;
        }}
        .card {{
            background: rgba(255,255,255,0.08);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        }}
        h1,h2,h3,h4,p,div {{ color:white !important; }}
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
    ("Beslenme tercihin?", "multi", [
        "Et ağırlıklı","Tavuk","Sebze ağırlıklı","Vegan",
        "Yüksek protein","Düşük kalorili"
    ]),
    ("Nasıl bir yemek?", "multi", ["Hafif","Doyurucu","Sağlıklı","Kaçamak"]),
    ("Evde ne var?", "multi", ["Tavuk","Et","Sebze","Makarna","Yumurta"]),
    ("Uğraş seviyesi?", "radio", ["Pratik","Orta","Detaylı"])
]

# -----------------------------
# DEVASA YEMEK HAVUZU
# -----------------------------
meals = [
    {"name": "Tavuk Sote", "category": "tavuk", "time": "15-30 dk", "cal": 400, "tags": ["protein","pratik"]},
    {"name": "Izgara Tavuk Salata", "category": "salata", "time": "<15 dk", "cal": 300, "tags": ["hafif"]},
    {"name": "Kıymalı Makarna", "category": "makarna", "time": "30+ dk", "cal": 650, "tags": ["doyurucu"]},
    {"name": "Sebze Stir Fry", "category": "sebze", "time": "15-30 dk", "cal": 300, "tags": ["sağlıklı"]},
    {"name": "Omlet", "category": "kahvalti", "time": "<15 dk", "cal": 280, "tags": ["protein"]},
    {"name": "Yulaf Bowl", "category": "kahvalti", "time": "<15 dk", "cal": 250, "tags": ["hafif"]},
    {"name": "Somon Izgara", "category": "balik", "time": "15-30 dk", "cal": 500, "tags": ["protein"]},
]

# -----------------------------
# SKOR SİSTEMİ (DAHA AKILLI)
# -----------------------------
def score(meal, a):
    s = 0

    if "Tavuk" in a["Beslenme tercihin?"] and meal["category"] == "tavuk":
        s += 5
    if "Et ağırlıklı" in a["Beslenme tercihin?"] and meal["category"] == "et":
        s += 5

    if meal["time"] == a["Ne kadar zamanın var?"]:
        s += 3

    for t in a["Nasıl bir yemek?"]:
        if t.lower() in meal["tags"]:
            s += 2

    return s

# -----------------------------
# CHEF-LEVEL TARİF MOTORU
# -----------------------------
def generate_recipe(meal):

    base_oils = ["zeytinyağı", "tereyağı"]
    spices = ["karabiber", "kekik", "pul biber"]

    oil = random.choice(base_oils)

    if meal["category"] == "tavuk":
        return f"""
### 🍽️ {meal['name']}

**Açıklama:** Dengeli ve yüksek proteinli tavuk yemeği

**Malzemeler:**
- 300g tavuk göğsü
- 1 adet soğan
- 1 adet biber
- 2 yemek kaşığı {oil}
- {", ".join(spices)}

**Yapılışı:**
1. Tavukları eşit boyutta doğra  
2. Tavayı yüksek ateşte ısıt  
3. Tavukları mühürle (renk alana kadar)  
4. Sebzeleri ekle  
5. Orta ateşte pişir  

**İpucu:**
Tavuğu fazla karıştırma → su salar
"""

    elif meal["category"] == "makarna":
        return f"""
### 🍝 {meal['name']}

**Malzemeler:**
- 100g makarna
- 1 bardak domates sosu
- 1 yemek kaşığı {oil}

**Yapılışı:**
1. Makarnayı tuzlu suda haşla  
2. Sosu tavada ısıt  
3. Makarnayı ekleyip karıştır  

**İpucu:**
Makarnayı az diri bırak (al dente)
"""

    elif meal["category"] == "salata":
        return f"""
### 🥗 {meal['name']}

**Malzemeler:**
- Marul
- Domates
- Salatalık
- {oil}
- Limon

**Yapılışı:**
Doğra, karıştır, servis et

**İpucu:**
Sosu en son ekle
"""

    elif meal["category"] == "kahvalti":
        return f"""
### 🍳 {meal['name']}

**Malzemeler:**
- 2 yumurta
- 1 tatlı kaşığı {oil}
- Tuz

**Yapılışı:**
Tavada pişir

**İpucu:**
Orta ateş kullan
"""

    else:
        return f"""
### 🍽️ {meal['name']}

Pratik bir yemek.
"""

# -----------------------------
# UI
# -----------------------------
st.title("🍽️ Chef-Level Yemek Önerici")

if st.session_state.step < len(questions):
    q, typ, opts = questions[st.session_state.step]

    st.subheader(q)

    if typ == "radio":
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

# -----------------------------
# SONUÇ
# -----------------------------
if st.session_state.step >= len(questions):

    scored = sorted(meals, key=lambda m: score(m, st.session_state.answers), reverse=True)

    main, alt1, alt2 = scored[0], scored[1], scored[2]

    st.markdown("## 🎯 Ana Öneri")
    st.markdown(f"<div class='card'>{generate_recipe(main)}</div>", unsafe_allow_html=True)

    st.markdown("## 🔁 Alternatifler")
    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='card'>{alt1['name']}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>{alt2['name']}</div>", unsafe_allow_html=True)

    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
