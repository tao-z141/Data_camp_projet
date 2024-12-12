# Analyse des Avis sur les Chaussures de Running sur Decathlon

Ce projet permet de :
1. Récupérer des avis sur des chaussures de running à partir du site Decathlon.
2. Normaliser, classifier et visualiser ces avis.
3. Déployer une application interactive pour les visualisations avec Streamlit.

Le projet repose sur plusieurs bibliothèques Python : **BeautifulSoup**, **Selenium**, **Streamlit**, **re**, **unidecode**, **optimum.onnxruntime** ,**transformers**, **Pandas**, **Seaborn**, et **Matplotlib**.

## Prérequis
Avant de commencer, assurez-vous d'avoir installé les outils et bibliothèques nécessaires sur votre machine :

### Outils requis
- **Python** (version 3.7 ou supérieure) ou **Anaconda** (pour exécuter le code dans JupyterLab ou directement avec Python).

### Installation des bibliothèques
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
   - Depuis Google Colab :
     ```python
     pip install unidecode
      ```
2. **Installer optimum** :
   - Depuis Google Colab :
     ```python
     pip install optimum
      ```
3. **Installer onnxruntime** :
- Depuis Google Colab :
     ```python
     pip install onnxruntime
      ```
4. **Installer  optimum onnxruntime onnx** :
   - Depuis Google Colab :
     ```python
     pip install  optimum onnxruntime onnx
      ```
    
5. **Installer  cupy-cuda11x** :
   - Depuis Google Colab :
     ```python
      !pip install cupy-cuda11x
      ```

#### Visualisation



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

### Utilisation d'un fichier Jupyter Notebook
Tous ces scripts sont regroupés dans le fichier `Projet.ipynb`, que vous pouvez utiliser pour une meilleure lisibilité et un suivi d'exécution clair.

### Visualisation avec Streamlit
1. Activez l'environnement Streamlit :
   ```bash
   conda activate vesu
   ```
2. Lancez l'application Streamlit :
   ```bash
   python streamlit.py
   streamlit run streamlit.py
   ```
  

## Déploiement de l'application sur Streamlit Cloud
1. **Fichier principal** : `streamlit.py` (contient le code de l'application).
 Vous pouvez lancer le code en lancant cette 

### URL de l'application




