# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class LiuXingTouZiSpider(GGFundNavSpider):
    name = 'FundNav_LiuXingTouZi'
    sitename = '杭州流星投资'
    channel = '投资顾问'

    fps = [{
        'url': 'http://www.liuxingtouzi.com/wp/%E6%97%97%E4%B8%8B%E4%BA%A7%E5%93%81/'
    }]

    def parse_fund(self, response):
        link_key = response.xpath(
            "//div[@class='wf-container-main']/div[@id='content']/table/tbody/tr[2]/td[2]/a//@href").extract()
        for i in link_key:
            url = i
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        nav_list = response.xpath(
            "//div[@class='wpb_text_column wpb_content_element ']/div[@class='wpb_wrapper']/div[2]/table/tbody/tr")
        fund_name_list = response.xpath("//div[@class='wf-td hgroup']/h1")
        fund_name = fund_name_list.xpath('.//text()').extract_first()
        for row in nav_list:
            i = row.xpath(".//text()").extract()
            i2 = [_ for _ in i if _.strip()]
            statistic_date = i2[0].replace('\xa0', '')
            nav = i2[1]
            added_nav = i2[2]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y.%m.%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item

