# Department : 保障部
# Author : 钱斌
# Create_date : 2018-05-07

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
from FundNavSpiders import Request
import json
import time


class MingHongInvestSpider(GGFundNavSpider):
    name = 'FundNav_MingHongInvest'
    sitename = '明汯投资'
    channel = '投资顾问'

    username = 'zyyx1'
    cookies = r'JSESSIONID=3C25265B3C73F3FDA230007287542A6D; cookie_625424_authState=1; type=1; investType=0; nickName=%E6%9C%9D%E9%98%B3%E6%B0%B8%E7%BB%AD1; customerName=%E6%9C%9D%E9%98%B3%E6%B0%B8%E7%BB%AD1; headImageUrl=http://wx.qlogo.cn/mmopen/ic3ibEjvYaKJzQR6VNVk5r7LgYib7pQrgfLlqY84BgnHpksFz4YFPT2YSNknFDRTPT1EkdWgFVFpoJYntPJiaNPwynFBTkuBPEU4/0; userCode=2758777; customerCode=2758777; companyName=%E4%B8%8A%E6%B5%B7%E6%98%8E%E6%B1%AF%E6%8A%95%E8%B5%84%E7%AE%A1%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; companyType=1; companyLogo=625424/image/f0bdbf2625e545c2860e1d19fb683817.png; simuSiteToken=fba2848f40835868ddc3ea8a2a7b893db346ae32c890def52536bea6d1ccc709bec38bc2fc7f40e4b84df820a2b2eded8d19973b5924e4a4974fa9c18e8af730c46e4972ab88fc2d061055145fa99a230d1727ec9d4a4c0870d8ffb4a2fc6fabdba72e73d69b0416ac70c4c992713746bba9c3552255799ddd9215e5df790671df947845eabff2ad758dce7ad0b2eeb9ef44b0e016528da49244b0f674c17221f9a748c5e523d08e99d83f350f19876f72986d1f8ca97967ab2347adde0d19c7f719729a1765ae817ccc532934eec8b85d4bb338a119aac3c1f3333fb40264bb3c3d2295df11f9a9568ee7ea76c517dd68ee82f07fdb43f0cc8dbbef300f2e6b050c863b05fd3837c0be05947d83b0f5c28eb5169d6dc75187da2e2e2f45fb136ed7ecbfaaa066d246457d5f8e2d8775bc43165b04cdbbc0252fea04888e97cff3aec8b9e3c2d1b09ab49c2ec3c20dd1d1686681a63a17e95ca41ce8750416d8aae33b50e29a2b28de631729d5d1a723a61df08a88d5e28691b900f7bdfdfb68bc43338217fc9efe51891bb4b7f506e0a87ebe02ce6e287c342ec7ce1c23d72c505d088f77716636a9275af73ddae34b8cd7900d807a0774623d0e66bfa8a967335b85831a7bf47b546d0e36e97adcc61501c0f14c2cf47dd90ed8a76766a606df4b439290855a31ed75a0dbf58d50387e06e4dad73a5df56a894b64432efc677263ec6956fd6bc0250b5be496fca7c6e37d050d2acb3ee9e9df5b7e3ee3fb42; companyCode=625424; telephone=""; configCode=3226138; isRealHost=1'

    def start_requests(self):
        yield Request(url='http://www.mhfunds.com/website/w/h', callback=self.parse_pre_fund)

    def parse_pre_fund(self, response):
        href_list = response.xpath('//div[@class="simu-site-subnav"]//a[re:test(text(),".*系列")]/@href').extract()
        for href in href_list:
            self.fps.append({
                'url': 'http://www.mhfunds.com/website/w/h' + href + '&fp=d',
                'ref': response.url
            })

    def parse_fund(self, response):
        pname_list = response.css('div.clickproduct::attr(productname)').extract()
        pcode_list = response.css('div.clickproduct::attr(productcode)').extract()
        for pcode, pname in zip(pcode_list, pname_list):
            parms = '?parms={companyCode:625424,userType:1,ReferCode:3145,ProductCode:%s}' % pcode
            self.ips.append({
                'url': 'http://www.mhfunds.com/website/mobile/getChartData' + parms,
                'ref': response.url,
                'ext': pname
            })

    def parse_item(self, response):
        data = json.loads(response.text)['data']
        if '访问过于频繁' in data:
            time.sleep(30)
            response.meta['proxy'] = 1
            self.ips.append(response.meta)

        elif data:
            for d1, d2 in zip(data[1], data[2]):
                date = d1[0]
                nav = d1[1]
                add_nav = d2[1]

                item = GGFundNavItem()
                item['sitename'] = self.sitename
                item['channel'] = self.channel
                item['url'] = response.url
                item['fund_name'] = response.meta['ext']
                item['statistic_date'] = datetime.strptime(date, '%Y-%m-%d')
                item['nav'] = float(nav) if nav is not None else None
                item['added_nav'] = float(add_nav) if add_nav is not None else None

                yield item
