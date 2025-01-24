import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Music Filter")
ACCESS_TOKEN = "qtqL3RCmEvqPiolzQRJtXnQIcHdM0YGYan1rmB4O_9oQN71tmiNDMYH2hvIxM0Tw"
GENIUS_API_URL = "https://api.genius.com"

st.title("Müzik Filtresi V1")
st.write("## Şarkı Arama V1")
st.write("Daha iyi sonuçlar elde etmek için daha spesifik şarkı sözleri belirleyebilirsiniz.")
keyword = st.text_input("Lütfen Anahtar Kelimeleri Giriniz. / İsteğe Göre Girdiğiniz Şarkıcının Şarkılarınıda Gösterir.")
secim = st.radio("Nasıl olmuş?",
         ("Fikrim Yok","Çok İyi", "Harika" , "Orta", "Kötü")
                )
if secim == "Çok İyi":
    st.write("Teşekkür Ederim.")
if secim == "Harika":
    st.write("Teşekkür Ederim.")
if secim == "Orta":
    st.write("Banane. Sordum mu?")
if secim == "Kötü":
    st.error("Yanlış Seçeneği Seçtin Sanırım")
    st.radio("Tekrar Seçebilirsin.",
             ("Çok İyi", "İyi"), key="secim2")


st.write("malsın ki")


def music_filter(keyword):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}  # Authorization header'ını düzeltme
    search_url = f"{GENIUS_API_URL}/search"
    params = {"q": keyword}  # params'ı düzgün şekilde kullanıyoruz
    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        hits = response.json()["response"]["hits"]
        return [{"title": hit["result"]["title"], "url": hit["result"]["url"]} for hit in hits]
    else:
        st.error("URL Alınamadı. Tekrar Deneyiniz.")
        return []


def sarki_sozleri(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Şarkı sözlerini içeren farklı HTML etiketleri kontrol ediliyor
        lyrics_div = soup.find("div", class_="lyrics")
        if not lyrics_div:
            lyrics_div = soup.find("div", class_="Lyrics_Container")

        # Eğer 'lyrics' veya 'Lyrics_Container' sınıfları yoksa, alternatif etiketlere bakıyoruz
        if not lyrics_div:
            lyrics_div = soup.find("p")

        if lyrics_div:
            return lyrics_div.get_text(separator="\n")


if keyword:
    results = music_filter(keyword)  # Anahtar kelime ile arama yap
    if results:
        st.subheader("Arama Sonuçları")  # Arama sonuçlarının başlığı
        for index, result in enumerate(results):  # Her bir şarkı sonucu için döngü
            if st.button(f"{result['title']}", key=f"button_{index}"):  # Benzersiz bir key ile buton
                # Şarkı sözlerini çekme
                lyrics = sarki_sozleri(result["url"])
                
                if lyrics:  # Eğer şarkı sözleri başarıyla çekilmişse
                    st.subheader(result["title"])  # Şarkı başlığını göster
                    st.text(lyrics)  # Şarkı sözlerini göster
                
                # Genius sayfasına yönlendiren bir bağlantı oluştur
                link_html = f'<a href="{result["url"]}" target="_blank" style="font-size: 20px; font-weight: bold; color: #1E90FF; text-decoration: none;">Şarkı Sözlerini Görmek İçin Tıklayınız 👀</a>'
                st.markdown(link_html, unsafe_allow_html=True)
    else:
        st.error("Sonuç bulunamadı!")  # Eğer hiçbir sonuç yoksa hata mesajı
