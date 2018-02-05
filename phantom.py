from time import sleep

from bs4 import BeautifulSoup
import configargparse
from selenium import webdriver

from utils import parse_price

DEBUG_FILE = 'tmp/coned.html'
IMAGE_FILE = 'tmp/screen.png'
LOGIN_URL = 'https://www.coned.com/en/login'


def _get_account_page(username, password, options=None):
    options = options or {}
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
    if options.get('debug'):
        open(DEBUG_FILE, "w").write(html_source)
        driver.save_screenshot(IMAGE_FILE)
    return html_source


def _parse_currend_bill(html):
    soup = BeautifulSoup(html, 'html.parser')
    return parse_price(soup.find(id='divAccountBalance').find('b').text)


p = configargparse.ArgParser(default_config_files=['.credentials'])
p.add('--username', required=True, help='username')
p.add('--password', required=True, help='password')

options = p.parse_args()
html = _get_account_page(options.username, options.password)
print _parse_currend_bill(html)
# print _parse_currend_bill(open(DEBUG_FILE).read())
