#!/usr/bin/python3

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
