# encoding: utf-8
from bs4 import BeautifulSoup
import pycurl
from StringIO import StringIO
from urllib import urlencode
from datetime import date
import argparse

parser = argparse.ArgumentParser(description="Calculate net salary from gross salary.")
parser.add_argument('amount', type=int, help="Gross amount per month.")
parser.add_argument('-t', dest="return_type", default="text", choices=["text", "oneline", "json"], help="Select type of response. When 'oneline' selected, it will be only average value.")

args = parser.parse_args()

buf = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.infor.pl/kalkulatory/kalkulator-wynagrodzen-plac.html')

amount = args.amount

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

srednio = sum(netto)/12

if args.return_type == "oneline":
    print "%.0f" % srednio
elif args.return_type == "text":
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
    """ % (netto+(srednio,))
elif args.return_type == "json":
    print "json"