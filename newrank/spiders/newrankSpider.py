# -*- coding:utf-8 -*-
import time

import scrapy
from scrapy import Selector

from newrank.settings import COOKIE
from newrank.items import WecatItem

TITLE = ["shyjfb", "shanghaiyamon"
                   "atqwish",
         "jiankangqixiang",
         "TC_Monitor",
         "chinaweathernews",
         "mojiweather1",
         "shanghaifabu",
         "dashenw",
         "helloshanghai2013",
         "shyjgl",
         "shfxwxh",
         "tq-0898",
         "jilianginsh",
         "iknow-021",
         "iknow021",
         "SH-top1",
         "shtt365",
         "modu100",
         "weish021",
         "shanghai9178",
         "charming-shanghai",
         "dunk233",
         "qingchunshanghai",
         "Mordor0007",
         "newsshanghai",
         "bst310",
         "modu20",
         "toutiao021",
         "shanghaishiti",
         "stvxwf",
         "shxwcb",
         "xmwb1929",
         "ChicShanghai",
         "pdnews"]


class WechatSub(scrapy.Spider):
    name = "newrank"
    cookie = COOKIE
    headers = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    def start_requests(self):
        urls = []
        # file = open("util/wechatNames.txt")
        for title in TITLE:
            # print(title)
            urls.append("https://www.newrank.cn/public/info/detail.html?account=" + title.strip())
        # start_urls = urls
        # start_urls = "https://www.newrank.cn/public/info/detail.html?account=helloshanghai2013"

        for url in urls:
            time.sleep(1)
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookie)
        # yield scrapy.Request(url=start_urls, headers=self.headers, cookies=self.cookie)

    def parse(self, response):
        try:
            sel = Selector(response)
            title = sel.xpath("//div[@class=\"info-detail-head-weixin-name\"]/span//text()").extract()
            # print(title)
            id = sel.xpath("//div[@class=\"info-detail-head-weixin-num\"]/p/span//text()").extract()[0][4:]
            # print(id)
            wechat_name = title[0].strip()
            script = str(sel.xpath("//script//text()").extract())
            list = script[script.index(':[') + 3:script.index(']') - 1]
            lists = list.split("},{")
            wechatItem = WecatItem()
            wechatItem['id'] = id
            wechatItem['name'] = wechat_name
            # print lists
            for data in lists:
                ll = data.split(',')
                for l in ll:
                    if l.split(':')[0].strip("\"") == "article_clicks_count":
                        wechatItem['click_count'] = l.split(':')[1].strip("\"")
                    if l.split(':')[0].strip("\"") == "article_likes_count":
                        wechatItem['likes_count'] = l.split(':')[1].strip("\"")
                    if l.split(':')[0].strip("\"") == "rank_date":
                        wechatItem['rank_date'] = l.split(':')[1].strip("\"")[0:-3]
                    # rank_date=time.strptime(str(rank_date),"%Y-%m-%d")
                if wechatItem['click_count'] == "" and wechatItem['likes_count'] == "" and wechatItem[
                    'rank_date'] == "":
                    return
                # print(wechatItem)
                yield wechatItem
        except Exception as e:
            # print e
            pass

        pass

    pass
