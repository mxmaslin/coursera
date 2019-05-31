from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    result = requests.get("http://www.cbr.ru/scripts/XML_daily.asp", {"date_req": date})
    soup = BeautifulSoup(result.content, 'xml')
    rates = {i.CharCode.string: (
            Decimal(i.Value.string.replace(',', '.')),
            int(i.Nominal.string)
        ) for i in soup('Valute')
    }
    rates['RUR'] = (Decimal(1), 1)

    result = amount * rates[cur_from][0] * rates[cur_to][1] / rates[cur_from][1] / rates[cur_to][0]
    return result.quantize(Decimal('.0001'))