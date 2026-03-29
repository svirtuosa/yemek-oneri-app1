import streamlit as st

st.set_page_config(page_title="🍽️ Akıllı Yemek Önerici", layout="centered")

# -----------------------------
# CSS (ORTALAMA + TEMİZ UI)
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 600px;
    margin: auto;
    padding: 2rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = {}

# -----------------------------
# SORULAR (7 ADET)
# -----------------------------
questions = [
    {"q": "Hangi öğün?", "type": "single", "options": ["Kahvaltı", "Öğle", "Akşam"]},
    {"q": "Ne kadar zamanın var?", "type": "single", "options": ["<15 dk", "15-30 dk", "30+ dk"]},
    {"q": "Beslenme tercihin?", "type": "multi", "options": ["Et", "Tavuk", "Sebze", "Vegan"]},
    {"q": "Nasıl bir yemek istersin?", "type": "single", "options": ["Hafif", "Doyurucu", "Sağlıklı"]},
    {"q": "Ruh halin?", "type": "single", "options": ["Yorgun", "Stresli", "Mutlu"]},
    {"q": "Evde ne var?", "type": "multi", "options": ["Tavuk", "Et", "Sebze", "Makarna"]},
    {"q": "Uğraş seviyesi?", "type": "single", "options": ["Pratik", "Orta", "Detaylı"]}
]

# -----------------------------
# YEMEK VERİ TABANI
# -----------------------------
meals = [
    {
        "name": "Tavuk Sote",
        "type": ["Tavuk"],
        "time": "<15 dk",
        "cal": 400,
        "tags": ["Hafif", "Pratik"],
        "ingredients": ["Tavuk", "Biber", "Soğan"],
        "recipe": ["Tavukları doğra", "Tavada pişir", "Sebzeleri ekle", "Baharatla"]
    },
    {
        "name": "Izgara Tavuk Salata",
        "type": ["Tavuk"],
        "time": "<15 dk",
        "cal": 300,
        "tags": ["Sağlıklı", "Hafif"],
        "ingredients": ["Tavuk", "Marul", "Domates"],
        "recipe": ["Tavuğu ızgara yap", "Sebzelerle karıştır"]
    },
    {
        "name": "Sebze Sote",
        "type": ["Sebze", "Vegan"],
        "time": "15-30 dk",
        "cal": 250,
        "tags": ["Hafif", "Sağlıklı"],
        "ingredients": ["Kabak", "Biber", "Havuç"],
        "recipe": ["Sebzeleri doğra", "Tavada pişir"]
    },
    {
        "name": "Kıymalı Makarna",
        "type": ["Et"],
        "time": "30+ dk",
        "cal": 650,
        "tags": ["Doyurucu"],
        "ingredients": ["Kıyma", "Makarna"],
        "recipe": ["Kıymayı pişir", "Makarnayı haşla", "Karıştır"]
    }
]

# -----------------------------
# SORU AKIŞI
# -----------------------------
st.title("🍽️ Yemek Önerici")

if st.session_state.step < len(questions):
    q_data = questions[st.session_state.step]
    st.subheader(q_data["q"])

    # Çoklu seçim
    if q_data["type"] == "multi":
        selected = st.multiselect("", q_data["options"])
    else:
        selected = st.radio("", q_data["options"])

    # Otomatik geçiş
    if selected:
        st.session_state.answers[q_data["q"]] = selected
        st.session_state.step += 1
        st.rerun()

# -----------------------------
# SKORLAMA FONKSİYONU
# -----------------------------
def score_meal(meal, answers):
    score = 0

    # Tür uyumu
    if any(t in answers["Beslenme tercihin?"] for t in meal["type"]):
        score += 3

    # Süre uyumu
    if meal["time"] == answers["Ne kadar zamanın var?"]:
        score += 2

    # Yemek tipi
    if answers["Nasıl bir yemek istersin?"] in meal["tags"]:
        score += 2

    # Malzeme uyumu
    if any(i in answers["Evde ne var?"] for i in meal["ingredients"]):
        score += 2

    # Pratiklik
    if answers["Uğraş seviyesi?"] == "Pratik" and meal["time"] == "<15 dk":
        score += 1

    return score

# -----------------------------
# SONUÇ EKRANI
# -----------------------------
else:
    st.subheader("🎯 Senin için öneriler")

    scored = [(meal, score_meal(meal, st.session_state.answers)) for meal in meals]
    scored.sort(key=lambda x: x[1], reverse=True)

    main, alt1, alt2 = scored[0][0], scored[1][0], scored[2][0]

    def show(meal, title):
        st.markdown(f"### {title}: {meal['name']}")
        st.write(f"Süre: {meal['time']}")
        st.write(f"Kalori: {meal['cal']} kcal")

    show(main, "Ana Yemek")
    show(alt1, "Alternatif")
    show(alt2, "Alternatif")

    # Tarif isteği
    if st.button("Tarifini görmek ister misiniz?"):
        st.markdown(f"## 📖 {main['name']} Tarifi")

        st.write("**Malzemeler:**")
        for i in main["ingredients"]:
            st.write(f"- {i}")

        st.write("**Adımlar:**")
        for step in main["recipe"]:
            st.write(f"- {step}")
