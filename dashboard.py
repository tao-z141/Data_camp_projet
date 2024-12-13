import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Charger les données depuis le fichier CSV
file_path = 'prediction.csv'
data = pd.read_csv(file_path, encoding='latin1', sep=';')

# Convertir la colonne 'Date' en format datetime et extraire le mois
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y', errors='coerce')
data['Month'] = data['Date'].dt.month

# Afficher le logo Decathlon dans la barre latérale
st.sidebar.image("image.png", width=200)

# Titre principal de l'application
st.markdown("<h1 style='text-align: center;'>Analyse des Avis des Produits Decathlon</h1>", unsafe_allow_html=True)

# Ajout des filtres dans la barre latérale
st.sidebar.header("Filtres")

# Filtre par sentiment
default_sentiments = data['Sentiment'].unique()
sentiments = st.sidebar.multiselect(
    "Sentiments:",
    options=data['Sentiment'].unique(),
    default=default_sentiments
)

# Filtre par mois
min_month = data['Month'].min()
max_month = data['Month'].max()
month_range = st.sidebar.slider(
    "Mois:",
    min_value=min_month,
    max_value=max_month,
    value=(min_month, max_month)
)
start_month, end_month = month_range

# Filtre par note
min_note, max_note = st.sidebar.slider(
    "Note:",
    min_value=int(data['Note'].min()),
    max_value=int(data['Note'].max()),
    value=(int(data['Note'].min()), int(data['Note'].max()))
)

# Appliquer les filtres aux données
filtered_data = data[
    (data['Sentiment'].isin(sentiments)) &
    (data['Month'] >= start_month) &
    (data['Month'] <= end_month) &
    (data['Note'] >= min_note) &
    (data['Note'] <= max_note)
]

# Organisation des visualisations dans une grille
row1_col1, row1_col2 = st.columns([1, 1])
row2_col1, row2_col2 = st.columns([1, 1])
row3_col1, row3_col2 = st.columns([1, 1])

# Visualisation 1 : Distribution des sentiments
with row1_col1:
    sentiment_count = filtered_data['Sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['Sentiment', 'Count']  # Renommer les colonnes pour plus de clarté
    fig1 = px.bar(sentiment_count, x='Sentiment', y='Count', labels={'Sentiment': 'Sentiment', 'Count': 'Nombre'},
                  title="Distribution des Sentiments", text='Count')
    fig1.update_traces(texttemplate='%{text}', textposition='outside')
    fig1.update_layout(xaxis_title="Sentiment", yaxis_title="Nombre", title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)

# Visualisation 2 : Répartition des notes (Histogramme horizontal)
with row1_col2:
    note_count = filtered_data['Note'].value_counts().reset_index()
    note_count.columns = ['Note', 'Count']  # Renommer les colonnes pour plus de clarté
    fig2 = px.bar(note_count, y='Note', x='Count', orientation='h',
                  labels={'Note': 'Note', 'Count': 'Nombre'},
                  title="Répartition des Notes", text='Count')
    fig2.update_traces(texttemplate='%{text}', textposition='outside')
    fig2.update_layout(xaxis_title="Nombre", yaxis_title="Note", title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)

# Visualisation 3 : Évolution des commentaires par mois
with row2_col1:
    comments_per_month = filtered_data.groupby('Month').size().reset_index(name='Count')
    fig3 = px.line(comments_per_month, x='Month', y='Count', markers=True, labels={'Month': 'Mois', 'Count': 'Nombre'},
                   title="Évolution des Commentaires")
    fig3.update_layout(xaxis_title="Mois", yaxis_title="Nombre de Commentaires", title_x=0.5)
    st.plotly_chart(fig3, use_container_width=True)

# Visualisation 4 : Corrélation entre la note et le score
with row2_col2:
    fig4 = px.scatter(filtered_data, x='Note', y='score', color='Sentiment',
                      labels={'Note': 'Note', 'score': 'Score', 'Sentiment': 'Sentiment'},
                      title="Corrélation entre Note et Score")
    fig4.update_layout(xaxis_title="Note", yaxis_title="Score", title_x=0.5)
    st.plotly_chart(fig4, use_container_width=True)

# Visualisation 5 : Comparaison entre notes et prédictions
with row3_col1:
    comparison = filtered_data[['Note', 'prediction']].melt(var_name='Type', value_name='Valeur')
    fig5 = px.histogram(comparison, x='Valeur', color='Type', barmode='group',
                        labels={'Valeur': 'Valeur (Note ou Prédiction)', 'Type': 'Type'},
                        title="Comparaison entre Notes et Prédictions")
    fig5.update_layout(xaxis_title="Valeur (Note ou Prédiction)", yaxis_title="Fréquence", title_x=0.5)
    st.plotly_chart(fig5, use_container_width=True)

# Visualisation 6 : Matrice de confusion entre notes et prédictions
with row3_col2:
    confusion_matrix = pd.crosstab(filtered_data['Note'], filtered_data['prediction'], rownames=['Note'], colnames=['Prédiction'])
    fig6 = go.Figure(data=go.Heatmap(
        z=confusion_matrix.values,
        x=confusion_matrix.columns,
        y=confusion_matrix.index,
        colorscale='Blues',
        text=confusion_matrix.values,
        texttemplate="%{text}"
    ))
    fig6.update_layout(title="Matrice de Confusion", xaxis_title="Prédiction", yaxis_title="Note", title_x=0.5)
    st.plotly_chart(fig6, use_container_width=True)
