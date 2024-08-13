import json
import re
import time
import requests
import sys
import datetime
from bs4 import BeautifulSoup

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Sec-Fetch-Site': 'none',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Sec-Fetch-Dest': 'document',
    'Connection': 'keep-alive',
}

session = requests.Session()

def parse(url):
    time.sleep(3)

    response = session.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    page = BeautifulSoup(response.text, features='html.parser')
    return (response.text, response.url, page)

def get_products(url, limit = 10):
    if limit == 0 or not url: return []

    (_, _, page) = parse(url)
    base_url = re.match(r'^(https?://[^/]+)', url).group(1)

    links = [base_url + l['href'] for l in page.find_all('a', attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})]

    next_link = page.find(attrs={'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})
    next_url = base_url + next_link['href'] if next_link else None

    return links + get_products(next_url, limit - 1)

def get_product(url):
    (html, product_url, page) = parse(url)
    title = page.find('span', {'id':"productTitle"}).text.strip()
    pricing = page.find('span', {'class':"priceToPay"})
    price = pricing.text.strip() if pricing else None
    ratings = page.find('div', attrs={'id': 'averageCustomerReviews'})
    rating = ratings.find('i').text.strip() if ratings else None
    images = re.findall('"hiRes":"(.+?)"', html)
    description = '\n'.join([li.text.strip() for li in page.find('div', {'id': "featurebullets_feature_div"}).find_all('li')])
    reviews = []
    for r in page.find_all('div', attrs={'class': 'review'}):
        review_text = r.find('div', attrs={'class': 'reviewText'})
        if review_text:
            text = review_text.text.strip()
            rating = r.find('span', attrs = {'class': 'a-icon-alt' }).text.strip()
            reviews.append({ 'text': text, 'rating': rating })

    return {
        'url': product_url,
        'title': title,
        'price': price,
        'rating': rating,
        'images': images,
        'description': description,
        'reviews': reviews,
    }

products_url = sys.argv[1] if len(sys.argv) > 1 else 'https://www.amazon.es/s?rh=n%3A4204449031&s=featured-rank&fs=true&ref=lp_4204449031_sar'

output = []
product_urls = get_products(products_url)
FILE = f'../data/bronze/output-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.json'
print(f'Found {len(product_urls)} products')
for product_url in product_urls:
    print(f'Retrieving {product_url}...')
    output.append(get_product(product_url))
    with open(FILE, 'w') as f:
        json.dump(output, f)

print(f'JSON data has been written to {FILE}')
