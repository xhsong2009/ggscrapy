
from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy.utils.response import get_base_url
from urllib.parse import urljoin


class FangZhengDongYaTrustSpider(GGFundNavSpider):

    name = 'FundNav_FangZhengDongYaTrust'
    sitename = '方正东亚信托'
    channel = '信托净值'

    proxy = 2
    fps = [
        {
            'url': 'http://www.gt-trust.com/index.php/index-show-tid-18.html'
        }
    ]

    def parse_fund(self, response):
        funds = response.xpath('/html/body/div[3]/div[3]//div[@class="table_wrap_two"]/table//tr/td[1]/a/@href').extract()
        next_url = response.xpath('/html/body/div[3]//div[@class="ny_page wow zoomIn"]/a[text()="下一页"]/@href').extract_first()
        for url in funds:
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url
            })
        if next_url is not None and next_url != '':
            next_url = urljoin(get_base_url(response), next_url)
            self.fps.append({
                'url': next_url,
                'ref': response.url
            })

    def parse_item(self, response):
        rows = response.xpath('//tr')
        fund_name = response.xpath('/html/body/div[3]/div[3]//div[@class="art-title"]/h3/text()').extract_first()
        for row in rows[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            if len(row.xpath('./td')) > 2:
                fund_date = row.xpath('./td[2]//text()').re_first('\d+-\d+-\d+')
                fund_nav = row.xpath('./td[3]//text()').re_first('\d+\.?\d*')
                if fund_date is None or fund_date == '':
                    fund_date = row.xpath('./td[1]//text()').re_first('\d+-\d+-\d+')
                    fund_nav = row.xpath('./td[2]//text()').re_first('\d+\.?\d*')
                item['nav'] = float(fund_nav) if fund_nav is not None and fund_nav != '' else None
                item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
                yield item
            else:
                fund_date = row.xpath('./td[1]//text()').re_first('\d+-+\d+-\d+')
                fund_date = fund_date.replace('--', '-', 2)
                fund_nav = row.xpath('./td[2]//text()').re_first('\d+\.?\d*')
                item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
                item['nav'] = float(fund_nav) if fund_nav is not None and fund_nav != '' else None
                yield item
        self.request_next()

