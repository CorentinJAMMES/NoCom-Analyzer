from core.crawler import start_crawler
from core.scanner import start_scanner

def start_autopwn(url_cible):
    """
    Lance le Crawler, récupère les liens, et passe les vulnérables au Scanner.
    Retourne la liste de toutes les failles trouvées.
    """
    print("\n" + "="*50)
    print("🚀 DÉMARRAGE DU MODE AUTO-PWN 🚀")
    print("="*50 + "\n")
    
    liens_trouves = start_crawler(url_cible)
    
    if not liens_trouves:
        print("[!] Aucun lien trouvé à attaquer. Fin de l'opération.")
        return []
        
    print(f"\n[*] Araignée de retour. {len(liens_trouves)} cibles verrouillées. Chargement du Scanner...\n")
    
    toutes_les_failles = []
    
    for lien in liens_trouves:
        # on n'attaque que les URLs qui ont un paramètre (avec un "?")
        if "?" in lien:
            failles = start_scanner(lien)
            if failles:
                toutes_les_failles.extend(failles)
                
    return toutes_les_failles