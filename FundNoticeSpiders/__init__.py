import hashlib
import traceback
from datetime import datetime
from urllib.parse import quote
from scrapy import Item, Field
from ggmssql.pool import Pool
from GGScrapy import GGSpider
import config


# 基金公告Spider基类
class GGFundNoticeSpider(GGSpider):
    channel = '公告'

    custom_settings = {
        'ITEM_PIPELINES': {'FundNoticeSpiders.GGFundNoticePipeline': 300}
    }

    dbPool = Pool(config.fund_notice['db']['host'],
                  config.fund_notice['db']['port'],
                  config.fund_notice['db']['user'],
                  config.fund_notice['db']['pswd'],
                  config.fund_notice['db']['name'],
                  timeout=config.fund_notice['db']['timeout'])


# 基金公告Item
class GGFundNoticeItem(Item):
    hkey = Field()  # 哈希唯一

    groupname = Field()  # 分组名称
    sitename = Field()  # 站点名称
    channel = Field()  # 频道名称
    url_entry = Field()  # 链接入口

    url = Field()  # 链接地址
    title = Field()  # 公告标题
    publish_time = Field()  # 发布时间


# 基金公告Pipeline
class GGFundNoticePipeline(object):
    def process_item(self, item, spider):
        try:
            groupname = item['groupname'] if 'groupname' in item else spider.groupname
            groupname = groupname.strip() if isinstance(groupname, str) else None
            groupname = groupname if groupname != '' else None
            assert groupname is None or groupname != ''

            sitename = item['sitename'] if 'sitename' in item else None
            sitename = sitename.strip() if isinstance(sitename, str) else None
            assert sitename is not None and sitename != ''

            channel = item['channel'] if 'channel' in item else None
            channel = channel.strip() if isinstance(channel, str) else None
            assert channel is not None and channel != ''

            url_entry = item['url_entry'] if 'url_entry' in item else None
            url_entry = url_entry.strip() if isinstance(url_entry, str) else None
            assert url_entry is not None and url_entry != ''

            url = item['url'] if 'url' in item else None
            url = url.decode() if isinstance(url, bytes) else url
            url = url.strip() if isinstance(url, str) else None
            assert url is not None and url != ''

            title = item['title'] if 'title' in item else None
            title = title.strip() if isinstance(title, str) else None
            assert title is not None and title != ''

            publish_time = item['publish_time'] if 'publish_time' in item else None
            assert publish_time is None or isinstance(publish_time, datetime)
            publish_time = publish_time.strftime('%Y-%m-%d %H:%M:%S') if isinstance(publish_time, datetime) else None

            md5 = hashlib.md5()
            seed = 'sitename=' + quote(sitename)
            seed += '&channel=' + quote(channel)
            seed += '&url_entry=' + quote(url_entry)
            seed += '&url=' + quote(url)
            if title is not None:
                seed += '&title=' + quote(title)
            if publish_time is not None:
                seed += '&publish_time=' + quote(publish_time)

            md5.update(seed.encode('utf-8'))
            hkey = md5.hexdigest()
            item['hkey'] = hkey

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                table = config.fund_notice['db']['table']
                cursor.execute('SELECT TOP 1 hkey FROM ' + table + ' WHERE url=%s ORDER BY tmstamp', (url,))
                row = cursor.fetchone()
                if row is None:
                    cursor.execute(
                        'INSERT INTO ' + table + ' (hkey,groupname,sitename,channel,url_entry,url,title,publish_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                        (hkey, groupname, sitename, channel, url_entry, url, title, publish_time,))
                elif row['hkey'] != hkey:
                    cursor.execute(
                        'UPDATE ' + table + ' SET hkey=%s,groupname=%s,sitename=%s,channel=%s,title=%s,publish_time=%s,update_time=GETDATE() WHERE hkey=%s',
                        (hkey, groupname, sitename, channel, title, publish_time, row['hkey'],))
            finally:
                cursor.close()
                spider.dbPool.release(conn)
        except:
            spider.crawler.engine.close_spider(spider, 'pipeline error!')
            spider.crawler.stats.set_value('exit_emsg', traceback.format_exc())
            spider.crawler.stats.set_value('exit_emsg_item', item)
            spider.crawler.stats.set_value('exit_code', 1)
        finally:
            return item
