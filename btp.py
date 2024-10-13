#!/usr/bin/python3
# Copyright (c) 2018-2024 Luca Falavigna
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
from time import sleep
from urllib.request import urlopen

btps = []
btp_data = []
url = 'http://www.borsaitaliana.it'
site = '{0}/borsa/obbligazioni/mot/btp/lista.html'.format(url)
header = ('Prezzo ufficiale',
          'Data prezzo ufficiale',
          'Indicizzazione',
          'Apertura',
          'Volume ultimo',
          'Volume totale',
          'Numero contratti',
          'Min oggi',
          'Max oggi',
          'Min anno',
          'Max anno',
          'Rendimento effettivo a scadenza lordo',
          'Rendimento effettivo a scadenza netto',
          'Rateo lordo',
          'Rateo netto',
          'Duration modificata',
          'Prezzo di riferimento',
          'Data di riferimento',
          'Codice ISIN',
          'Emittente',
          'Garante',
          'Subordinazione',
          'Tipologia',
          'Struttura bond',
          'Ammontare emesso',
          'Lotto minimo',
          'Valuta di negoziazione',
          'Mercato',
          'Clearing & settlement',
          'Data inizio negoziazione',
          'Denominazione',
          'Codice strumento',
          'Data godimento',
          'Data stacco prima cedola',
          'Scadenza',
          'Periodicità cedola',
          'Modalità di negoziazione',
          'Base di calcolo',
          'Tasso cedola periodale',
          'Tasso cedola su base annua')

while True:
    data = urlopen(site).read().decode('ISO-8859-1')
    btps += [url + x for x in findall(
      r'<a href="(/borsa/\S+mot\S+IT\d{10}\S+)"', data)]
    nextpage = findall(r'<a href="(\S+)" title="Successiva">', data)
    if nextpage:
        site = url + nextpage[0]
    else:
        break
for btp in btps:
    data = urlopen(btp).read().decode('ISO-8859-1')
    btp_data.append([x.strip() for x in
                    findall('<span class="t-text -right">(.*?)</span>',
                            data, DOTALL)])
    sleep(0.5)
with open('btp.csv', 'w', newline='') as csvfile:
    f = writer(csvfile, delimiter='|')
    f.writerows([header])
    f.writerows(btp_data)
