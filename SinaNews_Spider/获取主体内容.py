import requests  # 请求网址
from bs4 import BeautifulSoup  # 移除标签，去除网页中的内容
from datetime import datetime

res = requests.get('http://news.sina.com.cn/o/2018-03-02/doc-ifyrzinh1669818.shtml')
res.encoding = 'utf-8'
# print(res.text) 打印整个网址
soup = BeautifulSoup(res.text, 'html.parser')

title = soup.select('.main-title')[0].text
timeSource = soup.select('.date-source span')[0].text
dt = datetime.strptime(timeSource, '%Y年%m月%d日 %H:%M')
# soup.select('.date-source span')[0].contents 去掉外层标签
# soup.select('.date-source span')[0].contents.strip() 移除字符串头尾指定的字符
mediaName = soup.select('.date-source a')[0].text
# print(soup.select('.date-source')[0].text)
print(title)
print(dt)
print(mediaName)

article = []
for p in soup.select('#article p')[:-1]: # [:-1])不显示最后一个p标签的内容
    article.append(p.text.strip())

articleContents = ' '.join(article)  # 通过空格连接作为list的article中的所有内容
print(articleContents)
# 下述方法，"一行文"，等价于21-26的内容
articleContents2 = ' '.join([p.text.strip() for p in soup.select('#article p')[:-1]])
print(articleContents2)

# 获取编辑名称
editor = soup.select('.show_author')[0].text.lstrip('责任编辑：')
print(editor)

# 获取评论数和评论内容

