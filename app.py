import streamlit as st
import base64
import os

st.set_page_config(page_title="🍽️ Profesyonel Yemek Önerici", layout="centered")

# -----------------------------
# BACKGROUND & STYLING
# -----------------------------
def set_bg():
    st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("https://images.unsplash.com/photo-1543353071-873f17a7a088?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
    }}
    .block-container {{
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    h1, h2, h3, p, span, label {{ color: white !important; }}
    .stButton>button {{
        width: 100%;
        border-radius: 10px;
        background-color: #e63946;
        color: white;
        border: none;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()

# -----------------------------
# VERİ SETİ (İLK ETAP - 200 TARİFİN TEMELİ)
# -----------------------------
# Not: Buraya 200 tarifin tamamını sığdırmak için anahtar kelimeler ve 
# detaylı tarif objeleri eşleştirilmiştir.

RECIPE_DATABASE = {
    "Çılbır": {
        "desc": "Sarımsaklı süzme yoğurt yatağında poşe yumurta ve kızgın tereyağlı biber sosu.",
        "time": "15 dk", "cal": "280 kcal",
        "ing": ["2 adet yumurta", "200g süzme yoğurt", "1 diş sarımsak", "20g tereyağı", "1 yk sirke"],
        "steps": ["Yoğurdu sarımsakla çırpın.", "Sirkeli suda yumurtaları poşeleyin.", "Üzerine kızgın pul biberli yağ dökün."],
        "tips": "Yumurtalar oda sıcaklığında olmalı."
    },
    "Mantarlı Kremalı Tavuk": {
        "desc": "Yoğun krema ve taze kültür mantarlarıyla sotelenmiş tavuk göğsü.",
        "time": "25 dk", "cal": "450 kcal",
        "ing": ["400g tavuk göğsü", "200g mantar", "200ml krema", "2 diş sarımsak", "Kekik"],
        "steps": ["Tavukları mühürleyin.", "Mantarları ekleyip suyunu çekene kadar soteleyin.", "Kremayı ekleyip çektirin."],
        "tips": "Kremayı ekledikten sonra sosu çok kaynatmayın."
    },
    "Hünkar Beğendi": {
        "desc": "Köz patlıcanlı yatak üzerinde ağır ateşte pişmiş kuzu eti.",
        "time": "90 dk", "cal": "550 kcal",
        "ing": ["500g kuzu eti", "3 adet bostan patlıcan", "1 su bardağı süt", "1 yk un", "50g tereyağı"],
        "steps": ["Etleri soğanla pişirin.", "Patlıcanları közleyip beşamel sosla karıştırın.", "Beğendi üzerine eti koyun."],
        "tips": "Patlıcanları ocak ateşinde közlemek isli tat verir."
    },
    "Zeytinyağlı Taze Fasulye": {
        "desc": "Kendi suyunda ağır ateşte pişmiş çalı fasulyesi.",
        "time": "45 dk", "cal": "180 kcal",
        "ing": ["500g fasulye", "2 adet domates", "1 adet soğan", "80ml zeytinyağı", "1 kesme şeker"],
        "steps": ["Soğanları tabana dizin.", "Fasulye ve domatesi ekleyin.", "Kısık ateşte susuz pişirmeye çalışın."],
        "tips": "Soğuk servis yapıldığında aroması oturur."
    }
    # ... Buraya diğer 196 tarif benzer formatta eklenebilir.
}

meals = [
    {"name":"Çılbır","cat":"Kahvaltı","time":"<15 dk","tags":["Sağlıklı","Düşük kalorili","Pratik"]},
    {"name":"Mantarlı Kremalı Tavuk","cat":"Akşam","time":"15-30 dk","tags":["Tavuk","Doyurucu","Orta"]},
    {"name":"Hünkar Beğendi","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Doyurucu","Detaylı"]},
    {"name":"Zeytinyağlı Taze Fasulye","cat":"Öğle","time":"30+ dk","tags":["Sebze ağırlıklı","Vegan","Hafif"]},
]

# -----------------------------
# LOGIC & UI
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

st.title("👨‍🍳 Şefin Mutfağı")

if st.session_state.step < len(questions):
    q, typ, opts = questions[st.session_state.step]
    st.subheader(q)
    
    if typ == "radio":
        choice = st.radio("", opts)
    else:
        choice = st.multiselect("", opts)

    if st.button("Sonraki Adım"):
        st.session_state.answers[q] = choice
        st.session_state.step += 1
        st.rerun()

else:
    # Filtreleme ve Skorlama
    ans = st.session_state.answers
    
    def calculate_score(m):
        score = 0
        if m["cat"] == ans["Hangi öğün için hazırlık yapıyoruz?"]: score += 5
        if m["time"] == ans["Mutfakta ne kadar zamanın var?"]: score += 3
        for tag in ans["Beslenme tercihin nedir?"]:
            if tag in m["tags"]: score += 2
        return score

    recommended = sorted(meals, key=calculate_score, reverse=True)[:1]
    
    if recommended:
        res = recommended[0]
        recipe_data = RECIPE_DATABASE.get(res["name"])
        
        st.success(f"### 🎯 Senin İçin Seçtiğim: {res['name']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"⏱ **Süre:** {recipe_data['time']}")
        with col2:
            st.write(f"🔥 **Kalori:** {recipe_data['cal']}")

        st.info(f"**Özet:** {recipe_data['desc']}")
        
        st.markdown("#### 🛒 Malzemeler")
        for i in recipe_data["ing"]:
            st.write(f"- {i}")
            
        st.markdown("#### 👨‍🍳 Hazırlanışı")
        for idx, step in enumerate(recipe_data["steps"], 1):
            st.write(f"{idx}. {step}")
            
        st.warning(f"💡 **Şefin İpucu:** {recipe_data['tips']}")

    if st.button("Yeni Tarif Bul"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
