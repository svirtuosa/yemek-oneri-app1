import streamlit as st
import random

st.set_page_config(page_title="Yemek Öneri", page_icon="🍽️")

# ----------- STİL -----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
    url("https://raw.githubusercontent.com/svirtuosa/yemek-oneri-app1/main/bg.PNG");
    background-size: cover;
}
.card {
    padding: 10px;
    border-radius: 12px;
    background: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ----------- BAŞLIK -----------
st.markdown("<h1 style='text-align:center;'>🍽️ Yemek Öneri Sistemi</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ne yesem derdine son 😄</p>", unsafe_allow_html=True)

st.divider()

# ----------- SORULAR -----------
ogun = st.selectbox("Öğün:", ["kahvaltı", "öğle", "akşam", "tatlı"])
amac = st.selectbox("Amaç:", ["hızlı", "sağlıklı", "kilo verme", "keyif"])
sure = st.selectbox("Süre:", ["5 dk", "15 dk", "30+ dk"])
tat = st.selectbox("Tat:", ["tatlı", "tuzlu", "hafif"])
doyurucu = st.selectbox("Doyuruculuk:", ["hafif", "orta", "ağır"])
protein = st.selectbox("Protein:", ["evet", "hayır", "fark etmez"])
malzeme = st.selectbox("Malzeme:", ["temel", "sebze", "et/tavuk"])

st.divider()

# ----------- YEMEK + GÖRSEL DB -----------

yemekler = [
    {"ad": "🥞 Pankek", "kategori": "kahvaltı", "img": "https://images.unsplash.com/photo-1587738347117-7c8f3b8e2f63"},
    {"ad": "🍳 Omlet", "kategori": "kahvaltı", "img": "https://images.unsplash.com/photo-1559622214-f8a9850965bb"},
    {"ad": "🍅 Menemen", "kategori": "kahvaltı", "img": "https://images.unsplash.com/photo-1604908176997-4311c7c4b0f3"},
    {"ad": "🥪 Sandviç", "kategori": "öğle", "img": "https://images.unsplash.com/photo-1550317138-10000687a72b"},
    {"ad": "🌯 Wrap", "kategori": "öğle", "img": "https://images.unsplash.com/photo-1604908177522-4027c9d9e8c7"},
    {"ad": "🍝 Makarna", "kategori": "öğle", "img": "https://images.unsplash.com/photo-1521389508051-d7ffb5dc8c4f"},
    {"ad": "🥗 Salata", "kategori": "hafif", "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"},
    {"ad": "🍗 Tavuk", "kategori": "protein", "img": "https://images.unsplash.com/photo-1604908554165-0f8a6f7d9f5f"},
    {"ad": "🍖 Et", "kategori": "protein", "img": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092"},
    {"ad": "🍔 Burger", "kategori": "keyif", "img": "https://images.unsplash.com/photo-1550547660-d9450f859349"},
    {"ad": "🍕 Pizza", "kategori": "keyif", "img": "https://images.unsplash.com/photo-1548365328-8b849f13c0c5"},
    {"ad": "🍫 Brownie", "kategori": "tatlı", "img": "https://images.unsplash.com/photo-1606312619070-d48b4c652a52"},
    {"ad": "🍰 Cheesecake", "kategori": "tatlı", "img": "https://images.unsplash.com/photo-1563805042-7684c019e1cb"},
]

# ----------- FİLTRE -----------

filtreli = []

for y in yemekler:
    if ogun == "tatlı" and y["kategori"] == "tatlı":
        filtreli.append(y)
    elif ogun == "kahvaltı" and y["kategori"] == "kahvaltı":
        filtreli.append(y)
    elif ogun == "öğle" and y["kategori"] in ["öğle", "hafif"]:
        filtreli.append(y)
    elif ogun == "akşam" and y["kategori"] in ["protein", "hafif"]:
        filtreli.append(y)

# ----------- SONUÇ -----------

if filtreli:
    secim = random.choice(filtreli)

    st.image(secim["img"], use_column_width=True)
    st.markdown(f"<div class='card'>{secim['ad']}</div>", unsafe_allow_html=True)

# ----------- RANDOM -----------

if st.button("🎲 Rastgele"):
    secim = random.choice(yemekler)
    st.image(secim["img"], use_column_width=True)
    st.markdown(f"<div class='card'>{secim['ad']}</div>", unsafe_allow_html=True)
