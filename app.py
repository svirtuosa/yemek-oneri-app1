import streamlit as st

st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
    url("https://raw.githubusercontent.com/svirtuosa/yemek-oneri-app1/main/bg.png");
    background-size: cover;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Yemek Öneri", page_icon="🍽️")

st.title("🍽️ Yemek Öneri Sistemi")

ogun = st.selectbox("Öğün seç:", ["kahvaltı", "öğle", "akşam", "tatlı"])

# ---------------- KAHVALTI ----------------
if ogun == "kahvaltı":
    tat = st.selectbox("Tat seç:", ["tatlı", "tuzlu", "hafif"])

    if tat == "tatlı":
        pisirme = st.selectbox("Pişirme yöntemi:", ["tava", "fırın", "pişirmeden"])

        if pisirme == "tava":
            st.success("🥞 Pankek")
        elif pisirme == "fırın":
            st.success("🍰 Kek")
        else:
            st.success("🥣 Meyveli yoğurt veya yulaf")

    elif tat == "tuzlu":
        baz = st.selectbox("Baz seç:", ["yumurta", "ekmek"])

        if baz == "yumurta":
            st.success("🍳 Menemen / Omlet / Haşlanmış yumurta")
        else:
            st.success("🥪 Tost / Sandviç / Kızarmış ekmek")

    else:
        st.success("🥗 Salata / Kefir + meyve / Yoğurt / Meyve tabağı")

# ---------------- ÖĞLE ----------------
elif ogun == "öğle":
    tat = st.selectbox("Tat seç:", ["tatlı", "tuzlu"])

    if tat == "tatlı":
        st.success("🍓 Meyveli yoğurt / Yulaf / Smoothie / Meyve + kuruyemiş")

    else:
        tur = st.selectbox("Tür seç:", ["sıcak", "soğuk", "pratik"])

        if tur == "sıcak":
            st.success("🍝 Makarna / Tavuk / Sebze yemeği")
        elif tur == "soğuk":
            st.success("🥗 Salata / Sandviç / Yoğurtlu kase")
        else:
            st.success("⚡ Tost / Makarna / Sandviç")

# ---------------- AKŞAM ----------------
elif ogun == "akşam":
    tur = st.selectbox("Nasıl bir yemek?", ["hafif", "doyurucu", "pratik"])

    if tur == "hafif":
        st.success("🥗 Salata / Yoğurtlu kase / Sebze")
    elif tur == "doyurucu":
        st.success("🍗 Tavuk / Makarna / Sebze + yoğurt")
    else:
        st.success("⚡ Tost / Sandviç / Makarna")

# ---------------- TATLI ----------------
else:
    st.success("🍫 Fit tiramisu / Fit brownie / Fit cheesecake / Fit magnolia / Hurmalı trüf")

