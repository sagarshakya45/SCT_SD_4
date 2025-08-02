import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Your ScraperAPI key
SCRAPERAPI_KEY = "your_api_key_here"

def fetch_html(url):
    api_url = f"http://api.scraperapi.com?api_key={SCRAPERAPI_KEY}&url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        print("HTML fetched successfully.")
        return response.text
    else:
        print(f"Failed to fetch HTML: {response.status_code}")
        return None

def extract_product_info(html, domain):
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    if 'webscraper.io' in domain:
        cards = soup.select('.thumbnail')
        for card in cards:
            name = card.select_one('.title')
            price = card.select_one('.price')
            rating = len(card.select('.glyphicon-star'))
            if name and price:
                products.append([name.get_text(strip=True), price.get_text(strip=True), str(rating)])

    elif 'books.toscrape.com' in domain:
        books = soup.select('article.product_pod')
        for book in books:
            title = book.h3.a['title']
            price = book.select_one('.price_color').get_text(strip=True)
            rating = book.p['class'][1]
            products.append([title, price, rating])

    elif 'scrapeme.live' in domain:
        items = soup.select('li.product')
        for item in items:
            name = item.select_one('h2.woocommerce-loop-product__title')
            price = item.select_one('span.woocommerce-Price-amount')
            if name and price:
                products.append([name.get_text(strip=True), price.get_text(strip=True), "N/A"])

    elif 'demowebshop.tricentis.com' in domain:
        items = soup.select('div.item-box')
        for item in items:
            name = item.select_one('h2.product-title a')
            price = item.select_one('span.price.actual-price')
            if name and price:
                products.append([name.get_text(strip=True), price.get_text(strip=True), "N/A"])

    elif 'automationexercise.com' in domain:
        items = soup.select('.product-image-wrapper')
        for item in items:
            name = item.select_one('p')
            price = item.select_one('h2')
            if name and price:
                products.append([name.get_text(strip=True), price.get_text(strip=True), "N/A"])

    else:
        print("Unsupported domain.")
        return []

    if products:
        print("Products found:\n")
        for i, (name, price, rating) in enumerate(products, 1):
            print(f"{i}. {name} | Price: {price} | Rating: {rating}")
    else:
        print("No products matched the patterns.")

    return products

def save_to_csv(data, filepath):
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Price", "Rating"])
            writer.writerows(data)
        print(f"Data saved to '{filepath}' successfully.")
    except Exception as e:
        print(f"Failed to save CSV: {e}")

if __name__ == "__main__":
    url = input("Enter product page URL: ").strip()
    path = input("Enter CSV save path (e.g., products.csv): ").strip()

    if not url or not path:
        print("URL or file path missing. Exiting.")
    else:
        domain = urlparse(url).netloc
        html = fetch_html(url)
        if html:
            product_data = extract_product_info(html, domain)
            if product_data:
                save_to_csv(product_data, path)
