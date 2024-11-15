import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Diğer dosyalar buraya yazılıp işlendi.
file_path = "pubmed_machine_learning_20241114_214244.xlsx"
df = pd.read_excel(file_path)


def preprocess_text(text):
    if not isinstance(text, str):
        return ""

    text = text.lower()
    words = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word.isalpha()]

    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    return " ".join(words)


df['Ozet'] = df['Ozet'].apply(lambda x: preprocess_text(x) if pd.notna(x) else "")
df['Anahtar_Kelimeler'] = df['Anahtar_Kelimeler'].apply(
    lambda x: preprocess_text(x) if pd.notna(x) else "")

new_file_path = "islenmis.xlsx"  # Yeni dosya adı oluşturup daha sonra ismi değiştirildi.
df.to_excel(new_file_path, index=False)

print(f"Veriler işlenip {new_file_path} dosyasına kaydedildi.")