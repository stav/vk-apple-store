# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import requests_cache
import lxml.html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

requests_cache.install_cache(cache_name='apple_ctore', backend='sqlite')

def crawl_store(href):
    url = f'https://apple.com{href}'
    response = requests.get(url, headers=HEADERS)
    return {
        'url': response.url,
    }

def crawl_list(doc):
    for store in doc.cssselect('.store-address')[:2]:
        spans = store.xpath('.//span/text()')
        location = spans[0] if len(spans) > 0 else 'UNKNOWN'
        hrefs = store.xpath('.//a/@href')
        if hrefs:
            href = hrefs[0]
            print(store, location, href)
            yield crawl_store(href)

if __name__ == '__main__':
    url = 'https://www.apple.com/retail/storelist/'
    response = requests.get(url, headers=HEADERS)
    print(response.status_code)
    doc = lxml.html.fromstring(response.content)
    print(doc)
    for item in crawl_list(doc):
        print(item)
