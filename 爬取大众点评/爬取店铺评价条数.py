import requests
from lxml import etree

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
        'Cookie': 'cy=344; cye=changsha; _lxsdk_cuid=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _lxsdk=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _hc.v=f5abc8a0-5819-3384-27a8-87ba14cca074.1664188220; WEBDFPID=wz2zww6uvx3u52y50u7x8zzv92317z8681620409y14979580u72uyv4-1979548223318-1664188222630WIIGUAWfd79fef3d01d5e9aadc18ccd4d0c95073068; ctu=6c8c4705091c7a1a81d9497c561b4ccaea752de9b7d90bb002f89f86a0f2c4b6; s_ViewType=10; fspop=test; aburl=1; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1666401923,1666427267,1666428429,1666530641; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lgtoken=09df0485f-b327-4957-854f-4875ccded473; dplet=0480d52248254868f7e607ae736742ce; dper=819bea3a8855cb9a46ff7801d14e31e420788b099b8df9fba2802492c64bbcb0b02d88f0328827170c6b0eb2245b99a6b37ae71f99c7ecad0eb39903446ae7f2bad376e67c27002501eb7c5c54a939005fcc2e2147b5618ddb62ee8b41fcbce7; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%A2%A8%E6%9F%93%E6%B5%81%E4%BA%91; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1666532009; _lxsdk_s=18404f78274-ada-218-8d7%7C%7C103'
    }
url='https://www.dianping.com/shop/H5wjXWWxK8Q8LUb2'
res=requests.get(url,headers=headers)
html=etree.HTML(res.text)
list=html.xpath('//span[@id="reviewCount"]//text()')
print(list[1:])
for i in list[1:]:
    pass