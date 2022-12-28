import requests
from faker import Faker
import time
import random
import re
from queue import Queue
ua = Faker()
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


headers={
    'User-Agent': ua.chrome()
}

proxies = {
    'http':'117.92.127.212:12620',
    'https':'114.96.170.164:16265'
}
url_queue=Queue()
obj=Get_url(url_queue)
url_list=obj.main()
for url in url_list:
    res=requests.get(url,headers=headers,proxies=proxies)
    print(res.status_code)