import argparse
import os

from core.fuzzer import start_fuzzer
from core.crawler import start_crawler
from core.sql_scanner import start_sql_scanner
from core.xss_scanner import start_xss_scanner
from core.autopwn import start_autopwn

# Configuration des arguments CLI
parser = argparse.ArgumentParser(description="NoCom-Analyzer : Outil de reconnaissance Web")
parser.add_argument("-u", "--url", help="L'URL cible", required=True)
parser.add_argument("-w", "--wordlist", help="Fichier dictionnaire", default="../ressources/wordlist.txt") # On pointe vers ressources par défaut
parser.add_argument("-t", "--threads", help="Requêtes simultanées", type=int, default=10)
parser.add_argument("-o", "--output", help="Nom du fichier de sauvegarde (ex: rapport.txt)")
parser.add_argument("-m", "--mode", choices=["fuzzer", "crawler", "sql", "xss", "auto"], default="fuzzer", help="Mode d'analyse : fuzzer, crawler, sql, xss ou auto")
args = parser.parse_args()

chemin_complet_output = None

if args.output:
    # on définit le chemin du dossier de résultats
    dossier_resultats = "../results"
    
    # crée le dossier s'il n'existe pas, et ne fait rien s'il est déjà là (exist_ok=True)
    os.makedirs(dossier_resultats, exist_ok=True)
    
    # on fusionne le dossier et le nom du fichier (ex: ../results/rapport.txt)
    chemin_complet_output = os.path.join(dossier_resultats, args.output)
    
    print(f"[*] Les résultats seront sauvegardés dans : {chemin_complet_output}")

# On lance le module choisi
if args.mode == "fuzzer":
    try:
        with open(args.wordlist, "r") as fichier:
            mots = [ligne.strip() for ligne in fichier]
    except FileNotFoundError:
        print(f"[!] Erreur : Le fichier {args.wordlist} est introuvable.")
        exit()

    print(f"[*] Démarrage du Fuzzer sur {args.url} avec {args.threads} threads...")
    
    # on lance le fuzzer et on récupère sa réponse
    resultats = start_fuzzer(args.url, mots, args.threads)
    
    if chemin_complet_output and resultats:
        with open(chemin_complet_output, "a") as f:
            for ligne in resultats:
                f.write(ligne + "\n")
                
elif args.mode == "crawler":
    # on lance le Crawler et on récupère les liens
    resultats = start_crawler(args.url)

    if chemin_complet_output and resultats:
        with open(chemin_complet_output, "a") as f:
            for lien in resultats:
                f.write(f"[Lien trouvé] : {lien}\n")

elif args.mode == "sql":
    resultats = start_sql_scanner(args.url)
    if chemin_complet_output and resultats:
        with open(chemin_complet_output, "a") as f:
            for faille in resultats:
                f.write(f"[VULNÉRABILITÉ SQL] : {faille}\n")

elif args.mode == "auto":
    toutes_les_failles = start_autopwn(args.url)
    
    print("\n" + "="*50)
    print("RAPPORT FINAL AUTO-PWN")
    print("="*50)
    if toutes_les_failles:
        print(f"\033[91m[!!!] MISSION ACCOMPLIE : {len(toutes_les_failles)} FAILLES CRITIQUES DÉTECTÉES !\033[0m")
        for faille in toutes_les_failles:
            print(f" -> {faille}")
        
        if chemin_complet_output:
            with open(chemin_complet_output, "w") as f:
                f.write("=== RAPPORT DE VULNÉRABILITÉS ===\n")
                for faille in toutes_les_failles:
                    f.write(f"[VULNÉRABILITÉ] : {faille}\n")
    else:
        print("[+] Le site a résisté à l'assaut. Aucune faille évidente trouvée.")

elif args.mode == "xss":
    resultats = start_xss_scanner(args.url)
    if chemin_complet_output and resultats:
        with open(chemin_complet_output, "a") as f:
            for faille in resultats:
                f.write(f"[VULNÉRABILITÉ XSS] : {faille}\n")