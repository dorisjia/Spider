import requests  # 请求网址
import json

comments = requests.get(
    'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-fyrzinh1669818&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&callback=jsonp_1520051251353&_=1520051251353')
# id=comos-fyrzinh1669818 ,id后面的内容同新闻网址的某段
comments.encoding = 'utf-8'

# print(comments.text.lstrip('jsonp_1520051251353(').rstrip(')'))
jd = json.loads(comments.text.lstrip('jsonp_1520051251353(').rstrip(')'))
print(jd['result']['count']['total'])

# 获得新闻编号
newsUrl = 'http://news.sina.com.cn/o/2018-03-02/doc-ifyrzinh1669818.shtml'
print(newsUrl.split('/')[-1].rstrip('.shtml').lstrip('doc-i'))

# 方法2
import re

m = re.search('doc-i(.*).shtml', newsUrl)
newsId = m.group(1)  # group(0)获取所有匹配到的部分，group(1)获取（）部分
print(newsId)

# 将取评论数的方法整理成统一函数形式
commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=json&channel=gn&newsid=comos-{}&group=undefined&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=3&t_size=3&h_size=3&thread=1&callback=jsonp_1520051251353&_=1520051251353'
# print(commentURL.format(newsId)) URL拼接

def getCommentCount(newsUrl):
    m = re.search('doc-i(.*).shtml', newsUrl)
    newsId = m.group(1)
    comments = requests.get(commentURL.format(newsId))
    jd = json.loads(comments.text.lstrip('jsonp_1520051251353(').rstrip(')'))
    return jd['result']['count']['total']

num = getCommentCount(newsUrl)
print(num)