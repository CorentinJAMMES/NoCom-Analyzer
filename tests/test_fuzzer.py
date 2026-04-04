import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from core.fuzzer import start_fuzzer

def test_fuzzer_renvoie_bien_les_bonnes_urls():
    url_test = "http://demo.testfire.net"
    mots_a_tester = ["admin", "login", "nexistepas12345"]
    
    resultats = start_fuzzer(url_test, mots_a_tester, max_threads=3)
    
    assert type(resultats) is list # doit retourner une liste
    assert len(resultats) >= 1 # car on sait que 'admin' existe
    assert "[+] Succès (200) : http://demo.testfire.net/admin" in resultats