from datetime import datetime
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider
from urllib.parse import urljoin
from scrapy.utils.response import get_base_url
import re


class ShangHaiAoSuoHaoNaAssetSpider(GGFundNoticeSpider):
    name = 'FundNotice_ShangHaiAoSuoHaoNaAsset'
    sitename = '上海奥索灏纳资产'
    entry = 'http://www.panna-wealth.com/'

    lps = [
        {
            'url': 'http://www.ashnasset.com.cn/index.php?m=content&c=index&a=lists&catid=25',
            'ref': None
        }
    ]

    def parse_list(self, response):
        noticeList = response.xpath('/html/body/div/div[2]/div[2]/div[3]//div[@class="zp11_1 mg2 xi14"]')
        next_page = response.xpath('/html/body/div/div[2]/div[2]/div[3]/div[@class="fy cen xi14"]/a[text()="下一页"]/@href').extract_first()
        cur_page = int(response.xpath('/html/body/div/div[2]/div[2]/div[3]/div[@class="fy cen xi14"]/span/text()').extract_first())
        next_page_index = int(re.search(r'page=(\d+)', next_page).group(1))
        for notice in noticeList:
            noticeLink = notice.xpath('./a/@href').extract_first().strip()
            title = notice.xpath('./a/text()').extract_first()
            publish_time = notice.xpath('./span/text()').extract_first()
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = urljoin(get_base_url(response), noticeLink)
            item['title'] = title
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d')
            yield item
        if next_page and cur_page != next_page_index:
            next_url = urljoin(get_base_url(response), next_page)
            self.lps.append({
                'url': next_url,
                'ref': response.url,
            })

