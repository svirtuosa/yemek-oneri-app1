import streamlit as st
import base64
import os
import random

st.set_page_config(page_title="🍽️ AI Yemek Önerici", layout="centered")

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
# YEMEK HAVUZU
# -----------------------------
meals = [
    {"name": "Tavuk Sote", "category": "tavuk", "time": "15-30 dk", "cal": 400, "tags": ["protein","pratik"]},
    {"name": "Izgara Tavuk Salata", "category": "salata", "time": "<15 dk", "cal": 300, "tags": ["hafif"]},
    {"name": "Kıymalı Makarna", "category": "makarna", "time": "30+ dk", "cal": 650, "tags": ["doyurucu"]},
    {"name": "Sebze Stir Fry", "category": "sebze", "time": "15-30 dk", "cal": 300, "tags": ["sağlıklı"]},
    {"name": "Omlet", "category": "kahvalti", "time": "<15 dk", "cal": 280, "tags": ["protein"]},
    {"name": "Yulaf Bowl", "category": "kahvalti", "time": "<15 dk", "cal": 250, "tags": ["hafif"]},
    {"name": "Somon Izgara", "category": "balik", "time": "15-30 dk", "cal": 500, "tags": ["protein"]},
    {"name": "Pizza", "category": "fastfood", "time": "30+ dk", "cal": 800, "tags": ["kaçamak"]},
]

# -----------------------------
# GELİŞMİŞ SKOR
# -----------------------------
def advanced_score(meal, a):

    score = 0

    # HARD FILTER
    if a["Ne kadar zamanın var?"] == "<15 dk" and meal["time"] == "30+ dk":
        return -999

    if "Vegan" in a["Beslenme tercihin?"] and meal["category"] in ["et", "tavuk"]:
        return -999

    # BESLENME
    if meal["category"] == "tavuk" and "Tavuk" in a["Beslenme tercihin?"]:
        score += 5

    if meal["category"] == "et" and "Et ağırlıklı" in a["Beslenme tercihin?"]:
        score += 5

    # SÜRE
    if meal["time"] == a["Ne kadar zamanın var?"]:
        score += 3

    # TARZ
    for pref in a["Nasıl bir yemek?"]:
        if pref.lower() in meal["tags"]:
            score += 2

    # MALZEME
    for ing in a["Evde ne var?"]:
        if ing.lower() in meal["name"].lower():
            score += 2

    # UĞRAŞ
    if a["Uğraş seviyesi?"] == "Pratik" and meal["time"] == "<15 dk":
        score += 2

    return score

# -----------------------------
# DIVERSITY
# -----------------------------
def pick_diverse(scored_list):
    selected = []
    used = set()

    for meal, sc in scored_list:
        if meal["category"] not in used:
            selected.append(meal)
            used.add(meal["category"])

        if len(selected) == 3:
            break

    return selected

# -----------------------------
# TARİF MOTORU
# -----------------------------
def generate_recipe(meal):

    if meal["category"] == "tavuk":
        return f"""
### 🍽️ {meal['name']}

**Malzemeler:**
- 300g tavuk
- soğan
- biber
- zeytinyağı

**Yapılışı:**
Tavukları yüksek ateşte pişir, sebzeleri ekle.
"""

    if meal["category"] == "makarna":
        return f"""
### 🍝 {meal['name']}

Makarnayı haşla ve sosla karıştır.
"""

    if meal["category"] == "salata":
        return f"""
### 🥗 {meal['name']}

Sebzeleri doğra ve karıştır.
"""

    return f"""
### 🍽️ {meal['name']}

Pratik bir yemek.
"""

# -----------------------------
# UI
# -----------------------------
st.title("🍽️ AI Yemek Önerici")

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

    scored = [(m, advanced_score(m, st.session_state.answers)) for m in meals]
    scored = [x for x in scored if x[1] > 0]
    scored.sort(key=lambda x: x[1], reverse=True)

    selected = pick_diverse(scored)

    main, alt1, alt2 = selected[0], selected[1], selected[2]

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
