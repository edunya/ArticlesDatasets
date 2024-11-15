import requests
import pandas as pd
from datetime import datetime
import time

# API linki
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

titles, abstracts, keywords = [], [], []

# Buraya verilerini alacağımız sınıflar değiştirip girildi. (Artificial Neural Networks, Computer Science, Data Mining, Image Processing, Machine Learning)
category = "Artificial Neural Networks"
query = "Artificial Neural Networks"

# API kullanılarak konulara göre makale kimlikleri alındı.
search_url = f"{base_url}esearch.fcgi?db=pubmed&term={query}&retmax=5000&retmode=json"
search_response = requests.get(search_url)
id_list = search_response.json()["esearchresult"]["idlist"]

# Makale detaylarını alındı.
for pmid in id_list:
    fetch_url = f"{base_url}efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
    fetch_response = requests.get(fetch_url)

    if fetch_response.status_code == 200:
        xml_data = fetch_response.text

        from xml.etree import ElementTree as ET

        root = ET.fromstring(xml_data)

        title = root.findtext(".//ArticleTitle")
        abstract = root.findtext(".//Abstract/AbstractText")
        keyword_list = root.findall(".//Keyword")

        keywords_text = ", ".join([kw.text for kw in keyword_list if kw.text is not None])

        titles.append(title)
        abstracts.append(abstract)
        keywords.append(keywords_text)

        time.sleep(0.1)

# Dataframe haline getirdik excele kaydedebilmek için.
df = pd.DataFrame({
    'Baslik': titles,
    'Ozet': abstracts,
    'Anahtar_Kelimeler': keywords
})

# Dosya adı oluşturma zamanına göre oluşturuldu.
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"pubmed_artificial_neural_networks_{timestamp}.xlsx" #diğer dosyaların isimleri de değiştirildi aynı olmayabilir.

# Excel dosyasına kaydedildi.
df.to_excel(file_name, index=False)
print(f"Veriler {file_name} dosyasına kaydedildi.")
