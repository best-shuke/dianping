import random
import time

import pandas as pd
import requests
from lxml import etree


def get_name(l):
    name = l.xpath('./div/div/a/h4/text()')
    return name


def get_price(l):
    price = l.xpath('./div/div[2]/a[2]/b/text()')
    return price


def get_data(pages=50):
    names = []
    prices = []
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Host': 'www.dianping.com',
        'Referer': 'http://www.dianping.com/beijing/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Cookie': 's_ViewType=10; _lxsdk_cuid=18faaf080abc8-087a36cedb0fd9-26001c51-1fa400-18faaf080abc8; _lxsdk=18faaf080abc8-087a36cedb0fd9-26001c51-1fa400-18faaf080abc8; _hc.v=6d2f4618-3424-441a-5266-fb153c31d7ee.1716559840; qruuid=31fb2bfb-04ae-441f-bfe1-5a0abecf2373; WEBDFPID=u5w2w0243538549xz85vw4u7x1wvuw9v81uzzu917zu97958v40z9v81-2031919840198-1716559839576YESWEMOfd79fef3d01d5e9aadc18ccd4d0c95076419; dper=0202222201c490844a9af99f7c2df6c4682c0a4e3ced34c760fd457811280411d4a944116ac893c3cd3f82598fd88329f49b23420a367ae3613f000000005120000040b70900265dab64bd064e24fb7a84754bcf7fade2e67cdab460b3c05047c8b26b5ac420f8420fb6713c78dc58e7d541; ll=7fd06e815b796be3df069dec7836c3df; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1716559889; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1716562164; _lxsdk_s=18faaf080ac-0d3-812-3b1%7C%7C252'
    }
    for i in range(pages):
        url = 'https://www.dianping.com/search/keyword/1/0_DIY' + '/p' + str(i + 1)
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.encoding = 'utf-8'
        html = response.text
        li = etree.HTML(html).xpath('//*[@id="shop-all-list"]/ul/li')
        for l in li:
            name = get_name(l)
            price = get_price(l)
            if price == []:
                price = ['暂无价格']
            print(i, name, price)
            names.extend(name)
            prices.extend(price)
        time.sleep(10 + random.random() * 10)
    return names, prices


if __name__ == '__main__':
    names, prices = get_data(50)
    data = pd.DataFrame({'name': names, 'price': prices})
    data.to_csv('dianping.csv', index=False)
