import requests
import sys      # Pour lire les arguments du terminal

url_cible = sys.argv[1] 


with open("../ressources/wordlist.txt", "r") as fichier:
    for ligne in fichier:
        # .strip() sert à enlever le retour à la ligne invisible (\n) à la fin du mot
        mot = ligne.strip() 
        url_temp= f"{url_cible}/{mot}"  # On construit l'URL à tester
        print(f"[*] Lancement du scan sur : {url_temp}")

        try:
            reponse = requests.get(url_temp)
            
            # On affiche le résultat
            if reponse.status_code == 200:
                print(f"[+] Succès ! Le site a répondu : {reponse.status_code} OK, URL : {url_temp}")
            else:
                print(f"[-] Statut différent : {reponse.status_code}")

        except Exception as e:
            print(f"[!] Erreur de connexion : {e}")