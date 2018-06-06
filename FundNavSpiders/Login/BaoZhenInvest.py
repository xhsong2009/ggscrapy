from datetime import datetime
from scrapy import Request
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class BaoZhenInvestSpider(GGFundNavSpider):
    name = 'FundNav_BaoZhenInvest'
    sitename = '宝蓁投资'
    channel = '投资顾问'

    arc_username = '15538536932'
    arc_password = '123456'
    zyyx_username = '13916427906'
    zyyx_arc_password = 'ZYYXSM123'

    def start_requests(self):
        yield Request(url='http://www.szbztz.com/Html/login.html', callback=self.parse_pre_login)

    def parse_pre_login(self, response):
        url = 'http://www.szbztz.com/handler/bztz.ashx?action=login&name='+self.arc_username+'&pass='+self.arc_password
        yield Request(url=url, callback=self.parse_login)

    def parse_login(self, response):
        self.fps = [{
            'url': 'http://www.szbztz.com/handler/bztz.ashx?action=yjfhload&item=loadnav',
            'ref': response.url,
            'ext': {'type': '1'}
        }]

    def parse_fund(self, response):
        ext = response.meta['ext']
        type = int(ext['type'])
        if type == 1:
            fund_names = re.findall(r'>([\u4E00-\u9FA5]+)<\/a>', response.text)
            parent_ids = re.findall(r'vparentid=\'(\d+)\'', response.text)
            funds = response.xpath('/html//div[@class="view-content"]//a/@href').extract()
            for i in parent_ids:
                url = 'http://www.szbztz.com/handler/bztz.ashx?action=yjfhload&item=parentclick&parentid='+i
                self.fps.append({
                    'url': url,
                    'ref': response.url,
                    'ext': {'type': '2', 'fund_name': fund_names.pop(0)}
                })
        else:
            child_ids = re.search(r'vparentid=\'(\d+)\' vchildid=\'(\d+)\'>投资收益表', response.text)
            parent_id = child_ids.group(1)
            child_id = child_ids.group(2)
            fund_name = ext['fund_name']
            url = 'http://www.szbztz.com/handler/bztz.ashx?action=yjfhload&item=chlidclick&parentid='+parent_id+'&childid='+child_id
            self.ips.append({
                'url': url,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_name = ext['fund_name']
        datas = response.xpath('//tr')
        for row in datas[1:]:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['fund_name'] = fund_name
            item['channel'] = self.channel
            item['url'] = response.url
            tds = row.xpath('./td')
            if len(tds) > 4:
                statistic_date = row.xpath('./td[2]//text()').re_first(r'\d+-\d+-\d+')
                if statistic_date is None or statistic_date == '':
                    continue
                nav = row.xpath('./td[3]//text()').re_first(r'(\d+\.?\d*)')
                item['nav'] = float(nav) if nav is not None and nav != '' else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                yield item
            elif len(tds) > 2:
                statistic_date = row.xpath('./td[1]//text()').re_first(r'\d+年\d+月\d+日')
                if statistic_date is None or statistic_date == '':
                    continue
                nav = row.xpath('./td[2]//text()').re_first(r'(\d+\.?\d*)')
                item['nav'] = float(nav) if nav is not None and nav != '' else None
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y年%m月%d日')
                yield item
