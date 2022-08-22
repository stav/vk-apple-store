# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import requests_cache
from pprint import  pprint
import lxml.html


requests_cache.install_cache(cache_name='apple_ctore', backend='sqlite')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    }
    url = 'https://www.apple.com/retail/storelist/'
    response = requests.get(url, headers=headers)
    pprint(response.status_code)
    doc = lxml.html.fromstring(response.content)
    print(doc)
    for store in doc.cssselect('.store-address'):
        span = store.xpath('.//span/text()')
        location = span[0] if len(span) > 0 else 'UNKNOWN'
        print(store, location)
