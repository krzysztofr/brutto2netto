# encoding: utf-8
from bs4 import BeautifulSoup
import pycurl
from StringIO import StringIO
from urllib import urlencode

buf = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.infor.pl/kalkulatory/kalkulator-wynagrodzen-plac.html')

kwota = 10000

post_data = {
    'kwota': kwota,
    'rok':	2016
}

for i in range(1,13):
    post_data['miesiac[%s]' % i] = kwota

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

print """
Wynagrodzenie netto:

styczen     %.0f PLN
luty        %.0f PLN
marzec      %.0f PLN
kwiecien    %.0f PLN
maj         %.0f PLN
czerwiec    %.0f PLN
lipiec      %.0f PLN
sierpien    %.0f PLN
wrzesien    %.0f PLN
pazdziernik %.0f PLN
listopad    %.0f PLN
grudzien    %.0f PLN

srednio:    %.0f PLN miesiecznie
""" % (netto+(srednio,))