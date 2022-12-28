import requests
from lxml import etree
from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import ddddocr
from fontTools.ttLib import TTFont
import re
from 字体反爬_解析woff_ttf文件 import parse_woff_ttf

obj=parse_woff_ttf('./字体文件/字体1.woff')
rep_dic=obj.main()
print(rep_dic)

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
     'Cookie': '__mta=150806025.1669822995707.1669822995707.1669822995707.1; _lxsdk_cuid=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _lxsdk=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _hc.v=f5abc8a0-5819-3384-27a8-87ba14cca074.1664188220; WEBDFPID=wz2zww6uvx3u52y50u7x8zzv92317z8681620409y14979580u72uyv4-1979548223318-1664188222630WIIGUAWfd79fef3d01d5e9aadc18ccd4d0c95073068; ctu=6c8c4705091c7a1a81d9497c561b4ccaea752de9b7d90bb002f89f86a0f2c4b6; s_ViewType=10; aburl=1; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1669822994; fspop=test; cy=9; cye=chongqing; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1671784156,1671844620,1671851586,1671861752; qruuid=6966d4fa-4ed8-4e3e-bd8e-79f592a49641; dplet=bb723efd28473ee674070660d7414215; dper=2d065e0cd11ec9ceb1430999fd112f9cf3d9848dfda33a173ff3eaf64f33c43379f3b0cd244564ccf18c9d34c05aa9c266baaf528ec8f5e6fc4878bd438755ab; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%A2%A8%E6%9F%93%E6%B5%81%E4%BA%91; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1671862059; _lxsdk_s=18542b9d0fd-8a4-2c3-30f%7C%7C111'
}
url=input("请输入网址")
res=requests.get(url=url,headers=headers)
html=etree.HTML(res.text)

try:
    result=re.search('(人均: )(.*?)元',res.text,re.S)
    a=result.group(2).replace('<d class="num">','').replace(';</d>','').replace('&#x','uni')
    for k,v in rep_dic.items():
        a=a.replace(k,v)
    print(a)

except:
    print('未能获取到个人消费')







