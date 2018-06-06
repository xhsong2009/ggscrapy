from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class YaozhiFutureSpider(GGFundNavSpider):
    name = 'FundNav_YaozhiFuture'
    sitename = '耀之资产'
    channel = '投顾净值'
    username = 'ZYYXSM'
    password = 'ZYYXSM123'
    cookies = 'acceptDisclaimer=1; PHPSESSID=1kqg5hq712ohutl0vcbu5t4qh4'
    fps = [{
        'url': 'http://www.yzamc.com/index.php/performance'
    }]

    def parse_fund(self, response):
        urls = response.xpath('//table[@class="table table-hover table-striped performance"]//tr')
        for url in urls[1:]:
            href = url.xpath('./td[1]/a/@href').extract_first()
            code = href.rsplit('=', 1)[1]
            fund_name = url.xpath('./td[1]/a/text()').extract_first()
            self.ips.append({

                'url': 'http://www.yzamc.com/index.php/ajax/productdatalist?&p=1&id=' + str(code),
                'ref': response.url,
                'ext': {'code': code, 'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        code = ext['code']
        fund_names = ext['fund_name']
        rows = response.xpath('//tr')
        rows = rows[0:-1]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_names

            statistic_date = row.xpath("./td[1]/text()").re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

            nav = row.xpath('./td[2]/text()').extract_first()
            item['nav'] = float(nav) if nav else None

            yield item

        next_page = response.xpath('//ul[@class="pages"]/li[last()]/@onclick').re_first(r',\'(\d+)\'\)')
        if next_page:
            self.ips.append({
                'url': 'http://www.yzamc.com/index.php/ajax/productdatalist?&p=' + next_page + '&id=' + str(code) + '',
                'ref': response.url,
                'ext': {'code': code, 'fund_name': fund_names}
            })
