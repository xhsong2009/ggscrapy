# -*- coding: utf-8 -*-
# Department：保障部
# Author：王卓诚
# Create_Date：2018-05-28


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class WanLianSecuritySpider(GGFundNavSpider):
    name = 'FundNav_WanLianSecurity'
    sitename = '万联证券'
    channel = '券商资管净值'
    allowed_domains = ['www.wlzq.cn']
    cookies = 'JSESSIONID=abcym1Z36W1t8-8xGLkow; clientinfo=IWeq75+dwN2F+5fFVp5tNXDv6IF6mTyUTKq21LhU2Ek=&xPBSQiYdRhf0KJ5WvrBMwg==&xPBSQiYdRhf0KJ5WvrBMwg==&qfxYJ8xyR8yxjdhalY9g5tNN3Zd7+5iEeYKWv8xAoAs=&xPBSQiYdRhf0KJ5WvrBMwg==; @user_id=IWeq75+dwN2F+5fFVp5tNXDv6IF6mTyUTKq21LhU2Ek=; @fund_account=xPBSQiYdRhf0KJ5WvrBMwg==; tk_stat_b=2; tk_stat_c=1527041369814; tk_stat_e=44; tk_stat_a=17; tk_stat_id=01FB3ABE714A48C698CB10F47AD5E35; tk_stat_z=none'
    username = '13916427906'
    password = 'ZYYXSM123'

    fps = [{
        'url': 'http://www.wlzq.cn/main/zcgl/index.shtml',
        'ref': 'http://www.wlzq.cn'
    }]

    def parse_fund(self, response):
        arul = response.xpath('//table[@class="table02"]/tr')

        for uu in arul[1:]:
            url = uu.xpath('.//@onclick').extract_first()
            pname = uu.xpath('./td[1]//text()').extract_first()
            if (not url is None):
                pid = url.replace("showUrl('", '').replace("')", '').replace(';', '')
                self.ips.append({
                    'url': 'http://www.wlzq.cn/servlet/FundPageAction?function=AjaxFundNav&fundid=' + pid + '&rand=0.8130904473364353',
                    'ref': response.url,
                    'pg': 1,
                    'ext': {'pname': pname, 'pid': pid}
                })

    def parse_item(self, response):
        fund_name = response.meta['ext']['pname']
        jzinfo = response.text
        jzinfotype1 = re.compile(r'<title>(.*)</title>', re.S | re.I | re.M)
        jzinfotype2 = re.findall(jzinfotype1, jzinfo)
        jzdate1 = re.compile(r'<date>(.*)</date>', re.S | re.I | re.M)
        jzdate2 = re.findall(jzdate1, jzinfo)
        jzzhi1 = re.compile(r'<value>(.*)</value>', re.S | re.I | re.M)
        jzzhi2 = re.findall(jzzhi1, jzinfo)
        jzdate3 = jzdate2[0].split(',')

        if (len(jzinfotype2) > 0 and len(jzdate2) > 0 and len(jzzhi2) > 0):
            # 七日年化
            if (jzinfotype2[0].find('七日年化收益率') > -1):
                jzzhi3 = jzzhi2[0].split(',')
                for k1, v1 in enumerate(jzdate3):
                    statistic_date = v1
                    d7_annualized_return = jzzhi3[k1]
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['d7_annualized_return'] = float(d7_annualized_return) if d7_annualized_return else None
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
                    yield item
        # 净值
            elif (jzinfotype2[0].find('单位净值') > -1):
                jzzhi31 = jzzhi2[0].split('|')
                jzzhi41 = jzzhi31[0].split(',')
                jzzhi42 = jzzhi31[1].split(',')
                for k2, v2 in enumerate(jzdate3):
                    statistic_date = v2
                    nav = jzzhi41[k2]
                    added_nav = jzzhi42[k2]
                    item = GGFundNavItem()
                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name
                    item['nav'] = float(nav) if nav else None
                    item['added_nav'] = float(added_nav) if added_nav else None
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y%m%d')
                    yield item
