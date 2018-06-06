from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url


class ZhaoTuInvestSpider(GGFundNavSpider):
    name = 'FundNav_ZhaoTuInvest'
    sitename = '昭图投资'
    channel = '投顾净值'

    phone = '13916427906'
    cookies = 'PHPSESSID=8p82ofqf3tautuu9bg1gbioci3; UM_distinctid=1633fa484141b9-0b4c3c56fee0bf-3c3c5b05-15f900-1633fa4841525; realname=ZYYXSM; CNZZDATA3077745=cnzz_eid%3D144306366-1525775958-%26ntime%3D1527039952; reports=0'

    fps = [
        {'url': 'http://www.zoomtrend.cn/index.php?controller=products&action=read&id=1',
         'ext': {'type': '1'}
         }
    ]

    def parse_fund(self, response):
        ext = response.meta['ext']
        type = int(ext['type'])
        if type == 1:
            href_list = response.xpath('/html/body/table[3]//tr/td[1]/table[2]//a')
            for data in href_list:
                url = data.xpath('./@href').extract_first()
                fund_name = data.xpath('./text()').extract_first().strip().replace(' ', '')
                url = urljoin(get_base_url(response), url)
                self.fps.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'type': '2', 'fund_name': fund_name}
                })
        else:
            fund_name = ext['fund_name']
            url = response.xpath('//*[@id="pr_content"]/table//font[text()="基金净值"]/../../@href').extract_first()
            url = urljoin(get_base_url(response), url)
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'page': '0', 'url': url}
            })
        yield self.request_next()

    def parse_item(self, response):
        last_page = response.xpath('//*[@id="LastPage"]/@onclick').re_first('fnOnPageChanged\((\d+)\)')
        last_page = int(last_page)
        ext = response.meta['ext']
        datas = response.xpath('//*[@id="pr_content"]//table[@class="nets"]//tr')
        fund_name = ext['fund_name']
        page = int(ext['page'])
        url = ext['url']
        next_url = response.xpath('//*[@id="NextPage"]/a')
        for data in datas[1:]:
            fund_date = data.xpath('./td[1]/text()').extract_first()
            nav = data.xpath('./td[2]/text()').extract_first()
            added_nav = data.xpath('./td[3]/text()').extract_first()
            item = GGFundNavItem()

            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name.strip()
            item['statistic_date'] = datetime.strptime(fund_date, '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item
        if page < last_page:
            self.ips.append({
                'url': url+'&page='+str(page+1),
                'ref': response.url,
                'ext': {'fund_name': fund_name, 'page': str(page+1), 'url': url}
            })
        yield self.request_next()
