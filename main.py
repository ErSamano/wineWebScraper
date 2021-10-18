import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date

def get_data(product_type, product_url):

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)

    driver.get(product_url)

    products_names = []
    products_link = []
    products_price = []
    products_date = []
    products_type =[]
    '''
        When the content page is dynamic, we need to anable a way to load
        the hiden html site content. In order to achieve that we are going 
        to use Selenium Lib
        to load dynamic elements.
        '''
    # Setting up a waiting time before scroll down
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    res = driver.execute_script("return document.documentElement.outerHTML")
    driver.quit()
    soup = BeautifulSoup(res, 'lxml')

    # Get all the products name
    for contentName in soup.findAll(attrs={'class': 'product-item__name'}):
        # Get the Product Name
        products_names.append(contentName.find('a').text)
        products_date.append(date.today())
        products_type.append(product_type)

    # Get all the products link
    for contentLink in soup.findAll(attrs={'class': 'product-item__name'}):
        # Get the Product Link
        for links in contentLink.find_all('a'):
            products_link.append(links.get('href'))

    # Get all the products price
    for contentPrice in soup.findAll(attrs={'class': 'product-item__price'}):
        # Get the Product Name
        # Check if product is still available
        if contentPrice.find(class_="price-new"):
            products_price.append(contentPrice.find(class_="price-new").text)
        else:
            products_price.append("AGOTADO")

    product_table = pd.DataFrame({'Tipo':products_type, 'Nombre': products_names,'Links': products_link, 'Precios': products_price, 'Fecha':products_date })

    return product_table

products = {
    'Tequila': 'https://www.bodegasalianza.com/tequila?PS;12&OrderByReleaseDateDESC',
    'Mezcal': 'https://www.bodegasalianza.com/mezcal?PS;12&OrderByReleaseDateDESC',
    'Vinos': 'https://www.bodegasalianza.com/vinos/todos-los-vinos',
    'Brandy': 'https://www.bodegasalianza.com/brandy?PS;12&OrderByReleaseDateDESC',
    'Champagne': 'https://www.bodegasalianza.com/champagne?PS;12&OrderByReleaseDateDESC',
    'Cognag': 'https://www.bodegasalianza.com/cognac?PS;12&OrderByReleaseDateDESC',
    'CremasYLicores': 'https://www.bodegasalianza.com/cremas-y-licores?PS;12&OrderByReleaseDateDESC',
    'Ginebra': 'https://www.bodegasalianza.com/ginebra?PS;12&OrderByReleaseDateDESC',
    'Jerez': 'https://www.bodegasalianza.com/jerez?PS;12&OrderByReleaseDateDESC',
    'Ron': 'https://www.bodegasalianza.com/ron?PS;12&OrderByReleaseDateDESC',
    'Vodka': 'https://www.bodegasalianza.com/vodka?PS;12&OrderByReleaseDateDESC',
    'Whiskey': 'https://www.bodegasalianza.com/whisky?PS;12&OrderByReleaseDateDESC',
    'Ofertas': 'https://www.bodegasalianza.com/ofertas'
            }

count = 0
for type, url in products.items():
    if count == 0:
        get_data(type, url).to_csv('lista.csv', index=False)
    else:
        get_data(type, url).to_csv('lista.csv', mode='a', index=False, header=False)
    count += 1
