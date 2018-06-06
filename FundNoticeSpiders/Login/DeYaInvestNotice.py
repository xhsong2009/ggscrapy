# -*- coding: utf-8 -*-

from datetime import datetime
import time
from urllib.parse import urljoin
from scrapy import FormRequest, Request
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
import re


class DeYaInvestNoticeSpider(GGFundNoticeSpider):
    name = 'FundNotice_DeYaInvestNotice'
    sitename = '德亚投资'
    entry = 'http://www.deyainvest.com/'
    username = '13916427906'
    password = 'ZYYXSM123'
    #cookies = 'disclaimer=viewed; user_id=MTA3Ng%3D%3D--f21972507c46323f16bc9c323d4d978c043fcfc0; remember_token=luKemhDiRPU4qm71646y8Q; _deya_web_session=OFk4OUdFMU9DbUdHS0pDSVNldlgyck5Fd3luYkJUajgyYzNvWGJPc3RUOFh0ZzRtMytYWldhOG8rSEYzNVdKNVBiLzh0TWlGU3hBSFhBSzRsUCt1cU03aGU3V2pyWUpsK2I2dHRMbU1zTm0vakRJRGRPT0wxbnN3dkNFN09lOENXbmRBYm90MkhBYXI1ZnJDb3YyVTNwMmVQbzh3V3JXcWVmc0hDZWpBTU1FMFpZWHpjeFVzL2ZqeEMrbTI2YlZ5ODlnNjNCM2x2cDB6VlRMNGdJMi81TFpDSlBiR3I4MXJoUGRqM1dYcGtLSWFPMWNIQkI2cjBzWlJKbXF2RXN1dS0tQ2hudnAwWXNzVkFGSUlaOSt3czZVUT09--6509c8d1304bd44b327f0b31aec010ab38bd244d'
    lps = [
        {
            'url': 'http://www.deyainvest.com/my/products',
            'ref': None,
            'ext': {'page': '1'}
        }
    ]

    def start_requests(self):
        yield Request(url='http://www.deyainvest.com/', callback=self.parse_login_pre)

    def parse_login_pre(self, response):
        csrf_token = response.xpath('/html/head/meta[@name="csrf-token"]/@content').extract_first()
        url = 'http://www.deyainvest.com/disclaimer'
        yield Request(url= url,
                      method='PUT',
                      headers={'X-CSRF-Token': csrf_token,
                               'Accept':'*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript'},
                      callback=self.parse_login_next)

    def parse_login_next(self, response):
        yield Request(url='http://www.deyainvest.com/login', callback=self.parse_login)

    def parse_login(self, response):
        csrf_token = response.xpath('/html/body//input[@name="authenticity_token"]/@value').extract_first()
        form = {'utf8': '✓',
                'authenticity_token': csrf_token,
                'session[mobile]': self.username,
                'session[password]': self.password,
                'session[remember_me]': '0',
                'session[remember_me]': '1',
                'commit': '登录'}
        yield FormRequest(url='http://www.deyainvest.com/login',
                          method='POST',
                          formdata=form,
                          headers={
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                          },
                          )

    def parse_list(self, response):
        csrf_token = response.xpath('/html/head/meta[@name="csrf-token"]/@content').extract_first()
        self.ips.append({
            'url': 'http://www.deyainvest.com/announcements?page=1&to=products', 'ref': response.url,
            'X-Requested-With': 'XMLHttpRequest',
            'headers': {
                'X-CSRF-Token': csrf_token,
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
            }})

    def parse_item(self, response):
        line = response.text

        titles = re.findall(r'\\"\\">(\S+\s?\S+)\s*<\\/span>', line)

        dates = re.findall(r' text-right\\">\\n\s+(\d+年\d+月\d+日)\\n\s+<', line)
        urls = re.findall(r'data-remote=\\"true\\" href=\\"(\S+)\\">', line)
        next_url = re.search(r'href=\\"(/announcements\?\S+)\\">下一页', line)
        if next_url:
            next_url = next_url.group(1)
        for title in titles:
            url = urls.pop(0)
            url = urljoin(get_base_url(response), url)
            publish_time = dates.pop(0)
            publish_time = datetime.strptime(publish_time, '%Y年%m月%d日')
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = title   #
            item['publish_time'] = publish_time
            yield item
            #self.log(item)
        if next_url:
            next_url = urljoin(get_base_url(response), next_url)
            csrf_token = response.xpath('/html/head/meta[@name="csrf-token"]/@content').extract_first()
            self.ips.append({
                'url': next_url, 'ref': response.url,
                'X-Requested-With': 'XMLHttpRequest',
                'headers': {
                    'X-CSRF-Token': csrf_token,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01'
                }})