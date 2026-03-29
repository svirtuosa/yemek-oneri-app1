import streamlit as st
import base64
import os

st.set_page_config(page_title="🍽️ Şefin Mutfağı | Akıllı Yemek Önerici", layout="centered")

# -----------------------------
# CSS
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
            background: rgba(0,0,0,0.6);
            padding: 2rem;
            border-radius: 15px;
            max-width: 600px;
            margin: auto;
        }}

        h1, h2, h3, h4, p, div {{
            color: white !important;
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("bg.PNG bulunamadı. Aynı klasöre ekle.")
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
    "Guacamole Soslu Nachos": {
        "desc": "Olgun avokado, misket limonu ve taze kişnişli dip sos ile çıtır mısır cipsi.",
        "time": "15 dk", "cal": "320 kcal",
        "ing": ["2 adet olgun avokado", "1 adet küçük mor soğan", "1/2 misket limonu suyu", "1 paket mısır cipsi", "1 yk zeytinyağı"],
        "steps": ["Avokadoları çatal yardımıyla ezin.", "İnce kıyılmış soğan, kişniş ve limon suyunu ekleyip karıştırın.", "Cipslerle birlikte servis tabağına alın."],
        "tips": "Avokadonun kararmaması için çekirdeğini sosun içine koyup servis anına kadar bekletebilirsiniz."
    },
    "Buharda Sebzeli Gyozza": {
        "desc": "Uzak Doğu usulü, ince hamura sarılı sebze dolgulu Japon mantısı.",
        "time": "45 dk", "cal": "260 kcal",
        "ing": ["20 adet hazır gyoza hamuru", "200g ince kıyılmış lahana", "1 adet havuç", "2 yk soya sosu", "1 tk rendelenmiş taze zencefil"],
        "steps": ["Sebzeleri soya sosu ve zencefille soteleyip soğutun.", "Hamurların ortasına harcı koyup yarım ay şeklinde kapatın ve kenarlarını büzün.", "Buhar tenceresinde 10-12 dakika pişirin."],
        "tips": "Pişirmeden hemen önce tabanlarını tavada hafifçe kızartmak kıtırlık katar."
    },
    "Gavurdağı Salatası": {
        "desc": "İnce kıyılmış domates ve salatalığın bol ceviz ve nar ekşisiyle imza buluşması.",
        "time": "20 dk", "cal": "180 kcal",
        "ing": ["3 adet domates", "2 adet yeşil biber", "1/2 su bardağı ceviz içi", "3 yk nar ekşisi", "1 tatlı kaşığı sumak"],
        "steps": ["Tüm sebzeleri tavla zarı formunda çok küçük doğrayın.", "Nar ekşisi, zeytinyağı ve sumağı küçük bir kapta çırpın.", "Sebzeleri sosla harmanlayıp üzerine iri kırılmış cevizleri serpin."],
        "tips": "Domateslerin çekirdekli kısımlarını çıkarırsanız salatanız fazla sulanmaz."
    },
    "Lazanya (Bolognese)": {
        "desc": "Kat kat lazanya hamuru, yoğun kıymalı sos ve ipeksi beşamelin fırınlanmış hali.",
        "time": "70 dk", "cal": "620 kcal",
        "ing": ["12 adet lazanya yaprağı", "300g kıyma", "500ml beşamel sos", "200g rendelenmiş kaşar", "1 adet soğan"],
        "steps": ["Kıymayı soğan ve domates püresiyle pişirip bolonez sos hazırlayın.", "Fırın kabına sırasıyla sos, lazanya yaprağı ve beşamel dizin.", "En üste peyniri döküp 180 derece fırında 35 dk pişirin."],
        "tips": "Lazanya yapraklarını haşlamadan kullanacaksanız sosunuzu biraz sulu tutun."
    },
    "Falafel Salatası": {
        "desc": "Çıtır falafel toplarının tahin sos ve Akdeniz yeşillikleriyle modern sunumu.",
        "time": "25 dk", "cal": "340 kcal",
        "ing": ["6 adet hazır veya ev yapımı falafel", "1 kase Akdeniz yeşilliği", "2 yk tahin", "1/2 limon suyu", "5 adet çeri domates"],
        "steps": ["Yeşillikleri geniş bir kaseye alın.", "Tahin, limon suyu ve az suyu çırparak akışkan bir sos elde edin.", "Falafelleri yeşilliklerin üzerine dizip sosu gezdirin."],
        "tips": "Sosa bir diş ezilmiş sarımsak eklemek lezzeti derinleştirir."
    },
    "Karidesli Linguine": {
        "desc": "Sarımsak, acı biber ve beyaz şarap (veya üzüm suyu) aromalı lüks makarna.",
        "time": "25 dk", "cal": "410 kcal",
        "ing": ["250g linguine makarna", "200g ayıklanmış karides", "3 diş sarımsak", "1/2 demet maydanoz", "3 yk zeytinyağı"],
        "steps": ["Makarnayı haşlayın.", "Zeytinyağında sarımsak ve pul biberi kokusu çıkana kadar soteleyip karidesleri ekleyin.", "Haşlanan makarnayı ve ince kıyılmış maydanozu tavaya alıp karıştırın."],
        "tips": "Makarnayı süzmeden doğrudan tavaya alarak nişastalı suyunun sosa karışmasını sağlayın."
    },
    "Atom (Süzme Yoğurtlu Meze)": {
        "desc": "Süzme yoğurt üzerinde tereyağında yakılmış acı Arnavut biberleri.",
        "time": "10 dk", "cal": "210 kcal",
        "ing": ["250g süzme yoğurt", "1 diş sarımsak", "4 adet kurutulmuş Arnavut biberi", "2 yk tereyağı"],
        "steps": ["Yoğurdu ezilmiş sarımsak ve tuz ile çırpıp tabağa yayın.", "Tereyağını tavada kızdırıp içine parçaladığınız kuru biberleri atın.", "Biberli yağı yoğurdun üzerinde gezdirin."],
        "tips": "Biberleri yakarken kokusunun çıkması yeterli, siyahlaşırsa tadı acılaşır."
    },
    "Tavuklu Quesadilla": {
        "desc": "Tortilla ekmeği arasında eriyen peynir ve Meksika baharatlı tavuk dilimleri.",
        "time": "20 dk", "cal": "450 kcal",
        "ing": ["2 adet tortilla ekmeği", "150g tavuk göğsü", "100g rendelenmiş cheddar", "1/2 jülyen doğranmış soğan"],
        "steps": ["Tavukları baharatla soteleyin.", "Tortillanın yarısına peynir ve tavukları koyup ikiye katlayın.", "Tavada her iki yüzünü peynirler eriyene kadar ısıtın."],
        "tips": "Ekmeklerin çıtır olması için tavaya çok az tereyağı sürebilirsiniz."
    },
    "Vişneli Yaprak Sarma": {
        "desc": "Vişne taneleriyle pişirilen, ekşimsi ve hafif tatlı gurme zeytinyağlı.",
        "time": "90 dk", "cal": "220 kcal",
        "ing": ["250g asma yaprağı", "1 su bardağı pirinç", "1/2 su bardağı dondurulmuş vişne", "1 yk kuş üzümü", "1 yk dolmalık fıstık"],
        "steps": ["İç harcı bol soğanlı ve baharatlı hazırlayın.", "Sarmaları tencereye dizip aralarına vişne tanelerini yerleştirin.", "Zeytinyağı ve su ekleyip kısık ateşte pişirin."],
        "tips": "Piştikten sonra tencerede soğumasını beklemek yaprakların kararmasını önler."
    },
    "Beef Stroganoff": {
        "desc": "Krema, hardal ve turşu ile pişmiş yumuşacık dana eti şeritleri.",
        "time": "35 dk", "cal": "540 kcal",
        "ing": ["400g dana bonfile", "1 adet soğan", "100g mantar", "2 yk krema", "1 yk Dijon hardalı"],
        "steps": ["Etleri yüksek ateşte soteleyip kenara alın.", "Soğan ve mantarları kavurup hardal ve kremayı ekleyin.", "Etleri sosla birleştirip 2 dk daha tıkırdatın."],
        "tips": "Turşuları servis yaparken ince kıyılmış olarak üzerine eklemek ferahlık verir."
    },
    "Kabak Mücver": {
        "desc": "Rendelenmiş sakız kabaklarının taze dereotu ve beyaz peynirle fırınlanmış veya az yağda kızartılmış hali.",
        "time": "30 dk", "cal": "220 kcal",
        "ing": ["3 adet kabak", "2 adet yumurta", "1/2 su bardağı un", "100g beyaz peynir", "1/2 demet dereotu"],
        "steps": ["Kabakları rendeleyip sularını iyice sıkın.", "Yumurta, un, peynir ve ince kıyılmış dereotunu ekleyip karıştırın.", "Kaşıkla porsiyonlayıp az yağlı tavada arkalı önlü pişirin."],
        "tips": "Kabağın suyunu ne kadar iyi sıkarsanız mücveriniz o kadar çıtır olur ve un çekmez."
    },
    "Tom Yum Çorbası": {
        "desc": "Tayland mutfağının acı, ekşi ve baharatlı imza karides çorbası.",
        "time": "25 dk", "cal": "180 kcal",
        "ing": ["200g karides", "1 lt tavuk suyu", "2 yk balık sosu", "1 adet limon otu", "3 adet acı biber"],
        "steps": ["Tavuk suyunu limon otu ve zencefille kaynatın.", "Mantarları ve karidesleri ekleyip 5 dk pişirin.", "Limon suyu ve balık sosunu ekleyip taze kişnişle servis edin."],
        "tips": "Limon otu bulamazsanız taze limon kabuğu rendesi kullanabilirsiniz."
    },
    "Paçanga Böreği": {
        "desc": "Pastırma, kaşar peyniri, domates ve biberin çıtır yufka içindeki eşsiz uyumu.",
        "time": "20 dk", "cal": "410 kcal",
        "ing": ["2 adet yufka", "100g pastırma", "150g kaşar peyniri", "1 adet domates", "1 adet yeşil biber"],
        "steps": ["Yufkaları üçgen parçalara bölün.", "İçine pastırma, peynir ve küp doğranmış sebzeleri koyup genişçe sarın.", "Galeta ununa bulayıp kızgın yağda altın rengi olana dek kızartın."],
        "tips": "Domatesin çekirdeklerini çıkarın ki böreğin içini sulandırıp yumuşatmasın."
    },
    "Etli Kuru Fasulye": {
        "desc": "Tereyağlı, bol salçalı ve lokum gibi pişmiş dana etli geleneksel Türk yemeği.",
        "time": "90 dk", "cal": "380 kcal",
        "ing": ["2 su bardağı kuru fasulye", "200g dana kuşbaşı", "1 yk tereyağı", "1 yk biber salçası", "1 adet soğan"],
        "steps": ["Fasulyeleri geceden ıslatın.", "Etleri mühürleyip soğanla kavurun, salçayı ekleyin.", "Fasulyeleri ekleyip kısık ateşte özleşene kadar yaklaşık 1 saat pişirin."],
        "tips": "Pişerken içine atacağınız bir adet kuru acı biber derin bir aroma katar."
    },
    "Zeytinyağlı Enginar": {
        "desc": "Garnitürlü, limonlu ve bol dereotlu, karaciğer dostu hafif Ege yemeği.",
        "time": "40 dk", "cal": "160 kcal",
        "ing": ["4 adet enginar çanağı", "1 su bardağı garnitür", "1 adet portakal suyu", "1/2 su bardağı zeytinyağı", "1 tatlı kaşığı şeker"],
        "steps": ["Enginarları tencereye dizip üzerine garnitürleri paylaştırın.", "Zeytinyağı, portakal suyu, limon ve şekeri karıştırıp üzerine dökün.", "Enginarlar yumuşayana kadar kapağı kapalı pişirin."],
        "tips": "Enginarların kararmaması için pişirene kadar limonlu suda bekletin."
    },
    "Ispanaklı Gül Böreği": {
        "desc": "Elde açma tadında, bol ıspanaklı ve lor peynirli çıtır börek.",
        "time": "45 dk", "cal": "320 kcal",
        "ing": ["3 adet yufka", "500g ıspanak", "150g lor peyniri", "1 adet yumurta sarısı", "1/2 su bardağı süt"],
        "steps": ["Ispanakları soğanla soteleyip peynirle karıştırın.", "Yufkayı dörde bölün, sütlü karışımla ıslatıp harcı koyun ve rulo yapıp dolayın.", "Üzerine yumurta sarısı sürüp 180 derece fırında kızartın."],
        "tips": "Ispanak harcının tamamen soğuk olması yufkanın hamurlaşmasını önler."
    },
    "Ratatouille": {
        "desc": "Fransız usulü, ince dilimlenmiş sebzelerin domates sosu yatağında fırınlanmış hali.",
        "time": "50 dk", "cal": "190 kcal",
        "ing": ["1 adet patlıcan", "1 adet kabak", "2 adet domates", "2 diş sarımsak", "Taze kekik"],
        "steps": ["Sebzeleri çok ince halkalar halinde doğrayın.", "Tabana sarımsaklı domates sosu yayın, sebzeleri sırayla dizin.", "Zeytinyağı ve kekik gezdirip fırında sebzeler yumuşayana dek pişirin."],
        "tips": "Sebzelerin aynı boyutta olması pişme dengesi ve görsel şölen için önemlidir."
    },
    "İçli Köfte (Haşlama)": {
        "desc": "İncecik bulgur dış katmanı ve bol cevizli, baharatlı kıyma harcı.",
        "time": "120 dk", "cal": "350 kcal",
        "ing": ["2 su bardağı ince bulgur", "300g yağsız kıyma (dış için)", "300g orta yağlı kıyma (iç için)", "1/2 su bardağı ceviz"],
        "steps": ["İç harcı soğan ve cevizle kavurup dondurun.", "Bulgurlu dış hamuru iyice yoğurup şekil verin ve harcı içine doldurun.", "Kaynar tuzlu suda köfteler su yüzüne çıkana dek haşlayın."],
        "tips": "İç harcın soğuk, hatta donmuş olması şekil vermeyi çok kolaylaştırır."
    },
    "Karnıyarık": {
        "desc": "Kızarmış patlıcanların kıymalı ve sebzeli harçla doldurulup fırınlanması.",
        "time": "60 dk", "cal": "430 kcal",
        "ing": ["4 adet orta boy patlıcan", "200g kıyma", "2 adet sivri biber", "1 adet domates", "1 yk salça"],
        "steps": ["Patlıcanları alacalı soyup kızartın ve ortalarını açın.", "Kıymalı harcı hazırlayıp patlıcanların içine paylaştırın.", "Salçalı su ekleyip fırında 20 dakika daha pişirin."],
        "tips": "Patlıcanları kızarttıktan sonra kağıt havlu üzerinde bekleterek fazla yağını alın."
    },
    "İrmik Helvası": {
        "desc": "Bol tereyağlı, çam fıstıklı ve tam kıvamında şerbetli klasik tatlı.",
        "time": "30 dk", "cal": "420 kcal",
        "ing": ["1 su bardağı irmik", "100g tereyağı", "1 su bardağı şeker", "1 su bardağı süt", "2 yk çam fıstığı"],
        "steps": ["Tereyağında irmik ve fıstıkları rengi dönene kadar kavurun.", "Süt ve şekerle hazırladığınız sıcak şerbeti yavaşça dökün.", "Kapağı kapalı olarak demlenmeye bırakın."],
        "tips": "Kavurma işlemini kısık ateşte sabırla yaparsanız renk homojen olur."
    },
    "Tavuk Tantuni": {
        "desc": "Mersin usulü, incecik doğranmış tavuk etlerinin sacda baharat ve pamuk yağıyla eşsiz uyumu.",
        "time": "20 dk", "cal": "340 kcal",
        "ing": ["300g tavuk göğsü", "1 adet domates", "1 adet soğan", "1 tatlı kaşığı toz kırmızı biber", "3 yk pamuk yağı"],
        "steps": ["Tavukları tavla zarından küçük doğrayıp haşlayın.", "Sacda yağı kızdırıp tavukları ve biberi ekleyin, azar azar su serperek soteleyin.", "Lavaşın içine sumaklı soğan ve domatesle birlikte sarın."],
        "tips": "Saca eklediğiniz su, etin yumuşak kalmasını ve lavaşın nemlenmesini sağlar."
    },
    "Mantar Kokoreç": {
        "desc": "İnce kıyılmış istiridye mantarlarının bol kekik ve pul biberle kokoreç tadındaki vegan alternatifi.",
        "time": "15 dk", "cal": "180 kcal",
        "ing": ["400g istiridye mantarı", "1 yk tereyağı (veya zeytinyağı)", "1 yk kekik", "1 yk pul biber", "2 adet sivri biber"],
        "steps": ["Mantarları ve biberleri çok ince kıyın.", "Yüksek ateşte mantarlar suyunu salıp çekene kadar soteleyin.", "Baharatları ekleyip ekmek arası veya porsiyon olarak servis edin."],
        "tips": "Mantarları yıkamak yerine nemli bezle silerseniz daha iyi kızarırlar."
    },
    "Beluga Mercimek Salatası": {
        "desc": "Siyah mercimek, kapya biber ve nar ekşili soslu yüksek proteinli gurme salata.",
        "time": "25 dk", "cal": "240 kcal",
        "ing": ["1 su bardağı siyah mercimek", "1 adet közlenmiş kapya biber", "1/2 demet dereotu", "2 yk zeytinyağı", "1 yk hardal"],
        "steps": ["Mercimekleri diri kalacak şekilde haşlayın.", "Köz biberi ve dereotunu incecik kıyıp mercimeğe ekleyin.", "Hardal, zeytinyağı ve limonu çırpıp üzerine gezdirin."],
        "tips": "Mercimekleri süzdükten sonra hemen soslarsanız aromayı daha iyi çekerler."
    },
    "Fit Muzlu Ekmek (Banana Bread)": {
        "desc": "Şeker ilavesiz, tam buğday unu ve olgun muzlarla hazırlanan sağlıklı atıştırmalık.",
        "time": "50 dk", "cal": "210 kcal (dilim)",
        "ing": ["3 adet olgun muz", "2 adet yumurta", "1.5 su bardağı tam buğday unu", "1/2 su bardağı ceviz içi", "1 paket kabartma tozu"],
        "steps": ["Muzları ezin, yumurtalarla çırpın.", "Kuru malzemeleri ekleyip spatula ile karıştırın.", "Yağlı kağıt serili kalıpta 170 derece fırında 40 dk pişirin."],
        "tips": "Muzlar ne kadar kararmışsa kek o kadar tatlı ve aromatik olur."
    },
    "Falafel Burger": {
        "desc": "Dev falafel köftesi, tahinli coleslaw ve avokado dilimleriyle vegan burger.",
        "time": "30 dk", "cal": "420 kcal",
        "ing": ["200g falafel harcı", "1 adet vegan burger ekmeği", "1/4 lahana (ince kıyılmış)", "1 yk tahin", "1/2 avokado"],
        "steps": ["Falafel harcına büyük bir köfte şekli verip kızartın.", "Lahanayı tahin ve limonla karıştırıp salata yapın.", "Ekmeğin içine malzemeleri kat kat dizin."],
        "tips": "Köfteyi pişirirken dağılmaması için harcı buzdolabında iyice dinlendirin."
    },
    "Körili Nohut Yemeği (Chana Masala)": {
        "desc": "Hint mutfağından bol baharatlı, domates soslu ve doyurucu nohut güveci.",
        "time": "35 dk", "cal": "310 kcal",
        "ing": ["2 su bardağı haşlanmış nohut", "1 adet soğan", "2 yk köri", "1 kutu domates püresi", "1 tk taze zencefil"],
        "steps": ["Soğan ve zencefili soteleyin, baharatları ekleyip kokusunu çıkarın.", "Domates püresi ve nohutları ekleyip 15 dk ağır ateşte pişirin.", "Üzerine taze kişniş serperek servis edin."],
        "tips": "Yanında sade basmati pirinç pilavı ile servis yapılması önerilir."
    },
    "Avokadolu Yumurtalı Tost": {
        "desc": "Ekşi mayalı ekmek üzerinde ezilmiş avokado ve poşe yumurta.",
        "time": "15 dk", "cal": "380 kcal",
        "ing": ["1 dilim ekşi mayalı ekmek", "1/2 avokado", "1 adet yumurta", "1 çimdik pul biber", "1/2 limon"],
        "steps": ["Ekmeği kızartın, avokadoyu limon ve tuzla ezip üzerine sürün.", "Yumurtayı poşe teknikle (sirkeli suda) haşlayın.", "Yumurtayı avokadonun üzerine koyup pul biberle süsleyin."],
        "tips": "Avokadonun içine çok az labne peyniri eklemek kremsiliği artırır."
    },
    "Fırınlanmış Baharatlı Karnabahar": {
        "desc": "Tavuk kanadı tadında, çıtır kaplamalı ve acı soslu karnabahar lokmaları.",
        "time": "30 dk", "cal": "160 kcal",
        "ing": ["1 adet küçük karnabahar", "3 yk zeytinyağı", "1 yk mısır unu", "1 tk sarımsak tozu", "1 yk sriracha (veya acı sos)"],
        "steps": ["Karnabaharı küçük çiçeklere ayırın.", "Yağ, un ve baharatlarla harmanlayıp tepsiye dizin.", "200 derece fırında 20 dk kızartın, çıkınca acı sosla karıştırın."],
        "tips": "Fırın tepsisini önceden ısıtmak sebzelerin altının da çıtır olmasını sağlar."
    },
    "Piyaz (Antalya Usulü)": {
        "desc": "Tahinli sosuyla meşhur, bol proteinli ve doyurucu beyaz fasulye salatası.",
        "time": "15 dk", "cal": "290 kcal",
        "ing": ["2 su bardağı haşlanmış kuru fasulye", "1/2 su bardağı tahin", "1 adet haşlanmış yumurta", "1 adet soğan", "3 yk elma sirkesi"],
        "steps": ["Tahin, sirke, sarımsak ve az suyu çırparak sosu hazırlayın.", "Fasulyeleri sosla karıştırıp tabağa alın.", "Üzerini soğan ve yumurta dilimleriyle süsleyin."],
        "tips": "Fasulyelerin ılık olması sosu daha iyi emmelerini sağlar."
    },
    "Hurmalı Enerji Topları": {
        "desc": "Pişirme gerektirmeyen, hurma ve fındık tabanlı sağlıklı tatlı topları.",
        "time": "10 dk", "cal": "90 kcal (adet)",
        "ing": ["10 adet gün kurusu hurma", "1 su bardağı fındık", "1 yk kakao", "1 yk Hindistan cevizi yağı"],
        "steps": ["Hurmaların çekirdeklerini çıkarıp sıcak suda 5 dk bekletin.", "Tüm malzemeyi robottan geçirip hamur kıvamına getirin.", "Küçük toplar yapıp Hindistan cevizi tozuna bulayın."],
        "tips": "İçine bir tutam deniz tuzu eklemek çikolata tadını belirginleştirir."
    },
    "Basit Tavuklu Ramen": {
        "desc": "Zengin aromalı tavuk suyu içinde erişte, haşlanmış yumurta ve taze soğanlı Japon klasiği.",
        "time": "40 dk", "cal": "420 kcal",
        "ing": ["200g ramen eriştesi", "1 lt tavuk suyu", "1 adet haşlanmış yumurta", "2 yk soya sosu", "1 tk susam yağı"],
        "steps": ["Tavuk suyunu zencefil ve sarımsakla kaynatıp soya sosu ekleyin.", "Erişteleri ayrı bir yerde haşlayıp kaselere paylaştırın.", "Üzerine sıcak suyu döküp ikiye bölünmüş yumurta ve taze soğanla süsleyin."],
        "tips": "Yumurtanın sarısının kayısı kıvamında (6-7 dakika haşlanmış) olması makbuldür."
    },
    "Zeytinyağlı Bamya": {
        "desc": "Salyalanmadan, bol domates ve limon suyuyla pişmiş hafif ve şifalı sebze yemeği.",
        "time": "35 dk", "cal": "140 kcal",
        "ing": ["500g bamya", "2 adet domates", "1 adet soğan", "1/2 limon suyu", "3 yk zeytinyağı"],
        "steps": ["Bamyaların tepelerini koni şeklinde temizleyin.", "Soğan ve domatesi soteleyip bamyaları ekleyin.", "Limon suyunu ve az sıcak suyu ekleyip karıştırmadan pişirin."],
        "tips": "Bamyaları temizledikten sonra yıkamayın, pişerken fazla karıştırmayın."
    },
    "Tiramisu (Orijinal)": {
        "desc": "Mascarpone peyniri ve espresso ile ıslatılmış kedi dili bisküvilerin İtalyan buluşması.",
        "time": "30 dk", "cal": "380 kcal",
        "ing": ["200g kedi dili bisküvi", "250g mascarpone", "2 adet yumurta sarısı", "1 fincan sert espresso", "2 yk kakao"],
        "steps": ["Yumurta sarılarını şekerle çırpıp mascarpone ile homojen hale getirin.", "Bisküvileri kahveye batırıp bir kaba dizin.", "Üzerine kremayı yayın ve buzdolabında 4 saat bekletip kakao serpin."],
        "tips": "Bisküvileri kahveye çok hızlı batırıp çıkarın, yoksa hamurlaşır."
    },
    "Sebzeli Sushi Roll (Maki)": {
        "desc": "Nori yosunu içinde sirkeli pirinç, avokado ve salatalıklı başlangıç sushi.",
        "time": "45 dk", "cal": "220 kcal",
        "ing": ["2 adet nori yosunu", "1 su bardağı sushi pirinci", "1 yk pirinç sirkesi", "1/2 avokado", "1/2 salatalık"],
        "steps": ["Haşlanmış pirinci sirke ve şekerle tatlandırıp soğutun.", "Noriye pirinci yayın, ortasına şerit sebzeleri koyun.", "Bambu mat yardımıyla rulo yapıp keskin bıçakla dilimleyin."],
        "tips": "Bıçağınızı her kesimden sonra ıslatırsanız pirinçler bıçağa yapışmaz."
    },
    "Teriyaki Soslu Somon": {
        "desc": "Tatlı-tuzlu Japon sosuyla karamelize edilmiş yumuşak somon dilimleri.",
        "time": "20 dk", "cal": "440 kcal",
        "ing": ["200g somon", "3 yk soya sosu", "1 yk bal", "1 diş sarımsak", "1 tk susam"],
        "steps": ["Soya sosu, bal ve sarımsağı kaynatıp sosu koyulaştırın.", "Somonu tavada mühürleyip sosu üzerine dökün.", "Susam serperek buharda pişmiş pilav ile servis edin."],
        "tips": "Sosu yakmamak için somon pişmeye yakınken ekleyin."
    },
    "Kuzu Tandır": {
        "desc": "Uzun süre fırında ağır ateşte pişmiş, kemiğinden ayrılan yumuşacık kuzu eti.",
        "time": "180 dk", "cal": "580 kcal",
        "ing": ["1 kg kuzu kol", "2 dal taze kekik", "4 diş sarımsak", "1 yk tereyağı", "1 tk karabiber"],
        "steps": ["Eti sarımsak ve kekikle ovalayıp döküm tencereye alın.", "Üzerini yağlı kağıt ve folyo ile kapatıp 150 derece fırında 3 saat pişirin.", "Kendi suyunu üzerine gezdirerek servis edin."],
        "tips": "Pişirme süresinin son 15 dakikasında üzerini açarsanız eti kızartmış olursunuz."
    },
    "Portakallı Ördek (Basit)": {
        "desc": "Klasik Fransız mutfağından, portakal soslu lüks bir akşam yemeği alternatifi.",
        "time": "90 dk", "cal": "520 kcal",
        "ing": ["2 adet ördek göğsü", "2 adet portakalın suyu", "1 yk bal", "1 yk sirke", "1 dal biberiye"],
        "steps": ["Ördek derisine çizikler atıp soğuk tavaya deri tarafı alta gelecek şekilde koyun.", "Kendi yağında kızartıp fırında 10 dk pişirin.", "Portakal suyu, bal ve sirkeyi çektirip sos yapın ve etin üzerine dökün."],
        "tips": "Ördek yağını atmayın, fırın patatesleri için harika bir lezzet kaynağıdır."
    },
    "Chia Tohumlu Çilekli Parfe": {
        "desc": "Süzme yoğurt, chia ve taze çileklerle hazırlanan hafif ve fit tatlı.",
        "time": "15 dk", "cal": "190 kcal",
        "ing": ["1 kase süzme yoğurt", "2 yk chia tohumu", "10 adet çilek", "1 yk bal", "2 yk yulaf ezmesi"],
        "steps": ["Yoğurt, chia ve balı karıştırın.", "Çilekleri püre yapıp bardağın dibine koyun.", "Üzerine yoğurt ve yulafı ekleyip katmanlı bir görüntü oluşturun."],
        "tips": "En az 2 saat buzdolabında bekletmek kıvamın oturmasını sağlar."
    },
    "Etli Kara Lahana Sarması": {
        "desc": "Karadeniz mutfağının baş tacı, satır kıymalı ve hafif acılı sarma.",
        "time": "80 dk", "cal": "310 kcal",
        "ing": ["1 demet kara lahana", "200g dana kıyma", "1/2 su bardağı pirinç", "1 yk biber salçası", "1 adet kuru soğan"],
        "steps": ["Lahanaları haşlayıp soğuk suya alın.", "Kıyma, pirinç ve soğanla harcı hazırlayıp sarmaları sarın.", "Tencereye dizip üzerine zeytinyağlı su ekleyerek pişirin."],
        "tips": "İçine küçük doğranmış iç yağı eklemek lezzeti zirveye taşır."
    },
    "Pavlova": {
        "desc": "Dışı çıtır beze, içi yumuşak marshmallow dokulu meyveli tatlı.",
        "time": "90 dk", "cal": "280 kcal",
        "ing": ["4 adet yumurta akı", "1 su bardağı toz şeker", "1 tk mısır nişastası", "200ml çırpılmış krema", "Orman meyveleri"],
        "steps": ["Yumurta aklarını şekerle kar gibi olana dek çırpın.", "Nişastayı ekleyip yağlı kağıda daire şeklinde yayın.", "120 derece fırında 75 dk kurutun, soğuyunca krema ve meyvelerle süsleyin."],
        "tips": "Fırın kapağını pişme süresince asla açmayın, aksi takdirde beze söner."
    },
    "İncirli ve Cevizli Brie": {
        "desc": "Kızarmış ekşi mayalı ekmek üzerinde eriyen Brie peyniri, taze incir ve bal.",
        "time": "10 dk", "cal": "310 kcal",
        "ing": ["2 dilim ekşi mayalı ekmek", "100g Brie peyniri", "2 adet taze incir", "1 yk bal", "1 yk ceviz"],
        "steps": ["Ekmekleri kızartıp üzerine peynir dilimlerini koyun.", "Fırında 2 dk peynir yumuşayana kadar tutun.", "Üzerine dilimlenmiş incir, ceviz ve bal gezdirip servis edin."],
        "tips": "İncir yerine armut dilimleri de harika bir alternatif olur."
    },
    "Çilekli ve Reyhanlı Limonata": {
        "desc": "Taze çilek püresi ve mor reyhanın ferahlatıcı aromasıyla ev yapımı limonata.",
        "time": "15 dk", "cal": "120 kcal",
        "ing": ["4 adet limon", "10 adet çilek", "1/2 su bardağı şeker", "1 dal mor reyhan", "1 lt su"],
        "steps": ["Limon sularını şekerle birlikte şeker eriyene kadar karıştırın.", "Çilekleri blenderdan geçirip limonlu suya ekleyin.", "Reyhan yapraklarını içine atıp soğuk servis edin."],
        "tips": "Reyhanları elinizle hafifçe ovuşturarak aromalarını serbest bırakın."
    },
    "Muhammara (Acuka)": {
        "desc": "Közlenmiş biber, bol ceviz ve özel baharatlarla hazırlanan yoğun kıvamlı kahvaltılık meze.",
        "time": "20 dk", "cal": "280 kcal",
        "ing": ["2 adet közlenmiş kapya biber", "1 su bardağı ceviz", "1 yk biber salçası", "2 yk nar ekşisi", "1 tk kimyon"],
        "steps": ["Biberleri ve cevizleri mutfak robotunda hafif pütürlü kalacak şekilde çekin.", "Salça, nar ekşisi, zeytinyağı ve baharatları ekleyip karıştırın.", "Üzerine sızma zeytinyağı gezdirip dinlendirin."],
        "tips": "Galeta unu eklemek kıvamın daha ekmeğe sürülebilir olmasını sağlar."
    },
    "Ispanaklı Smoothie Bowl": {
        "desc": "Bebek ıspanak, donmuş muz ve fıstık ezmesiyle hazırlanan süper besleyici kahvaltı kasesi.",
        "time": "10 dk", "cal": "290 kcal",
        "ing": ["1 adet donmuş muz", "1 avuç bebek ıspanak", "1/2 su bardağı badem sütü", "1 yk fıstık ezmesi"],
        "steps": ["Tüm malzemeyi pürüzsüz bir krema kıvamına gelene kadar yüksek devirde çekin.", "Geniş bir kaseye dökün.", "Üzerini granola ve taze meyvelerle süsleyin."],
        "tips": "Smoothie'nin yoğun olması için muzun tamamen donmuş olması şarttır."
    },
    "Kabak Çiçeği Dolması": {
        "desc": "Ege mutfağının en zarif zeytinyağlısı; pirinç ve taze otlarla doldurulmuş kabak çiçekleri.",
        "time": "50 dk", "cal": "190 kcal",
        "ing": ["10 adet kabak çiçeği", "1/2 su bardağı pirinç", "1 adet soğan", "1 yk kuş üzümü", "1 demet taze nane"],
        "steps": ["İç harcı hazırlayıp çiçeklerin ortasındaki sarı kısımları temizleyin.", "Harcı çiçeklere çok doldurmadan paylaştırıp uçlarını kapatın.", "Tencereye dik dizip az suyla 20 dk pişirin."],
        "tips": "Çiçekleri sabahın erken saatlerinde toplamak veya almak, açık kalmalarını sağlar."
    },
    "Fesleğenli Mantar Sote": {
        "desc": "Yüksek ateşte mühürlenmiş mantarların taze fesleğen ve parmesanla İtalyan dokunuşu.",
        "time": "15 dk", "cal": "210 kcal",
        "ing": ["300g kültür mantarı", "2 diş sarımsak", "1 avuç taze fesleğen", "20g parmesan", "2 yk zeytinyağı"],
        "steps": ["Mantarları yüksek ateşte sularını bırakmalarına izin vermeden soteleyin.", "Sarımsak ve tuzu ekleyip 2 dk daha çevirin.", "Ocağı kapatıp taze fesleğen ve rendelenmiş peyniri ekleyin."],
        "tips": "Mantarları yıkamayın, unlu suyla silerek temizleyin."
    },
    "Çılbır Soslu Avokado": {
        "desc": "Klasik çılbırın modern yorumu; avokado yatağında poşe yumurta ve süzme yoğurt.",
        "time": "15 dk", "cal": "340 kcal",
        "ing": ["1/2 avokado", "1 adet yumurta", "2 yk süzme yoğurt", "1 yk tereyağı", "Pul biber"],
        "steps": ["Avokadoyu dilimleyip tabağa dizin.", "Üzerine yoğurdu ekleyin ve poşe pişirdiğiniz yumurtayı yerleştirin.", "Kızgın tereyağını üzerinden gezdirin."],
        "tips": "Yoğurdun oda sıcaklığında olması yemeğin hızlı soğumasını engeller."
    },
    "Orman Meyveli Ev Yapımı Dondurma": {
        "desc": "Sadece donmuş meyve ve süzme yoğurt ile hazırlanan katkısız, şekersiz dondurma.",
        "time": "10 dk", "cal": "150 kcal",
        "ing": ["1 su bardağı donmuş böğürtlen/ahududu", "2 yk süzme yoğurt", "1 yk bal"],
        "steps": ["Donmuş meyveleri ve yoğurdu robotta dondurma kıvamına gelene dek çekin.", "Hemen servis yapın veya dondurucuya atın.", ""],
        "tips": "Meyvelerin tamamen donmuş olduğundan emin olun, aksi halde ayran kıvamında olur."
    },
    "Fırınlanmış Baharatlı Nohut": {
        "desc": "Cips yerine tüketilebilecek, çıtır çıtır ve protein deposu bir atıştırmalık.",
        "time": "30 dk", "cal": "180 kcal",
        "ing": ["1 su bardağı haşlanmış nohut", "1 yk zeytinyağı", "1 tk isli paprika", "1 tk kekik"],
        "steps": ["Nohutları kağıt havluyla tamamen kurulayın.", "Yağ ve baharatlarla harmanlayıp fırın tepsisine yayın.", "200 derece fırında 20-25 dk çıtır olana dek pişirin."],
        "tips": "Kurulama aşaması nohutların haşlanmış gibi değil, çıtır olmasını sağlar."
    },
    "Buzlu Matcha Latte": {
        "desc": "Japonya'dan gelen Matcha yeşil çayı ve soğuk sütün ferahlatıcı birleşimi.",
        "time": "5 dk", "cal": "110 kcal",
        "ing": ["1 tk matcha tozu", "1/2 su bardağı sıcak su", "1 su bardağı soğuk süt", "Buz küpleri"],
        "steps": ["Matchayı sıcak suyla köpürene kadar çırpın (bambu fırça veya mikserle).", "Bardağa buzları koyun, sütü ekleyin.", "En son matcha karışımını sütün üzerine dökün."],
        "tips": "Topaklanmaması için toz çayı önceden elemeniz önerilir."
    }
}

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
    {"name":"Mercimekli Vegan Burger","cat":"Öğle","time":"30+ dk","tags":["Vegan","Doyurucu"]},

    {"name":"Somon Izgara","cat":"Akşam","time":"15-30 dk","tags":["Sağlıklı","Düşük kalorili","Balık"]},
    {"name":"Ezogelin Çorbası","cat":"Öğle","time":"30+ dk","tags":["Sağlıklı","Doyurucu"]},
    {"name":"San Sebastian Cheesecake","cat":"Akşam","time":"30+ dk","tags":["Kaçamak","Tatlı"]},
    {"name":"Karides Güveç","cat":"Akşam","time":"15-30 dk","tags":["Doyurucu","Balık"]},
    {"name":"Kıymalı Tarhana Çorbası","cat":"Akşam","time":"15-30 dk","tags":["Sağlıklı","Et ağırlıklı"]},
    {"name":"Magnolia (Muzlu)","cat":"Öğle","time":"15-30 dk","tags":["Tatlı","Pratik"]},
    {"name":"Levrek Buğulama","cat":"Akşam","time":"30+ dk","tags":["Sağlıklı","Balık"]},
    {"name":"Chia Tohumlu Puding","cat":"Kahvaltı","time":"<15 dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Domates Çorbası (Közlenmiş)","cat":"Öğle","time":"30+ dk","tags":["Sağlıklı","Hafif"]},
    {"name":"Fırın Sütlaç","cat":"Akşam","time":"30+ dk","tags":["Tatlı","Orta"]},

    {"name":"Guacamole Soslu Nachos","cat":"Öğle","time":"<15 dk","tags":["Kaçamak","Vegan"]},
    {"name":"Buharda Sebzeli Gyozza","cat":"Akşam","time":"30+ dk","tags":["Vegan","Uzak Doğu"]},
    {"name":"Gavurdağı Salatası","cat":"Öğle","time":"15-30 dk","tags":["Sağlıklı","Hafif"]},
    {"name":"Lazanya (Bolognese)","cat":"Akşam","time":"30+ dk","tags":["Makarna","Doyurucu"]},
    {"name":"Falafel Salatası","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Sağlıklı"]},
    {"name":"Karidesli Linguine","cat":"Akşam","time":"15-30 dk","tags":["Makarna","Balık"]},
    {"name":"Atom (Süzme Yoğurtlu Meze)","cat":"Öğle","time":"<15 dk","tags":["Pratik","Sağlıklı"]},
    {"name":"Tavuklu Quesadilla","cat":"Akşam","time":"15-30 dk","tags":["Tavuk","Doyurucu"]},
    {"name":"Vişneli Yaprak Sarma","cat":"Akşam","time":"30+ dk","tags":["Vegan","Sağlıklı"]},
    {"name":"Beef Stroganoff","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Doyurucu"]},

    {"name":"Kabak Mücver","cat":"Öğle","time":"15-30 dk","tags":["Sebze ağırlıklı","Sağlıklı","Hafif"]},
    {"name":"Tom Yum Çorbası","cat":"Akşam","time":"15-30 dk","tags":["Uzak Doğu","Düşük kalorili"]},
    {"name":"Paçanga Böreği","cat":"Kahvaltı","time":"15-30 dk","tags":["Kaçamak","Doyurucu"]},
    {"name":"Etli Kuru Fasulye","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Doyurucu"]},
    {"name":"Zeytinyağlı Enginar","cat":"Öğle","time":"30+ dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Ispanaklı Gül Böreği","cat":"Öğle","time":"30+ dk","tags":["Sebze ağırlıklı","Doyurucu"]},
    {"name":"Ratatouille","cat":"Akşam","time":"30+ dk","tags":["Vegan","Sağlıklı","Sebze ağırlıklı"]},
    {"name":"İçli Köfte (Haşlama)","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Detaylı"]},
    {"name":"Karnıyarık","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Doyurucu"]},
    {"name":"İrmik Helvası","cat":"Öğle","time":"15-30 dk","tags":["Tatlı","Pratik"]},

    {"name":"Tavuk Tantuni","cat":"Öğle","time":"15-30 dk","tags":["Tavuk","Doyurucu","Kaçamak"]},
    {"name":"Mantar Kokoreç","cat":"Akşam","time":"<15 dk","tags":["Vegan","Hafif","Pratik"]},
    {"name":"Beluga Mercimek Salatası","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Sağlıklı","Yüksek protein"]},
    {"name":"Fit Muzlu Ekmek (Banana Bread)","cat":"Kahvaltı","time":"30+ dk","tags":["Tatlı","Sağlıklı"]},
    {"name":"Falafel Burger","cat":"Akşam","time":"15-30 dk","tags":["Vegan","Doyurucu","Kaçamak"]},
    {"name":"Körili Nohut Yemeği (Chana Masala)","cat":"Akşam","time":"30+ dk","tags":["Vegan","Doyurucu","Sağlıklı"]},
    {"name":"Avokadolu Yumurtalı Tost","cat":"Kahvaltı","time":"<15 dk","tags":["Sağlıklı","Pratik","Yüksek protein"]},
    {"name":"Fırınlanmış Baharatlı Karnabahar","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Düşük kalorili","Hafif"]},
    {"name":"Piyaz (Antalya Usulü)","cat":"Öğle","time":"<15 dk","tags":["Sağlıklı","Yüksek protein"]},
    {"name":"Hurmalı Enerji Topları","cat":"Akşam","time":"<15 dk","tags":["Tatlı","Sağlıklı","Hafif"]},

    {"name":"Basit Tavuklu Ramen","cat":"Akşam","time":"30+ dk","tags":["Uzak Doğu","Doyurucu"]},
    {"name":"Zeytinyağlı Bamya","cat":"Öğle","time":"30+ dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Tiramisu (Orijinal)","cat":"Akşam","time":"15-30 dk","tags":["Tatlı","Kaçamak"]},
    {"name":"Sebzeli Sushi Roll (Maki)","cat":"Öğle","time":"30+ dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Teriyaki Soslu Somon","cat":"Akşam","time":"15-30 dk","tags":["Balık","Uzak Doğu"]},
    {"name":"Kuzu Tandır","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Detaylı"]},
    {"name":"Portakallı Ördek (Basit)","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Detaylı"]},
    {"name":"Chia Tohumlu Çilekli Parfe","cat":"Kahvaltı","time":"<15 dk","tags":["Sağlıklı","Vegan","Hafif"]},
    {"name":"Etli Kara Lahana Sarması","cat":"Akşam","time":"30+ dk","tags":["Et ağırlıklı","Doyurucu"]},
    {"name":"Pavlova","cat":"Akşam","time":"30+ dk","tags":["Tatlı","Hafif"]},

    {"name":"İncirli ve Cevizli Brie","cat":"Kahvaltı","time":"<15 dk","tags":["Sağlıklı","Hafif"]},
    {"name":"Çilekli ve Reyhanlı Limonata","cat":"Öğle","time":"15-30 dk","tags":["Sağlıklı","Hafif"]},
    {"name":"Muhammara (Acuka)","cat":"Kahvaltı","time":"15-30 dk","tags":["Vegan","Doyurucu"]},
    {"name":"Ispanaklı Smoothie Bowl","cat":"Kahvaltı","time":"<15 dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Kabak Çiçeği Dolması","cat":"Akşam","time":"30+ dk","tags":["Vegan","Sağlıklı"]},
    {"name":"Fesleğenli Mantar Sote","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Pratik"]},
    {"name":"Çılbır Soslu Avokado","cat":"Kahvaltı","time":"15-30 dk","tags":["Yüksek protein","Sağlıklı"]},
    {"name":"Orman Meyveli Ev Yapımı Dondurma","cat":"Akşam","time":"<15 dk","tags":["Tatlı","Hafif","Sağlıklı"]},
    {"name":"Fırınlanmış Baharatlı Nohut","cat":"Öğle","time":"15-30 dk","tags":["Vegan","Sağlıklı","Hafif"]},
    {"name":"Buzlu Matcha Latte","cat":"Öğle","time":"<15 dk","tags":["Sağlıklı","Hafif"]}
]

