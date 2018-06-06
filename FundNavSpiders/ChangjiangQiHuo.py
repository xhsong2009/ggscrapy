# coding:utf-8

import re
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import GGFundNavItem


class ChangjiangQiHuoSpider(GGFundNavSpider):
    name = 'FundNav_ChangjiangQiHuo'
    sitename = '长江期货'
    channel = '发行机构'

    fps = [
        {'url': 'http://www.cjfco.com.cn/main/info/zcglgg/index.html'}
    ]

    def parse_fund(self, response):
        ext = response.meta['ext']
        if 'type' not in ext:
            urls = response.xpath('//div[@class = "listcontent"]/*/li/a[contains(text(),"产品净值公告")]')
        else:
            urls = response.xpath('//*/li/a[contains(text(),"产品净值公告")]')
        for url in urls:
            href = url.xpath('./@href').extract_first()
            ips_url = urljoin(get_base_url(response), href)
            self.ips.append({
                'url': ips_url,
                'ref': response.url
            })
        page_count_info = re.findall(r'pagecount:(\d+)', response.text)
        curpage_info = re.findall(r'curpage:(\d+)', response.text)
        if page_count_info and curpage_info:
            page_count = page_count_info[0]
            curpage = curpage_info[0]
            if int(curpage) < int(page_count):
                self.fps.append({
                    'url': 'http://www.cjfco.com.cn/servlet/Article?catalogId=3055&_=1524619825165&pageNumber='+str(int(curpage)+1)+'&rowOfPage=25&reqUrl=%2Fservlet%2FArticle%3FcatalogId%3D3055',
                    'ref': response.url,
                    'ext': {'type': '1'}
                })

        yield self.request_next()

    def parse_item(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract_first()
        if '('in title:
            statistic_date = title.split('(', 1)[1].replace(')', '').strip()
        elif '（' in title:
            statistic_date = title.split('（', 1)[1].replace('）', '').strip()
        funds = response.css('table tbody tr')
        if funds:
            title_name = funds[0].xpath('./td[1]/p/strong/text()').extract_first()
            if title_name is not None:
                for fund in funds[1:]:
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    fund_name = fund.xpath('./td[1]/p/text()').extract_first().strip().replace('(', '').replace(')', '').replace('\t', '').replace('\r', '').replace('\n', '')
                    item['fund_name'] = fund_name
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
                    nav = fund.xpath('./td[3]/p/text()').extract_first().strip().replace('(', '').replace(')', '').replace('\t', '').replace('\r', '').replace('\n', '')
                    if nav is None or nav == '':
                        return
                    item['nav'] = float(nav)
                    yield item
            else:
                title_name = funds[0].xpath('./td[1]/text()').extract_first()
                if title_name is None:
                    title_name = funds[0].xpath('./td[1]/font/text()').extract_first()
                if '产品净值公告'in title_name:
                    funds.pop(0)
                title_four_name = funds[0].xpath('./td[4]/text()').extract_first()
                if '产品净值' == title_four_name:
                    for fund in funds[1:]:
                        item = GGFundNavItem()
                        item['sitename'] = self.sitename
                        item['channel'] = self.channel
                        item['url'] = response.url
                        fund_name = fund.xpath('./td[1]/text()').extract_first()
                        item['fund_name'] = fund_name
                        item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
                        nav = fund.xpath('./td[4]/text()').extract_first()
                        item['nav'] = float(nav)
                        yield item
                else:
                    if '基金全称' != title_name:
                        title_name = funds[0].xpath('./td[1]/text()').extract_first()
                        nav_name = funds[0].xpath('./td[3]/text()').extract_first()
                        for fund in funds[1:]:
                            item = GGFundNavItem()
                            item['sitename'] = self.sitename
                            item['channel'] = self.channel
                            item['url'] = response.url
                            fund_name = fund.xpath('./td[1]/text()').extract_first()
                            if fund_name is None:
                                fonts = fund.xpath('./td[1]/font')
                                font_name = ''
                                for font in fonts:
                                    text = font.xpath('./text()').extract_first()
                                    font_name += text
                                fund_name = font_name
                            item['fund_name'] = fund_name
                            item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
                            if '单位净值' == nav_name or '净值' == nav_name:
                                nav = fund.xpath('./td[3]/text()').extract_first()
                                if '无' != nav:
                                    item['nav'] = float(nav)
                                    yield item

                                youxian_nav = fund.xpath('./td[4]/text()').extract_first()
                                if '无' != youxian_nav:
                                    item['fund_name'] = fund_name+'_优先级'
                                    item['nav'] = float(youxian_nav)
                                    yield item

                                jinqu_nav = fund.xpath('./td[5]/text()').extract_first()
                                if '无' != jinqu_nav:
                                    item['fund_name'] = fund_name+'_进取级'
                                    item['nav'] = float(jinqu_nav)
                                    yield item
                            elif '累计净值' == nav_name:
                                added_nav = fund.xpath('./td[3]/text()').extract_first()
                                item['added_nav'] = float(added_nav)
                                yield item
                                youxian_nav = fund.xpath('./td[4]/text()').extract_first()
                                if '无' != youxian_nav:
                                    item['fund_name'] = fund_name + '_优先级'
                                    item['nav'] = float(youxian_nav)
                                    yield item

                                jinqu_nav = fund.xpath('./td[5]/text()').extract_first()
                                if '无' != jinqu_nav:
                                    item['fund_name'] = fund_name + '_进取级'
                                    item['nav'] = float(jinqu_nav)
                                    yield item
                    else:
                        for fund in funds[1:]:
                            item = GGFundNavItem()
                            item['sitename'] = self.sitename
                            item['channel'] = self.channel
                            item['url'] = response.url
                            fund_name = fund.xpath('./td[2]/text()').extract_first()
                            item['fund_name'] = fund_name
                            item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
                            nav = fund.xpath('./td[5]/text()').extract_first()
                            item['nav'] = float(nav)
                            yield item

