from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class XinshidaizhengquanSecuritySpider(GGFundNavSpider):
    name = 'FundNav_XinshidaizhengquanSecurity'
    sitename = '新时代证券'
    channel = '券商资管净值'

    fps = [{
        'url': 'http://www.xsdzq.cn/cmsproduct/D23001/brief.shtml?procode=D23001&fundtype=xjgl',
    }]

    def parse_fund(self, response):

        urls = response.xpath(
            '//div[@class = "fgsgk_main"]/ul/li[@style="background:#FFFFFF;padding-left:5px;width:90%;display:none"]')
        for url in urls:
            code = url.xpath('./a/@id').extract_first()
            fund_name = url.xpath('./a/text()').extract_first()
            self.ips.append({
                'url': 'http://www.xsdzq.cn/xsdweb/xsdweb/netvalue/getNetValueListByCode.do?pageSize=1000&gotoPage=1',
                'form': {'netValue.product_code': code},
                'ref': response.url,
                'ext': {'fundname': fund_name}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        fundname = ext['fundname']
        rows = response.xpath('//table[@class="zcgl_cpjj"]//tr')
        rows = rows[1:-2]
        for row in rows:
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fundname
            statistic_date = row.xpath('./td[1]/text()').re_first('\d+-\d+-\d+')
            statistic_date = '20' + str(statistic_date)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d') if statistic_date else None

            if '7日年化收益率（%）' in response.xpath('//table/tr[1]/th[2]/text()').extract_first():
                d7_annualized_return = row.xpath('./td[2]').re_first('>\s*([0-9.]+)\s*<')
                item['d7_annualized_return'] = float(
                    d7_annualized_return) if d7_annualized_return else None
                yield item

            else:
                nav = row.xpath('./td[2]/text()').extract_first()
                item['nav'] = float(nav) if nav else None

                added_nav = row.xpath('./td[3]/text()').extract_first()
                item['added_nav'] = float(added_nav) if added_nav else None
                yield item
