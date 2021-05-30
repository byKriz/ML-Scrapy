from bs4 import BeautifulSoup
import requests
import time
import random
import csv

# url = 'https://listado.mercadolibre.com.ve/repuestos#D[A:repuestos]'
url = 'https://carros.mercadolibre.com.ve/repuestos-camionetas/'

articulo_link = lambda item: item.find('div', {'class': 'ui-search-item__group ui-search-item__group--title'}).find('a')['href']
clean_n = lambda item: float(item.replace('.', ''))

def clean_sells(item):
    element = item.replace('Nuevo  |  ', '').replace(' vendidos', '').replace(' vendido', '').replace('Nuevo', '').replace('Usado  |  ', '')
    if element == '':
        n = 0
    else:
        n = int(element)
    return n

def product_img(item):
    try:
        item = item.find('div', {'class': 'slick-slide slick-active'}).find('img')['data-src']
    except:
        item = item.find('div', {'class': 'slick-slide slick-active'}).find('img')['src']
    return item

# Ahora los articulos
def recopilator(link):
    r = requests.get(link)
    micro_soup = BeautifulSoup(r.text, 'lxml')
    title = micro_soup.find('div', {'class': 'ui-pdp-header__title-container'}).find('h1', {'class': 'ui-pdp-title'}).text
    price = micro_soup.find('div', {'class': 'ui-pdp-price__second-line'}).find('span', {'class': 'price-tag-fraction'}).text
    sells = micro_soup.find('div', {'class': 'ui-pdp-header'}).find('span', {'class': 'ui-pdp-subtitle'}).text

    seller_data = micro_soup.find_all('li', {'class': 'ui-pdp-seller__item-description'})
    seller_rate = seller_data[0].find('strong', {'class': 'ui-pdp-seller__sales-description'}).text
    seller_old = seller_data[1].find('strong', {'class': 'ui-pdp-seller__sales-description'}).text
    seller_sells = seller_data[2].find('strong', {'class': 'ui-pdp-seller__sales-description'}).text

    try:
        seller_name = micro_soup.find('div', {'class': 'ui-pdp-seller__header__info-container'}).find('p', {'class': 'ui-pdp-seller__header__title'}).text
    except AttributeError:
        seller_name = 'Sin Nombre'

    return title, clean_n(price), clean_sells(sells), seller_name, seller_rate, seller_old, int(seller_sells), link

def ml_scrap(url, page=5):
    products_scrap_list = []
    r = requests.get(url)

    for i in range(page):
        soup = BeautifulSoup(r.text, 'lxml')
        products = soup.find_all('li', class_='ui-search-layout__item')

        for product in products:
            time.sleep(random.uniform(2, 4))
            products_scrap_list.append(recopilator(articulo_link(product)))
            print(recopilator(articulo_link(product)))

        try:
            time.sleep(random.uniform(3, 5))
            next_page_link = soup.find('li', {'class': 'andes-pagination__button andes-pagination__button--next'}).find('a')['href']
            r = requests.get(next_page_link)
        except:
            pass

    return products_scrap_list

if __name__ == '__main__':
    lista = ml_scrap(url, 3)


