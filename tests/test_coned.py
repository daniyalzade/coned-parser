import os

import coned

PATH = os.path.join(os.path.dirname(__file__), './assets/coned.html')
HTML = open(PATH).read()

EXPECT = [
    {'current': False, 'amount': 165.29, 'due': u'02/14/2018'},
    {'current': True, 'amount': None, 'due': None}
]

def test_parse_current_bill():
    assert EXPECT == coned._parse_current_bill(HTML), "correctly parsed account"
