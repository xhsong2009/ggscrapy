# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-07

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import FormRequest


class MingShenInvestSpider(GGFundNavSpider):
    name = 'FundNav_MingShenInvest'
    sitename = '铭深资产'
    channel = '投资顾问'

    username = 'ZYYXSM'
    password = '13916427906'
    ips = [{'url': 'http://www.mindeep.cn/a/chanpinyujishu/dianxingchanpin/21.html'}]

    def start_requests(self):
        yield FormRequest(url='http://www.mindeep.cn/member/index_do.php',
                          formdata={'person': '1',
                                    'fmdo': 'login',
                                    'dopost': 'login',
                                    'gourl': '<?php if(!empty($gourl)) echo $gourl;?>',
                                    'username': 'ZYYXSM',
                                    'phone': '13916427906'
                                    })

    def parse_item(self, response):
        data1 = response.css('div.ac-mid-p2 tr')[1:-2]
        f_name = '外贸信托-铭深1号'
        for td in data1:
            fund_list = td.xpath('./td//text()').extract()
            filter_info = [_.strip() for _ in fund_list if _.strip()]
            fund_date = filter_info[0]
            fund_nav = filter_info[2]
            fund_added_nav = filter_info[1]

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = f_name
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(fund_nav) if fund_nav else None
            item['added_nav'] = float(fund_added_nav) if fund_added_nav else None
            yield item

        data2 = response.css('div.ac-mid-p2 tr')[-2]
        column1 = data2.xpath('./td[1]//text()').extract()
        date_col = [_.strip() for _ in column1 if _.strip()]
        column2 = data2.xpath('./td[2]//text()').extract()
        add_nav_col = [_.strip() for _ in column2 if _.strip()]
        column3 = data2.xpath('./td[3]//text()').extract()
        nav_col = [_.strip() for _ in column3 if _.strip()]

        for date, nav, add_nav in zip(date_col, nav_col, add_nav_col):
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = f_name
            item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(add_nav) if add_nav else None
            yield item
