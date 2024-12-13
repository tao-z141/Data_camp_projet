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

# Liste des mois pour affichage
month_labels = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
    7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

# Afficher le logo Decathlon dans la barre latérale
st.sidebar.image("Decathlon.png", width=200)

# Titre principal de l'application
st.markdown("<h1 style='text-align: center;'>Analyse des Avis sur une Chaussure de Running sur Decathlon</h1>", unsafe_allow_html=True)

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

# Organisation des visualisations
row1_col1 = st.container()  # Conteneur unique pour la première visualisation
row2_col1, row2_col2 = st.columns([1, 1])
row3_col1, row3_col2 = st.columns([1, 1])

# Visualisation 1 : Distribution des sentiments
with row1_col1:
    sentiment_count = filtered_data['Sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['Sentiment', 'Count']
    fig1 = px.bar(sentiment_count, x='Sentiment', y='Count', labels={'Sentiment': 'Sentiment', 'Count': 'Nombre'},
                  title="Distribution des Sentiments", text='Count', height=400, width=900)
    fig1.update_traces(texttemplate='%{text}', textposition='outside')
    fig1.update_layout(xaxis_title="Sentiment", yaxis_title="Nombre", title={'text': "Distribution des Sentiments", 'font': {'size': 16}})
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("**Interprétation :** Cet article est majoritairement apprécié, avec de nombreux avis positifs et très positifs. Mettre en avant cet article dans les promotions pour capitaliser sur son image positive. Cependant, analyser en détail les commentaires négatifs pour comprendre ce qui pourrait freiner certaines ventes (exemple : qualité perçue, taille, fonctionnalité).")

# Visualisation 2 : Évolution des commentaires par mois
with row2_col1:
    comments_per_month = filtered_data.groupby('Month').size().reset_index(name='Count')
    comments_per_month['Month Name'] = comments_per_month['Month'].map(month_labels)
    fig3 = px.line(comments_per_month, x='Month Name', y='Count', markers=True,
                   labels={'Month Name': 'Mois', 'Count': 'Nombre'},
                   title="Évolution des Commentaires", height=400, width=700)
    fig3.update_layout(xaxis_title="Mois", yaxis_title="Nombre de Commentaires", title={'text': "Évolution des Commentaires", 'font': {'size': 16}})
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("**Interprétation :** La hausse des commentaires en octobre peut indiquer un grand intérêt pour cet article à cette période (par exemple, en raison de promotions ou de la saisonnalité). Maintenir ou intensifier les efforts marketing à ce moment-là. La baisse des commentaires en décembre doit être étudiée : cela pourrait signifier que l'article n'est pas bien adapté aux besoins de cette période (période de noel). ")

# Visualisation 3 : Corrélation entre la note et le score
with row2_col2:
    fig4 = px.scatter(filtered_data, x='Note', y='score', color='Sentiment',
                      labels={'Note': 'Note', 'score': 'Score', 'Sentiment': 'Sentiment'},
                      title="Corrélation entre Note et Score", height=400, width=700)
    fig4.update_layout(xaxis_title="Note", yaxis_title="Score", title={'text': "Corrélation entre Note et Score", 'font': {'size': 16}})
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("**Interprétation :** Les notes élevées (4 et 5) montrent que les clients satisfaits attribuent souvent des scores positifs. Identifier les caractéristiques ou fonctionnalités qui plaisent le plus (par exemple, qualité, prix) et les mettre en avant dans les descriptions de produit et les promotions. Pour les notes faibles, analyser les retours des clients pour repérer les problèmes récurrents et corriger ces défauts (exemple : ajustement, robustesse).")

# Visualisation 4 : Comparaison entre notes et prédictions
with row3_col1:
    comparison = filtered_data[['Note', 'prediction']].melt(var_name='Type', value_name='Valeur')
    fig5 = px.histogram(comparison, x='Valeur', color='Type', barmode='group',
                        labels={'Valeur': 'Valeur (Note ou Prédiction)', 'Type': 'Type'},
                        title="Comparaison entre Notes et Prédictions", text_auto=True, height=400, width=700)
    fig5.update_xaxes(tickmode='linear', dtick=1)
    fig5.update_layout(xaxis_title="Valeur (Note ou Prédiction)", yaxis_title="Fréquence", title={'text': "Comparaison entre Notes et Prédictions", 'font': {'size': 16}})
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("**Interprétation :** Les clients satisfaits donnent des notes élevées accompagnées de commentaires positifs, tandis que les notes faibles sont liées à des commentaires négatifs. Il est essentiel d'analyser ces retours négatifs pour identifier les points à améliorer sur l'article).")

# Visualisation 5 : Matrice de confusion
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
    fig6.update_xaxes(tickmode='linear', dtick=1)
    fig6.update_yaxes(tickmode='linear', dtick=1)
    fig6.update_layout(title={'text': "Matrice de Confusion", 'font': {'size': 16}}, xaxis_title="Prédiction", yaxis_title="Note", height=400, width=700)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("**Interprétation :** La comparaison entre les notes et les prédictions montre que les clients sont très nombreux à attribuer des notes élevées (4 et 5). Cependant, les avis négatifs, bien que rares, méritent une attention particulière. Les commentaires associés aux notes faibles doivent être analysés pour mieux comprendre les causes de l'insatisfaction et y apporter des solutions rapides, comme des ajustements sur l'article ou un meilleur accompagnement client.")

# Conclusion générale
st.markdown("""
### Conclusion
Le dashboard montre que cet article est largement apprécié, mais des efforts spécifiques peuvent être faits pour réduire les retours négatifs et maximiser son potentiel commercial, notamment en adaptant le produit ou en ciblant les promotions aux périodes d'intérêt. En suivant ces recommandations, le manager pourra augmenter les ventes et fidéliser davantage les clients pour cet article.
""")
