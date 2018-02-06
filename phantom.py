import re
from time import sleep

from bs4 import BeautifulSoup
import configargparse
from selenium import webdriver

from utils import parse_price

DEBUG_FILE = 'tmp/coned.html'
IMAGE_FILE = 'tmp/screen.png'
LOGIN_URL = 'https://www.coned.com/en/login'
REGEX_DATE = r'(\d+/\d+/\d+)'
REGEX_AMOUNT = r'\$(\d+.\d+)'


def _get_account_page(username, password, debug=False):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)
    driver.get(LOGIN_URL)
    element = driver.find_element_by_id("form-login-email")
    element.send_keys(username)
    element = driver.find_element_by_id("form-login-password")
    element.send_keys(password)
    driver.find_element_by_class_name("js-login-submit-button").submit()

    print 'sleeping to get the new page'
    sleep(10)
    html_source = driver.page_source.encode('utf8')
    if debug:
        open(DEBUG_FILE, "w").write(html_source)
        driver.save_screenshot(IMAGE_FILE)
    return html_source


def _parse_bill_text(text):
    due = re.search(REGEX_DATE, text).group(1)
    amount = parse_price(re.search(REGEX_AMOUNT, text).group(1))
    return (due, amount)


def _parse_current_bill(html):
    soup = BeautifulSoup(html, 'html.parser')
    prev, cur = soup.find(id='divAccountBalance').text.lower().split('current')
    prev_due, prev_amount = _parse_bill_text(prev)
    cur_due, cur_amount = _parse_bill_text(cur)
    return [{
            'amount': prev_amount,
            'due': prev_due,
            'current': False,
            },
            {
            'amount': cur_amount,
            'due': cur_due,
            'current': True,
            }]

p = configargparse.ArgParser(default_config_files=['.credentials'])
p.add('--username', required=True, help='username')
p.add('--password', required=True, help='password')
p.add('--debug', help='debug', action='store_true')

options = p.parse_args()
html = _get_account_page(options.username, options.password,
        debug=options.debug
        )
print _parse_current_bill(html)

# print _parse_current_bill(open(DEBUG_FILE).read())
