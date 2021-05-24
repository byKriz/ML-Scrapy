from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import random

# driver = webdriver.Chrome('./chromedriver.exe')
url = 'https://listado.mercadolibre.com.ve/repuestos#D[A:repuestos]'
# page_url = driver.get(url)
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

products = soup.find_all('li', class_='ui-search-layout__item')


product_title = lambda item: item.find('div', {'class': 'ui-search-item__group ui-search-item__group--title'}).find('h2', {'class': 'ui-search-item__title'}).text
product_price = lambda item: item.find('div', {'class': 'ui-search-price__second-line'}).find('span', {'class': 'price-tag-fraction'}).text.replace('.', '')
articulo_link = lambda item: item.find('div', {'class': 'ui-search-item__group ui-search-item__group--title'}).find('a')['href']

product1 = products[0]

def product_img(item):
    try:
        item = item.find('div', {'class': 'slick-slide slick-active'}).find('img')['data-src']
    except:
        item = item.find('div', {'class': 'slick-slide slick-active'}).find('img')['src']
    return item

producto1 = products[0]

# Ahora los articulos
def recopilator(link):
    r = requests.get(link)
    micro_soup = BeautifulSoup(r.text, 'lxml')
    title = micro_soup.find('div', {'class': 'ui-pdp-header__title-container'}).find('h1', {'class': 'ui-pdp-title'}).text
    price = micro_soup.find('div', {'class': 'ui-pdp-price__second-line'}).find('span', {'class': 'price-tag-fraction'}).text
    sells = micro_soup.find('div', {'class': 'ui-pdp-header'}).find('span', {'class': 'ui-pdp-subtitle'}).text
    seller_name = micro_soup.find('div', {'class': 'ui-pdp-seller__header__info-container'}).find('p', {'class': 'ui-pdp-seller__header__title'}).text
    return title, price, sells, seller_name

if __name__ == '__main__':
    for i in range(1):
        soup = BeautifulSoup(r.text, 'lxml')
        products = soup.find_all('li', class_='ui-search-layout__item')

        for product in products:
            time.sleep(random.uniform(2, 4))
            print(recopilator(articulo_link(product)))

        try:
            time.sleep(random.uniform(9, 11))
            next_page_link = soup.find('li', {'class': 'andes-pagination__button andes-pagination__button--next'}).find('a')['href']
            r = requests.get(next_page_link)
        except:
            pass

