# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
import csv
import json
import requests
import requests_cache
import lxml.html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}
LATITUDE = re.compile(r"lat=([\d.-]+)")
LONGITUDE = re.compile(r"long=([\d.-]+)")

requests_cache.install_cache(cache_name='apple_ctore', backend='sqlite')

def export(items):
    with open('stores.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'street', 'locality', 'region', 'postal_code', 'latitude', 'longitude', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)

def crawl_store(url):
    response = requests.get(url, headers=HEADERS)
    doc = lxml.html.fromstring(response.content)
    script = doc.xpath('/html/head/script[@type="application/ld+json"]/text()')
    data = json.loads(script[0])
    address = data['address']
    geo = data['geo']
    item = {
        'name': doc.xpath('/html/head/meta[@property="og:title"]/@content')[0].split('-', 1)[0].strip(),
        'street': address['streetAddress'],
        'locality': address['addressLocality'],
        'region': address['addressRegion'],
        'postal_code': address['postalCode'],
        'latitude': geo['latitude'],
        'longitude': geo['longitude'],
        'url': doc.xpath('/html/head/meta[@property="og:url"]/@content')[0],
    }
    print(item)
    return item

def crawl_stores(html):
    doc = lxml.html.fromstring(html)
    stores = doc.cssselect('.store-address a')[:100]
    for store in stores:
        href = store.get('href')
        url = f'https://apple.com{href}'
        yield crawl_store(url)

if __name__ == '__main__':
    url = 'https://www.apple.com/retail/storelist/'
    response = requests.get(url, headers=HEADERS)
    items = crawl_stores(response.content)
    export(items)
