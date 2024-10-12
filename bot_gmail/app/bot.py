from seleniumwire import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from indian_names import get_first_name, get_last_name
from datetime import date
import time
import random
import string
import requests
import csv
import json


proxy = {
    'http': 'socks5://FHU5X7HJ:FHU5X7HJ@90.119.64.63:30018',
    'https': 'socks5://FHU5X7HJ:FHU5X7HJ@90.119.64.63:30018',
}

rotation_url = 'http://90.119.64.63/selling/rotate?token=8ce0eebbdb5044f2a25089a390f70790'

def get_public_ip():
    try:
        # Requête vers https://api.ipify.org pour obtenir l'IP publique via le proxy
        response = requests.get('https://api.ipify.org', proxies=proxy, timeout=10)
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de l'IP publique via le proxy : {e}")
        return None

def rotate_ip():
    try:
        # Requête pour déclencher la rotation d'IP
        response = requests.get(rotation_url)
        if response.status_code == 200:
            print("Rotation d'IP effectuée avec succès.")
        else:
            print(f"Erreur lors de la rotation d'IP : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la rotation d'IP : {e}")

def rotate_and_check_ip():
    # Obtenir l'IP avant la rotation
    print("IP avant la rotation :")
    initial_ip = get_public_ip()
    if initial_ip:
        print(f"IP initiale : {initial_ip}")

    # Effectuer la rotation d'IP
    rotate_ip()

    # Attendre quelques secondes pour laisser le temps à la rotation de s'appliquer
    time.sleep(10)

    # Obtenir l'IP après la rotation
    print("IP après la rotation :")
    new_ip = get_public_ip()
    if new_ip:
        print(f"Nouvelle IP : {new_ip}")

def setup_browser(url):
    # Liste des user-agents pour simuler différents navigateurs
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (X11; CrOS x86_64 14440.0.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4807.0 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (X11; CrOS x86_64 14440.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4807.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14467.0.2022) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4838.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.7.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14455.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4827.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.17 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14436.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4803.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14475.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14471.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14409.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4829.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14395.0.2021) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4765.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.14 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14484.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14450.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4817.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14473.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14324.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.91 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14454.0.2022) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4824.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14453.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4816.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14447.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4815.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14477.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14476.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.22 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.57.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.64 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.93 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.91.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.55 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.23.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.20 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.36.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.36 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.26 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14682.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.16 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.9.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.5 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14574.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4937.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14716.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14268.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.48 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.61.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.37 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.51.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.32 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.56 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.43.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.54 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14505.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4870.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.16.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.25 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.28.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.44 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14543.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4918.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.31.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.19 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14658.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4975.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36'
    ]

    # Sélection aléatoire d'un user-agent
    user_agent = random.choice(user_agents)
    print(f"User-Agent sélectionné : {user_agent}")

    # Informations sur le proxy SOCKS5
    proxy_options = {
        'proxy': {
            'http': 'socks5://FHU5X7HJ:FHU5X7HJ@90.119.64.63:30018',
            'https': 'socks5://FHU5X7HJ:FHU5X7HJ@90.119.64.63:30018',
            'no_proxy': 'localhost,127.0.0.1'  # Ne pas utiliser le proxy pour ces adresses
        }
    }

    # Configuration des options de Chrome
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={user_agent}")  # Utilisation du user-agent sélectionné
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Contourner les protections anti-robots
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('--no-sandbox')  # Options pour éviter certains problèmes de compatibilité
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialiser le WebDriver avec Selenium Wire et les options de proxy
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=proxy_options, options=chrome_options)
        print("Navigateur lancé avec succès.")
    except Exception as e:
        print(f"Erreur lors du lancement du navigateur : {e}")
        return None

    # Masquer la propriété 'webdriver' pour contourner certaines détections anti-robots
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Accéder à l'URL
    try:
        driver.get(url)
        print(f"Accès à {url} effectué avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'accès à l'URL : {e}")
        driver.quit()  # Fermer le navigateur en cas d'erreur
        return None

    return driver

