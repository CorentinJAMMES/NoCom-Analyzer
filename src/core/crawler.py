import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def start_crawler(url_cible):
    """
    Crawle une page web et RETOURNE la liste des liens trouvés.
    """
    print(f"[*] Démarrage du Crawler (Araignée) sur {url_cible}...")
    
    liens_trouves = []
    
    try:
        reponse = requests.get(url_cible, timeout=5)
        if reponse.status_code != 200:
            print(f"[!] Le site a répondu avec le code {reponse.status_code}. Impossible de crawler.")
            return liens_trouves # on retourne une liste vide en cas d'erreur

        soup = BeautifulSoup(reponse.text, 'html.parser')
        
        liens = soup.find_all('a')
        print(f"[*] {len(liens)} liens potentiels trouvés sur la page !\n")
        
        for lien in liens:
            href = lien.get('href')
            if href:
                url_complete = urljoin(url_cible, href) 
                
                if url_complete not in liens_trouves:
                    liens_trouves.append(url_complete)
                    print(f"[Lien trouvé] : {url_complete}")
                    
    except requests.RequestException as e:
        print(f"[!] Erreur de connexion : {e}")
        
    # On retourne la liste propre à la fin
    return liens_trouves