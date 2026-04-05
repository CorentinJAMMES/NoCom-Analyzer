from core.crawler import start_crawler
from core.sql_scanner import start_sql_scanner
from core.xss_scanner import start_xss_scanner # <-- NOUVEAU

def start_autopwn(url_cible):
    """
    Lance le Crawler, récupère les liens, et passe les vulnérables aux Scanners (SQL et XSS).
    Retourne la liste de toutes les failles trouvées.
    """
    print("\n" + "="*50)
    print("🚀 DÉMARRAGE DU MODE AUTO-PWN 🚀")
    print("="*50 + "\n")
    
    liens_trouves = start_crawler(url_cible)
    
    if not liens_trouves:
        print("[!] Aucun lien trouvé à attaquer. Fin de l'opération.")
        return []
        
    print(f"\n[*] Araignée de retour. {len(liens_trouves)} cibles verrouillées. Chargement des Scanners...\n")
    
    toutes_les_failles = []
    
    if url_cible not in liens_trouves:
        liens_trouves.insert(0, url_cible) # On l'ajoute tout au début de la liste
        
    for lien in liens_trouves:
        # on n'attaque que les URLs qui ont un paramètre (avec un "?")
        
        if "?" in lien:
            # 1. Attaque SQL
            failles_sql = start_sql_scanner(lien)
            if failles_sql:
                toutes_les_failles.extend(failles_sql)
            
            # 2. Attaque XSS
            failles_xss = start_xss_scanner(lien)
            if failles_xss:
                toutes_les_failles.extend(failles_xss)
                
    return toutes_les_failles