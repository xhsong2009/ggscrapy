from datetime import datetime
from urllib.parse import urljoin
import html
from scrapy.utils.response import get_base_url
from FundNoticeSpiders import GGFundNoticeItem
from FundNoticeSpiders import GGFundNoticeSpider


class XiNanFutureSpider(GGFundNoticeSpider):
    name = 'FundNotice_XiNanFuture'
    sitename = '西南期货'
    entry = 'http://www.swfutures.com/e/member/login/'

    username = '13916427906'
    password = 'ZYYXSM123'
    cookies = 'UM_distinctid=1633d537dff82-098842fdf1ec7-3c3c5b05-15f900-1633d537e0330c; jjqcccheckinfokey=1525742175%2C94a4afec66fb4beb142e0faf560e3159%2C9c693b040f150014937c0072d90c00db; CNZZDATA1261917271=1803972790-1525737813-http%253A%252F%252Fwww.swfutures.com%252F%7C1525777209; jjqccmlusername=13916427906; jjqccmluserid=93; jjqccmlgroupid=1; jjqccmlrnd=jGAait1s4nyRKDN1jwX6; jjqccmlauth=8b12ef2512d77bf658cd3c50daf26a8e'

    lps = [{
        'url': 'http://www.swfutures.com/e/action/ListInfo/?classid=11'

    }]

    def parse_list(self, response):
        next_url = response.xpath('/html/body/div[4]/div/div[2]/div/a[text()="下一页"]/@href').extract_first()
        notices = response.xpath('/html/body/div[4]/div/div[2]/ul/li')
        for notice in notices:
            url = notice.xpath('./a/@href').extract_first()
            title = notice.xpath('./a/text()').extract_first()
            publish_time = notice.xpath('./a/span/text()').extract_first()
            url = urljoin(get_base_url(response), url)
            item = GGFundNoticeItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url_entry'] = self.entry
            item['url'] = url
            item['title'] = html.unescape(title)
            item['publish_time'] = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
            yield item
        if next_url is not None:
            next_url = urljoin(get_base_url(response), next_url)
            self.lps.append({
                'url': next_url,
                'ref': response.url
            })
