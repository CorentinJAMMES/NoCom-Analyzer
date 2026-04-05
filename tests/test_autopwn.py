import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.autopwn import start_autopwn

# on simule d'abord le crawler, puis le scanner
@patch('core.autopwn.start_scanner')
@patch('core.autopwn.start_crawler')
def test_autopwn_filtre_et_attaque_correctement(mock_crawler, mock_scanner):
    # on dit au faux Crawler de trouver 2 liens.
    # l'un a un "?", l'autre non.
    mock_crawler.return_value = [
        "http://cible.com/page.php?id=1", 
        "http://cible.com/contact.html" 
    ]
    
    # on dit au faux Scanner de trouver une faille quand il est appelé
    mock_scanner.return_value = ["http://cible.com/page.php?id=1'"]
    
    # on lance le mode Auto (il va utiliser les fausses fonctions)
    failles = start_autopwn("http://cible.com")
    
    # on vérifie que le résultat est une liste avec une faille dedans
    assert type(failles) is list
    assert len(failles) == 1
    
    # on vérifie que le scanner a bien ignoré "contact.html" !
    # il ne doit avoir été appelé qu'une seule fois, sur le lien avec le "?"
    mock_scanner.assert_called_once_with("http://cible.com/page.php?id=1")