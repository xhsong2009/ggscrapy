# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-18

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import re


class ShanXiXinTuoTrustSpider(GGFundNavSpider):
    name = 'FundNav_ShanXiXinTuoTrust'
    sitename = '山西信托'
    channel = '信托净值'
    allowed_domains = ['www.sxxt.net']

    fps = [
        {'url': 'http://www.sxxt.net/xxpl/cpgg/jzgg/',
         'pg': 1},
    ]

    def parse_fund(self, response):
        fund_urls = response.xpath("//div[@class='in_news']/ul/li//@href").extract()
        for fund_url in fund_urls:
            self.ips.append({
                'url': 'http://www.sxxt.net' + fund_url,
                'ref': response.url,
            })
        if fund_urls:
            pg = response.meta['pg']
            next_pg = pg + 1
            self.fps.append({
                'url': 'http://www.sxxt.net/xxpl/cpgg/jzgg/index' + str(next_pg) + '.html',
                'ref': response.url,
                'pg': next_pg
            })

    def parse_item(self, response):
        zz = '<td style="([\s\S]*?)">20([\s\S]*?)<([\s\S]*?)>(\d.\d+)<'
        if '>净值公告</td>' in response.text:
            navinfos = response.text.split('>净值公告</td>')
        else:
            navinfos = response.text.split('产品名称：')

        for navinfo in navinfos:
            if '>净值公告</td>' not in response.text:
                navinfo = '产品名称：' + navinfo
            if '产品名称' in navinfo:
                name = re.findall('产品名称：(.*?)</td>', navinfo)
                if name:
                    fund_name = name[0].split(' ')[0].replace('</strong>', '').replace('&nbsp;', '')
                else:
                    fund_name = re.findall('产品名称：(.*?)<', navinfo)[0].split(' ')[0].replace('</strong>', '').replace(
                        '&nbsp;', '')
                if '累计净值' in navinfo:
                    zz = '<td style="([\s\S]*?)">20([\s\S]*?)<([\s\S]*?)">(\d.\d+)<([\s\S]*?)>(\d.\d+|[\s\S+]|&nbsp;)</'
                rows = re.findall(zz, navinfo)
                for row in rows:
                    added_nav = None
                    item = GGFundNavItem()
                    nav = row[3]
                    if '累计净值' in navinfo:
                        added_nav = row[5].replace(' ', '').replace('　', '').replace('&nbsp;', '')
                        if added_nav:
                            item['added_nav'] = float(added_nav) if added_nav is not None else None
                    statistic_date = '20' + row[1]
                    if '<' in nav:
                        nav = re.findall('>(.*?)<', nav)[0]
                        statistic_date = re.findall('(.*?)<', statistic_date)[0]
                    statistic_date = statistic_date.replace('年', '-').replace('月', '-').replace('日', '')

                    item['sitename'] = self.sitename
                    item['channel'] = self.channel
                    item['url'] = response.url
                    item['fund_name'] = fund_name.replace('</span>', '')
                    item['nav'] = float(nav)
                    item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
                    yield item
