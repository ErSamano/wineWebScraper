import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

'''
When the content page is dynamic, we need to anable a way to load
the hole html site. To achieve that we are going to use Selenium Lib
to load dynamic elements.
'''
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
url = "https://www.bodegasalianza.com/ofertas"
driver.get(url)

#page = driver.execute_script('return document.body.innerHTML')

SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
print(last_height)

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
soup = BeautifulSoup(res, 'html.parser')

products_names = []
products_link = []
products_price = []

#Loop to bring all the products name
for contentName in soup.findAll(attrs={'class':'product-item__name'}):
    # Get the Product Name
    name_desc = contentName.find('a')
    products_names.append(name_desc.text)
    print(products_names)

#Loop to bring all the products link
for contentLink in soup.findAll(attrs={'class':'product-item__name'}):
    # Get the Product Link
    for links in contentLink.find_all('a'):
        product_link = links.get('href')
        products_link.append(product_link)
        print(products_link)

#Loop to bring all the products price
for contentPrice in soup.findAll(attrs={'class':'product-item__price'}):
    # Get the Product Name
    product_price = contentPrice.find(class_="price-promo")
    products_price.append(product_price)
    print(products_price)


table = {'Nombre': products_names,
         'Links': products_link,
         'Precios': products_price
        }
full_table = pd.DataFrame(table)
#full_table.to_csv('lista.csv')
print("Full table:\n")
print(full_table)
