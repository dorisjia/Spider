# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader

# from BoLe_Spider.items import JobBoleItem
from BoLe_Spider.items import JobBoleItem,ArticleItemLoader
from BoLe_Spider.utils.common import get_md5


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表中的文章url并交给scrapy下载后并进行解析函数进行具体字段的解析
        2.获取下一页的url并交给scrpay进行下载

        """

        # 解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        # 提取下一页并交给Scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleItem()

        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css('.vote-post-up h10::text').extract()[0]
        fav_nums = response.css('.bookmark-btn::text').extract()[0]
        match_re = re.match(r".*?(\d+).*", fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css("a[href='#article-comment'] span::text").extract()[0]
        match_re = re.match(r".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0

        content = response.css('div.entry').extract()[0]

        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        article_item["url_object_id"] = get_md5(response.url)
        article_item["title"] = title
        article_item["url"] = response.url
        try:
            create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["content"] = content
        article_item["tags"] = tags

        # 通过item loader加载item。加强了可配置性。。item_loader.load_item()  # 会全部存为list

        item_loader = ArticleItemLoader(item=JobBoleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        item_loader.add_value("url", response.url)  # 没有通过css选择器选择，是通过值传递的方式获得的数据
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])

        article_item = item_loader.load_item()  # 会全部存为list

        yield article_item  # 就会将这些内容传递到pipelines中


"""
        # 以start_urls = ['http://blog.jobbole.com/113707/']举例
        title = response.xpath('// *[ @ id = "post-113707"] / div[1] / h1 /text()').extract()[0]

        time = response.xpath('//*[@id="post-113707"]/div[2]/p/text()').extract()[0].strip().replace("·", "").strip()
        # praise = response.xpath("//span[contains(@class,'vote-post-up')]")
        praise_nums = response.xpath('//*[@id="113707votetotal"]/text()').extract()[0]

        fav_text = response.xpath('//*[@id="post-113707"]/div[3]/div[5]/span[2]/text()').extract()[0]
        match_re = re.match(r".*(\d+).*", fav_text)
        if match_re:
            fav_nums = match_re.group(1)
        pass

        comment_text = response.xpath('//*[@id="post-113707"]/div[3]/div[5]/a/span/text()').extract()[0]
        match_re = re.match(r".*(\d+).*", comment_text)
        if match_re:
            comment_nums = match_re.group(1)
        pass

        content = response.xpath('//div[@class="entry"]').extract()[0]

        tag_list = response.xpath('//*[@id="post-113707"]/div[2]/p/a/text()').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        # 通过CSS选择器选择字段

        title = response.css(".entry-header h1::text").extract()[0]
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·", "").strip()
        praise_nums = response.css('.vote-post-up h10::text').extract()[0]
        fav_nums = response.css('.bookmark-btn::text').extract()[0]
        match_re = re.match(r".*(\d+).*", fav_nums)
        if match_re:
            fav_nums = match_re.group(1)
        pass
        comment_text = response.css("a[href='#article-comment']::text").extract()[0]
        match_re = re.match(r".*(\d+).*", comment_text)
        if match_re:
            comment_nums = match_re.group(1)
        pass
        content = response.css('div.entry').extract()[0]


        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        print(tags)
"""
