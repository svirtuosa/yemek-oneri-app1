import streamlit as st
import base64
import os

st.set_page_config(page_title="🍽️ Şefin Mutfağı | Akıllı Yemek Önerici", layout="centered")

# -----------------------------
# CSS
# -----------------------------
def set_bg():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
        url("https://images.unsplash.com/photo-1556910103-1c02745aae4d");
        background-size: cover;
    }
    .block-container {
        background: rgba(255,255,255,0.05);
        padding: 3rem;
        border-radius: 25px;
    }
    h1,h2,h3,p,div {color:white !important;}
    </style>
    """, unsafe_allow_html=True)

set_bg()

# ================================
# 🔴 SENİN TÜM TARİFLERİN
# ================================

# RECIPE_DATABASE kısmına eklenecekler:
NEW_RECIPES = {
    "Menemen": {
        "desc": "Bol sulu domates, taze yeşil biber ve tam kıvamında pişmiş yumurtanın uyumu.",
        "time": "15 dk", "cal": "210 kcal",
        "ing": ["3 adet yumurta", "3 adet sivri biber", "2 adet büyük domates (rendelenmiş)", "1 yk tereyağı", "5g tuz"],
        "steps": ["Biberleri tereyağında hafifçe öldürün.", "Domatesleri ekleyip suyunu biraz çekene kadar pişirin.", "Yumurtaları kırıp sarılarını dağıtmadan 2 dk pişirin."],
        "tips": "Domateslerin kabuklarını mutlaka soyun."
    },
    "Tavuk Fajita": {
        "desc": "Renkli biberler ve soğan eşliğinde yüksek ateşte mühürlenmiş baharatlı tavuk şeritleri.",
        "time": "20 dk", "cal": "380 kcal",
        "ing": ["400g tavuk göğsü", "1 adet kırmızı kapya biber", "1 adet sarı dolmalık biber", "1 orta boy soğan", "3 yk zeytinyağı", "1 tk kimyon"],
        "steps": ["Tavukları ve sebzeleri uzun şeritler halinde doğrayın.", "Döküm tavada önce tavukları mühürleyin.", "Sebzeleri ekleyip diriliklerini kaybetmeden yüksek ateşte çevirin."],
        "tips": "Tavayı çok doldurmayın ki sebzeler haşlanmasın, sotelensin."
    },
    "Izgara Köfte": {
        "desc": "Anne usulü, az baharatlı ve bol sulu dana köftesi.",
        "time": "25 dk", "cal": "420 kcal",
        "ing": ["500g orta yağlı dana kıyma", "1 adet soğan (rendelenmiş)", "1/2 demet maydanoz", "1 çay bardağı galeta unu", "1 tk kimyon"],
        "steps": ["Kıyma ve tüm malzemeyi 10 dk yoğurun.", "Ceviz büyüklüğünde parçalar koparıp şekil verin.", "Kızgın tavada her yüzünü 4'er dakika pişirin."],
        "tips": "Harcı buzdolabında 1 saat dinlendirmek lezzeti artırır."
    },
    "Mantar Soslu Bonfile": {
        "desc": "Mühürlenmiş dana bonfile üzerinde kremsi kestane mantarı sosu.",
        "time": "30 dk", "cal": "520 kcal",
        "ing": ["2 dilim bonfile (200g/adet)", "150g kestane mantarı", "100ml krema", "1 dal taze biberiye", "2 diş sarımsak"],
        "steps": ["Etleri yüksek ateşte mühürleyip kenara alın.", "Aynı tavada dilimlenmiş mantarları soteleyin.", "Krema ve biberiyeyi ekleyip sos koyulaşınca eti tekrar içine koyun."],
        "tips": "Eti pişirdikten sonra 5 dk dinlendirmeyi unutmayın."
    },
    "Pankek": {
        "desc": "Pofuduk dokulu, akçaağaç şurubu veya bal ile servis edilen kahvaltılık.",
        "time": "20 dk", "cal": "310 kcal",
        "ing": ["2 adet yumurta", "1.5 su bardağı süt", "2 su bardağı un", "2 yk toz şeker", "1 paket kabartma tozu"],
        "steps": ["Sıvı ve kuru malzemeleri pürüzsüz olana dek çırpın.", "Yağsız tavaya bir küçük kepçe dökün.", "Üzeri göz göz olunca ters çevirin."],
        "tips": "Tavanın aşırı ısınmamasına dikkat edin, yoksa içi çiğ kalır."
    },
    "Shakshuka (Şakşuka)": {
        "desc": "Kızarmış sebzelerin sarımsaklı domates sosu ile buluşması.",
        "time": "40 dk", "cal": "240 kcal",
        "ing": ["2 adet patlıcan", "2 adet kabak", "3 adet sivri biber", "4 adet domates", "3 diş sarımsak"],
        "steps": ["Patlıcan ve kabakları küp doğrayıp kızartın.", "Domates ve sarımsakla yoğun bir sos hazırlayın.", "Kızarmış sebzeleri sosla harmanlayıp soğuk servis yapın."],
        "tips": "Patlıcanların acısını almak için tuzlu suda bekletin."
    },
    "Mercimek Çorbası": {
        "desc": "Süzme kıvamında, tereyağlı ve limonlu klasik başlangıç.",
        "time": "35 dk", "cal": "160 kcal",
        "ing": ["1 su bardağı kırmızı mercimek", "1 adet havuç", "1 adet patates", "1 yk tereyağı", "1.5 litre sıcak su"],
        "steps": ["Tüm sebzeleri tencereye alıp haşlayın.", "Sebzeler yumuşayınca blenderdan geçirin.", "Tereyağında yaktığınız pul biberi üzerine gezdirin."],
        "tips": "İçine ekleyeceğiniz bir parça kemik suyu lezzeti ikiye katlar."
    },
    "Tavuklu Sezar Salata": {
        "desc": "Izgara tavuk, kruton ve parmesan peynirli zengin salata.",
        "time": "20 dk", "cal": "340 kcal",
        "ing": ["1 adet tavuk göğsü", "1 baş marul", "1/2 su bardağı kruton", "3 yk Sezar sos", "50g parmesan"],
        "steps": ["Tavukları ızgara yapıp dilimleyin.", "Marulları elle parçalayıp sosla karıştırın.", "Tavuk ve krutonları üzerine ekleyin."],
        "tips": "Marullar mutlaka kurutulmuş olmalı, yoksa sosu sulandırır."
    },
    "Mercimek Köftesi": {
        "desc": "Kırmızı mercimek ve ince bulgurun taze yeşilliklerle buluştuğu çay saati klasiği.",
        "time": "50 dk", "cal": "280 kcal",
        "ing": ["1 su bardağı kırmızı mercimek", "1.5 su bardağı ince bulgur", "1 adet soğan", "2 yk salça", "1 demet taze soğan"],
        "steps": ["Mercimeği haşlayıp suyunu çekince içine bulguru ekleyip bekletin.", "Kavrulmuş soğan ve salçayı karışıma yedirin.", "Yeşillikleri ekleyip şekil verin."],
        "tips": "Yoğururken elinizi ara ara soğuk suyla ıslatın."
    },
    "Izgara Çipura": {
        "desc": "Sadece zeytinyağı, limon ve tuz ile tatlandırılmış Ege klasiği.",
        "time": "25 dk", "cal": "320 kcal",
        "ing": ["1 adet bütün çipura", "3 yk zeytinyağı", "1/2 limon", "1 dal taze kekik", "2 diş sarımsak"],
        "steps": ["Balığın üzerine çizikler atın.", "Zeytinyağı, sarımsak ve kekik ile marine edin.", "Izgara tavasında her yüzünü 8-10 dk pişirin."],
        "tips": "Balığın içinin pişmesi için çok yüksek ateşte pişirmeyin."
    },
    "Falafel": {
        "desc": "Orta Doğu mutfağından, dışı çıtır içi yumuşak baharatlı nohut köftesi.",
        "time": "45 dk", "cal": "310 kcal",
        "ing": ["2 su bardağı haşlanmış nohut", "1 adet soğan", "3 diş sarımsak", "1 demet maydanoz", "1 tatlı kaşığı kişniş"],
        "steps": ["Nohut ve tüm malzemeyi mutfak robotundan geçirin.", "Ceviz büyüklüğünde toplar yapıp dolapta 20 dk dinlendirin.", "Kızgın derin yağda altın sarısı olana dek kızartın."],
        "tips": "Nohutların çok sulu olmamasına dikkat edin, yoksa dağılır."
    },
    "Penne Arrabbiata": {
        "desc": "Acı pul biber ve sarımsaklı domates soslu İtalyan makarnası.",
        "time": "20 dk", "cal": "380 kcal",
        "ing": ["250g penne makarna", "3 adet domates", "2 diş sarımsak", "1 yk acı pul biber", "2 yk zeytinyağı"],
        "steps": ["Makarnayı bol tuzlu suda 'al dente' haşlayın.", "Zeytinyağında sarımsak ve pul biberi kokusu çıkana dek soteleyin.", "Domates sosuyla makarnayı yüksek ateşte harmanlayın."],
        "tips": "Makarnanın haşlama suyundan bir kepçe sosa eklemek kıvamı artırır."
    },
    "Ev Yapımı Burger": {
        "desc": "Karamele soğan ve cheddar peynirli, %100 dana etinden sulu burger.",
        "time": "30 dk", "cal": "650 kcal",
        "ing": ["200g dana döş kıyma", "1 adet burger ekmeği", "1 dilim cheddar peyniri", "1 adet soğan", "1 yk mayonez"],
        "steps": ["Kıymayı sadece tuz ve karabiberle yoğurup şekil verin.", "Soğanları düşük ateşte şekerle karamelize edin.", "Eti döküm tavada pişirip üzerine cheddar koyup eritin."],
        "tips": "Eti pişirirken üzerine spatulayla bastırmayın, suyu içinde kalsın."
    },
    "Sebzeli Pad Thai": {
        "desc": "Uzak Doğu usulü, fıstıklı ve soya soslu pirinç eriştesi.",
        "time": "25 dk", "cal": "420 kcal",
        "ing": ["150g pirinç eriştesi", "1 adet havuç", "1 adet kapya biber", "2 yk soya sosu", "1 yk yer fıstığı"],
        "steps": ["Erişteleri sıcak suda yumuşatın.", "Sebzeleri wok tavada yüksek ateşte hızlıca soteleyin.", "Erişte ve sosu ekleyip fıstıklarla süsleyerek servis edin."],
        "tips": "Sebzelerin çıtır kalması için pişirme süresini kısa tutun."
    },
    "Mantar Risotto": {
        "desc": "Arborio pirinci ve taze mantarlarla hazırlanan kremsi İtalyan pilavı.",
        "time": "40 dk", "cal": "440 kcal",
        "ing": ["1 su bardağı arborio pirinci", "200g mantar", "1 lt sebze suyu", "50g parmesan", "2 yk tereyağı"],
        "steps": ["Pirinci tereyağında şeffaflaşana dek kavurun.", "Sıcak sebze suyunu kepçe kepçe ekleyip sürekli karıştırın.", "Pirinç yumuşayınca peynir ve sotelenmiş mantarları ekleyin."],
        "tips": "Risottoyu asla durulamayın, nişastası kremsi doku için gereklidir."
    },
    "Çıtır Tavuk Kanat": {
        "desc": "Özel mısır gevrekli kaplamasıyla dışı aşırı çıtır kanatlar.",
        "time": "35 dk", "cal": "520 kcal",
        "ing": ["500g tavuk kanat", "1 su bardağı mısır gevreği (ufalanmış)", "1 adet yumurta", "1 su bardağı un", "1 tk toz kırmızı biber"],
        "steps": ["Kanatları önce una, sonra yumurtaya, en son mısır gevreğine bulayın.", "180 derece yağda 10-12 dakika kızartın.", "Acı sos ile servis edin."],
        "tips": "Mısır gevreğini çok un ufak etmeyin, parçalı kalsın."
    },
    "Humus Yatağında Mantar": {
        "desc": "Pürüzsüz humus üzerinde sotelenmiş baharatlı istiridye mantarı.",
        "time": "20 dk", "cal": "290 kcal",
        "ing": ["1 su bardağı haşlanmış nohut", "2 yk tahin", "150g istiridye mantarı", "1/2 limon", "1 diş sarımsak"],
        "steps": ["Nohut, tahin ve limon suyunu blenderdan geçirip pürüzsüz humus yapın.", "Mantarları yüksek ateşte soteleyin.", "Humusun üzerine mantarları ve zeytinyağını ekleyin."],
        "tips": "Humusun pürüzsüz olması için nohutların kabuklarını soyun."
    },
    "Ev Yapımı Pizza": {
        "desc": "İnce hamurlu, bol mozzarellalı ve taze fesleğenli Margarita pizza.",
        "time": "60 dk", "cal": "580 kcal",
        "ing": ["2 su bardağı un", "1 yk kuru maya", "200g mozzarella", "1 su bardağı domates püresi", "5 yaprak fesleğen"],
        "steps": ["Hamuru yoğurup 30 dk mayalandırın.", "İncecik açıp üzerine sos ve peyniri yayın.", "250 derece fırında 10-12 dk pişirin."],
        "tips": "Fırını en yüksek dereceye getirip önceden ısıtın."
    },
    "Kinoa Salatası": {
        "desc": "Yüksek proteinli, narlı ve taze otlu besleyici vegan salata.",
        "time": "20 dk", "cal": "260 kcal",
        "ing": ["1 su bardağı kinoa", "1/2 adet nar", "1 adet salatalık", "1 demet maydanoz", "2 yk zeytinyağı"],
        "steps": ["Kinoayı haşlayıp soğutun.", "Sebzeleri küçük küpler halinde doğrayın.", "Tüm malzemeyi nar ekşisi ve zeytinyağı ile harmanlayın."],
        "tips": "Kinoayı haşlamadan önce iyice yıkayarak acı tadını atın."
    },
    "Mercimekli Vegan Burger": {
        "desc": "Et tadını aratmayan, doyurucu yeşil mercimek köfteli burger.",
        "time": "40 dk", "cal": "390 kcal",
        "ing": ["1 su bardağı yeşil mercimek", "1/2 su bardağı yulaf ezmesi", "1 adet soğan", "1 tk kimyon", "1 yk salça"],
        "steps": ["Haşlanmış mercimeği yulaf ve baharatla robottan geçirin.", "Köfte şekli verip tavada arkalı önlü pişirin.", "Vegan mayonez ve marul ile servis edin."],
        "tips": "Harcın kıvamı yumuşak olursa biraz daha yulaf ekleyin."
    },
    "Somon Izgara": {
        "desc": "Portakal aromalı marinasyon ile fırınlanmış, içi sulu dışı hafif karamelize somon.",
        "time": "20 dk", "cal": "410 kcal",
        "ing": ["200g somon filato", "1/2 portakal suyu", "1 yk bal", "1 yk soya sosu", "1 dal taze kekik"],
        "steps": ["Portakal suyu, bal ve soya sosunu karıştırıp somonu 10 dk marine edin.", "Yağlı kağıt serili tepsiye alıp kalan sosu üzerine dökün.", "200 derece fırında 12-15 dk pişirin."],
        "tips": "Somonun kurumaması için iç sıcaklığı 55-60 dereceyi geçmemelidir."
    },
    "Ezogelin Çorbası": {
        "desc": "Anadolu mutfağının bol baharatlı, bulgur ve pirinçli doyurucu mercimek çorbası.",
        "time": "40 dk", "cal": "190 kcal",
        "ing": ["1 su bardağı kırmızı mercimek", "1 yk bulgur", "1 yk pirinç", "1 yk kuru nane", "1 yk tereyağı"],
        "steps": ["Mercimek, bulgur ve pirinci yumuşayana kadar haşlayın.", "Soğanı tereyağında kavurup salça ve naneyi ekleyin.", "Sosu tencereye boşaltıp 10 dk daha kısık ateşte kaynatın."],
        "tips": "Naneyi yağda yakarken renginin kararmamasına dikkat edin."
    },
    "San Sebastian Cheesecake": {
        "desc": "Dışı yanık, içi akışkan ve kremsi dokulu meşhur Bask keki.",
        "time": "60 dk", "cal": "480 kcal",
        "ing": ["500g labne peyniri", "250g sıvı krema", "3 adet yumurta", "1 su bardağı toz şeker", "1 yk un"],
        "steps": ["Peynir ve şekeri pürüzsüz olana dek çırpın.", "Yumurtaları tek tek ekleyip karıştırın, en son krema ve unu ilave edin.", "210 derece fırında üzeri koyu kahverengi olana dek 25-30 dk pişirin."],
        "tips": "Fırından çıkınca sallandığında jöle gibi titremeli, oda sıcaklığında dinlendirilmelidir."
    },
    "Karides Güveç": {
        "desc": "Sarımsaklı tereyağı ve mantarla fırınlanmış, kaşar peynirli karides.",
        "time": "25 dk", "cal": "320 kcal",
        "ing": ["300g ayıklanmış karides", "2 diş sarımsak", "100g mantar", "50g kaşar peyniri", "2 yk tereyağı"],
        "steps": ["Mantarları ve sarımsağı tereyağında soteleyin.", "Karidesleri ekleyip 2 dk çevirdikten sonra güveç kabına alın.", "Üzerine kaşar rendesi serpip fırında peynirler kızarana dek tutun."],
        "tips": "Karidesleri tavada çok pişirmeyin, fırında da pişecekleri için sertleşebilirler."
    },
    "Kıymalı Tarhana Çorbası": {
        "desc": "Geleneksel ev tarhanasının kıyma ve bol sarımsakla güçlendirilmiş hali.",
        "time": "20 dk", "cal": "220 kcal",
        "ing": ["4 yk toz tarhana", "100g dana kıyma", "2 diş sarımsak", "1 yk tereyağı", "1 tk pul biber"],
        "steps": ["Tarhanayı bir bardak suyla önceden ıslatın.", "Kıymayı tereyağında kavurun, sarımsak ve salçayı ekleyin.", "Islanmış tarhanayı ve suyu ekleyip sürekli karıştırarak pişirin."],
        "tips": "Topaklanmaması için kaynayana kadar karıştırmayı asla bırakmayın."
    },
    "Magnolia (Muzlu)": {
        "desc": "Hafif pastacı kreması, bebe bisküvisi ve taze muz dilimlerinin birleşimi.",
        "time": "30 dk", "cal": "350 kcal",
        "ing": ["1 lt süt", "2 yk nişasta", "1 paket bebe bisküvisi", "2 adet muz", "1 paket sıvı krema"],
        "steps": ["Süt, şeker ve nişastayı pişirip soğutun.", "Soğuyan karışıma çırpılmış kremayı ekleyin.", "Bisküvi, krema ve muz dilimlerini bardaklara kat kat dizin."],
        "tips": "Kremayı eklemeden önce muhallebinin tamamen soğuk olduğundan emin olun."
    },
    "Levrek Buğulama": {
        "desc": "Kendi suyunda, sebzeler ve defne yaprağı ile pişen hafif deniz yemeği.",
        "time": "35 dk", "cal": "280 kcal",
        "ing": ["2 adet levrek fileto", "1 adet patates", "1 adet soğan", "2 dal defne yaprağı", "1/2 çay bardağı zeytinyağı"],
        "steps": ["Sebzeleri ince halkalar şeklinde doğrayıp tencere tabanına dizin.", "Üzerine balıkları ve defne yapraklarını yerleştirin.", "Zeytinyağı ve az su ekleyip kapağı kapalı şekilde kısık ateşte pişirin."],
        "tips": "Suyuna bir dilim limon eklemek balığın kokusunu dengeler."
    },
    "Chia Tohumlu Puding": {
        "desc": "Badem sütü ve meyvelerle hazırlanan, şeker ilavesiz sağlıklı vegan tatlı.",
        "time": "10 dk", "cal": "180 kcal",
        "ing": ["1 su bardağı badem sütü", "3 yk chia tohumu", "1 yk bal veya akçaağaç şurubu", "5 adet çilek"],
        "steps": ["Süt, chia ve balı karıştırıp buzdolabında en az 4 saat bekletin.", "Jöle kıvamına gelince karıştırın.", "Üzerini taze çileklerle süsleyerek servis edin."],
        "tips": "Bekleme süresinde ilk 1 saat içinde 2 kez karıştırmak topaklanmayı önler."
    },
    "Domates Çorbası (Közlenmiş)": {
        "desc": "Közlenmiş domates ve biberlerin isli tadıyla hazırlanan yoğun kıvamlı çorba.",
        "time": "40 dk", "cal": "140 kcal",
        "ing": ["5 adet domates", "2 adet kapya biber", "1 yk un", "1 yk tereyağı", "Rendelenmiş kaşar"],
        "steps": ["Domates ve biberleri fırında közleyip kabuklarını soyun.", "Unu yağda kavurup közlenmiş sebzeleri ekleyin ve blenderdan geçirin.", "Süt ekleyerek kıvamını açın ve kaşar peyniriyle servis edin."],
        "tips": "Közleme işlemi çorbaya derinlik ve isli bir aroma katar."
    },
    "Fırın Sütlaç": {
        "desc": "Nişastasız, sadece pirinç ve sütün özleşmesiyle pişen, üzeri yanık geleneksel tatlı.",
        "time": "50 dk", "cal": "310 kcal",
        "ing": ["1 lt tam yağlı süt", "1/2 su bardağı pirinç", "1 su bardağı toz şeker", "2 su bardağı su"],
        "steps": ["Pirinçleri suda iyice yumuşayana kadar haşlayın.", "Sütü ve şekeri ekleyip kıvam alana kadar yaklaşık 30 dk kaynatın.", "Güveçlere paylaştırıp fırının sadece üst ızgara ayarında üzerini yakın."],
        "tips": "Fırın tepsisine güveçlerin yarısına gelecek kadar su koyun ki altı kurumasın."
    },


}


# ================================
# DATABASE
# ================================
RECIPE_DATABASE = {
    "Çılbır": {
        "desc": "Klasik",
        "time": "15 dk","cal":"280 kcal",
        "ing":["yumurta"],
        "steps":["yap"],
        "tips":"afiyet"
    }
}

RECIPE_DATABASE.update(NEW_RECIPES)
RECIPE_DATABASE.update(VEGAN_FAST_PASTA)

# ================================
# MEALS
# ================================
meals = [
    {"name":"Menemen","cat":"Kahvaltı","time":"<15 dk","tags":["Sağlıklı","Pratik"]},
    {"name":"Tavuk Fajita","cat":"Akşam","time":"15-30 dk","tags":["Tavuk","Doyurucu"]},
    {"name":"Izgara Köfte","cat":"Akşam","time":"15-30 dk","tags":["Et ağırlıklı","Doyurucu"]},
    {"name":"Mantar Soslu Bonfile","cat":"Akşam","time":"15-30 dk","tags":["Et ağırlıklı","Detaylı"]},
    {"name":"Pankek","cat":"Kahvaltı","time":"15-30 dk","tags":["Kaçamak"]},
    {"name":"Shakshuka (Şakşuka)","cat":"Öğle","time":"30+ dk","tags":["Vegan"]},
    {"name":"Mercimek Çorbası","cat":"Öğle","time":"30+ dk","tags":["Sağlıklı"]},
    {"name":"Tavuklu Sezar Salata","cat":"Öğle","time":"15-30 dk","tags":["Tavuk"]},
    {"name":"Mercimek Köftesi","cat":"Öğle","time":"30+ dk","tags":["Vegan"]},
    {"name":"Izgara Çipura","cat":"Akşam","time":"15-30 dk","tags":["Sağlıklı"]},
    {"name":"Falafel","cat":"Öğle","time":"30+ dk","tags":["Vegan"]},

    {"name":"Falafel","cat":"Öğle","time":"30+ dk","tags":["Vegan","Sağlıklı","Yüksek protein"]},
    {"name":"Penne Arrabbiata","cat":"Akşam","time":"15-30 dk","tags":["Makarna","Pratik"]},
    {"name":"Ev Yapımı Burger","cat":"Akşam","time":"15-30 dk","tags":["Kaçamak","Doyurucu"]},
    {"name":"Sebzeli Pad Thai","cat":"Akşam","time":"15-30 dk","tags":["Vegan","Uzak Doğu"]},
    {"name":"Mantar Risotto","cat":"Akşam","time":"30+ dk","tags":["Makarna","Detaylı"]},
    {"name":"Çıtır Tavuk Kanat","cat":"Akşam","time":"30+ dk","tags":["Kaçamak","Tavuk"]},
    {"name":"Humus Yatağında Mantar","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Sağlıklı"]},
    {"name":"Ev Yapımı Pizza","cat":"Akşam","time":"30+ dk","tags":["Kaçamak","Doyurucu"]},
    {"name":"Kinoa Salatası","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Mercimekli Vegan Burger","cat":"Öğle","time":"30+ dk","tags":["Vegan","Doyurucu"]}






]



# ================================
# UI (aynı kaldı)
# ================================
st.title("🍽️ Yemek Önerici")
st.write("Hazır.")
