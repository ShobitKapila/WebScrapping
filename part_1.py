import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []

    # Extract product information from the page
    product_list = soup.find_all('div', {'data-component-type': 's-search-result'})

    for product in product_list:
        data = {}

        # Extract the required information
        data['Product URL'] = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        data['Product Name'] = product.find('span', {'class': 'a-size-medium'}).text.strip()
        data['Product Price'] = product.find('span', {'class': 'a-price-whole'}).text.strip()

        rating = product.find('span', {'class': 'a-icon-alt'})
        if rating:
            data['Rating'] = rating.text.strip().split()[0]
        else:
            data['Rating'] = 'Not available'

        reviews = product.find('span', {'class': 'a-size-base'})
        if reviews:
            data['Number of Reviews'] = reviews.text.strip()
        else:
            data['Number of Reviews'] = '0'

        products.append(data)

    return products

# Set the number of pages to scrape
num_pages = 20

# Base URL for product listing
base_url = 'https://www.amazon.in/s'

# Parameters for the initial page
params = {
    'k': 'bags',
    'crid': '2M096C61O4MLT',
    'qid': '1653308124',
    'sprefix': 'ba,aps,283',
    'ref': 'sr_pg_1'
}

# Create a CSV file to store the scraped data
csv_file = open('products.csv', 'w', newline='')
csv_writer = csv.DictWriter(csv_file, fieldnames=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
csv_writer.writeheader()

# Scrape multiple pages
for page in range(1, num_pages + 1):
    params['ref'] = f'sr_pg_{page}'
    response = requests.get(base_url, params=params)
    page_products = scrape_product_page(response.url)
    csv_writer.writerows(page_products)

csv_file.close()
