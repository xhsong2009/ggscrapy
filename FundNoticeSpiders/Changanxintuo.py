# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class ChanganxintuoSpider(GGFundNoticeSpider):
    name = 'FundNotice_Changanxintuo'
    sitename = '长安信托'
    entry = 'https://www.xitic.cn/'
    cookies = '_shcdcms=74336f879f3549a1864085b13391c5ee; TS01caa770=01b2148ee2c8064dbe39ba558349546fcfc101cf6d2138303b2327f84fa853465da02a171063542a4ec4934600b0850314cf494048e99feab8fc2b49400325a6f8919a9cddaa8ea76cfd778773e46e7d8bde15a255; JSESSIONID=74336f879f3549a1864085b13391c5ee; __guid=177915299.1109513210227355400.1527492594004.2322; BIGipServerEweb_nginx_pool=1731428362.20480.0000; UM_distinctid=163a5a75e404a0-000d76d879ca2a-6b1b1279-1fa400-163a5a75e413f7; monitor_count=11; CNZZDATA1000026426=270451545-1527487437-https%253A%252F%252Fwww.caitc.cn%252F%7C1527492871; TS01afccea=01b2148ee2d3913314353e011913e4461f938511fba1e0726af63cea930dd444eda69574ad78de3e2b703004d60907d2f5f0beae6f9cc201be90962888337773d6fd27084f'
    ips = [
        {
            'url': 'https://www.caitc.cn/home/productReportSearch.jspx?reportType=0&title=&page=1',
        },
        {
            'url': 'https://www.caitc.cn/home/productReportSearch.jspx?reportType=3&title=&page=1',
        },
    ]

    def parse_item(self, response):
        rows = response.xpath('//ul[@class="cmnList"]/li')

        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            if url == 'javascript:void(0)':
                # <a href="javascript:void(0)"  onclick="getPdf('/home','/projectText/201510201386/1010/101002/144643001676888.pdf')">
                # r",\'(\S+)\'" 意思是： 以逗号开始的截取后面的单引号里面的多个非空字符，单引号里面的东西用（）定位
                on_click = row.xpath('./a/@onclick').re_first(r",\'(\S+)\'")
                on_click = str('/uploads/fore') + on_click
                url = on_click
            url = urljoin(get_base_url(response), url)

            title = row.xpath('./a/text()').extract_first().replace('\t', '').replace('\r', '').replace('\n', '')

            publish_time = row.xpath('./span/text()').extract_first()
            publish_time = datetime.strptime(publish_time, '%Y/%m/%d')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title
            item['publish_time'] = publish_time

            yield item

        next_url = response.xpath('//div[@class="pdtPaging"]/a[text()="下一页"]/@href').extract_first()
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            self.ips.append({
                'url': next_url,
                'ref': response.url
            })
