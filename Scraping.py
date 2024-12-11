import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.decathlon.fr/r/chaussures-de-running-femme-kalenji-run-active-grip-gris-rose/_/R-p-100260?mc=8544265&c=BLEU')
driver.implicitly_wait(5)

pages = 38
current_page = 1

data = []

soup = BeautifulSoup(driver.page_source, 'html.parser')

title_element = soup.find('h1', class_='vtmn-leading-tight vtmn-font-normal vtmn-uppercase vtmn-m-0')
title = title_element.text.strip() if title_element else "Titre non trouvé"
print(f"Titre du produit : {title}")

while current_page <= pages:
    print(f"Scraping page {current_page} des avis...")
    time.sleep(5) 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    comments_section = soup.find_all('article', class_='review-item vtmn-flex vtmn-flex-col vtmn-px-3 vtmn-py-4 vtmn-border-t vtmn-border-border-primary svelte-yoqbtd')
    
    for review in comments_section:
        try:
            author = review.find('div', class_='vtmn-text-lg vtmn-text-content-secondary vtmn-font-bold').text.strip()
            date = review.find('time', class_='vtmn-mt-1 vtmn-text-sm')['datetime']
            comment_content = review.find('p', class_='review-item__body vtmn-break-words vtmn-pt-3 vtmn-mb-0 vtmn-whitespace-pre-line svelte-yoqbtd').text.strip()
            rate = review.find('span', class_='vtmn-rating_comment--primary').text.strip()
            
            data.append({
                'Auteur': author,
                'Date': date,
                'Commentaire': comment_content,
                'Note': rate
            })
            
        except AttributeError as e:
            print(f"Erreur lors de l'extraction d'un avis : {e}")

    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next review page" and @aria-disabled="false"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)  
        driver.execute_script("arguments[0].click();", next_button)
        current_page += 1
        time.sleep(3)  
    except NoSuchElementException:
        print("Bouton 'Suivant' introuvable.")
        break
    except ElementClickInterceptedException as e:
        print(f"Erreur : {str(e)}. Tentative de fermeture d'éléments bloquants.")
        try:
            overlay_close = driver.find_element(By.CSS_SELECTOR, ".popup-close-class")  
            overlay_close.click()
            time.sleep(2)
        except NoSuchElementException:
            print("Pas d'élément bloquant.")
        continue

driver.quit()

csv_name = "Bronze/Article_data.csv"
csv_colonnes = ['Auteur', 'Date', 'Commentaire', 'Note']

try:
    with open(csv_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_colonnes)
        writer.writeheader()
        for i in data:
            writer.writerow(i)
    print(f"Les données ont été sauvegardées dans le fichier '{csv_name}' avec succès.")
except IOError as e:
    print(f"Erreur lors de l'écriture du fichier CSV : {e}")
