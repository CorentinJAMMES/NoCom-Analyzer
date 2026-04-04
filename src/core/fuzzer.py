import requests
import concurrent.futures

def start_fuzzer(url_cible, liste_mots, max_threads=10):
    """
    Fuzze une URL avec une liste de mots et RETOURNE les résultats.
    """
    def tester_url(mot):
        url_test = f"{url_cible}/{mot}"
        try:
            reponse = requests.get(url_test, timeout=3)
            if reponse.status_code in [200, 204, 301, 302, 403]:
                resultat = f"[+] Succès ({reponse.status_code}) : {url_test}"
                print(resultat) # on affiche en direct pour le style
                return resultat
        except requests.RequestException:
            pass
        return None

    # on collecte tous les résultats ici
    resultats_valides = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for res in executor.map(tester_url, liste_mots):
            if res: # si c'est pas None (donc si on a un succès)
                resultats_valides.append(res)
                
    return resultats_valides