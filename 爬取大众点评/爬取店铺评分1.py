import requests
import re
url='https://www.dianping.com/shop/H5wjXWWxK8Q8LUb2'

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
     'Cookie':'_lxsdk_cuid=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _lxsdk=18268bdbc53c8-046e3b9042ba29-76492e29-e1000-18268bdbc53af; _hc.v=f5abc8a0-5819-3384-27a8-87ba14cca074.1664188220; WEBDFPID=wz2zww6uvx3u52y50u7x8zzv92317z8681620409y14979580u72uyv4-1979548223318-1664188222630WIIGUAWfd79fef3d01d5e9aadc18ccd4d0c95073068; ctu=6c8c4705091c7a1a81d9497c561b4ccaea752de9b7d90bb002f89f86a0f2c4b6; s_ViewType=10; aburl=1; ua=%E5%A2%A8%E6%9F%93%E6%B5%81%E4%BA%91; fspop=test; cy=344; cye=changsha; dplet=02882cc77cd3bebc537e38cfe66079e9; dper=819bea3a8855cb9a46ff7801d14e31e47d7074101aa5816134f724e4884678ee6a16f94b5199ea381cd32691be9a09b0a53ef64fd1fb6b01e4650108fe595fd6b59bfa3468a3c2360155ef2a35898c8ce233d03202a9381e4748bfff8d97bbc0; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1669822994; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1669867616,1669900194,1669976418,1670053334; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1670053942; _lxsdk_s=184d6ef896e-60-a3e-441%7C%7C111',
    'Referer':'https://www.dianping.com/shop/H5wjXWWxK8Q8LUb2'
}

res=requests.get(url,headers=headers)
shopId=re.search('shopId: (.*?),',res.text).group(1).strip('"')

cityId=re.search('cityId: (.*?),',res.text).group(1).strip('"')

mainCategoryId=re.search('mainCategoryId:(.*?),',res.text).group(1)
#print(shopId,cityId,mainCategoryId,sep='**')
url_score=f'https://www.dianping.com/ajax/json/shopDynamic/reviewAndStar?shopId={shopId}&cityId={cityId}&mainCategoryId={mainCategoryId}'

res_score=requests.get(url=url_score,headers=headers)
print(res_score.json()['fiveScore'])