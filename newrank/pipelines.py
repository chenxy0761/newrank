# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys

from newrank.items import WecatItem
from util.con_Oracle import Dba
import logging

logger = logging.getLogger(__name__)

class WechatSubPipeline(object):
    def __init__(self):
        self.ora = Dba()

        # self.ConSql = """
        #             INSERT INTO  QXJ.QXJ_YQ_READNUM_DAY (type, id, name,readnum,thumbs_up_num,dta_date)
        #             VALUES ('wechat','%s','%s','%s','%s',to_date('%s','yyyy-mm-dd')) """
        self.ConSql = """
                    INSERT INTO  QXJ.QXJ_YQ_READNUM_DAY (type, id, name,readnum,thumbs_up_num,dta_date)
                    VALUES ('wechat','%s','%s','%s','%s',to_date('%s','yyyy-mm-dd')) """

    def process_item(self, item, spider):
        if isinstance(item, WecatItem):
            id = item['id']
            name = item['name']
            click_count = item['click_count']
            likes_count = item['likes_count']
            rank_date = item['rank_date']
            try:
                ConSql = self.ConSql % (
                    id,
                    name,
                    int(click_count),
                    int(likes_count),
                    rank_date,
                )
                self.ora.cux_sql_wechat(self.ora.connect(), ConSql, id, rank_date)
            except Exception as e:
                logger.error("ConSql: <<%s>>" % e)
