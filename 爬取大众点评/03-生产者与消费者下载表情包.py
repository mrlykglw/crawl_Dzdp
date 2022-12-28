'''
一个生产者
一个消费者
数据是存在在队列当中
'''
import re
import threading
import random
from  urllib import request
import requests
from lxml import etree
from queue import Queue
import time


# 生产者——获取图片url以及标题
class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }

    def __init__(self, page_queue, img_queue):
        super().__init__()  # 调用父类的__init__方法
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:  # 当队列为空的时候，就结束循环
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            # 处理数据
            self.parse_page(url)

    def parse_page(self, url):
        # 发请求，获取响应
        res = requests.get(url, headers=self.headers)
        time.sleep(random.random())  # 0-1
        text = res.text
        # 解析数据，拿真的图片地址
        html = etree.HTML(text)
        # 将获取的所有img标签放到列表里面
        time.sleep(random.random())  # 0-1
        images = html.xpath('//img[@class="ui image lazy"]')
        print('images==', len(images))  #
        # 取出每一个图片的地址
        for img in images:
            # 图片url
            img_url = img.xpath('@data-original')[0]  # ['xxxx']
            title = img.xpath('@title')[0]
            # 保存图片
            # title = title.replace('?', '').replace('<', '').replace('/', '')
            title = re.sub(r'[，。？?/\\<>:]', '', title)
            img_title = title+'.jpg'  # 将图片url以及图片标题拿到
            # 将数据存放到队列当中，给消费者处理
            self.img_queue.put((img_url, img_title))
            print(self.img_queue.qsize())  # 10页有450个，长度不对？


# 消费者
class Consumer(threading.Thread):
    def __init__(self, img_queue):
        super().__init__()
        self.img_queue = img_queue

    def run(self):
        while True:  # 生产者数据没有产生，而消费者开始执行
            if self.img_queue.empty():
                break
            img_data = self.img_queue.get()  # 元组类型
            # 解包操作 a,b = (1, 2)
            url, filename = img_data
            request.urlretrieve(url, f'images/{filename}')
            print(filename+"下载完成")


if __name__ == '__main__':
    # 1.url存放到队列
    page_queue = Queue()
    # 2. 存放数据的队列
    img_queue = Queue()
    for i in range(1, 11):
        url = f'https://www.fabiaoqing.com/biaoqing/lists/page/{i}.html'
        page_queue.put(url)

    p_lst = []
    # 创建三个生产者对象， join等待子线程结束
    for i in range(3):
        t = Producer(page_queue, img_queue)  # 创建对象时进行传参
        t.start()  # 会执行run方法
        # t.join()  # 单线程
        p_lst.append(t)

    for p in p_lst:
        p.join()

    # 创建三个消费者
    for j in range(3):
        t = Consumer(img_queue)
        t.start()