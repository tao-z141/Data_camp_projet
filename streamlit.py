import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Visualisation des Scores et Notes après Classification", layout="wide")

st.title("Visualisation des Scores, Notes et Résultat de la Classification")
st.markdown("""
    Cette application permet de visualiser les résultats d'un modèle de classification appliqué à des données d'avis. 
    Voici comment l'utiliser :
    
    1. **Téléchargez un fichier CSV contenant les résultats du modèle de classification non normalisé** 
    (ex: `avis_pred.csv`). Vous pourrez visualiser la répartition des catégories d'étoiles et des prédictions.
    
    2. **Téléchargez un fichier CSV contenant les résultats normalisés** 
    (ex: `avis_pred_visu.csv`) pour visualiser les graphiques des notes réelles, des prédictions et des scores.
    
    **Important :**
    - Le fichier non normalisé contient obligatoirement la colonne `prediction` pour les résultats du modèle.
    - Le fichier normalisé contient obligatoirement les colonnes `Note` pour les valeurs réelles, `prediction` pour les classifications et `score`.
""")

uploaded_file = st.file_uploader("Chargez votre fichier CSV issu du modèle de classification non normalisé (ex: avis_pred.csv)", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file, delimiter=";")
    
    st.write("Aperçu des données :")
    st.dataframe(data.head())

    star_count = data['prediction'].value_counts().sort_index()
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x=star_count.index, y=star_count.values, palette="viridis")
    plt.xlabel("Catégorie d'étoiles (classification)", fontsize=12)
    plt.ylabel("Nombre d'avis", fontsize=12)
    plt.title("Répartition de la satisfaction selon la catégorie d'étoiles", fontsize=14)

    for i, value in enumerate(star_count.values):
        plt.text(i, value + 0.5, str(value), ha='center', fontsize=10)

    description = """
    1 étoile: représente une appréciation très mauvaise,
    2 étoiles: appréciation mauvaise,
    3 étoiles: appréciation neutre,
    4 étoiles: appréciation bonne,
    5 étoiles: appréciation excellente.
    """
    plt.text(5.5, max(star_count.values) * 0.8, description, fontsize=10, va="top", ha="left")

    plt.tight_layout()
    st.pyplot(fig)
    if "prediction" in data.columns:
        counts = data['prediction'].value_counts().reset_index()
        counts.columns = ['prediction', 'count']

        counts = counts.sort_values(by="prediction")  
        pivot_data = pd.DataFrame({'prediction': counts['prediction'], 'count': counts['count']})

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(
            pivot_data.set_index('prediction').T,  # Mettre "prediction" en index et la transpose pour une heatmap
            annot=True,
            fmt="d",
            cmap="Reds",
            cbar_kws={"label": "Nombre d'occurrences"}
        )

        plt.title("Heatmap des catégories de prédiction", fontsize=14)
        plt.xlabel("Catégorie de prédiction", fontsize=12)
        plt.ylabel("Données", fontsize=12)  # Si une seule ligne, peut rester général
        st.pyplot(fig)
        print("")
        st.markdown("""
                Diagramme à Barres et heatmap: classifications des avis clients
                Objectif :

                Classifier les avis clients entre 1 à 5 star.
                Interprétation et Analyse :

                Les barres(et heatmap) montrent que sur 100 avis recupérés:
                    41 personnes ont eu une appréciation excellente du produit acer.
                    40 personnes ont eu une appréciation bonne du produit acer.
                    7 personnes ont eu un avis neutre.
                    8 personnes ont trouvé le produit mauvais.
                    seulement 4 personnes ont eu une aprpréciation très mauvaise.
                    les résultats de la classification sont conformes au notes mises par les clients.
                """)
        print("")

uploaded_file = st.file_uploader("Chargez votre fichier CSV issu du modèle de classification normalisé pour la visualisation (ex: avis_pred_visu.csv)", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file, delimiter=";")
    df_melted = pd.melt(
    data, 
    id_vars=["Date"], 
    value_vars=["Note", "prediction"], 
    var_name="Type de Note", 
    value_name="Valeur des Notes"
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x="Date", y="Valeur des Notes", hue="Type de Note", data=df_melted, ax=ax)
    ax.set_title("Notes Réelles et Prédictions")
    ax.set_ylabel("Valeur des Notes")
    plt.xticks(rotation=45)
    plt.xticks([])
    plt.tight_layout()  
    st.pyplot(fig)
    st.markdown("""
                Diagramme à Barres : Notes Réelles et classifications
                Objectif :

                Comparer les notes réelles attribuées et les classification faites par le modèle.
                Interprétation et Analyse :

                Les barres représentant les notes réelles et les classification permettent de vérifier si le modèle est précis et cohérent par rapport aux notes réelles.
                Si les barres pour les prédictions et les notes réelles sont proches les unes des autres, cela montre une bonne performance du modèle.
                Les écarts importants entre les barres pourraient indiquer des périodes où le modèle a sous-évalué ou sur-évalué les notes.
                En cas de tendance ou d'écart systématique, cela pourrait révéler un biais temporel dans les classification (par exemple, des classifications moins fiables à certaines périodes)
                Mais le Model dans sa globalité reste trés performant.
    """)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.histplot(data['Note'], bins=5, color='blue', label="Notes Réelles", kde=True, ax=ax2)
    sns.histplot(data['prediction'], bins=5, color='orange', label="Prédictions", kde=True, ax=ax2)
    ax2.set_title("Distribution des Notes Réelles et Prédictions")
    ax2.set_xlabel("Valeur des Notes")
    ax2.set_ylabel("Fréquence")
    ax2.legend()  # Affiche la légende
    plt.tight_layout()
    st.pyplot(fig2)
    st.markdown("""
                Histogramme : Distribution des Notes Réelles et des classifications
                Objectif :

                Visualiser la répartition des valeurs des notes réelles et des classifications pour évaluer leur correspondance globale.
                Interprétation et Analyse :

                Des distributions similaires entre les notes réelles et les classifications indiquent que le modèle capture bien la structure des données.
                Si la distribution des classifications est plus concentrée autour de certaines valeurs par rapport aux notes réelles, cela pourrait indiquer une incapacité du modèle à prédire des valeurs variées.
                Une différence entre les courbes des deux distributions peut montrer un biais systématique, comme une tendance à surestimer ou sous-estimer les notes.
                La forme des distributions (par exemple, symétrique, biaisée à droite ou à gauche) peut aussi fournir des indications sur la qualité des classifications.
                Mais d'apres le résultat de la visualisation montre que le Model est performant.
    """)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['score'], bins=10, kde=True, color='green', ax=ax)
    ax.set_title("Distribution des Scores")
    ax.set_xlabel("Score (0 à 1)")
    ax.set_ylabel("Fréquence")
    plt.tight_layout()
    st.pyplot(fig)  
    st.markdown("""
                Histogramme : Distribution des Scores
                Objectif :

                Analyser la répartition des scores de confiance ou de probabilité (entre 0 et 1) associés aux classifications.
                Interprétation et Analyse :

                Une distribution de scores étalée sur toute la plage (de 0 à 1) indique une bonne variabilité dans la confiance des classifications.
                Si les scores se concentrent autour d'une valeur spécifique (par exemple, 0.5), cela pourrait signifier que le modèle manque de certitude dans ses classifications.
                Des scores élevés proches de 1 pour la plupart des classifications indiquent que le modèle est très confiant, mais cela peut parfois signaler une sur-optimisation.
                Si une proportion importante de scores est inférieure à un seuil critique (par exemple, <0.3), cela pourrait indiquer des lacunes dans les données d'entraînement ou des problèmes dans le modèle.
    """) 