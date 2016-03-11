# encoding: utf-8
from bs4 import BeautifulSoup
import pycurl
from StringIO import StringIO
from urllib import urlencode
from datetime import date
import argparse
import json


def calculate_comp(amount):
    buf = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'http://www.infor.pl/kalkulatory/kalkulator-wynagrodzen-plac.html')
    c.setopt(c.USERAGENT, "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36")

    post_data = {
        'kwota': amount,
        'rok':	date.today().year
    }

    for i in range(1,13):
        post_data['miesiac[%s]' % i] = amount

    postfields = urlencode(post_data)
    c.setopt(c.POSTFIELDS, postfields)

    c.setopt(c.WRITEDATA, buf)
    c.perform()
    c.close()

    body = buf.getvalue().decode('utf8')

    bs = BeautifulSoup(body, 'html.parser')

    netto = (
            float(bs.find_all('td')[6].string),
            float(bs.find_all('td')[15].string),
            float(bs.find_all('td')[24].string),
            float(bs.find_all('td')[33].string),
            float(bs.find_all('td')[42].string),
            float(bs.find_all('td')[51].string),
            float(bs.find_all('td')[60].string),
            float(bs.find_all('td')[69].string),
            float(bs.find_all('td')[78].string),
            float(bs.find_all('td')[87].string),
            float(bs.find_all('td')[96].string),
            float(bs.find_all('td')[105].string)
    )

    average = sum(netto)/12

    return netto, average


def print_values(netto, average, amount, return_type="text"):
    if return_type == "oneline":
        print "%.0f" % average

    elif return_type == "text":
        print """
        Net compensation:

        January     %.0f PLN
        February    %.0f PLN
        March       %.0f PLN
        April       %.0f PLN
        May         %.0f PLN
        June        %.0f PLN
        July        %.0f PLN
        August      %.0f PLN
        September   %.0f PLN
        October     %.0f PLN
        November    %.0f PLN
        December    %.0f PLN

        average:    %.0f PLN per month

        Disclaimer: calculations based on scraping infor.pl online calculator. Don't include additional
        elements, i.e. sick leave, medical care deduction, English lessons, etc. Values rounded to 1 PLN.
        """ % (netto+(average,))

    elif return_type == "json":
        print json.dumps({
            "amount": amount,
            "compensation": {
                "monthly_avg": round(average, 2),
                "months": netto
            }
        })


parser = argparse.ArgumentParser(description="Calculate net salary from gross salary.")
parser.add_argument('-t', dest="return_type", default="text", choices=["text", "oneline", "json"], help="Select type of response. When 'oneline' selected, it will be only average value.")
parser.add_argument('amount', type=int, help="Gross amount per month.", nargs='?')
parser.add_argument('-i', dest="interactive", action="store_true", help="Enter interactive mode. Type 'exit' or Ctrl+C to finish.")

args = parser.parse_args()


if args.interactive:
    while True:
        line = raw_input('Gross value in PLN ("exit" or Ctrl+C to quit): ')
        if line == 'exit':
            break
        try:
            amount = int(line)  # may throw ValueError
            if amount <= 0:
                raise ValueError
        except ValueError:
            print "Provide numeric value greater than 0."
        else:
            netto, average = calculate_comp(amount)
            print_values(netto=netto, average=average, amount=amount, return_type=args.return_type)

else:
    amount = args.amount
    if amount is None:
        raise ValueError("Provide numeric value greater than 0 as an argument.")
    netto, average = calculate_comp(amount)
    print_values(netto=netto, average=average, amount=amount, return_type=args.return_type)



