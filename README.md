# Analyse des Avis sur les Chaussures de Running sur Decathlon

Ce projet permet de :
1. Récupérer des avis sur des chaussures de running à partir du site Decathlon.
2. Normaliser, classifier et visualiser ces avis.
3. Déployer une application interactive pour les visualisations avec Streamlit.

Le projet repose sur plusieurs bibliothèques Python : **BeautifulSoup**, **Selenium**, **Streamlit**, **re**, **unidecode**, **optimum.onnxruntime** ,**transformers**, **Pandas**, **Seaborn**, et **Matplotlib**.

## Prérequis
Avant de commencer, assurez-vous d'avoir installé les outils et bibliothèques nécessaires sur votre machine :

### Outils requis
- pour le scrapping et la partie streamlit ( dashboard ) utilisez **Python** ou **Anaconda** (pour exécuter le code dans JupyterLab ou directement avec Python)
- pour le pretraitment et la classification utilisez **google collab**

### Installation des dépendances
Pour installer les dependances et les bibliotheque necessaire , vous avez le choix d'executer le fichier requirement ou d'installer chaque bibliotheque independament : 
     ```bash
     pip install -r requirements.txt
     ```
#### Scraping
1. **Installer BeautifulSoup** :
   - Depuis l'Anaconda Prompt :
     ```bash
     pip install beautifulsoup4
     ```
   - Depuis un notebook Jupyter :
     ```python
     !pip install beautifulsoup4
     ```
2. **Installer Selenium** :
   - Depuis l'Anaconda Prompt :
     ```bash
     pip install selenium
     pip install webdriver-manager
     ```
   - Depuis un notebook Jupyter :
     ```python
     !pip install selenium
     !pip install webdriver-manager
     ```

#### Prétraitement et classification
1. **Installer unidecode** :
   - Depuis un Google collab:
     ```python
     pip install unidecode
      ```
2. **Installer optimum** :
   - Depuis un Google collab :
     ```python
      pip install optimum
      ```
3. **Installer onnxruntime** :
- Depuis un Google collab :
     ```python
      pip install onnxruntime
      ```
4. **Installer  optimum onnxruntime onnx** :
   - Depuis un Google collab :
     ```python
       pip install  optimum onnxruntime onnx
      ```
    
5. **Installer  cupy-cuda11x** :
   - Depuis un Google collab :
     ```python
      pip install cupy-cuda11x
      ```


#### Visualisation
1. **Installer pandas** :
     ```python
     pip install pandas
      ```
2. **Installer plotly** :
     ```python
     pip install plotly
      ```


#### Streamlit 
Utilisé pour afficher les résultats sous forme de graphiques interactifs.
- Installez Streamlit avec :
  ```bash
  pip install streamlit
  ```

## Ordre d'exécution
### Depuis l'Anaconda Prompt
1. Activez votre environnement virtuel :
   ```bash
   conda activate myenv
   ```

2. Exécutez les scripts dans l'ordre suivant :
   1. **Extraction des avis** :
      ```bash
      python extraction.py
      ```
      (Génère ` Article_data.csv`)
   2. **Normalisation des avis** :
      ```bash
      python Prétraitement.ipynb
      ```
      (Génère ` data_pretraité.csv`)
   3. **Classification des avis** :
      ```bash
      python classification.ipynb
      ```
      (Génère ` prediction.csv`, utilisé pour la visualisation)
   4. **Streamlit** :
      Pour exécuter Streamlit, assurez-vous que l'image Decathlon ainsi que le fichier prediction.csv se trouvent dans le même répertoire que votre fichier streamlit.py, puis exécutez la commande suivante :
  ```bash
      streamlit run  streamlit.py 
      ```

## Déploiement de l'application sur Streamlit Cloud
1. **Fichier principal** : `streamlit.py` (contient le code de l'application).
 Vous pouvez lancer l'application en executant cette commande sur votre terminal : 
   ```bash
   streamlit run streamli  t.py
   ```

### URL de l'application




