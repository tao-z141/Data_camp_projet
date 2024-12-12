import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Visualisation des Données et Graphiques", layout="wide")

st.title("Visualisation des Données et Graphiques")
st.markdown("""
    Cette application permet de visualiser les données et différents graphiques à partir de fichiers CSV. 
    Veuillez charger un fichier CSV contenant les colonnes appropriées pour générer les visualisations.
""")

uploaded_file = st.file_uploader("Chargez votre fichier CSV (ex: prediction.csv)", type=["csv"])

if uploaded_file:
    # Lecture des données
    data = pd.read_csv(uploaded_file, delimiter=",")

    # Conversion de la colonne 'Date' en type datetime
    # if 'Date' in data.columns:
    #     data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
    #     print()

    st.write("Aperçu des données :")
    st.dataframe(data.head())

    # Distribution des sentiments
    if 'prediction_class' in data.columns:
        st.subheader("Distribution des Sentiments")
        fig, ax = plt.subplots(figsize=(8, 6))
        sentiment_counts = data['prediction_class'].value_counts()
        sentiment_counts.plot(kind='bar', ax=ax, color='skyblue')
        plt.title('Distribution des Sentiments (Positif/Négatif)')
        plt.xlabel('Sentiment')
        plt.ylabel('Nombre de commentaires')

        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=9, color='black', fontweight='bold')
        st.pyplot(fig)

    # Répartition des notes
    if 'Note' in data.columns:
        st.subheader("Répartition des Notes")
        fig, ax = plt.subplots(figsize=(8, 6))
        notes_counts = data['Note'].value_counts().sort_index()
        notes_counts.plot(kind='barh', ax=ax, color='skyblue')
        plt.title('Répartition des Notes')
        plt.xlabel('Nombre de commentaires')
        plt.ylabel('Notes')

        for index, value in enumerate(notes_counts):
            ax.text(value, index, str(value), va='center', color='black', fontweight='bold', fontsize=7)
        st.pyplot(fig)

    # Évolution des commentaires au fil du temps
    # if 'Date' in data.columns:
    #     st.subheader("Évolution des Commentaires dans le Temps")
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     line_plot = data.groupby(data['Date'].dt.date).size()
    #     ax.plot(line_plot.index, line_plot.values, marker='o', color='orange')
    #     plt.title("Évolution des commentaires dans le temps")
    #     plt.xlabel('Date')
    #     plt.ylabel('Nombre de commentaires')
    #     plt.grid()

    #     for x, y in zip(line_plot.index, line_plot.values):
    #         ax.text(x, y, str(y), fontsize=9, ha='center', va='bottom')
    #     st.pyplot(fig)

    # Corrélation entre Note et Score
    if 'Note' in data.columns and 'score' in data.columns:
        st.subheader("Corrélation entre la Note et le Score")
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(data['Note'], data['score'], alpha=0.5)
        plt.title('Corrélation entre la Note et le Score')
        plt.xlabel('Note')
        plt.ylabel('Score')
        st.pyplot(fig)

    # Distribution des scores
    if 'score' in data.columns:
        st.subheader("Distribution des Scores")
        fig, ax = plt.subplots(figsize=(8, 6))
        n, bins, patches = ax.hist(data['score'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)

        for i in range(len(patches)):
            ax.text(
                x=(bins[i] + bins[i+1]) / 2,
                y=n[i] + 0.5,
                s=f'{int(n[i])}',
                ha='center',
                fontsize=8,
                fontweight='bold'
            )

        plt.title('Distribution des Scores', fontweight='bold')
        plt.xlabel('Score', fontweight='bold')
        plt.ylabel('Fréquence', fontweight='bold')
        plt.grid(axis='y')
        st.pyplot(fig)

    # Boxplot des scores par sentiment
    if 'score' in data.columns and 'prediction_class' in data.columns:
        st.subheader("Boxplot des Scores par Sentiment")
        fig, ax = plt.subplots(figsize=(10, 6))
        data.boxplot(column='score', by='prediction_class', grid=False, notch=True, patch_artist=True, ax=ax)
        plt.title('Boxplot des Scores par Sentiment')
        plt.suptitle('')  # Retirer le titre automatique
        plt.xlabel('Sentiment')
        plt.ylabel('Score')
        st.pyplot(fig)

    # Comparaison entre Notes et Prédictions
    if 'Note' in data.columns and 'prediction_numerique' in data.columns:
        st.subheader("Comparaison entre Notes et Prédictions")
        comparison = data[['Note', 'prediction_numerique']].melt(var_name='Type', value_name='Valeur')

        fig, ax = plt.subplots(figsize=(10, 6))
        ax = comparison.groupby(['Type', 'Valeur']).size().unstack(level=0).plot(kind='bar', stacked=False, ax=ax)

        plt.title('Comparaison entre Notes et Prédictions', fontsize=14)
        plt.xlabel('Valeur (Note ou Prédiction)', fontsize=12)
        plt.ylabel('Fréquence', fontsize=12)
        plt.xticks(rotation=0, fontsize=10)
        plt.legend(title='Légende', loc='upper right', fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for container in ax.containers:
            for bar in container:
                height = bar.get_height()
                if height > 0:
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        height,
                        f'{int(height)}',
                        ha='center',
                        va='bottom',
                        fontweight='bold',
                        fontsize=8
                    )
        st.pyplot(fig)
