import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from bs4 import BeautifulSoup

# Configurer le driver
driver = webdriver.Chrome()
driver.get('https://www.decathlon.fr/r/chaussures-de-running-femme-kalenji-run-active-grip-gris-rose/_/R-p-100260?mc=8544265&c=BLEU')
driver.implicitly_wait(5)

# Pages à scraper
pages_to_scrape = 38
current_page = 1

# Stockage des données dans un tableau
data = []

# Utiliser BeautifulSoup pour extraire les informations
soup = BeautifulSoup(driver.page_source, 'html.parser')

title_element = soup.find('h1', class_='vtmn-leading-tight vtmn-font-normal vtmn-uppercase vtmn-m-0')
title = title_element.text.strip() if title_element else "Titre non trouvé"
print(f"Titre du produit : {title}")

while current_page <= pages_to_scrape:
    print(f"Scraping page {current_page} des avis...")
    time.sleep(5)  # Attendre le chargement complet de la page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Trouver tous les articles contenant un avis
    comments_section = soup.find_all('article', class_='review-item vtmn-flex vtmn-flex-col vtmn-px-3 vtmn-py-4 vtmn-border-t vtmn-border-border-primary svelte-yoqbtd')
    
    for review in comments_section:
        try:
            author = review.find('div', class_='vtmn-text-lg vtmn-text-content-secondary vtmn-font-bold').text.strip()
            date = review.find('time', class_='vtmn-mt-1 vtmn-text-sm')['datetime']
            comment_content = review.find('p', class_='review-item__body vtmn-break-words vtmn-pt-3 vtmn-mb-0 vtmn-whitespace-pre-line svelte-yoqbtd').text.strip()
            rate = review.find('span', class_='vtmn-rating_comment--primary').text.strip()

            # Ajouter les données dans la liste
            data.append({
                'Auteur': author,
                'Date': date,
                'Commentaire': comment_content,
                'Note': rate
            })
            
        except AttributeError as e:
            print(f"Erreur lors de l'extraction d'un avis : {e}")

    # Allez à la page suivante
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next review page" and @aria-disabled="false"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)  # Attendre la fin des animations
        driver.execute_script("arguments[0].click();", next_button)
        current_page += 1
        time.sleep(3)  # Attendre le chargement de la nouvelle page
    except NoSuchElementException:
        print("Bouton 'Suivant' introuvable ou désactivé. Fin du scraping.")
        break
    except ElementClickInterceptedException as e:
        print(f"Erreur : {str(e)}. Tentative de fermeture d'éléments bloquants.")
        # Gestion des popups ou overlays
        try:
            overlay_close = driver.find_element(By.CSS_SELECTOR, ".popup-close-class")  # Exemple de popup
            overlay_close.click()
            time.sleep(2)
        except NoSuchElementException:
            print("Pas d'élément bloquant identifié.")
        continue

driver.quit()

# Écrire les données dans un fichier CSV
csv_file_name = "Article1_data.csv"
csv_columns = ['Auteur', 'Date', 'Commentaire', 'Note']

try:
    with open(csv_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
    print(f"Les données ont été sauvegardées dans le fichier '{csv_file_name}' avec succès.")
except IOError as e:
    print(f"Erreur lors de l'écriture du fichier CSV : {e}")
