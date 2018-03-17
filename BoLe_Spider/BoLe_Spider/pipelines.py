# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# 数据存储
import codecs  # 避免很多编码方面的繁杂工作
import json
from scrapy.pipelines.images import ImagesPipeline  # 存储图片
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import MySQLdb
import MySQLdb.cursors


class BoleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):  # 初始化的时候执行
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    # 通过pipeline将数据写入数据库中（同步操作），数据量不大的时候比较适用
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'jia', '123456', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
             insert into jobbole_article(title, url ,create_date, fav_nums, url_object_id) VALUES (%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,
                            (item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    # 连接池，[异步]操作数据存取到mysql中
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 将文件settings.py中的值传递过来
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms) # **dbparms也可以替换为 host=settings["MYSQL_HOST"]等等
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)  # 处理异常

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
              insert into jobbole_article(title, url ,create_date, fav_nums, url_object_id) VALUES (%s,%s,%s,%s,%s)
         """
        cursor.execute(insert_sql,
                       (item["title"], item["url"], item["create_date"], item["fav_nums"], item["url_object_id"]))


# 获取图片保存路径

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item: # 有封面图才处理
            for ok, value in results:
                image_file_path = value['path']
            item["front_image_path"] = image_file_path
        return item

    pass