def prenom(driver):
    try:
        prenoms = []

        # Ouvrir le fichier CSV dans le bloc 'with' pour s'assurer qu'il est bien ouvert pendant la lecture
        with open('app/prenom.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                prenoms.append(row[0])  # Ajouter chaque prénom à la liste
        
        # Choisir un prénom aléatoire parmi la liste
        prenom_choisi = random.choice(prenoms)

        print("Le prénom choisi est :", prenom_choisi)
        
        # Créer une instance d'ActionChains avec le driver
        actions = ActionChains(driver)
        
        # Saisir chaque caractère avec un délai aléatoire entre chaque frappe
        for char in prenom_choisi:
            actions.send_keys(char)
            actions.perform()
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe
        
        # Appuyer sur la touche Tab pour passer au champ suivant
        actions.send_keys(Keys.TAB)
        actions.perform()
        
        # Attendre un peu avant de passer à l'étape suivante
        time.sleep(2)

        # Retourner le prénom généré
        return prenom_choisi
        
    except Exception as e:
        print(f"Erreur lors de la saisie du prénom : {e}")
        return None
 
def nom(driver):
    try:
        with open('app/nom_français.json', 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)  

        last_name = data['noms_de_famille']

        noms_de_famille_choisi = random.choice(last_name)


        print("Le noms_de_famille choisi est :", noms_de_famille_choisi)
        
        # Créer une instance d'ActionChains avec le driver
        actions = ActionChains(driver)
        
        # Saisir chaque caractère du nom de famille avec un délai aléatoire entre chaque frappe
        for char in noms_de_famille_choisi:
            actions.send_keys(char)
            actions.perform()
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe
        
        # Appuyer sur la touche Tab pour passer au champ suivant
        actions.send_keys(Keys.TAB)
        actions.perform()
        
        # Attendre un peu avant de passer à l'étape suivante
        time.sleep(2)

        # Appuyer sur la touche Entrée (si nécessaire)
        actions.send_keys(Keys.ENTER).perform()

        # Retourner le nom de famille généré
        return noms_de_famille_choisi
        
    except Exception as e:
        print(f"Erreur lors de la saisie du nom : {e}")
        return None

def saisir_jour(driver):
    try:
        # Générer un nombre aléatoire entre 1 et 26
        nombre_aleatoire = random.randint(1, 26)
        print(f"Nombre aléatoire généré : {nombre_aleatoire}")

        # Trouver le champ du jour par XPath
        champ_jour = driver.find_element(By.XPATH, '//*[@id="day"]')

        # Créer une instance d'ActionChains pour simuler un déplacement et un clic
        actions = ActionChains(driver)
        
        # Déplacer la souris vers le champ et cliquer dessus
        actions.move_to_element(champ_jour).pause(random.uniform(0.2, 0.5)).click().perform()

        # Attendre un peu avant de commencer à saisir
        time.sleep(random.uniform(0.2, 0.5))

        # Saisir chaque chiffre du nombre avec un délai aléatoire
        for digit in str(nombre_aleatoire):
            champ_jour.send_keys(digit)
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe

        # Attendre un peu après la saisie
        time.sleep(2)

        print(f"Le nombre {nombre_aleatoire} a été saisi dans le champ.")

    except Exception as e:
        print(f"Erreur lors de la saisie du jour : {e}")

def choisir_mois(driver):
    try:
        # Générer un nombre aléatoire entre 1 et 12 pour sélectionner le mois
        mois_aleatoire = random.randint(1, 12)
        print(f"Mois choisi : {mois_aleatoire}")

        # Trouver le champ du menu déroulant pour les mois par son XPath
        champ_mois = driver.find_element(By.XPATH, '//*[@id="month"]')

        # Utiliser Select pour interagir avec le menu déroulant
        select_mois = Select(champ_mois)

        # Sélectionner le mois par son index. Les mois commencent à option[2], donc nous décalons de +1.
        select_mois.select_by_index(mois_aleatoire)

        # Attendre un peu pour vérifier l'action
        time.sleep(2)
        print(f"Le mois numéro {mois_aleatoire} a été sélectionné.")

    except Exception as e:
        print(f"Erreur lors de la sélection du mois : {e}")

def choisir_annee(driver):
    try:
        # Ouvrir le fichier CSV et lire les données
        with open('app/date_naissence.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Lire la première ligne et extraire l'année 1
            line1 = next(reader)
            if '=' in line1[0]:
                year1 = line1[0].split('=')[1].strip()  # Extraire la valeur après le signe '='
            else:
                year1 = 'Non trouvé'  # Valeur par défaut si non trouvée
            
            # Lire la deuxième ligne et extraire l'année 2
            line2 = next(reader)
            if '=' in line2[0]:
                year2 = line2[0].split('=')[1].strip()  # Extraire la valeur après le signe '='
            else:
                year2 = 'Non trouvé'  # Valeur par défaut si non trouvée

        # Afficher les deux années extraites
        print("Année 1:", year1)
        print("Année 2:", year2)

        # Générer une année aléatoire entre year1 et year2
        annees = random.randint(int(year1), int(year2))
        print(f"Année choisie : {annees}")

        # Trouver le champ de saisie pour l'année par son XPath
        champ_annee = driver.find_element(By.XPATH, '//*[@id="year"]')

        # Cliquer sur le champ pour le rendre actif
        champ_annee.click()

        # Effacer le champ avant d'y saisir une nouvelle valeur
        champ_annee.clear()

        # Saisir chaque chiffre de l'année avec un délai aléatoire entre chaque frappe
        for digit in str(annees):
            champ_annee.send_keys(digit)
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe

        # Attendre un peu pour vérifier l'action
        time.sleep(2)
        print(f"L'année {annees} a été saisie dans le champ.")

    except Exception as e:
        print(f"Erreur lors du choix de l'année : {e}")

def choisir_genre(driver):
    try:
        # Trouver le champ du menu déroulant pour le genre par son XPath
        champ_genre = driver.find_element(By.XPATH, '//*[@id="gender"]')

        # Utiliser Select pour interagir avec le menu déroulant
        select_genre = Select(champ_genre)

        # Sélectionner l'option "Femelle" par son index. Ici, option[2] correspond à l'index 1 (index basé sur 0)
        select_genre.select_by_index(1)

        # Attendre un peu pour vérifier l'action
        time.sleep(2)
        print("Le genre 'Femelle' a été sélectionné.")

    except Exception as e:
        print(f"Erreur lors de la sélection du genre : {e}")

def date_nass_suivant(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="birthdaygenderNext"]/div/button/span'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()

        # Confirmation du clic
        print("Le bouton 'Suivant' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

def cliquer_creer_adresse_mail(driver):
    try:
        # Attendre que l'élément "Créer une adresse mail" soit cliquable
        creer_adresse_mail = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[1]/div/div[3]/div/div[3]/div'))
        )
        
        # Cliquer sur l'élément
        creer_adresse_mail.click()
        print("Le bouton 'Créer une adresse mail' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur 'Créer une adresse mail' : {e}")

def cliquer_suivant(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button/span'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'Suivant' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

def generer_nom_utilisateur(prenom, nom):
    # Générer un nombre aléatoire entre 9999 et 100000
    nombre_aleatoire = random.randint(9999, 100000)
    # Combiner le prénom, le nom et le nombre aléatoire
    nom_utilisateur = f"{prenom}.{nom}{nombre_aleatoire}"
    return nom_utilisateur

def verifier_et_ecrire_username(driver, first_name, last_name):
    # XPath de l'élément à vérifier
    xpath = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div/div[1]/div/div[1]/div/div[1]/input'

    try:
        # Vérifier si l'élément avec le XPath donné est présent
        element_present = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        if element_present:
            # Si l'élément est présent, cliquer dessus
            element_present.click()
            print("Élément trouvé et cliqué avec succès.")
            
            # Générer le nom d'utilisateur
            nom_utilisateur = generer_nom_utilisateur(first_name, last_name)
            print(f"Nom d'utilisateur généré : {nom_utilisateur}")
            
            # Saisir chaque caractère du nom d'utilisateur avec un délai aléatoire
            for char in nom_utilisateur:
                element_present.send_keys(char)
                time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre les frappes
            time.sleep(2)
            champ_username = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[1]/div/div[3]/div')))
            champ_username.click()

    except Exception as e:
        print(f"L'élément n'a pas été trouvé ou une erreur s'est produite : {e}")

    # Retourner False pour indiquer que l'élément n'a pas été trouvé
    return False

def suivents_username_bis(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*//*[@id="next"]/div/button/span"]'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'Suivant' a été cliqué avec succès.")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")
 
def ecrire_nom_utilisateur(driver, prenom, nom):
    try:
        # Générer le nom d'utilisateur
        nom_utilisateur = generer_nom_utilisateur(prenom, nom)
        print(f"Nom d'utilisateur généré : {nom_utilisateur}")

        # Attendre que le premier champ soit cliquable et cliquer dessus
        champ_username = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[1]/div/div[3]/div'))
        )
        champ_username.click()
        time.sleep(1)  # Attendre un peu après le clic

        # Attendre que le deuxième champ soit cliquable et cliquer dessus
        champ_supplementaire = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input'))
        )
        champ_supplementaire.click()
        time.sleep(1)  # Attendre un peu après le clic

        # Saisir chaque caractère du nom d'utilisateur avec un délai aléatoire entre chaque frappe
        for char in nom_utilisateur:
            champ_supplementaire.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe

        # Attendre un peu pour vérifier l'action
        time.sleep(2)
        print("Le nom d'utilisateur a été saisi avec succès.")

    except Exception as e:
        print(f"Erreur lors de la saisie du nom d'utilisateur : {e}")

def username_suivant(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next"]/div/button/span'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'Suivant' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

def password(driver):
    try:
        # Créer une instance d'ActionChains
        actions = ActionChains(driver)
        
        # Définir les caractères possibles pour le mot de passe
        characters = string.ascii_letters + string.digits + string.punctuation
        
        # Générer un mot de passe aléatoire de 12 caractères
        mot_de_passe = ''.join(random.choice(characters) for i in range(12))
        
        # Afficher le mot de passe généré
        print(f"Mot de passe généré : {mot_de_passe}")
        
        # Saisir le mot de passe généré dans le champ actif, caractère par caractère
        for char in mot_de_passe:
            driver.switch_to.active_element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe
        
        # Attendre un peu avant de passer au champ suivant
        time.sleep(2)
        
        # Appuyer sur Tab pour passer au champ de confirmation (si nécessaire)
        actions.send_keys(u'\uE004').perform()
        time.sleep(1)
        
        # Saisir à nouveau le mot de passe dans le champ de confirmation, caractère par caractère
        for char in mot_de_passe:
            driver.switch_to.active_element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire entre chaque frappe
 
        # Attendre un peu pour vérifier l'action
        time.sleep(2)

        return mot_de_passe

    except Exception as e:
        print(f"Erreur lors de la génération ou confirmation du mot de passe : {e}")

def password_suivant(driver):
    try:
        actions = ActionChains(driver)
        time.sleep(3)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(3)
        print("Le bouton 'Suivant' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

def go_num(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="phoneNumberId"]'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'Suivant' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

def buy_num_and_get_otp(driver):
    api_key = 'cA41b33A372dccd7b771A1A07dc785Ab'
    service = 'go'
    country = '78'

    # URL de l'API pour obtenir un numéro
    url = f'https://api.sms-activate.io/stubs/handler_api.php?api_key={api_key}&action=getNumber&service={service}&country={country}'

    # Essayer jusqu'à 3 fois pour obtenir un numéro
    for attempt in range(10):
        response = requests.get(url)
        print(f"Tentative {attempt + 1}: Réponse de l'API pour l'obtention du numéro : {response.text}")

        # Vérifier si la réponse est correcte
        if response.status_code == 200 and response.text.startswith("ACCESS_NUMBER"):
            # Diviser la réponse pour isoler l'ID et le numéro
            parts = response.text.split(":")
            activation_id = parts[1]
            numero = parts[2]
            numero_full = f"+{numero}"
            print(f"Le numéro : {numero_full}")
            print(f"L'ID : {activation_id}")

            try:
                # Utiliser l'élément actif pour saisir le numéro
                active_element = driver.switch_to.active_element

                # Saisir chaque caractère du numéro avec un délai aléatoire
                for char in numero_full:
                    active_element.send_keys(char)
                    time.sleep(random.uniform(0.1, 0.3))
                
                # Attendre un peu après la saisie
                time.sleep(2)

                # Attendre que le bouton "Suivant" soit cliquable
                bouton_suivant = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button/span'))
                )
                bouton_suivant.click()
                print("Le bouton 'num' a été cliqué avec succès.")

                # Récupérer l'OTP
                otp_url = f'https://api.sms-activate.io/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={activation_id}'
                time.sleep(2)
                # Vérifier l'OTP 5 fois, toutes les 20 secondes
                for otp_attempt in range(4):
                    try:
                        otp_response = requests.get(otp_url)
                        otp_response.raise_for_status()
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur lors de la requête HTTP : {e}")
                        continue

                    # Afficher la réponse brute
                    print(f"Tentative OTP {otp_attempt + 1}: {otp_response.text}")

                    # Vérifier et extraire l'OTP si présent
                    if otp_response.text.startswith("STATUS_OK"):
                        otp_code = otp_response.text.split(':')[1]
                        print(f"L'OTP reçu est : {otp_code}")

                        try:
                            # Saisir l'OTP dans le champ actif
                            active_element = driver.switch_to.active_element
                            active_element.send_keys(otp_code)
                            for char in otp_code:
                                active_element.send.key(char)
                                time.sleep(random.uniform(0.1, 0.3))
                            print("L'OTP a été saisi avec succès.")
                        except Exception as e:
                            print(f"Erreur lors de l'envoi de l'OTP : {e}")
                        return  # Sortir de la fonction si l'OTP est trouvé
                    elif otp_response.text.startswith("STATUS_WAIT_CODE"):
                        print("En attente de l'OTP...")
                    else:
                        print("Une erreur s'est produite :", otp_response.text)

                    # Attendre 20 secondes avant la prochaine vérification
                    time.sleep(20)

                # Si on arrive à la fin des 5 tentatives, fermer la page et retourner un code 404
                print("Nombre maximal de tentatives d'OTP atteint. Fermeture du navigateur.")
                driver.quit()
                return 404  # Retourner un code 404 pour signaler l'échec des tentatives d'OTP

            except Exception as e:
                print(f"Erreur lors de l'envoi du numéro ou du clic sur 'Suivant' : {e}")
            break  # Sortir de la boucle si le numéro a été obtenu avec succès
        
        else:
            print(f"Erreur : La réponse de l'API est incorrecte ou ne contient pas de numéro valide. Tentative {attempt + 1} a échoué.")

        # Attendre 5 secondes avant de réessayer
        if attempt < 2:
            print("Nouvelle tentative dans 5 secondes...")
            time.sleep(5)

    # Si les 3 tentatives échouent, afficher un message d'erreur
    print("Impossible d'obtenir un numéro après 3 tentatives.")
    driver.quit()
    return 404  # Retourner un code 404 si le numéro n'a pas pu être obtenu

def suivents_otp(driver):
    try:
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="next"]/div/button/span'))
        )
        bouton_suivant.click()
        print("Le bouton 'Suivant' a été cliqué avec succès.")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'Suivant' : {e}")

def saisir_adresse_humaine(driver):
    try:
        # Attendre que le champ "Email de récupération" soit cliquable
        champ_email_recup = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recoveryEmailId"]'))
        )
        champ_email_recup.click()
        print("Le champ 'Email de récupération' a été cliqué avec succès.")
    except Exception as e:
        print(f"Erreur lors du clic sur le champ 'Email de récupération' : {e}")
        quit.driver()
        return  # Arrêter l'exécution si une erreur se produit

    # Générer une adresse e-mail aléatoire
    nombre_aleatoire_recup = random.randint(9999, 100000)
    nom_recup = get_last_name()  # Remplacez par votre fonction pour obtenir un nom de famille
    prenom_recup = get_first_name()  # Remplacez par votre fonction pour obtenir un prénom
    adresse_recup = f"{nom_recup}.{prenom_recup}{nombre_aleatoire_recup}@hotmail.com"
    print(f"Adresse e-mail générée : {adresse_recup}")
    
    # Saisir chaque caractère dans le champ avec un délai aléatoire
    for char in adresse_recup:
        champ_email_recup.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  # Délai aléatoire pour simuler une saisie humaine
    return adresse_recup

