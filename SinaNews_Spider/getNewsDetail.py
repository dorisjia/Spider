import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

# 新闻首页：http://news.sina.com.cn/china/

# newsUrl = 'http://news.sina.com.cn/o/2018-03-02/doc-ifyrzinh1669818.shtml'
commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&callback=jsonp_1520051251353&_=1520051251353'


def getCommentCount(newsUrl):
    m = re.search('doc-i(.*).shtml', newsUrl)
    newsId = m.group(1)
    comments = requests.get(commentURL.format(newsId))
    jd = json.loads(comments.text.lstrip('jsonp_1520051251353(').rstrip(')'))
    return jd['result']['count']['total']


def getNewsDetail(newsUrl):
    result = {}
    res = requests.get(newsUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('.main-title')[0].text
    result['newsSource'] = soup.select('.date-source a')[0].text
    timeSource = soup.select('.date-source span')[0].text
    result['dt'] = datetime.strptime(timeSource, '%Y年%m月%d日 %H:%M')
    result['article'] = ' '.join([p.text.strip() for p in soup.select('#article p')[:-1]])
    result['editor'] = soup.select('.show_author')[0].text.lstrip('责任编辑：')
    result['comment'] = getCommentCount(newsUrl)
    return result


# doc XHR JS
# dist = getNewsDetail(newsUrl)
# print(dist)

# 建立剖析清单链接函式
def parseListLinks(url):
    newsdetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails


url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&callback=newsloadercallback&_=1520131407580&page={}'
# dist2 = parseListLinks(url)  测试page=1时的显示
# print(dist2)

news_total = []
for i in range(1, 3):
    newsUrl = url.format(i)
    print(newsUrl)
    newsAry = parseListLinks(newsUrl)  # 每个分页产生出来的list
    news_total.extend(newsAry)  # 所有新闻内容
print(len(news_total))

# 使用pandas整理资料
import pandas
dataframe = pandas.DataFrame(news_total)
print(dataframe.head(10))  # head(num) num为展示数量

# 保存数据
dataframe.to_excel('news.xlsx')
import sqlite3
# 存
with sqlite3.connect('news.sqlite') as db:
    dataframe.to_sql('news', con=db)
# 取
with sqlite3.connect('news.sqlite') as db:
    df2 = pandas.read_sql_query('SELECT * FROM news', con=db)