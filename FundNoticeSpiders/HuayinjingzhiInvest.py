# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class HuayinjingzhiInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_HuayinjingzhiInvest'
    sitename = '深圳华银精治资产'
    entry = 'http://szfine.com.cn'

    ips = [{
        'url': 'http://szfine.com.cn/NewsList.Asp?SortID=1',
    }]

    def parse_item(self, response):
        rows = response.xpath('//div[@id="info"]/table/tr[2]/td/table[1]/tr')
        for row in rows:
            url = row.xpath('./td[1]/a/@href').extract_first()#获取路径
            url = urljoin(get_base_url(response), url)#拼接绝对路径

            title = row.xpath('./td[1]/a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')#标题

            publish_time = row.xpath('./td[2]/text()').extract_first()
            if publish_time:
                publish_time = publish_time.strip().replace('\t', '').replace('\r', '').replace('\n', '')
            publish_time = datetime.strptime(publish_time, '%Y.%m.%d')#转换时间格式

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time
            yield item

        last_url = response.xpath('//a[contains(@title,"跳转到")]/@href').extract_first()
        if last_url:
            last_page = last_url.rsplit('=', 1)[1]
            current_page = response.xpath('//*[@id="info"]/table/tr[2]/td/table[2]/tr/td/strong[4]/text()').extract_first()
            if int(current_page) < int(last_page):
                self.ips.append({
                    'url': 'http://szfine.com.cn/NewsList.Asp?SortID=1&Page='+str(int(current_page)+1),
                    'ref': response.url
                })
