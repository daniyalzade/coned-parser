from time import sleep

from bs4 import BeautifulSoup
import configargparse

from utils import get_account_page_driver
from utils import parse_price

DEBUG_FILE = 'tmp/coned.html'
IMAGE_FILE = 'tmp/screen.png'
LOGIN_CONFIG = {
    'url': 'https://www.nationalgridus.com/NY-Home/Default',
    'username_xpath': '//input[@name=\'txtUsername\']',
    'password_xpath': '//input[@name=\'txtPassword\']',
    'submit_xpath': '//button[@class=\'site-button\']',
    'login_error': '//div[@class=\'error\']'
}


def _get_account_page(username, password, debug=False):
    config = dict(LOGIN_CONFIG,
                  username=username,
                  password=password)

    driver = get_account_page_driver(config)
    print 'sleeping to get the new page'
    sleep(10)
    driver.switch_to_frame(driver.find_element_by_name('_sweclient'))
    driver.switch_to_frame(driver.find_element_by_name('_sweview'))
    if debug:
        html_source = driver.page_source.encode('utf8')
        open(DEBUG_FILE, "w").write(html_source)
        driver.save_screenshot(IMAGE_FILE)
    return driver


def _get_bills_page(driver):
    element = driver.find_element_by_xpath("//a[text()='View My Bills']").click()
    print 'sleeping to get the new page'
    sleep(10)
    return driver


def _parse_bills(html):
    soup = BeautifulSoup(html, 'html.parser')
    for row in soup.find_all('tr', {'class':'listRowOff'}):
        print row.text
    return None


def _parse_current_bill(html):
    soup = BeautifulSoup(html, 'html.parser')
    cur_amount = parse_price(soup.find(id='s_4_1_16_0').text.lower())
    cur_due = soup.find(id='s_4_1_17_0').text.lower()
    prev_amount = parse_price(soup.find(id='s_4_1_2_0').text.lower())
    prev_due = soup.find(id='s_4_1_3_0').text.lower()
    return [{
        'amount': prev_amount,
        'due': prev_due,
        'current': False,
    }, {
        'amount': cur_amount,
        'due': cur_due,
        'current': True,
    }]


p = configargparse.ArgParser(default_config_files=['.nationalcredentials'])
p.add('--username', required=True, help='username')
p.add('--password', required=True, help='password')
p.add('--debug', help='debug', action='store_true')

options = p.parse_args()
driver = _get_account_page(options.username, options.password,
                        debug=options.debug)
html = driver.page_source.encode('utf8')
print _parse_current_bill(html)
driver = _get_bills_page(driver)
html = driver.page_source.encode('utf8')
_parse_bills(html)
