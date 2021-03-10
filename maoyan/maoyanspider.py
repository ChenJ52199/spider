import requests
import re
from lxml import etree

from maoyan.font import get_num


class MaoYan(object):
    def __init__(self):
        self.s = requests.Session()
        self.url = 'https://maoyan.com/films/1217023'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Win x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        }
        self.item = dict()

    def run(self):
        resp = self.s.get(self.url, headers=self.headers)
        html = etree.HTML(resp.text)
        print(resp.text)
        self.item['video_name'] = html.xpath('//div/h1[@class="name"]/text()')[0]
        self.item['video_name_en'] = html.xpath('//div[@class="ename ellipsis"]/text()')[0]
        score_code = html.xpath('//div[contains(@class, "score")]/span/span/text()')[0]
        font_url = 'https:' + re.search("url\('(.+?)'\) format\('woff'\);", resp.text).group(1)  # 字体文件url
        with open('font_temp.woff', 'wb') as f:
            f.write(self.s.get(font_url).content)

        score = ''.join([get_num(s, 'font_temp.woff') for s in score_code])
        self.item['score'] = score
        box_office = html.xpath('//div[@class="movie-index"][2]/div//span[@class="stonefont"]/text()')[0]
        unit = html.xpath('//div[@class="movie-index"][2]/div//span[@class="unit"]/text()')[0]
        self.item['box_office'] = ''.join([get_num(s, 'font_temp.woff') for s in box_office]) + unit

        print(self.item)


if __name__ == '__main__':
    maoyan = MaoYan()
    maoyan.run()
