import os

import coned

cur_dir = os.path.dirname(__file__)

EXPECT = [
    {'current': False, 'amount': 165.29, 'due': u'02/14/2018'},
    {'current': True, 'amount': None, 'due': None}
]

def test_parse_current_bill():
    html = open(os.path.join(cur_dir, './assets/coned.html')).read()
    assert EXPECT == coned._parse_current_bill(html), "correctly parsed account"

def test_parse_bills():
    html = open(os.path.join(cur_dir, './assets/coned_bills.html')).read()
    assert 18 == len(coned._parse_bills(html)), "correctly parsed account"
