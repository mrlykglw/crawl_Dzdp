import requests
from lxml import etree
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import ddddocr
from fontTools.ttLib import TTFont
import random
from queue import Queue
from faker import Faker
import time
import re
from 字体反爬_解析woff_ttf文件 import parse_woff_ttf
import csv
import threading
#对详情页url进行解析
class Dzdp(threading.Thread):
    #初始化
    def __init__(self,url_queue,data_queue):
        super().__init__()
        self.url_queue=url_queue
        self.data_queue=data_queue

        self.ua=Faker().chrome()
        self.headers = {
            'User-Agent':self.ua
        }
    #获取woff_ttf的替换字典
    def get_rep_dict(self,*filename_list):
        a=parse_woff_ttf(*filename_list)
        rep_dic=a.main()
        return rep_dic
    #解析店铺评分
    def parse_score(self,res):
        try:
            shopId = re.search('shopId: (.*?),', res.text).group(1).strip('"')
            cityId = re.search('cityId: (.*?),', res.text).group(1).strip('"')
            mainCategoryId = re.search('mainCategoryId:(.*?),', res.text).group(1)
            url_score = f'https://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?shopId={shopId}&cityId={cityId}&mainCategoryId={mainCategoryId}'
            res_score = requests.get(url=url_score, headers=self.headers).json()['fiveScore']
        except:
            print('未能获取到店铺评分url')
            res_score=' '

        return res_score
    #获得个人消费
    def parse_fee(self,res,rep_dic):
        try:
            result = re.search('(人均: )(.*?)元', res.text, re.S)
            fee = result.group(2).replace('<d class="num">', '').replace(';</d>', '').replace('&#x', 'uni')
            for k, v in rep_dic.items():
                fee = fee.replace(k, v)


        except:
            print('未能获取到个人消费')
            fee=' '
        return fee

    #获取评价数
    def parse_review(self,html,mapping_dict):
        list=html.xpath('//span[@id="reviewCount"]//text()')
        # 获得自然字符串组成的列表
        result_list = []
        for i in range(len(list)):
            m = list[i]
            m = str(m)
            n = m.encode('unicode_escape')
            result = n.decode('utf-8')
            result_list.append(result)
        result_final=''
        for i in result_list[1:-1]:
            for a, b in mapping_dict.items():
                i=i.replace(r'\u', '&#x')
                i=i.replace(a,b)
            result_final+=i
        result_final=result_final+list[-1]
        return result_final
    #获取电话号码
    def parse_phone_address(self,html,mapping_dict):
        shopId=re.search('shopId: (.*?),',html.text).group(1).strip('"')

        url_phone='https://www.dianping.com/ajax/json/shopDynamic/basicHideInfo?shopId='+shopId
        res=requests.get(url=url_phone,headers=self.headers)
        result = res.json()['msg']['shopInfo']['phoneNo']
        phone_number = result.replace('<d class="num">', '').replace(';</d>', '').replace('**', '')
        address = res.json()['msg']['shopInfo']['address'].replace('<e class="address">', '').replace(';</e>',                                                                                                    '').replace(
            '<d class="num">', '').replace(';</d>', '')

        for a, b in mapping_dict.items():
            phone_number = phone_number.replace(a, b)
        for a,b in mapping_dict.items():
            address = address.replace(a,b)


        return (phone_number,address)
    #请求
    def spider_parse(self,url):
        tiquApiUrl = 'http://proxy.siyetian.com/apis_get.html?token=gHbi1iTUtWNPR0a14keJBTTB1STqFUeNpWR51kaJpXTEVENNpWVz0EVjlXT6NGM.QO0MTMzEjM3YTM&limit=1&type=0&time=10&split=1&split_text=&area=0&repeat=0&isp=0'
        apiRes = requests.get(tiquApiUrl, timeout=5)
        #代理服务器
        ipport = apiRes.text
        proxies = {
            'http': '121.234.172.2:11844',
            'https': ipport
        }

        res=requests.get(url=url,headers=self.headers,proxies=proxies)
        html=etree.HTML(res.text)
        return res,html
    def main(self,url):
        res,html=self.spider_parse(url)
        rep_dic={'uniede8':'1','unif7b0':'2','unif0b6':'3','unied6c':'4','unif6ef':'5','unif4f8':'6','unie51c':'7','unif4ee':'8','unif6e1':'9','unieb9a':'0'}
        time.sleep(0.2)
        fee=self.parse_fee(res,rep_dic)
        score=self.parse_score(res)
        if fee==" " or "score"==" ":
            pass
        print('爬取成功')
        time.sleep(random.random())
        return (score,fee)
    def run(self):
        while True:  # 当队列为空的时候，就结束循环
            if self.url_queue.empty():
                break
            url = self.url_queue.get()
            # 处理数据
            score,fee=self.main(url)
            data_queue.put((score,fee))


