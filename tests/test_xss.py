import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.xss_scanner import start_xss_scanner

@patch('core.xss_scanner.requests.get')
def test_xss_scanner_detecte_faille(mock_get):
    # faux serveur VULNÉRABLE (Il recrache le code tel quel)
    fausse_reponse = MagicMock()
    fausse_reponse.text = "<html><body>Recherche pour : <script>alert('XSS')</script></body></html>"
    mock_get.return_value = fausse_reponse

    resultats = start_xss_scanner("http://cible.com/page.php?search=")

    assert len(resultats) > 0
    assert "http://cible.com/page.php?search=<script>alert('XSS')</script>" in resultats

@patch('core.xss_scanner.requests.get')
def test_xss_scanner_ignore_si_securise(mock_get):
    # faux serveur SÉCURISÉ (Il "encode" les chevrons en entités HTML)
    fausse_reponse = MagicMock()
    fausse_reponse.text = "<html><body>Recherche pour : &lt;script&gt;alert('XSS')&lt;/script&gt;</body></html>"
    mock_get.return_value = fausse_reponse

    resultats = start_xss_scanner("http://cible.com/page.php?search=")

    assert len(resultats) == 0