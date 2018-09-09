import requests
import urllib.parse
import json
from lxml import etree
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
}


def spiders(keyword, page):
    get_arg = {
        'keyword': keyword,
        'enc': 'utf-8',
        'page': page,
        's': 31,
        'scrolling': 'y',
        'log_id': time.time()
    }
    url = 'https://search.jd.com/Search?'
    url = url + urllib.parse.urlencode(get_arg)
    print(url)
    session = requests.Session()
    response = session.get(url=url, headers=headers)
    print(response.status_code)
    html_string = response.content.decode('utf-8')

    html_etree = etree.HTML(html_string)
    data_list = []
    div_tree = html_etree.xpath('//li[@class="gl-item"]')
    for div in div_tree:
        price = ''.join(div.xpath('.//strong/i/text()')).strip()
        title = ''.join(div.xpath('.//a/em/text()')).strip()
        data_list.append({'price': price, 'title': title})
    data_json = json.dumps(data_list, ensure_ascii=False)
    print(data_json)
    return data_json


if __name__ == '__main__':
    keyword = '华为'
    # page = 1
    for i in range(1, 200 + 1):
        data_json = spiders(keyword=keyword, page=i)
        with open('%s.json' % i, 'w', encoding='utf-8') as fp:
            fp.write(data_json)
        print('\n')