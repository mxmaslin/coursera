from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    # import requests
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date)
    response = requests.get(url)  # Использовать переданный requests
    xml = response.text
    soup = BeautifulSoup(xml, 'html.parser')

    nominal_from = 1
    value_from = Decimal(1)
    try:
        from_cur_node = soup(text=cur_from)[0].parent.parent
        nominal_from = int(from_cur_node.find('nominal').contents[0].replace(',', '.'))
        value_from = Decimal(from_cur_node.find('value').contents[0].replace(',', '.'))
    except IndexError:
        pass

    from_in_roubles = (amount * value_from) / nominal_from

    nominal_to = 1
    value_to = Decimal(1)
    to_cur_node = soup(text=cur_to)[0].parent.parent
    try:
        nominal_to = int(to_cur_node.find('nominal').contents[0].replace(',', '.'))
        value_to = Decimal(to_cur_node.find('value').contents[0].replace(',', '.'))
    except IndexError:
        pass

    result = (from_in_roubles / value_to) * nominal_to

    return result.quantize(Decimal('1.0000'))  # не забыть про округление до 4х знаков после запятой


# convert(25, 'JPY', 'USD', "17/02/2005", 'requests')
