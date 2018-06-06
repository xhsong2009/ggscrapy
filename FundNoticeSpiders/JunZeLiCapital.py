# -*- coding: utf-8 -*-
from datetime import datetime
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class JunZeLiCapitalSpider(GGFundNoticeSpider):
    name = 'FundNotice_JunZeLiCapital'
    sitename = '深圳君泽利投资发展企业'
    entry = 'http://www.jzlfund.com/News.asp'

    lps = [
        {
            'url': 'http://www.jzlfund.com/News.asp'
        }
    ]

    def parse_list(self, response):
        rows = response.xpath('//div[@class="left_menu"]/a[contains(text(),"企业动态") or contains(text(),"企业公告")]')
        for row in rows:
            url = row.xpath('./@href').extract_first()
            class_id = row.xpath('./@href').re_first('ClassID=(\d+)')
            self.ips.append({
                'url': urljoin(get_base_url(response), url),
                'ref': response.url,
                'pg': 1,
                'ext': {'class_id': class_id}
            })

    def parse_item(self, response):
        ext = response.meta['ext']
        rows = response.xpath('//ul[@id="news"]/li')
        for row in rows:
            url = row.xpath('./a/@href').extract_first()
            url = urljoin(get_base_url(response), url)
            title = row.xpath('./a/text()').extract_first()
            publish_time = row.xpath('./span/text()').re_first('\d+-\d+-\d+')

            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['title'] = title
            item['url'] = url
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item

        class_id = ext['class_id']
        tp = int(response.xpath('//div[@id="showpage"]/div/a/@href')[-1].re_first('Page=(\d+)'))
        pg = response.meta['pg'] + 1
        if pg <= tp:
            self.ips.append({
                'url': 'http://www.jzlfund.com/News.asp?ClassID={0}&Page={1}'.format(class_id, pg),
                'ref': response.url,
                'pg': pg,
                'ext': {'class_id': class_id}
            })
