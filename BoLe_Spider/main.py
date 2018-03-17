# -*- coding: utf-8 -*-

from scrapy.cmdline import execute
import sys
import os
import  PIL

sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # 获取main文件所在目录的父(文件夹)目录

execute(["scrapy", "crawl", "jobbole"])