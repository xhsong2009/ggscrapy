# Department : 保障部
# Author : 陈雅婷
# Create_date : 2018-05-23

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HarvestCapitalSpider(GGFundNavSpider):
    name = 'FundNav_HarvestCapital'
    sitename = '嘉实资本'
    channel = '公募专户净值'

    username = 'yuangh@go-goal.com'
    password = 'ZYYXSM123.'
    cookies = 'JSESSIONID=CF0EDB5BE1DB365D6A5F93B0288261F9'
    # 每次爬取需更换cookies

    fps = [{
        'url': 'http://www.harvestcm.com/publicPage/web_cn/netWorth_list.action?language=cn&pageNum_networth=1&pageSize_networth=10',
        'ref': 'http://www.harvestcm.com/publicPage/web_cn/mediaIndex_index.action?contentType=0&language=cn',
        'pg': 1
    }]

    def parse_fund(self, response):
        page_1 = response.meta['pg']
        page_number_1 = response.xpath('//div[@id="PageSelectorSelectorArea"]/a[@title="尾页"]/@href').extract_first()
        end_page_1 = int(page_number_1.replace('javascript: gotoPage_networth(', '').replace(')', ''))
        if page_1 < end_page_1:
            next_pg_1 = page_1 + 1
            next_url = response.url.replace('&pageNum_networth=' + str(page_1), '&pageNum_networth=' + str(next_pg_1))
            self.fps.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg_1
            })

        fund_link_key = response.xpath(
            '//div[@id="netWorthList"]/div[@id="MainArea"]/table[@id="J_approval2"]/tbody[@id="TableData"]/tr/td[3]/a/@href').extract()

        pg = 1
        for key in fund_link_key:
            key_code = key.replace('netWorth_detailList.action?language=cn', '')
            fund_link = 'http://www.harvestcm.com/publicPage/web_cn/netWorth_detailList.action?language=cn' + '&pageNum_networth=' + str(
                pg) + '&pageSize_networth=10' + key_code

            self.ips.append({
                'url': fund_link,
                'ref': response.url,
                'pg': pg
            })

    def parse_item(self, response):

        page_number = response.xpath('//div[@id="PageSelectorSelectorArea"]/a[@title="尾页"]/@href').extract_first()
        end_page = int(page_number.replace('javascript: gotoPage_networth(', '').replace(')', ''))

        nav_rows = response.xpath('//tr[@class="TableDetail1 template"]')
        for row in nav_rows:
            row_info = row.xpath('td/text()').extract()
            fund_name = row_info[3].strip()
            statistic_date = row_info[1].strip().replace('/', '-')
            nav = row_info[4].strip()
            added_nav = row_info[5].strip()

            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None
            item['nav'] = float(nav) if nav else None
            item['added_nav'] = float(added_nav) if added_nav else None
            yield item

        pg = response.meta['pg']
        if pg < end_page:
            next_pg = pg + 1
            next_url = response.url.replace('&pageNum_networth=' + str(pg), '&pageNum_networth=' + str(next_pg))
            self.ips.append({
                'url': next_url,
                'ref': response.url,
                'pg': next_pg
            })
