import os

import national

PATH = os.path.join(os.path.dirname(__file__), './assets/national.html')
HTML = open(PATH).read()

def test_parse_bills():
    assert 19 == len(national._parse_bills(HTML)), "number of parsed bills"
