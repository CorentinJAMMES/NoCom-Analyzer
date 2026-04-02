import requests
import sys      # Pour lire les arguments du terminal

url_cible = sys.argv[1] 


with open("../ressources/wordlist.txt", "r") as fichier:
    for ligne in fichier:
        # .strip() sert à enlever le retour à la ligne invisible (\n) à la fin du mot
        mot = ligne.strip() 
        url_temp= f"{url_cible}/{mot}"  # On construit l'URL à tester

        try:
            reponse = requests.get(url_temp)
            
            # On affiche le résultat
            if reponse.status_code == 200:
                print(f"[+] Succès ! Le site a répondu : {reponse.status_code} OK, URL : {url_temp}")
            elif reponse.status_code == 403:
                print(f"[~] Accès non autorisé : {reponse.status_code}, URL : {url_temp}")
            elif reponse.status_code == 301 or reponse.status_code == 302:
                print(f"[~] Redirection détectée : {reponse.status_code}, URL : {url_temp}")
            elif reponse.status_code == 204:
                print(f"[~] Pas de contenu : {reponse.status_code}, URL : {url_temp}")

        except Exception as e:
            print(f"[!] Erreur de connexion : {e}")