#获取详情页url列表
class Get_url(object):
    def __init__(self,url_queue):
        self.url_queue=url_queue
        self.headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
    'Cookie': '__mta=150806025.1669822995707.1669822995707.1669822995707.1; _lxsdk_cuid=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _lxsdk=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _hc.v=f5abc8a0-5819-3384-27a8-87ba14cca074.1664188220; WEBDFPID=wz2zww6uvx3u52y50u7x8zzv92317z8681620409y14979580u72uyv4-1979548223318-1664188222630WIIGUAWfd79fef3d01d5e9aadc18ccd4d0c95073068; ctu=6c8c4705091c7a1a81d9497c561b4ccaea752de9b7d90bb002f89f86a0f2c4b6; s_ViewType=10; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1669822994; fspop=test; qruuid=2402a227-a4ae-4936-a6d7-46bbb8baa0a1; dplet=d9daf51d7fdc12f0ab3f5eb40fe4c1b6; dper=2d065e0cd11ec9ceb1430999fd112f9cc5779615d95f08c18e82d099c352eac0318b87482e840fe470d4886e27faa063c028242cd6d8a45b54d159414ea50cd6; ua=%E5%A2%A8%E6%9F%93%E6%B5%81%E4%BA%91; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1671940505,1671961550,1672021367,1672044541; cy=9; cye=chongqing; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1672050079; _lxsdk_s=1854e2b8785-04-288-46d%7C%7C3'
}
    #解析一级页面
    def get_url_one(self,keyword,page):
        url1_list=['https://www.dianping.com/search/keyword/16/0_'+keyword+f'/p{i}' for i in range(1,page+1)]


        return url1_list

    #解析二级页面
    def get_url_two(self,url1):
        # tiquApiUrl = 'http://proxy.siyetian.com/apis_get.html?token=gHbi1STU1EeOp3az4EVVJzTB1STqFUeNpWR51kaJpXTEVENNpWVz0EVjlXT6NGM.gM5gjM2kTM3YTM&limit=1&type=0&time=10&split=1&split_text=&area=0&repeat=0&isp=0'
        # apiRes = requests.get(tiquApiUrl, timeout=5)
        # 代理服务器
        # ipport = apiRes.text
        # proxies = {
        #     'http': ipport,
        #     'https': ipport
        # }
        res=requests.get(url1,headers=self.headers)
        result=list(set(re.findall('https://www.dianping.com/shop/(\w*?)"',res.text,re.S)))
        for i in range(len(result)):
            result[i]='https://www.dianping.com/shop/'+result[i]
            self.url_queue.put(result[i])
        return result
    def main(self):
        result_list_final=[]
        url1_list=self.get_url_one('火锅',2)
        for url1 in url1_list:

            result_list1=self.get_url_two(url1)
            result_list_final+=result_list1
        print(result_list_final)
        print(len(result_list_final))
        return result_list_final



if __name__=="__main__":
    # 2. 存放url的队列
    url_queue = Queue()
    data_queue = Queue()
    a = Get_url(url_queue)
    detail_url_list=a.main()


    p_lst = []
    # 创建三个生产者对象， join等待子线程结束
    for i in range(3):

        t = Dzdp(url_queue, data_queue)  # 创建对象时进行传参
        t.start()  # 会执行run方法
        p_lst.append(t)

    for p in p_lst:
        p.join()
    final_list=[]
    while True:
        if data_queue.empty():
            break
        dict={}
        score,fee = data_queue.get()
        dict['score']=score
        dict['fee']=fee
        final_list.append(dict)
    f = open('data.csv', 'w', encoding='utf-8', newline='')
    writer=csv.DictWriter(f,fieldnames=['score','fee'])
    writer.writeheader()
    writer.writerows(final_list)
    f.close()











