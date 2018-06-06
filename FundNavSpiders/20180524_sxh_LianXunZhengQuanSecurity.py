# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 宋孝虎
# Create_date : 2018-05-24
# Alter_date : 2018-05-30


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
import time


class LianXunZhengQuanSecuritySpider(GGFundNavSpider):
    name = 'FundNav_LianXunZhengQuanSecurity'
    sitename = '联讯证券'
    channel = '券商PB净值列表'
    allowed_domains = ['125.93.53.236:8716']

    def start_requests(self):
        ids = [('12&pageSize=100&orderCond=netValueDate+desc&name=盘通1号投资基金', '盘通1号投资基金'),
               ('13&pageSize=100&orderCond=netValueDate+desc&name=富锦-领航增利1期私募证券投资基金', '富锦-领航增利1期私募证券投资基金'),
               ('14&pageSize=100&orderCond=netValueDate+desc&name=富锦-领航增利2期私募证券投资基金', '富锦-领航增利2期私募证券投资基金'),
               ('15&pageSize=100&orderCond=netValueDate+desc&name=聚力财富稳健1号证券投资基金', '聚力财富稳健1号证券投资基金'),
               ('16&pageSize=100&orderCond=netValueDate+desc&name=明星9号私募投资基金', '明星9号私募投资基金'),
               ('17&pageSize=100&orderCond=netValueDate+desc&name=弘达资本盈东一号基金', '弘达资本盈东一号基金'),
               ('18&pageSize=100&orderCond=netValueDate+desc&name=恒大普惠证券投资基金二号', '恒大普惠证券投资基金二号'),
               ('19&pageSize=100&orderCond=netValueDate+desc&name=(已清盘)大兆新价值发现1号私募证券投资基金', '(已清盘)大兆新价值发现1号私募证券投资基金'),
               ('19&pageSize=100&orderCond=netValueDate+desc&name=大兆新价值发现1号私募证券投资基金', '大兆新价值发现1号私募证券投资基金'),
               ('20&pageSize=100&orderCond=netValueDate+desc&name=万喜稳盈一号', '万喜稳盈一号'),
               ('20&pageSize=100&orderCond=netValueDate+desc&name=万喜稳赢一号', '万喜稳赢一号'),
               ('21&pageSize=100&orderCond=netValueDate+desc&name=数金赤壁量化对冲私募证券投资基金', '数金赤壁量化对冲私募证券投资基金'),
               ('22&pageSize=100&orderCond=netValueDate+desc&name=天信俊霖1期基金', '天信俊霖1期基金'),
               ('23&pageSize=100&orderCond=netValueDate+desc&name=丹阳资本新三板2号定增基金', '丹阳资本新三板2号定增基金'),
               ('24&pageSize=100&orderCond=netValueDate+desc&name=钡镭永进私募证券投资基金', '钡镭永进私募证券投资基金'),
               ('25&pageSize=100&orderCond=netValueDate+desc&name=盛为联赢1号私募证券投资基金', '盛为联赢1号私募证券投资基金'),
               ('26&pageSize=100&orderCond=netValueDate+desc&name=真鑫如意二期证券投资基金', '真鑫如意二期证券投资基金'),
               ('27&pageSize=100&orderCond=netValueDate+desc&name=天运证券投资一号基金', '天运证券投资一号基金'),
               ('28&pageSize=100&orderCond=netValueDate+desc&name=明星11号私募投资基金', '明星11号私募投资基金'),
               ('29&pageSize=100&orderCond=netValueDate+desc&name=明星10号私募投资基金', '明星10号私募投资基金'),
               ('30&pageSize=100&orderCond=netValueDate+desc&name=恒裕满堂一号私募基金', '恒裕满堂一号私募基金'),
               ('31&pageSize=100&orderCond=netValueDate+desc&name=吉石创盈私募证券投资基金', '吉石创盈私募证券投资基金'),
               ('32&pageSize=100&orderCond=netValueDate+desc&name=华诺2号私募股权投资基金', '华诺2号私募股权投资基金'),
               ('33&pageSize=100&orderCond=netValueDate+desc&name=翊善致远一号私募基金', '翊善致远一号私募基金'),
               ('34&pageSize=100&orderCond=netValueDate+desc&name=千安二号平衡型证券投资私募基金', '千安二号平衡型证券投资私募基金'),
               ('35&pageSize=100&orderCond=netValueDate+desc&name=汉唐1号私募基金', '汉唐1号私募基金'),
               ('36&pageSize=100&orderCond=netValueDate+desc&name=深圳众享财富1号私募基金', '深圳众享财富1号私募基金')]
        for id in ids:
            self.ips.append({
                'url': 'http://125.93.53.236:8716/lxzq-info/api/data/list.action?requestId=o17miub1ej2nlhBjTskhLaMkhNgy8XV9&clientId=100001&table=trusteeship_netValue&mainId=' +
                       id[0],
                'ref': 'https://mall.lczq.com/servlet/',
                'ext': {'fund_name': id[1]}
            })
        urls = [(
                '43&starttime=&endtime=&page=0&size=20&name=%C3%96%C3%8A%C3%91%C2%BA%C2%B1%C2%A61%C2%BA%C3%85%C3%93%C3%85%C3%8F%C3%88%C2%BC%C2%B6A1',
                '质押宝1号优先级A1'), (
                '29&starttime=&endtime=&page=0&size=20&name=%C3%8C%C3%AC%C3%90%C3%87%C3%97%C3%8A%C2%B1%C2%BE1%C2%BA%C3%85',
                '天星资本1号'), ('58&starttime=&endtime=&page=0&size=20&name=%C3%81%C2%AA%C2%B0%C2%B28%C2%BA%C3%85', '联安8号'),
                ('27&starttime=&endtime=&page=0&size=20&name=%C2%BC%C3%9B%C3%96%C2%B57%C2%BA%C3%85', '价值7号'),
                ('63&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C2%BB%C2%AA5%C2%BA%C3%85', '尊华5号'),
                ('38&starttime=&endtime=&page=0&size=20&name=%C2%BB%C3%9D%C2%B8%C2%BB1%C2%BA%C3%85', '惠富1号'), (
                '46&starttime=&endtime=&page=0&size=20&name=%C3%96%C3%8A%C3%91%C2%BA%C2%B1%C2%A61%C2%BA%C3%85%C2%B4%C3%8E%C2%BC%C2%B6B',
                '质押宝1号次级B'),
                ('28&starttime=&endtime=&page=0&size=20&name=%C2%BC%C3%9B%C3%96%C2%B59%C2%BA%C3%85', '价值9号'), (
                '45&starttime=&endtime=&page=0&size=20&name=%C3%96%C3%8A%C3%91%C2%BA%C2%B1%C2%A61%C2%BA%C3%85%C3%93%C3%85%C3%8F%C3%88%C2%BC%C2%B6A2',
                '质押宝1号优先级A2'), (
                '30&starttime=&endtime=&page=0&size=20&name=%C3%8C%C3%AC%C3%90%C3%87%C3%97%C3%8A%C2%B1%C2%BE2%C2%BA%C3%85',
                '天星资本2号'), ('57&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C3%8F%C3%AD7%C2%BA%C3%85', '尊享7号'),
                ('39&starttime=&endtime=&page=0&size=20&name=%C3%94%C3%82%C3%94%C3%82%C3%93%C2%AF1%C2%BA%C3%85',
                 '月月盈1号'), ('55&starttime=&endtime=&page=0&size=20&name=%C3%81%C2%AA%C3%93%C2%AE2%C2%BA%C3%85', '联赢2号'),
                ('25&starttime=&endtime=&page=0&size=20&name=%C3%88%C3%BD%C2%B0%C3%A5%C2%BB%C3%A31%C2%BA%C3%85',
                 '三板汇1号'), ('54&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C3%8F%C3%AD5%C2%BA%C3%85', '尊享5号'),
                ('56&starttime=&endtime=&page=0&size=20&name=%C3%81%C2%AA%C2%B0%C2%B27%C2%BA%C3%85', '联安7号'), (
                '15&starttime=&endtime=&page=0&size=20&name=%C2%BB%C3%9D%C2%B0%C2%B21%C2%BA%C3%85%C3%93%C3%85%C3%8F%C3%88%C2%BC%C2%B6',
                '惠安1号优先级'),
                ('42&starttime=&endtime=&page=0&size=20&name=%C3%81%C2%AA%C2%B0%C2%B26%C2%BA%C3%85', '联安6号'), (
                '33&starttime=&endtime=&page=0&size=20&name=%C3%8C%C3%AC%C3%90%C3%87%C3%97%C3%8A%C2%B1%C2%BE3%C2%BA%C3%85',
                '天星资本3号'), (
                '41&starttime=&endtime=&page=0&size=20&name=%C3%81%C2%AA%C3%93%C2%AE1%C2%BA%C3%85%C2%B4%C3%8E%C2%BC%C2%B6',
                '联赢1号次级'), ('59&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C2%BB%C2%AA1%C2%BA%C3%85', '尊华1号'),
                (
                '16&starttime=&endtime=&page=0&size=20&name=%C2%BB%C3%9D%C2%B0%C2%B21%C2%BA%C3%85%C2%B4%C3%8E%C2%BC%C2%B6',
                '惠安1号次级'), (
                '40&starttime=&endtime=&page=0&size=20&name=%C3%81%C2%AA%C3%93%C2%AE1%C2%BA%C3%85%C3%93%C3%85%C3%8F%C3%88%C2%BC%C2%B6',
                '联赢1号优先级'), (
                '47&starttime=&endtime=&page=0&size=20&name=%C3%96%C3%8A%C3%91%C2%BA%C2%B1%C2%A61%C2%BA%C3%85%C3%93%C3%85%C3%8F%C3%88%C2%BC%C2%B6A3',
                '质押宝1号优先级A3'), (
                '19&starttime=&endtime=&page=0&size=20&name=%C3%8C%C3%AC%C3%8C%C3%AC%C3%80%C3%BB1%C2%BA%C3%85',
                '天天利1号'), ('52&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C3%8F%C3%AD1%C2%BA%C3%85', '尊享1号'),
                ('62&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C3%8F%C3%AD9%C2%BA%C3%85', '尊享9号'),
                ('1&starttime=&endtime=&page=0&size=20&name=%C3%8F%C3%96%C2%BD%C3%B0%C2%BB%C3%9D', '现金惠'),
                ('53&starttime=&endtime=&page=0&size=20&name=%C3%97%C3%B0%C3%8F%C3%AD3%C2%BA%C3%85', '尊享3号')]
        for url in urls:
            self.ips.append({
                'url': 'http://www.lxzq.com.cn/api/financials/netannouncement/page?detailid=' + url[0],
                'ref': 'https://mall.lczq.com/servlet/',
                'ext': {'fund_name': url[1]}
            })
        yield self.request_next()

    def parse_item(self, response):
        fund_name = response.meta['ext']['fund_name']
        row_info = json.loads(response.text)
        if '125.93.53.23' in response.url:
            rows = row_info['result']
        else:
            rows = row_info['get_response']['netAnnouncements']['items']
        for row in rows:
            statistic_date = row['netValueDate']
            nav = row['netValue']
            added_nav = row['totalNetValue']
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if nav is not None else None
            if '125.93.53.23' in response.url:
                item['channel'] = self.channel
                item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            else:
                item['channel'] = '券商资管净值'
                item['statistic_date'] = datetime.strptime(
                    time.strftime("%Y-%m-%d", time.localtime(int(statistic_date) / 1000)), '%Y-%m-%d')
            yield item
