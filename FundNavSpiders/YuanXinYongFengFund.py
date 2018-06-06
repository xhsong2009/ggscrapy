from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YuanXinYongFengFundSpider(GGFundNavSpider):
    name = 'FundNav_YuanXinYongFengFund'
    sitename = '圆信永丰基金'
    channel = '投资顾问'
    cookies = 'ant_stream_58f8ded42f583=1525780301/2858073168; bow_stream_58f8ded42f583=13; HttpOnly=true; Secure=true; Hm_lvt_db4388806b6dc4f0176aeb7b266292a8=1524205932,1525676217,1525751781; ant_stream_590a19478316c=1525788896/1910063861; bow_stream_590a19478316c=13; bot_stream_590a19478316c=3; JSESSIONID=JpvKhxBJLxMZy8qbdkln56T6qVvqxLhcPYQPnGTpSts2JvmBF25f!-274733271; Hm_lpvt_db4388806b6dc4f0176aeb7b266292a8=1525760569'

    fps = [{
        'url': 'http://www.gtsfund.com.cn/',
        'ext': {'type': '1'}
    }]

    def parse_fund(self, response):
        print(response.text)
        type = response.meta['ext']['type']
        if type == '1':
            tables = response.xpath('//div[@id="content"]/div[@class="pagefund"]//table')
            for table in tables:
                thCount = len(table.xpath(".//tr[1]/th"))
                rows = table.xpath(".//tr")
                for row in rows[1:]:
                    is_currency_type = '0'  # 是否为货币型产品
                    if thCount == 6:
                        is_currency_type = '1'
                    fund_code = row.xpath('./td[1]/a/@title').extract_first().strip()
                    fund_name = row.xpath('./td[1]/a/text()').extract_first().strip()
                    self.fps.append({
                        'url': 'http://www.gtsfund.com.cn/products/' + fund_code + '/introduction/index.html',
                        'ref': response.url,
                        'ext': {'type': '2', 'fund_code': fund_code, 'is_currency_type': is_currency_type, 'fund_name': fund_name}
                    })

        if type == '2':
            fund_name = response.meta['ext']['fund_name']
            fund_code = response.meta['ext']['fund_code']
            is_currency_type = response.meta['ext']['is_currency_type']
            self.ips.append({
                'url': 'http://www.gtsfund.com.cn/chart-web/chart/fundnettable?pages=1-15&fundcode=' + fund_code + '&from=&to=',
                'ref': response.url,
                'ext': {'fund_code': fund_code, 'fund_name': fund_name, 'page': '1',
                        'is_currency_type': is_currency_type}
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_code = response.meta['ext']['fund_code']
        fund_name = response.meta['ext']['fund_name']
        is_currency_type = response.meta['ext']['is_currency_type']
        tpg = response.xpath('//*[@class="dtitle_t"]/table/tr/td/text()[1]').re_first('共\s*(\d+)\s*页')
        page = response.meta['ext']['page']
        table = response.xpath('//*[@id="dataTable"]')
        rows = table.xpath(".//tr")
        for row in rows[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            statistic_date = row.xpath('./td[2]/text()').extract_first().strip()
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            if is_currency_type == '0':  # 常规产品
                nav = row.xpath('./td[3]/text()').extract_first().strip()
                added_nav = row.xpath('./td[4]/text()').extract_first().strip()
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(added_nav) if added_nav is not None else None
            if is_currency_type == '1':  # 货币型产品
                income_value_per_ten_thousand = row.xpath('./td[3]/text()').extract_first().strip()
                d7_annualized_return = row.xpath('./td[4]/text()').extract_first().strip().replace('%', '')
                item['income_value_per_ten_thousand'] = float(
                    income_value_per_ten_thousand) if income_value_per_ten_thousand is not None else None
                item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return is not None else None
            # self.log(item)
            yield item
        if tpg is not None:
            page = int(page)
            if page < int(tpg):
                self.ips.append({
                    'url': 'http://www.gtsfund.com.cn/chart-web/chart/fundnettable?pages=' + str(
                        page + 1) + '-15&fundcode=' + fund_code + '&from=&to=',
                    'ref': response.url,
                    'ext': {'fund_code': fund_code, 'fund_name': fund_name, 'page': str(page + 1),
                            'is_currency_type': is_currency_type}
                })