def suivents_recup(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recoveryNext"]/div/button/span'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'suivents_recup' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'suivents_recup' : {e}")

def suivents_ignore_num(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="recoverySkip"]/div/button/span'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'suivents_ignore_num' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'suivents_ignore_num' : {e}")

def suivents_suit(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button/span'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'suivents_suit' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'suivents_suit' : {e}")

def experss(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]/div/div[3]/div'))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'experss' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'experss' : {e}")

def suiv_experss(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable en utilisant un XPath basé sur le texte
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Suivant']"))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'suiv_experss' a été cliqué avec succès.")
    
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'suiv_experss' : {e}")

def defiler_jusqu_en_bas(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Défilement jusqu'en bas de la page effectué avec JavaScript.")

def acepte_suivent(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Tout accepter']"))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'acepte_suivent' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'acepte_suivent' : {e}")

def confirme(driver):
    try:
        # Attendre que le bouton "Suivant" soit cliquable
        bouton_suivant = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Confirmer']"))
        )
        
        # Cliquer sur le bouton "Suivant"
        bouton_suivant.click()
        print("Le bouton 'confirme' a été cliqué avec succès.")

    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'confirme' : {e}")

def acepte(driver):
    try:
        bouton_jaccepte = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='VfPpkd-vQzf8d']"))
        )
        bouton_jaccepte.click()
        print("Le bouton 'J'accepte' a été cliqué avec succès.")
    except Exception as e:
        print(f"Erreur lors du clic sur le bouton 'J'accepte' : {e}")
        return False


def ecrit_gmail(generer_nom_utilisateur, password, saisir_adresse_humaine):
    with open('GMAIL.csv', mode='w', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv)
    
    info = f"{generer_nom_utilisateur}:{password}:{saisir_adresse_humaine}"

    writer.writerow([info])  

print("Les GMAIL ont été écrites dans le fichier GMAIL.csv avec succès.")





def start_full_process():
    # Effectuer la rotation d'IP avant de lancer le navigateur
    rotate_and_check_ip()

    # Lancer le navigateur avec l'URL de création de compte Google
    url = 'https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp'
    driver = setup_browser(url)

    # Si le navigateur a été lancé avec succès
    if driver:
        print("Le navigateur est prêt pour les interactions.")
    else:
        print("Le navigateur n'a pas pu être initialisé.")
        return False  # Arrêter le processus si le navigateur ne démarre pas

    try:
        # Exécuter toutes les étapes de création de compte
        time.sleep(2)

        # Générer et récupérer le prénom
        first_name = prenom(driver)
        time.sleep(2)

        # Générer et récupérer le nom de famille
        last_name = nom(driver)
        time.sleep(2)

        # Saisir la date de naissance et le genre
        saisir_jour(driver)
        time.sleep(2)
        choisir_mois(driver)
        time.sleep(2)
        choisir_annee(driver)
        time.sleep(2)
        choisir_genre(driver)
        time.sleep(2)
        date_nass_suivant(driver)
        time.sleep(2)

        # Créer une adresse e-mail
        cliquer_creer_adresse_mail(driver)
        time.sleep(2)
        cliquer_suivant(driver)
        time.sleep(2)

        # Générer le nom d'utilisateur
        username = generer_nom_utilisateur(first_name, last_name)
        time.sleep(2)

        # Vérifier et écrire le nom d'utilisateur
        username_written = verifier_et_ecrire_username(driver, first_name, last_name)
        time.sleep(2)

        # Si le nom d'utilisateur n'a pas été écrit, continuer le processus normal
        if not username_written:
            ecrire_nom_utilisateur(driver, first_name, last_name)
            time.sleep(2)
            username_suivant(driver)
            time.sleep(2)

        # Saisie du mot de passe
        password(driver)
        time.sleep(2)
        password_suivant(driver)
        time.sleep(2)

        # Achat du numéro et gestion de l'OTP
        go_num(driver)
        time.sleep(2)
        otp_status = buy_num_and_get_otp(driver)  # Vérifier le statut de retour de l'OTP
        time.sleep(4)
        suivents_otp(driver)

        # Si l'OTP n'a pas été reçu (404), retourner False pour redémarrer le processus
        if otp_status == 404:
            print("OTP non reçu après 5 tentatives. Redémarrage du processus.")
            driver.quit()
            return False  # Retourner False pour relancer tout le processus

        time.sleep(4)
        saisir_adresse_humaine(driver)
        time.sleep(2)
        suivents_recup(driver)
        time.sleep(2)
        suivents_ignore_num(driver)
        time.sleep(2)
        suivents_suit(driver)
        time.sleep(2)
        experss(driver)
        time.sleep(2)
        suiv_experss(driver)
        time.sleep(2)
        defiler_jusqu_en_bas(driver)
        time.sleep(2)
        acepte_suivent(driver)
        time.sleep(2)
        defiler_jusqu_en_bas(driver)
        time.sleep(2)
        confirme(driver)
        time.sleep(2)
        defiler_jusqu_en_bas(driver)
        time.sleep(2)
        adresse_recup = saisir_adresse_humaine(driver)
        mdp = password(driver)
        mail = generer_nom_utilisateur(prenom, nom)
        if adresse_recup is not None:
            if acepte(driver):
            # Appel de la fonction ecrit_gmail avec les informations requises
                ecrit_gmail(mail, mdp, adresse_recup)
                print("Les informations ont été écrites dans le fichier GMAIL.csv")
            else:
                print("Le bouton 'J'accepte' n'a pas été cliqué.")
                driver.quit()
        else:
            print("Erreur lors de la génération de l'adresse de récupération.")
        time.sleep(3)
        driver.quit()

        return True  # Retourner True si tout s'est bien déroulé



    except Exception as e:
        print(f"Erreur lors de l'exécution du processus : {e}")
        driver.quit()  # Fermer le navigateur en cas d'erreur
        return False  # Retourner False si une erreur s'est produite

# Boucle pour redémarrer le processus si le navigateur se ferme ou si une erreur se produit
max_retries = 10  # Nombre maximum de redémarrages du processus
retry_count = 0

while retry_count < max_retries:
    success = start_full_process()
    if success:
        print("Processus terminé avec succès.")

        break  # Sortir de la boucle si tout s'est bien déroulé
    else:
        retry_count += 1
        print(f"Redémarrage du processus... ({retry_count}/{max_retries})")
        time.sleep(5)  # Attendre un peu avant de redémarrer le processus

if retry_count == max_retries:
    print("Nombre maximal de tentatives atteint. Le processus a échoué.")



