# encoding: utf-8
from bs4 import BeautifulSoup
import pycurl
from StringIO import StringIO
from urllib import urlencode

buf = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.infor.pl/kalkulatory/kalkulator-wynagrodzen-plac.html')

kwota = 7800

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

netto = {
        1: bs.find_all('td')[6].string,
        2: bs.find_all('td')[15].string,
        3: bs.find_all('td')[24].string,
        4: bs.find_all('td')[33].string,
        5: bs.find_all('td')[42].string,
        6: bs.find_all('td')[51].string,
        7: bs.find_all('td')[60].string,
        8: bs.find_all('td')[69].string,
        9: bs.find_all('td')[78].string,
        10: bs.find_all('td')[87].string,
        11: bs.find_all('td')[96].string,
        12: bs.find_all('td')[105].string
    }

print netto