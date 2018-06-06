from datetime import datetime
from urllib.parse import urljoin
from scrapy import FormRequest
from scrapy.utils.response import get_base_url
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class ShenzhenyouliSpider(GGFundNavSpider):
    name = 'FundNav_Shenzhenyouli'
    sitename = '深圳友利基金'
    channel = '投资顾问'

    username = 'ZYYXSM'
    password = 'ZYYXSM123'

    cookies = 'ASP.NET_SessionId=40voc455ixlpweinl4r1y445; WHIR_USERINFOR=whir_mem_member_pid=189&membertype=&loginname=ZYYXSM&password=bd6NsQhCPVcfhA9seucM4Q%3d%3d&realname=&sex=&mobile=13916427906&email=yuangh%40go-goal.com&address=&integral=100&accountstate=&typeid=1&subjectid=0&state=-1&sort=&isdel=False&createdate=2018-5-14+11%3a37%3a33&createuser=&updateuser=&updatedate=2018-5-14+11%3a37%3a33&nickname=&brithdate=&takename=&takeaddress=&takeregion=&taketel=&takepostcode=&takeemail=&randomnum=&codes=&activatecode=xkfy&typeofcertificate=1417&purchasestatus=1&customertype=1&clientsname=%e9%83%91%e7%9b%8a%e6%98%8e&idnumber=350402197902120017'
    fps = [{
        'url': 'http://www.youlifund.com/cpjz/list_57.aspx?itemid=207'
    }]

    def parse_fund(self, response):
        urls = response.xpath('//ul[@class="ul"]/li')
        for url in urls:
            href = url.xpath('./a/@href').extract_first()
            myurl = urljoin(get_base_url(response), href)
            fund_name = url.xpath('./a/text()').extract_first()
            self.ips.append({
                'url': myurl,
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fund_names = ext['fund_name']
        rows = response.xpath('//table[@id="txt"]/tr')
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_names

            statistic_date = row.xpath("./td[3]/text()").re_first('\d+-\d+-\d+')
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

            nav = row.xpath("./td[4]/text()").extract_first()
            item['nav'] = float(nav) if nav else None

            added_nav = row.xpath("./td[5]/text()").extract_first()
            item['added_nav'] = float(added_nav) if added_nav else None

            yield item
