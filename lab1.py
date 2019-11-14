# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt

# funkcja do wczytywania waluty nbp z zadanego okresu, zwraca obiekt typu DataFrame
def loadData(data_from, data_to, currency):
    url = 'http://api.nbp.pl/api/exchangerates/rates/A/{}/{}/{}/'.format(currency, data_from, data_to)
    currency_req = requests.get(url)
    currency_data = currency_req.json()
    return pd.DataFrame.from_dict(currency_data['rates'])

#przyklad uzycia funkcji
#print(loadData('2019-09-01', '2019-09-08', 'USD'))
#print(loadData('2019-09-01', '2019-09-08', 'EUR'))

#utworzenie DataFrame
usd  = loadData('2019-09-01', '2019-09-08', 'USD')
gbp  = loadData('2019-09-01', '2019-09-08', 'GBP')

#badanie danych przy pomocy funkcji z modułu pandas
print('wyswietlenie rekordow z DataFrame usd:')
print(usd.head())
print('-----------------------------------------')
print('minimum z kolumny mid dla gbp:')
print(gbp[['mid']].min())
print('-----------------------------------------')

#konwersja do typu datetime wartosci z kolumny 'effectiveDate'
print('konwersja do typu data/czas przy wykorzystaniu funkcji to_datetime() z modułu pandas:')
print('typ przed konwersja:')
print(usd['effectiveDate'].dtypes)
print('typ po konwersji:')
usd['effectiveDate'] = pd.to_datetime(usd['effectiveDate'])
gbp['effectiveDate'] = pd.to_datetime(gbp['effectiveDate'])
print(usd['effectiveDate'].dtypes)
print('-----------------------------------------')

#ustawienie indeksu na date
usd = usd.set_index('effectiveDate')
gbp = gbp.set_index("effectiveDate")


#obliczenie wzajemnej korelacji dla usd i gbp
#przekonwertowanie wartosci z kolumny 'mid' obiektu DataFrame do typu obslugiwanego przez numpy
usd_val = usd['mid'].values
gbp_val = gbp['mid'].values
corr = np.corrcoef(gbp_val, usd_val)
print('tabela korelacji:')
print(corr)

print('-----------------------------------------')
#rysowanie wykresow przy uzyciu funkcji subplots
x =usd['mid']
y =gbp['mid']

#zdefiniowanie uklady wykresow(2 wiersze 1 kolumna), os X dzielona dla calej kolumny )
fig, (ax1, ax2) = plt.subplots(2, 1, sharex = 'col')

# ustawienie nazw 
ax1.set_title('USD')
ax2.set_title('GBP')
#użycie DateFormatter do zmiany formatu daty wyswietlanej na osi x
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#ta funkcja zmienia sposob wyswietlania oznaczen osi X na bardziej czytelny
fig.autofmt_xdate()
ax1.plot(x)
ax2.plot(y)
plt.show()




