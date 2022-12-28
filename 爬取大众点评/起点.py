# 目标网站：https://www.qidian.com/rank/yuepiao/
#
# 一、目标需求：
# 1. 解密该网站月票数字的字体反爬
# 2. 获取小说名称，作者，更新时间，类型，简介，月票数据，进行csv保存。
# 3. 爬取前5页数据。
# 4. (重点！！！)使用面向对象或函数编写代码


import re
import csv
import urllib.request
import requests
from lxml import etree
from fontTools.ttLib import TTFont


class QiDian:
    def __init__(self):
        self.replace_dict = {}

    # 1. 获取网页源代码和字体文件
    def get_html(self,url):
        # url = 'https://www.qidian.com/rank/yuepiao/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }

        resp = requests.get(url, headers=headers)
        # 匹配字体文件url
        font_url = re.match(".*src: url\('(.*?)'\) ", resp.text).group(1)
        # 下载字体文件
        urllib.request.urlretrieve(font_url, 'qd.woff')

        return resp.text

    # 2. 建立映射关系
    def font(self):
        ts = TTFont('qd.woff')
        ts.saveXML('qd.xml')

        name = {'period': '', 'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7,
                'eight': 8, 'nine': 9}

        for k, v in ts.getBestCmap().items():
            key = '&#' + str(k) + ';'
            value = str(name[v])

            self.replace_dict[key] = value

    # 3. 解析网页
    def parse_html(self,resp_text):
        for k,v in self.replace_dict.items():
            resp_text = resp_text.replace(k,v)

        content = etree.HTML(resp_text)
        lis = content.xpath('//div[@id="book-img-text"]/ul/li')
        lst = []
        for li in lis:
            dic = {}
            dic['title'] = li.xpath('./div[2]/h2/a/text()')[0]

            data = li.xpath('./div[2]/p[1]/a/text()')

            dic['author'] = data[0]
            dic['type'] = data[1] + '.' + data[-1]

            dic['update_time'] = li.xpath('.//div[2]/p[3]/span[1]/text()')[0]
            dic['intro'] = li.xpath('.//div[2]/p[2]/text()')[0]
            dic['month_nums'] = li.xpath('./div[3]/div[1]/p[1]/span[1]/span[1]/text()')[0]
            print(dic)
            lst.append(dic)

        return lst


    # 4. 数据保存
    def save_data(self,lst,writer):
        # col = ["title", "author", "update_time", "type", "intro", "month_nums"]
        # with open('qd.csv', 'w', encoding='utf-8-sig', newline='') as f:
        #     writer = csv.DictWriter(f, fieldnames=col)
        #     writer.writeheader()
        writer.writerows(lst)

    # 主函数
    def main(self):
        col = ["title", "author", "update_time", "type", "intro", "month_nums"]
        f = open('qd.csv', 'w', encoding='utf-8-sig', newline='')
        writer = csv.DictWriter(f, fieldnames=col)
        writer.writeheader()


        for i in range(1,6):
            url = f'https://www.qidian.com/rank/yuepiao/year2022-month12-page{i}/'
            resp_text = self.get_html(url)
            self.font()
            lst = self.parse_html(resp_text)
            self.save_data(lst,writer)
        f.close()

if __name__ == '__main__':
    qd = QiDian()
    qd.main()
