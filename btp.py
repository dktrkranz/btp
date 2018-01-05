#!/usr/bin/python3
# Copyright (c) 2018 Luca Falavigna
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from csv import writer
from re import findall, DOTALL
from urllib.request import urlopen

btps = []
btp_data = []
url = 'http://www.borsaitaliana.it'
site = '{0}/borsa/obbligazioni/mot/btp/lista.html'.format(url)
header = ('Prezzo ufficiale',
          'Lotto minimo',
          'Valuta di negoziazione',
          'Valuta di liquidazione',
          'Data Ultima Cedola Pagata',
          'Tasso Prossima Cedola',
          'Scadenza',
          'Apertura',
          'Volume Ultimo',
          'Volume totale',
          'Numero Contratti',
          'Min Oggi',
          'Max Oggi',
          'Min Anno',
          'Max Anno',
          'Tipo Bond',
          'Codice Isin',
          'Mercato',
          'Tipologia')

while True:
    data = urlopen(site).read().decode('ISO-8859-1')
    btps += [url + x for x in findall(
      '<a href="(/borsa/\S+mot\S+IT\d{10}\S+)"', data)]
    nextpage = findall('<a href="(\S+)" title="Successiva">', data)
    if nextpage:
        site = url + nextpage[0]
    else:
        break
for btp in btps:
    data = urlopen(btp).read().decode('ISO-8859-1')
    btp_data.append([x.strip() for x in
                    findall('<span class="t-text -right">(.*?)</span>',
                            data, DOTALL)])
with open('btp.csv', 'w', newline='') as csvfile:
    f = writer(csvfile, delimiter='|')
    f.writerows([header])
    f.writerows(btp_data)
