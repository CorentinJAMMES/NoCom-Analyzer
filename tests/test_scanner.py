import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.scanner import start_scanner

# le mot-clé @patch va "capturer" la fonction requests.get utilisée dans scanner.py
@patch('core.scanner.requests.get')
def test_scanner_ne_trouve_rien_sur_site_securise(mock_get):
    # on crée une fausse réponse de serveur (qui ne contient pas d'erreur SQL)
    fausse_reponse = MagicMock()
    fausse_reponse.text = "<html><body>Bienvenue sur la page normale</body></html>"
    mock_get.return_value = fausse_reponse # on dit au Mock de renvoyer ça
    
    # on lance le scanner (il va taper dans notre Mock sans s'en rendre compte !)
    resultats = start_scanner("http://mon-site.com/page.php?id=1")
    
    # il ne doit rien trouver
    assert type(resultats) is list
    assert len(resultats) == 0

@patch('core.scanner.requests.get')
def test_scanner_detecte_faille_sql(mock_get):
    # on crée une fausse réponse qui contient une grosse erreur SQL
    fausse_reponse = MagicMock()
    fausse_reponse.text = "<b>Warning</b>: You have an error in your SQL syntax near '''"
    mock_get.return_value = fausse_reponse

    resultats = start_scanner("http://mon-site.com/page.php?id=1")
    
    # assert : Il DOIT trouver les failles
    assert len(resultats) > 0 # la liste ne doit pas être vide
    # on vérifie que le premier payload (') a bien été concaténé à l'URL
    assert "http://mon-site.com/page.php?id=1'" in resultats