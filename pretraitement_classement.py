import pandas as pd
import numpy as np
from google.colab import files
import re
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import CamembertTokenizer, pipeline
from unidecode import unidecode

uploaded = files.upload()

df = pd.read_csv('Article_data.csv')
df['Auteur'] = df['Auteur'].str.split('|').str[0].str.strip()
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else '')
df['Note'] = df['Note'].str.extract(r'(\d+)').astype(int)


def nettoyer_texte(texte):

    texte = unidecode(texte)
    texte = re.sub(r'[^a-zA-Z\s]', '', texte)
    texte = re.sub(r'\s+', ' ', texte).strip()
    texte = texte.lower()
    return texte

df['Commentaire'] = df['Commentaire'].apply(nettoyer_texte)
df = df.drop_duplicates()
df.to_csv('data_pretraité.csv', index=False, encoding='utf-8')

HUB_MODEL = "cmarkea/distilcamembert-base-sentiment"

tokenizer = CamembertTokenizer.from_pretrained(HUB_MODEL)
quantized_model = ORTModelForSequenceClassification.from_pretrained(HUB_MODEL, file_name="model.onnx")
onnx_qa_quantized = pipeline("text-classification", model=quantized_model, tokenizer=tokenizer)


df['prediction'] = df['Commentaire'].apply(lambda x: onnx_qa_quantized(x)[0]['label'])
df['score'] = df['Commentaire'].apply(lambda x: onnx_qa_quantized(x)[0]['score'])
    


star_mapping = {
    "1 stars": "très négatif",
    "2 stars": "négatif",
    "3 stars": "neutre",
    "4 stars": "positif",
    "5 stars": "très positif"
}

df['prediction_class'] = df['prediction'].map(star_mapping)

     

df.head(50)
df.to_csv('Gold/predictions.csv', index=False, encoding='utf-8')