# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import re


class ZhongjinInvestSpider(GGFundNoticeSpider):
    name = 'FundNotice_ZhongjinInvest'
    sitename = '中金'
    entry = 'http://www.cicc.com'

    lps = [{
        'url': 'http://www.cicc.com/portal/business/am_products_cn.xhtml?productType=0&columniditr=528&columnidano=348&columnidlaw=538&attributevalue=ALL'
    }]

    def parse_list(self, response):
        rows = response.xpath('//tbody[@id="listForm:data:tbody_element"]/tr')
        for row in rows:
            href = row.xpath('./td[2]/a/@href').re_first(r'(\?\S+)')
            self.ips.append({
                'url': 'http://www.cicc.com/portal/business/show_amproduct_cn_body.xhtml'+str(href),
                'ref': response.url,
                'headers': {'Upgrade-Insecure-Requests': '1'}
            })

    def parse_item(self, response):

        rows = response.xpath('//*[@id="announcement"]/ul/li')
        if rows:
            for row in rows:
                url = row.xpath('./span[1]/a/@onclick').extract_first()

                urls1 = re.search(r'\'(\/portal\/business\/am\/\S+/)\',', url).group(1)
                urls2 = re.search(r'\/\',\'(\S*)\'', url).group(1)

                if urls2 == '':
                    urls2 = re.search(r"showArticle\(\'(\d+)\'", url).group(1)  # 152447
                    url = 'http://www.cicc.com/portal/business/show_amannouncement_cn.xhtml?articleId='+str(urls2)
                else:
                    url_all = urls1+str('//')+urls2
                    url = urljoin(get_base_url(response), url_all)

                title = row.xpath('./span[1]/a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')

                publish_time = row.xpath('./span[2]/text()').re_first('\d+-\d+-\d+')
                publish_time = datetime.strptime(publish_time, '%Y-%m-%d')

                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['url'] = url
                item['title'] = title
                item['publish_time'] = publish_time
                yield item

        rows_another = response.xpath('//div[@id="lawfiles"]/ul/li')
        if rows_another:
            for row in rows_another:
                url = row.xpath('./span/a/@onclick').extract_first()

                urls1 = re.search(r'\'(\/portal\/business\/am\/\S+/)\',', url).group(1)
                urls2 = re.search(r'\/\',\'(\S*)\'', url).group(1)

                if urls2 == '':
                    urls2 = re.search(r"showArticle\(\'(\d+)\'", url).group(1)
                    url = 'http://www.cicc.com/portal/business/show_amannouncement_cn.xhtml?articleId=' + str(urls2)
                else:
                    url_all = urls1 + str('//') + urls2
                    url = urljoin(get_base_url(response), url_all)
                title = row.xpath('./span/a/text()').extract_first().strip().replace('\t', '').replace('\r', '').replace('\n', '')

                publish_time = None

                item = GGFundNoticeItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url_entry'] = self.entry
                item['url'] = url
                item['title'] = title
                item['publish_time'] = publish_time
                yield item