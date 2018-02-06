from selenium import webdriver
import re


def parse_price(price, fun=max):
    """
    @param price: str
    @param fun: max | min : determine max or min of price range when there is
    conflicts
    @return: float
    taking
    """
    price = price.lower().replace('for', '|')
    price = re.sub(r'[\(\)a-z\s$&;:]', '', price.lower())
    # Strip leading / trailing .'s
    price = price.strip('.')
    # Combine comma-separation used for denoting 000s
    if '|' in price:
        quantity, amount = price.split('|')
        return float(amount) / float(quantity)
    return float(fun(price.replace(',', '').split('-')))  # '$308.00 - $440.00'


def get_account_page_driver(login_config):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1024, 768)
    driver.get(login_config['url'])
    element = driver.find_element_by_xpath(login_config['username_xpath'])
    element.send_keys(login_config['username'])
    element = driver.find_element_by_xpath(login_config['password_xpath'])
    element.send_keys(login_config['password'])
    driver.find_element_by_xpath(login_config['submit_xpath']).submit()
    return driver
