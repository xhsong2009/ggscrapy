# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-02

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class HongHuTouZiInvestSpider(GGFundNavSpider):
    name = 'FundNav_HongHuTouZiInvest'
    sitename = '泓湖投资'
    channel = '投顾净值'
    allowed_domains = ['www.honghuinvest.com']

    cookies = 'JSESSIONID=72482488132D214E5B0C823D33FF66B1; cookie_2726861_authState=1; configCode=2728275; isRealHost=1; headImageUrl=; customerCode=2745024; companyName=%E4%B8%8A%E6%B5%B7%E6%B3%93%E6%B9%96%E6%8A%95%E8%B5%84%E7%AE%A1%E7%90%86%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; companyType=1; companyLogo=2726861/image/12ae4a222ce549e9957f3825a2673462.png; companyCode=2726861; type=3; investType=1; nickName=%E4%B8%8A%E6%B5%B7%E6%9C%9D%E9%98%B3%E6%B0%B8%E7%BB%AD%E5%9F%BA%E9%87%91%E9%94%80%E5%94%AE%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; customerName=%E4%B8%8A%E6%B5%B7%E6%9C%9D%E9%98%B3%E6%B0%B8%E7%BB%AD%E5%9F%BA%E9%87%91%E9%94%80%E5%94%AE%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8; userCode=2745024; simuSiteToken=dd60fc115f16e1a5e182fa29de9e5bc9b84df820a2b2eded4154e00240061da1cee4421e5dd3eb2c35aca25807d77eb133e54f54d3dc7fd258ecfd93cd4763840e714de335820aa41b52d4bef707129bb435648b93e53eb510fb518439aac87ff22c82d35901f877619764b99c668433be6a9093e7e02166d5b59eff496503d9b936cb48bc3c7c72ad927bff43db0e8530e8f07b3816fd40b31be849a9829a3973c3719ee1a4461aefca102c37f6dded726303b31bb56a5b6022d767c9cb5cf604bb8d2d95071136c05d1d8492b9257df64968ddc77fbf1007599e2eaf5bc4b3db0bf73311d3c62d1958930ebe3aedf3b925659610f1fb7bbec7d654d69ab213f64968ddc77fbf10d2a59075fe4fd8ecf7fac9894dd11252635070e74375d6a92fe9a82b0daed8368abc1b92d2bbf51fe625f666ab6b91458fe726bbf9f628b7ac70c4c992713746f719729a1765ae81ec7c71a0232742ce050c863b05fd3837ecc4aa23ca9811223ab36293b06de91ed5a1a68261ac3904a997b1de5b5a70c7ef87a5f80ff7afc138b587db2c39cf0991fd434e9e9b8e4f01ee33549312e0049e05681920b7dd64; telephone=""'
    fps = [{'url': 'http://www.honghuinvest.com/website/w/h?mt=8&mc=2730542&cc=2726861&fp=d'}]

    def parse_fund(self, response):
        fund_ids = response.xpath("//div[@class='clickproduct']")
        for url in fund_ids:
            fund_name = url.xpath(".//@productname").extract_first()
            fund_id = url.xpath(".//@productcode").extract_first()
            self.ips.append({
                'url': 'http://www.honghuinvest.com/website/mobile/getChartReferData?parms={companyCode:%s,userType:3,ReferCode:0,ProductCode:%s}&_=1525221380874' % (
                    fund_id, fund_id),
                'ref': response.url,
                'ext': {'fund_name': fund_name}
            })

    def parse_item(self, response):
        nav_info = json.loads(response.text)
        navs = nav_info['data'][1]
        added_navs = nav_info['data'][2]
        fund_name = response.meta['ext']['fund_name']
        for row in zip(navs, added_navs):
            statistic_date = row[0][0]
            nav = row[0][1]
            added_nav = row[1][1]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav)
            item['added_nav'] = float(added_nav)
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item

