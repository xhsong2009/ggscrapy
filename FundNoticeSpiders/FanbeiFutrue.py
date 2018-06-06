# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from scrapy import FormRequest


class FanbeiFutrueSpider(GGFundNoticeSpider):
    name = 'FundNotice_FanbeiFutrue'
    sitename = '凡贝资产'
    entry = 'http://www.fbamc.com/index.php'
    proxy = 2
    
    def start_requests(self):
        yield FormRequest(
            url='http://www.fbamc.com/index.php?p=default',  # 首页面
            callback=self.parse_list  # 回调下面方法
        )

    def parse_list(self, response):
        self.ips.append({
            'url': 'http://www.fbamc.com/index.php?p=news_list&c_id=17&lanmu=1',  # 数据列表页面
        })
        yield self.request_next()

    def parse_item(self, response):

        rows = response.xpath('//div[@class="news_list p2"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()#获取路径
            url = urljoin(get_base_url(response), url)#拼接绝对路径

            title = row.xpath('./a/@title').extract_first()#标题

            publish_time = row.xpath('./a/h1/span/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#时间格式
            publish_time = datetime.strptime(publish_time, '%Y/%m/%d')#转换时间格式

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        yield self.request_next()