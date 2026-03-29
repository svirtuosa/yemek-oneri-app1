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

    ("Beslenme tercihin?", "multi", ["Et ağırlıklı","Tavuk","Sebze ağırlıklı","Vegan","Yüksek protein","Düşük kalorili"]),

    ("Nasıl bir yemek?", "multi", ["Hafif","Doyurucu","Sağlıklı","Kaçamak"]),

    ("Evde ne var?", "multi", ["Tavuk","Et","Sebze","Makarna","Yumurta"]),

    ("Uğraş seviyesi?", "radio", ["Pratik","Orta","Detaylı"])

]



# -----------------------------

# YEMEK HAVUZU

# -----------------------------

meals = [

    {"name":"Tavuk Sote","cat":"tavuk","time":"15-30 dk","tags":["protein","pratik"]},

    {"name":"Omlet","cat":"kahvalti","time":"<15 dk","tags":["protein","pratik"]},

    {"name":"Yulaf Bowl","cat":"kahvalti","time":"<15 dk","tags":["hafif"]},

    {"name":"Sebze Sote","cat":"sebze","time":"15-30 dk","tags":["vegan","sağlıklı"]},

    {"name":"Kıymalı Makarna","cat":"et","time":"30+ dk","tags":["doyurucu"]},

    {"name":"Pizza","cat":"fast","time":"30+ dk","tags":["kaçamak"]},

    {"name":"Salata","cat":"sebze","time":"<15 dk","tags":["hafif"]},

    {"name":"Tost","cat":"fast","time":"<15 dk","tags":["kaçamak"]},

]



# -----------------------------

# GARANTİ SETLERİ

# -----------------------------

guarantee_sets = {

    "hizli": ["Omlet","Yulaf Bowl","Tost"],

    "vegan": ["Sebze Sote","Salata","Yulaf Bowl"],

    "protein": ["Tavuk Sote","Omlet","Yulaf Bowl"],

    "doyurucu": ["Kıymalı Makarna","Pizza","Tavuk Sote"],

    "hafif": ["Salata","Yulaf Bowl","Sebze Sote"]

}



# -----------------------------

# KEY BELİRLE

# -----------------------------

def get_key(a):

    if a["Ne kadar zamanın var?"] == "<15 dk":

        return "hizli"

    if "Vegan" in a["Beslenme tercihin?"]:

        return "vegan"

    if "Yüksek protein" in a["Beslenme tercihin?"]:

        return "protein"

    if "Doyurucu" in a["Nasıl bir yemek?"]:

        return "doyurucu"

    return "hafif"



# -----------------------------

# SKOR

# -----------------------------

def score(m,a):

    s=0

    if m["time"]==a["Ne kadar zamanın var?"]:

        s+=3

    for t in a["Nasıl bir yemek?"]:

        if t.lower() in m["tags"]:

            s+=2

    return s



# -----------------------------

# TARİF

# -----------------------------

def recipe(name):

    return f"""

### 🍽️ {name}



**Malzemeler:**

- Ana malzeme

- Yağ

- Baharat



**Yapılışı:**

1. Hazırla

2. Pişir

3. Servis et

"""



# -----------------------------

# UI

# -----------------------------

st.title("🍽️ Yemek Önerici")



if st.session_state.step < len(questions):

    q, typ, opts = questions[st.session_state.step]



    st.subheader(q)



    choice = st.radio("",opts) if typ=="radio" else st.multiselect("",opts)



    if st.button("Devam"):

        if choice:

            st.session_state.answers[q]=choice

            st.session_state.step+=1

            st.rerun()

        else:

            st.warning("Seçim yap")



# -----------------------------

# SONUÇ

# -----------------------------

if st.session_state.step>=len(questions):



    scored=sorted(meals,key=lambda m:score(m,st.session_state.answers),reverse=True)

    selected=scored[:3]



    if len(selected)<3:

        key=get_key(st.session_state.answers)

        selected=[m for m in meals if m["name"] in guarantee_sets[key]]



    main,alt1,alt2=selected[0],selected[1],selected[2]



    st.markdown("## 🎯 Ana Yemek")

    st.markdown(recipe(main["name"]))



    st.markdown("## 🔁 Alternatifler")

    st.write(alt1["name"])

    st.write(alt2["name"])



    if st.button("Baştan"):

        st.session_state.step=0

        st.session_state.answers={}

        st.rerun()
