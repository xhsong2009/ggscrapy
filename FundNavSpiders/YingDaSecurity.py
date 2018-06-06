# -*- coding: utf-8 -*-
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YingDaSecuritySpider(GGFundNavSpider):
    name = 'FundNav_YingDaSecurity'
    sitename = '英大证券'
    channel = '券商资管净值'

    fps = [
        {
            'url': 'http://www.ydsc.com.cn/ydzq/zcgl/content.jsp?classid=0002000100130006'
        }
    ]

    def parse_fund(self, response):
        rows = response.xpath('//ul[@id="side-menu"]/li[5]/ul/li/a')
        for row in rows:
            class_id = row.xpath('./@href').re_first('classid=([^/]+)&num=1')
            self.ips.append({
                'url': 'http://www.ydsc.com.cn/ydzq/zcgl/cpjhjzList.jsp',
                'form': {
                    'classid': class_id,
                    'pageIndex': '1',
                    'pageSize': '10',
                    'hrefURL': '',
                    'filter': ''
                },
                'pg': 1
            })

    def parse_item(self, response):
        rows = response.xpath('//table[@class="tab_01"]/tr')[1:]
        for row in rows:
            fund_name = row.xpath('./td[2]/text()').extract_first()
            statistic_date = row.xpath('./td[3]/text()').re_first('\d+-\d+-\d+')
            nav = row.xpath('./td[4]/text()').re_first('[0-9.]+')
            added_nav = row.xpath('./td[5]/text()').re_first('[0-9.]+')

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

        t_count = response.xpath('//div[@class="pages_ul_page33"]/ul/li[1]/text()').re_first('共有([\d]+)条记录')
        tp = int(t_count) / 10 if int(t_count) % 10 == 0 else int(t_count) // 10 + 1
        pg = response.meta['pg'] + 1
        if pg <= tp:
            class_id = response.meta['form']['classid']
            self.ips.append({
                'url': 'http://www.ydsc.com.cn/ydzq/zcgl/cpjhjzList.jsp',
                'form': {
                    'classid': class_id,
                    'pageIndex': str(pg),
                    'pageSize': '10',
                    'hrefURL': '',
                    'filter': ''
                },
                'pg': pg
            })
