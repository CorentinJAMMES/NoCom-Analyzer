import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.autopwn import start_autopwn

@patch('core.autopwn.start_xss_scanner')
@patch('core.autopwn.start_sql_scanner')
@patch('core.autopwn.start_crawler')
def test_autopwn_filtre_et_attaque_correctement(mock_crawler, mock_sql, mock_xss):
    # on dit au faux Crawler de trouver 2 liens.
    mock_crawler.return_value = [
        "http://cible.com/page.php?id=1", 
        "http://cible.com/contact.html" 
    ]
    
    # nos faux scanners trouvent chacun une faille différente
    mock_sql.return_value = ["http://cible.com/page.php?id=1' (SQL)"]
    mock_xss.return_value = ["http://cible.com/page.php?id=1<script> (XSS)"]
    
    # on lance le mode Auto 
    failles = start_autopwn("http://cible.com")
    
    # on vérifie que le résultat est une liste avec 2 failles dedans (1 SQL + 1 XSS)
    assert type(failles) is list
    assert len(failles) == 2
    
    # on vérifie que les 2 scanners ont bien ignoré "contact.html"
    mock_sql.assert_called_once_with("http://cible.com/page.php?id=1")
    mock_xss.assert_called_once_with("http://cible.com/page.php?id=1")