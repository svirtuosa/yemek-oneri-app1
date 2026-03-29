import streamlit as st
import base64
import os
import time

st.set_page_config(page_title="🍽️ AI Yemek Önerici", layout="centered")

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
            background: rgba(0,0,0,0.7);
            padding: 2rem;
            border-radius: 15px;
            max-width: 700px;
            margin: auto;
        }}
        h1, h2, h3, h4, p, div {{
            color: white !important;
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("bg.PNG bulunamadı. Lütfen aynı klasöre ekle.")
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
# DETAYLI YEMEK HAVUZU
# -----------------------------
meals = [
    {"name":"Tavuk Sote", "cat":"tavuk", "time":"15-30 dk", "tags":["protein","pratik","doyurucu"],
     "ingredients": ["250g Tavuk Göğsü", "1 adet Biber", "1 adet Domates", "Kekik", "Zeytinyağı"],
     "steps": ["Tavukları küp küp doğrayıp yüksek ateşte mühürleyin.", "Biberleri ekleyip sotelemeye devam edin.", "Domates ve baharatları ekleyip suyunu çekene kadar pişirin."]},
     
    {"name":"Omlet", "cat":"kahvalti", "time":"<15 dk", "tags":["protein","pratik"],
     "ingredients": ["2 adet Yumurta", "1 tatlı kaşığı Tereyağı", "Kaşar Peyniri", "Tuz", "Karabiber"],
     "steps": ["Yumurtaları bir kasede iyice çırpın.", "Tavada tereyağını eritin ve yumurtayı dökün.", "Üzerine kaşar serpip katlayın, sıcak servis edin."]},
     
    {"name":"Yulaf Bowl", "cat":"kahvalti", "time":"<15 dk", "tags":["hafif", "sağlıklı"],
     "ingredients": ["4 yemek kaşığı Yulaf", "1 bardak Süt/Su", "1 adet Muz", "1 tatlı kaşığı Fıstık Ezmesi", "Tarçın"],
     "steps": ["Yulaf ve sütü kıvam alana kadar pişirin.", "Kaseye alıp üzerine dilimlenmiş muzları ekleyin.", "Fıstık ezmesi ve tarçınla süsleyerek servis yapın."]},
     
    {"name":"Sebze Sote", "cat":"sebze", "time":"15-30 dk", "tags":["vegan","sağlıklı", "hafif"],
     "ingredients": ["1 adet Kabak", "1 adet Havuç", "Yarım Brokoli", "2 yemek kaşığı Zeytinyağı", "Soya Sosu"],
     "steps": ["Sebzeleri jülyen veya küp küp doğrayın.", "Tavada zeytinyağını ısıtıp sertten yumuşağa doğru sebzeleri soteleyin.", "Son aşamada soya sosu ekleyip ocaktan alın."]},
     
    {"name":"Kıymalı Makarna", "cat":"et", "time":"30+ dk", "tags":["doyurucu"],
     "ingredients": ["Yarım paket Makarna", "200g Kıyma", "1 yemek kaşığı Salça", "1 adet Soğan", "Tuz ve Baharatlar"],
     "steps": ["Makarnayı tuzlu suda haşlayın.", "Soğanı ve kıymayı kavurun, salça ve baharatları ekleyin.", "Haşlanmış makarna ile sosu birleştirin."]},
     
    {"name":"Pizza", "cat":"fast", "time":"30+ dk", "tags":["kaçamak", "doyurucu"],
     "ingredients": ["Hazır Pizza Tabanı veya Lavaş", "Domates Sosu", "Bol Kaşar/Mozzarella", "Sucuk, Mantar, Mısır"],
     "steps": ["Tabanın üzerine domates sosunu yayın.", "Peyniri ve dilediğiniz malzemeleri dizin.", "Önceden ısıtılmış 200 derece fırında peynirler eriyene kadar pişirin."]},
     
    {"name":"Salata", "cat":"sebze", "time":"<15 dk", "tags":["hafif", "sağlıklı", "vegan"],
     "ingredients": ["Mevsim Yeşillikleri", "Çeri Domates", "Salatalık", "Zeytinyağı", "Limon"],
     "steps": ["Yeşillikleri yıkayıp elinizle iri iri koparın.", "Domates ve salatalıkları doğrayın.", "Zeytinyağı, limon ve az tuz ile soslayıp harmanlayın."]},
     
    {"name":"Tost", "cat":"fast", "time":"<15 dk", "tags":["kaçamak", "pratik"],
     "ingredients": ["2 dilim Tost Ekmeği", "Kaşar Peyniri", "Sucuk (İsteğe bağlı)", "Tereyağı"],
     "steps": ["Ekmeklerin arasına kaşar ve sucukları dizin.", "Tost makinesinde bastırın.", "Dışına hafif tereyağı sürerek kızarana kadar pişirin."]}
]

# -----------------------------
# GARANTİ SETLERİ & SKORLAMA
# -----------------------------
guarantee_sets = {
    "hizli": ["Omlet","Yulaf Bowl","Tost"],
    "vegan": ["Sebze Sote","Salata","Yulaf Bowl"],
    "protein": ["Tavuk Sote","Omlet","Yulaf Bowl"],
    "doyurucu": ["Kıymalı Makarna","Pizza","Tavuk Sote"],
    "hafif": ["Salata","Yulaf Bowl","Sebze Sote"]
}

def get_key(a):
    if a.get("Ne kadar zamanın var?") == "<15 dk": return "hizli"
    if "Vegan" in a.get("Beslenme tercihin?", []): return "vegan"
    if "Yüksek protein" in a.get("Beslenme tercihin?", []): return "protein"
    if "Doyurucu" in a.get("Nasıl bir yemek?", []): return "doyurucu"
    return "hafif"

def score(m, a):
    s = 0
    if m["time"] == a.get("Ne kadar zamanın var?"): s += 3
    for t in a.get("Nasıl bir yemek?", []):
        if t.lower() in m["tags"]:
            s += 2
    return s

# -----------------------------
# AI GÖRÜNÜMLÜ TARİF UI
# -----------------------------
def recipe_ui(meal_obj):
    st.markdown(f"### ✨ AI Önerisi: {meal_obj['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🛒 Malzemeler")
        for ing in meal_obj.get("ingredients", ["Malzeme bilgisi bulunamadı"]):
            st.markdown(f"- {ing}")
            
    with col2:
        st.markdown("#### ⏲️ Hazırlanış")
        for i, step in enumerate(meal_obj.get("steps", ["Adım bilgisi bulunamadı"]), 1):
            st.markdown(f"**{i}.** {step}")
            
    st.info("💡 **AI İpucu:** Kendi damak zevkine göre baharatları ve malzemeleri özelleştirmekten çekinme!")

# -----------------------------
# ANA UI UYGULAMASI
# -----------------------------
st.title("🍽️ AI Yemek Önerici")

if st.session_state.step < len(questions):
    q, typ, opts = questions[st.session_state.step]

    st.subheader(q)
    choice = st.radio("", opts) if typ == "radio" else st.multiselect("", opts)

    if st.button("Devam Et"):
        if choice:
            st.session_state.answers[q] = choice
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Lütfen bir seçim yap.")

# -----------------------------
# SONUÇ EKRANI
# -----------------------------
if st.session_state.step >= len(questions):
    
    # AI Bekleme Efekti
    if "calculated" not in st.session_state:
        with st.spinner("🤖 Yapay Zeka en uygun tarifi hesaplıyor..."):
            time.sleep(1.5)
        st.session_state.calculated = True

    scored = sorted(meals, key=lambda m: score(m, st.session_state.answers), reverse=True)
    selected = scored[:3]

    if len(selected) < 3:
        key = get_key(st.session_state.answers)
        selected = [m for m in meals if m["name"] in guarantee_sets[key]]

    main, alt1, alt2 = selected[0], selected[1], selected[2]

    st.markdown("---")
    st.markdown("### 🎯 Senin İçin En Uygun Seçim")
    recipe_ui(main)

    st.markdown("---")
    st.markdown("### 🔁 Alternatif Seçeneklerin")
    
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"**{alt1['name']}**")
        st.caption(f"Süre: {alt1['time']} | {', '.join(alt1['tags']).title()}")
    with c2:
        st.success(f"**{alt2['name']}**")
        st.caption(f"Süre: {alt2['time']} | {', '.join(alt2['tags']).title()}")

    st.markdown("---")
    if st.button("🔄 Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        del st.session_state.calculated
        st.rerun()
    
