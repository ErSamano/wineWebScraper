import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'blue' if val > 90 else 'black'
    return 'color: % s' % color

response = requests.get("https://www.bodegasalianza.com/ofertas")
if response.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = response.content
soup = BeautifulSoup(response.content, 'html.parser')

products_names = []
products_link = []
products_price = []

#Loop to bring all the products name
for contentName in soup.findAll(attrs={'class':'product-item__name'}):
    # Get the Product Name
    name_desc = contentName.find('a')
    products_names.append(name_desc.text)

#Loop to bring all the products link
for contentLink in soup.findAll(attrs={'class':'product-item__name'}):
    # Get the Product Link
    for links in contentLink.find_all('a'):
        product_link = links.get('href')
        products_link.append(product_link)

#Loop to bring all the products price
for contentPrice in soup.findAll(attrs={'class':'product-item__price'}):
    # Get the Product Name
    product_price = contentPrice.find(class_="price-promo")
    products_price.append(product_price.text)


table = {'Nombre': products_names,
         'Links': products_link,
         'Precios': products_price
        }
full_table = pd.DataFrame(table)
#full_table.to_csv('lista.csv')
print(full_table)
