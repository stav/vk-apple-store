# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import requests_cache
import lxml.html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
}

requests_cache.install_cache(cache_name='apple_ctore', backend='sqlite')

def crawl_store(href):
    url = f'https://apple.com{href}'
    response = requests.get(url, headers=HEADERS)
    doc = lxml.html.fromstring(response.content)
    street, city, _, __, state, ___, zipcode, phone = doc.xpath('//address/text()')
    return {
        'url': doc.xpath('/html/head/meta[@property="og:url"]/@content')[0],
        'name': doc.xpath('/html/head/meta[@property="og:title"]/@content')[0].split('-', 1)[0].strip(),
        'street': street,
        'locality': city,
        'region': state,
        'postal_code': zipcode,
    }

def crawl_list(doc):
    for store in doc.cssselect('.store-address')[:20]:
        spans = store.xpath('.//span/text()')
        location = spans[0] if len(spans) > 0 else 'UNKNOWN'
        hrefs = store.xpath('.//a/@href')
        if hrefs:
            href = hrefs[0]
            yield crawl_store(href)

if __name__ == '__main__':
    url = 'https://www.apple.com/retail/storelist/'
    response = requests.get(url, headers=HEADERS)
    print(response.status_code)
    doc = lxml.html.fromstring(response.content)
    for item in crawl_list(doc):
        print(item)
