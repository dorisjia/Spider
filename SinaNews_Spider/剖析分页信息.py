# 1.选择Network页签。
# 2.点选JS
# 3.点找到下列连接：【page】
# http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=2&callback=newsloadercallback&_=1520131407580

import requests
import json

# res = requests.get('http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=1&callback=newsloadercallback&_=1520131407580')
# jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');')) # 字典形式存储
# print(jd)

# for ent in jd['result']['data']:
#     print(ent['url'])

# 使用for循环产生多页连接
url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&callback=newsloadercallback&_=1520131407580&page={}'
for i in range(1,4):
    newsUrl = url.format(i)
    # print(newsUrl)
    res = requests.get(newsUrl)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        print(ent['url'])
    print('\n')