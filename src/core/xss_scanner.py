import requests

PAYLOADS_XSS = [
    "<script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>"
]

def start_xss_scanner(url_cible):
    """
    Teste une URL pour des failles XSS (Reflected) basiques.
    """
    print(f"[*] Démarrage du Scanner XSS sur {url_cible}...")
    failles_trouvees = []

    if "?" not in url_cible:
        print("[-] Attention : L'URL ne contient pas de paramètres (ex: ?search=test).")
        return failles_trouvees

    headers_navigateur = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }

    for payload in PAYLOADS_XSS:
        url_test = f"{url_cible}{payload}"
        print(f"[*] Test en cours : {url_test}")

        try:
            reponse = requests.get(url_test, headers=headers_navigateur, timeout=10)
            
            # on vérifie si le serveur a recraché notre payload sans le nettoyer
            if payload in reponse.text:
                # \033[93m = Texte en Jaune/Orange pour différencier du SQL (Rouge)
                alerte = f"[!!!] FAILLE XSS DÉTECTÉE avec '{payload}' !"
                print(f"\033[93m{alerte}\033[0m") 
                
                failles_trouvees.append(url_test)
                break # on passe au lien suivant
                    
        except requests.RequestException as e:
            print(f"[!] Erreur de connexion : {e}")

    if not failles_trouvees:
        print("[+] Le site semble nettoyer ses paramètres (Sécurisé contre le XSS basique).")
        
    return failles_trouvees