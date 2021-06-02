from bs4 import BeautifulSoup
import requests
import csv

url = 'https://finance.yahoo.com/quote/MSFT/financials?p=MSFT'

HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
r = requests.get(url, headers=HEADER)
soup = BeautifulSoup(r.text, 'lxml')

titles = soup.find('div', {'class': 'D(tbr) C($primaryColor)'}).find_all('span')
elements = soup.find_all('div', {'data-test': 'fin-row'})

def stract_row(titles, elements):
    data = []

    # Titulos y Fechas
    data_cache = []
    for i in titles:
        # print(i.text)
        data_cache.append(i.text)

    data.append(data_cache)

    # Datos
    for i in elements:
        data_cache = []
        span_data = i.find_all('span')

        for e in span_data:
            # print(e.text)
            data_cache.append(e.text.replace(',', ''))

        data.append(data_cache)

    return data

def csv_file(data):
    with open('data_yh.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(data)

if __name__ == '__main__':
    datos = stract_row(titles, elements)
    print(datos)
    csv_file(datos)
