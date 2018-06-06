# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 柳美云
# Create_date : 2018-05-04


from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from datetime import datetime


class GuoJinChuangXinInvestSpider(GGFundNavSpider):
    name = 'FundNav_GuoJinChuangXinInvest'
    sitename = '国金创新投资'
    channel = '投顾净值'

    # username = '13916427906'
    # password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.gjll.com.cn/index.php?s=/product/detail/sort_id/40/id/17.html'
    }]

    def parse_fund(self, response):
        # 取各产品对应的链接，当前选中和未选中的大类对应上一级class不同，故不取
        link_key = response.xpath(
            '//div[@class="cmm_pro_content"]/div[@class="cmm_pro_left"]/ul//p//@onclick').extract()
        for i in link_key:
            url = i.replace('window.location.href=', '').replace("'", '')
            self.ips.append({
                'url': url,
                'ref': response.url
            })

    def parse_item(self, response):
        list_info = response.xpath('//div[@class="cmm_pro_right"]/div[@class="cmm_pro_rbox"][2]/ul//li')
        fund_name = list_info.xpath('.//span[1]//text()').extract()
        statistic_date = list_info.xpath('.//span[2]//text()').extract()
        nav = list_info.xpath('.//span[3]//text()').extract()
        added_nav = list_info.xpath('.//span[4]//text()').extract()

        for fund_name, statistic_date, nav, added_nav in zip(fund_name, statistic_date, nav, added_nav):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None

            yield item


