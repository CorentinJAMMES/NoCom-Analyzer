import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.crawler import start_crawler

def test_crawler_trouve_les_bons_liens():

    url_test = "http://demo.testfire.net"

    liens = start_crawler(url_test)

    assert type(liens) is list
    assert len(liens) > 10 # on sait qu'il y a au moins 40 liens sur cette page
    
    # on vérifie qu'il a bien trouvé un lien spécifique qu'on connait
    lien_attendu = "http://demo.testfire.net/login.jsp"
    assert lien_attendu in liens
    
def test_crawler_gere_les_fausses_urls():

    liens = start_crawler("http://cette-url-n-existe-vraiment-pas-1234.com")
    
    assert type(liens) is list
    assert len(liens) == 0 # doit retourner une liste vide, pas faire crasher le script