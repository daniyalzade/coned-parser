import os

import national

PATH = os.path.join(os.path.dirname(__file__), './assets/national.html')
HTML = open(PATH).read()

def test_answer():
    assert 19 == len(national._parse_bills(HTML)), "number of parsed bills"
