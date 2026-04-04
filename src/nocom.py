import requests
import concurrent.futures
import argparse  # La bibliothèque pour gérer les flags dans le terminal

# 1. On configure le menu d'aide et les arguments
parser = argparse.ArgumentParser(description="NoCom-Analyzer : Fuzzer et outil de reconnaissance Web")

# Les arguments obligatoires et optionnels
parser.add_argument("-u", "--url", help="L'URL cible (ex: http://demo.testfire.net)", required=True)
parser.add_argument("-w", "--wordlist", help="Le fichier dictionnaire à utiliser", default="../ressources/wordlist.txt")
parser.add_argument("-t", "--threads", help="Le nombre de requêtes simultanées", type=int, default=10)
parser.add_argument("-o", "--output", help="Le nom du fichier pour sauvegarder les résultats (optionnel)")

# On lit ce que l'utilisateur a tapé dans le terminal
args = parser.parse_args()

print(f"[*] Cible : {args.url} | Threads : {args.threads} | Wordlist : {args.wordlist}")
if args.output:
    print(f"[*] Les résultats seront sauvegardés dans : {args.output}")

# 2. La fonction de test (modifiée pour écrire dans le fichier si l'option -o est utilisée)
def tester_url(mot):
    url_test = f"{args.url}/{mot}"
    try:
        reponse = requests.get(url_test, timeout=3)
        if reponse.status_code in [200, 204, 301, 302, 403]:
            resultat = f"[+] Succès ({reponse.status_code}) : {url_test}"
            print(resultat)
            
            # Si l'utilisateur a utilisé le flag -o, on écrit dans le fichier
            if args.output:
                with open(args.output, "a") as fichier_rapport:
                    fichier_rapport.write(resultat + "\n")
                    
    except requests.RequestException:
        pass

# 3. Chargement de la wordlist (en utilisant args.wordlist)
liste_mots = []
try:
    with open(args.wordlist, "r") as fichier:
        for ligne in fichier:
            liste_mots.append(ligne.strip())
except FileNotFoundError:
    print(f"[!] Erreur : Le fichier {args.wordlist} est introuvable.")
    exit()

# 4. Le mode Turbo (en utilisant args.threads)
print(f"[*] Démarrage du scan...")
with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    executor.map(tester_url, liste_mots)

print("[*] Scan terminé !")