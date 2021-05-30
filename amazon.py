from bs4 import BeautifulSoup
import requests
import time
import random
import csv

url = r'https://www.amazon.com/-/es/gp/bestsellers/videogames?ref_=Oct_s9_apbd_obs_hd_bw_b1xuk_S&pf_rd_r=S8Q2RKMCGDFNQ0BDGF82&pf_rd_p=dd1c0d94-841d-5e3f-9316-363e0da02d54&pf_rd_s=merchandised-search-13&pf_rd_t=BROWSE&pf_rd_i=468642'
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}

r = requests.get(url, headers=HEADER)
soup = BeautifulSoup(r.text, 'lxml')

products = soup.find_all('li', {'class': 'zg-item-immersion'})
product_link = lambda item: item.find('span', {'class': 'aok-inline-block zg-item'}).find('a')['href']

def recopilator(link):
    p_link = 'https://www.amazon.com' + link
    HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}
    print(p_link)

    r = requests.get(p_link, headers=HEADER)
    time.sleep(3)
    micro_soup = BeautifulSoup(r.content, 'lxml')
    time.sleep(3)
    tittle = micro_soup.find('div', {'class': 'celwidget'}).find('div', {'class': 'a-section a-spacing-none'}).find('span', {'class': 'a-size-large product-title-word-break'}).text

    return tittle

if __name__ == '__main__':
    for i in products:
        time.sleep(random.uniform(3, 4))
        print(recopilator(product_link(i)))


