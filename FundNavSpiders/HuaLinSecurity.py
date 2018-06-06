from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider


class HuaLinSecuritySpider(GGFundNavSpider):
    name = 'FundNav_HuaLinSecurity'
    sitename = '华林证券'
    channel = '券商资管净值'

    ips = []
    fund_dict = {'富贵竹9号': '8', '富贵竹12号': '8', '富贵竹13号': '136',
                 '富贵竹2号': '0', '富贵竹5号': '3', '富贵竹3号': '1',
                 '富贵竹11号': '7', '富贵竹17号': '137', '满天星1号': '140',
                 }
    for (fund_name, fund_code) in fund_dict.items():
        ips.append({
            'url': 'https://mall.chinalions.cn/servlet/financial/IndexAction?function=AjaxPricePage&product_egroup={}'.format(
                fund_code),
            'ext': {'pg': 1, 'fund_code': fund_code, 'fund_name': fund_name},
            'form': {'curPage': '1', 'numPerPage': '17'}
        })

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        rows = response.xpath("//tr")[1:]
        for row in rows:
                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = fund_name
                statistic_date = row.xpath("./td[1]").re_first('\d+-\d+-\d+')
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')

                nav = row.xpath("./td[2]").re_first('>\s*([0-9.]+)\s*<')
                item['nav'] = float(nav) if nav is not None else None

                added_nav = row.xpath("./td[5]").re_first('>\s*([0-9.]+)\s*<')
                item['added_nav'] = float(added_nav) if added_nav is not None else None
                yield item

        # ext = response.meta['ext']
        # pg = ext['pg']
        # fund_code = ext['fund_code']
        # if pg < 10:
        #     pg += 1
        #     self.ips.append({
        #         'url': 'https://mall.chinalions.cn/servlet/financial/IndexAction?function=AjaxPricePage&product_egroup={0}'.format(
        #             fund_code),
        #         'ext': {'pg': pg, 'fund_code': fund_code, 'fund_name': fund_name},
        #         'from': {'curPage': str(pg), 'numPerPage': '17'},
        #         'headers': {'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded'}
        #     })
