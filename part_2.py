import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    # Extract the required information
    data['Product URL'] = url
    product_title = soup.find('span', {'id': 'productTitle'})
    if product_title:
        data['Product Name'] = product_title.text.strip()
    else:
        data['Product Name'] = 'Not available'

    price = soup.find('span', {'class': 'a-offscreen'})
    if price:
        data['Product Price'] = price.text.strip()
    else:
        data['Product Price'] = 'Not available'

    rating = soup.find('span', {'class': 'a-icon-alt'})
    if rating:
        data['Rating'] = rating.text.strip().split()[0]
    else:
        data['Rating'] = 'Not available'

    reviews = soup.find('span', {'id': 'acrCustomerReviewText'})
    if reviews:
        data['Number of Reviews'] = reviews.text.strip()
    else:
        data['Number of Reviews'] = '0'

    description = soup.find('div', {'id': 'productDescription'})
    if description:
        data['Description'] = description.text.strip()
    else:
        data['Description'] = 'Not available'

    asin = soup.find('th', string='ASIN')
    if asin:
        data['ASIN'] = asin.find_next_sibling('td').text.strip()
    else:
        data['ASIN'] = 'Not available'

    product_description = soup.find('div', {'id': 'productDescription'})
    if product_description:
        data['Product Description'] = product_description.text.strip()
    else:
        data['Product Description'] = 'Not available'

    manufacturer = soup.find('th', string='Manufacturer')
    if manufacturer:
        data['Manufacturer'] = manufacturer.find_next_sibling('td').text.strip()
    else:
        data['Manufacturer'] = 'Not available'

    return data

# Read the product URLs from products.csv
product_urls = []
with open('products.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        product_urls.append(row['Product URL'])

# Create a CSV file to store the scraped data
csv_file = open('output.csv', 'w', newline='')
csv_writer = csv.DictWriter(csv_file, fieldnames=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])
csv_writer.writeheader()

# Iterate over the product URLs
for url in product_urls:
    product_data = scrape_product_page(url)
    csv_writer.writerow(product_data)

csv_file.close()
