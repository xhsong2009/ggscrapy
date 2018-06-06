# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-04

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from scrapy import Request
import re


class MaiDaoZiChanInvestSpider(GGFundNavSpider):
    name = 'FundNav_MaiDaoZiChanInvest'
    sitename = '麦岛资产'
    channel = '投资顾问'
    allowed_domains = ['www.maidaoziguan.com']

    username = '13916427906'
    password = '111111'
    cookies = 'PHPSESSID=40scgb8hn8cdrkpfak9ar93276; 0203_110_179_245=0203.110.179.245; 0203_110_179_245time=1526533306; Hm_lvt_c9477ef9d8ebaa27c94f86cc3f505fa5=1526533309; Hm_lpvt_c9477ef9d8ebaa27c94f86cc3f505fa5=1526533309; quote.color=2; SSID=0203.110.179.2451526533306'

    def start_requests(self):
        yield Request(url='http://www.maidaoziguan.com/index.php/category/index/id/111.html',
                      callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        fund_urls = response.xpath("//div[@class='m_con_in']/ul[@id='dom_set']//li")
        for url in fund_urls:
            fund_url = url.xpath('.//@href').extract_first()
            self.fps.append({
                'url': 'http://www.maidaoziguan.com' + fund_url.replace('.html#dom_set', '/p/1.html#dom_set'),
                'ref': response.url,
            })

    def parse_fund(self, response):
        rows_urls = response.xpath("//ul[@class='cplb_ul2']/li/a[@class='fr']//@href").extract()
        if rows_urls:
            for url in rows_urls:
                self.ips.append({
                    'url': 'http://www.maidaoziguan.com' + url,
                    'ref': response.url,
                })
            pg = re.findall(r'/p/(\d+).html', response.url)[0]
            next_pg = str(int(pg) + 1)
            self.fps.append({
                'url': response.url.replace('/p/' + pg + '.html', '/p/' + next_pg + '.html'),
                'ref': response.url,
            })

    def parse_item(self, response):
        fund_info = re.findall(r'摘要：([\s\S]*?)</p>', response.text)[0]
        fund_info = fund_info.replace('累计参考净值：', ',').replace('参考净值：', '').replace(',', '，').replace('	', '')
        fund_infos = fund_info.split('，')
        fund_name = fund_infos[0]
        statistic_date = fund_infos[1].strip().replace('年', '-').replace('月', '-').replace('日', '')

        nav = fund_infos[2]
        item = GGFundNavItem()
        item['sitename'] = self.sitename
        item['channel'] = self.channel
        item['url'] = response.url
        item['fund_name'] = fund_name
        item['nav'] = float(nav)
        item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
        if '累计参考净值' in response.text:
            added_nav = fund_infos[3]
            item['added_nav'] = float(added_nav) if added_nav is not None else None

        yield item
