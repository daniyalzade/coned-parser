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