# ================================
# ⚙️ MANTIK (LOGIC)
# ================================
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

questions = [
    ("Hangi öğün?", "radio", ["Kahvaltı", "Öğle", "Akşam"]),
    ("Zamanın ne kadar?", "radio", ["<15 dk", "15-30 dk", "30+ dk"]),
    ("Beslenme tercihin?", "multi", ["Et ağırlıklı","Tavuk","Sebze ağırlıklı","Vegan","Düşük kalorili"]),
    ("Nasıl bir yemek?", "multi", ["Hafif","Doyurucu","Sağlıklı","Kaçamak"])
]

# ================================
# 🖥️ ARAYÜZ (UI)
# ================================
st.title("👨‍🍳 Şefin Akıllı Mutfağı")

if st.session_state.step < len(questions):
    q, typ, opts = questions[st.session_state.step]
    st.subheader(q)
    choice = st.radio("", opts) if typ == "radio" else st.multiselect("", opts)
    
    if st.button("Devam"):
        st.session_state.answers[q] = choice
        st.session_state.step += 1
        st.rerun()
else:
    # Skorlama ve Öneri
    ans = st.session_state.answers
    
    def score_meal(m):
        score = 0
        if m["cat"] == ans["Hangi öğün?"]: score += 5
        if m["time"] == ans["Zamanın ne kadar?"]: score += 3
        return score

    best_match = sorted(meals, key=score_meal, reverse=True)[0]
    recipe = NEW_RECIPES.get(best_match["name"], None)


    if recipe:
        st.success(f"### Önerim: {best_match['name']}")
        col1, col2 = st.columns(2)
        col1.metric("Süre", recipe["time"])
        col2.metric("Kalori", recipe["cal"])
        
        st.write(f"**Açıklama:** {recipe['desc']}")
        
        st.subheader("🛒 Malzemeler")
        for i in recipe["ing"]: st.write(f"- {i}")
        
        st.subheader("👨‍🍳 Hazırlanışı")
        for idx, step in enumerate(recipe["steps"], 1): st.write(f"{idx}. {step}")
        
        st.info(f"💡 **Şefin İpucu:** {recipe['tips']}")

    if st.button("Baştan Başla"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
