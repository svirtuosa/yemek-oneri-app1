import streamlit as st
import random

st.set_page_config(page_title="Yemek Öneri", layout="wide")

# ----------- ARKA PLAN -----------
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1490818387583-1baba5e638af");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* içerik okunabilirliği */
.block-container {
    background-color: rgba(0, 0, 0, 0.6);
    padding: 2rem;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ----------- BAŞLIK -----------
st.markdown("<h1 style='text-align:center;'>🍽️ Yemek Öneri Sistemi</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ne yesem derdine son 😄</p>", unsafe_allow_html=True)

st.divider()

# ----------- SORULAR -----------
ogun = st.selectbox("Öğün:", ["kahvaltı", "öğle", "akşam", "tatlı"])

amac = st.selectbox("Amacın ne?", [
    "hızlıca yemek",
    "sağlıklı beslenmek",
    "kilo vermek",
    "keyif yapmak"
])

sure = st.selectbox("Ne kadar vaktin var?", [
    "5 dk",
    "15 dk",
    "30+ dk"
])

tat = st.selectbox("Tat tercihi:", ["tatlı", "tuzlu", "hafif"])

doyurucu = st.selectbox("Ne kadar doyurucu olsun?", [
    "hafif",
    "orta",
    "çok doyurucu"
])

protein = st.selectbox("Protein ister misin?", [
    "evet",
    "hayır",
    "fark etmez"
])

malzeme = st.selectbox("Evde ne var?", [
    "temel şeyler",
    "sebze var",
    "et/tavuk var"
])

mutfak = st.selectbox("Mutfak tercihi:", [
    "Türk mutfağı",
    "dünya mutfağı",
    "fark etmez"
])

st.divider()

# ----------- YEMEK HAVUZU -----------

yemekler = {
    "kahvaltı": {
        "tatlı": ["🥞 Pankek", "🥣 Yulaf", "🍯 Bal + kaymak", "🍌 Smoothie bowl"],
        "tuzlu": ["🍳 Omlet", "🍅 Menemen", "🧀 Peynir tabağı", "🥪 Tost"],
        "hafif": ["🥗 Yoğurt + meyve", "🥛 Kefir", "🍎 Meyve tabağı"]
    },
    "öğle": {
        "hızlıca yemek": ["🥪 Sandviç", "🌯 Wrap", "🍝 Makarna"],
        "sağlıklı beslenmek": ["🥗 Tavuk salata", "🥦 Sebze yemeği", "🍚 Bulgur + yoğurt"],
        "kilo vermek": ["🥗 Yeşil salata", "🥒 Zeytinyağlı sebze"],
        "keyif yapmak": ["🍔 Burger", "🍕 Pizza", "🍝 Makarna"]
    },
    "akşam": {
        "hafif": ["🥗 Salata", "🥦 Sebze yemeği", "🍲 Çorba"],
        "orta": ["🍝 Makarna", "🍛 Tavuk sote", "🍲 Çorba + ana yemek"],
        "çok doyurucu": ["🍖 Et yemeği", "🍗 Tavuk + pilav", "🍲 Güveç"]
    },
    "tatlı": [
        "🍫 Fit brownie",
        "🍰 Fit cheesecake",
        "🍯 Fit baklava",
        "🍌 Muzlu pankek",
        "🍓 Yoğurtlu tatlı"
    ]
}

# ----------- ÖNERİ MOTORU -----------

oneriler = []

if ogun == "kahvaltı":
    oneriler = yemekler["kahvaltı"].get(tat, [])

elif ogun == "öğle":
    oneriler = yemekler["öğle"].get(amac, [])

elif ogun == "akşam":
    oneriler = yemekler["akşam"].get(doyurucu, [])

elif ogun == "tatlı":
    oneriler = yemekler["tatlı"]

# ----------- EK FİLTRELER -----------

if protein == "evet":
    oneriler += ["🍗 Tavuk", "🥚 Yumurta", "🥩 Et"]

if sure == "5 dk":
    oneriler = oneriler[:3]

if malzeme == "temel şeyler":
    oneriler = [y for y in oneriler if "Et" not in y and "Tavuk" not in y]

# ----------- SONUÇ -----------

if oneriler:
    secim = random.choice(oneriler)
    st.success(f"👉 Sana önerim: {secim}")

# ----------- RANDOM BUTON -----------

if st.button("🎲 Kararsızım, bana seç"):
    tum = []
    for k in yemekler:
        if isinstance(yemekler[k], dict):
            for alt in yemekler[k].values():
                tum.extend(alt)
        else:
            tum.extend(yemekler[k])

    st.success(f"👉 Rastgele: {random.choice(tum)}")
