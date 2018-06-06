import hashlib
import traceback
from decimal import Decimal
from datetime import datetime
from urllib.parse import quote
from scrapy import Item, Field
from scrapy import Request, FormRequest
from ggmssql.pool import Pool
from GGScrapy import GGSpider
from GGScrapy import MultiPartFormRequest
import config


# 基金净值Spider基类
class GGFundNavSpider(GGSpider):
    custom_settings = {
        'ITEM_PIPELINES': {'FundNavSpiders.GGFundNavPipeline': 300}
    }

    dbPool = Pool(config.fund_nav['db']['host'],
                  config.fund_nav['db']['port'],
                  config.fund_nav['db']['user'],
                  config.fund_nav['db']['pswd'],
                  config.fund_nav['db']['name'],
                  timeout=config.fund_nav['db']['timeout'])
    dbTable = config.fund_nav['db']['table']

    fps = []  # fund (list) pages
    ips = []  # item (list) pages

    def request_next(self):
        if not (self.ips or self.fps):
            if hasattr(self, 'gen_request') and callable(self.gen_request):
                request = self.gen_request()
                if isinstance(request, Request):
                    return request
        ps = self.ips or self.fps  # pages
        pf = self.parse_item if self.ips else self.parse_fund  # parse function
        if ps:
            pi = ps.pop(0)  # page info

            pg = pi['pg'] if 'pg' in pi else None
            ext = pi['ext'] if 'ext' in pi else {}

            url = pi['url'] if 'url' in pi else None
            req_url = url(pg) if callable(url) else url

            ref = pi['ref'] if 'ref' in pi else None
            req_ref = ref(pg) if callable(ref) else ref

            self.logger.info('Preparing Request <%s> %s', req_url, {'pg': pg, 'ext': ext})

            headers = pi['headers'] if 'headers' in pi else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = req_ref

            meta = {
                'pi': pi,
                'pg': pg, 'url': url, 'ref': ref, 'ext': ext,
                'headers': headers,
            }

            gg_reset_cookies = pi.get('gg_reset_cookies', None)
            if gg_reset_cookies is not None:
                meta['gg_reset_cookies'] = gg_reset_cookies

            dont_redirect = pi.get('dont_redirect', None)
            if dont_redirect is not None:
                meta['dont_redirect'] = dont_redirect

            dont_retry = pi.get('dont_retry', None)
            if dont_retry is not None:
                meta['dont_retry'] = dont_retry
            max_retry_times = pi.get('max_retry_times', None)
            if max_retry_times is not None:
                meta['max_retry_times'] = max_retry_times
            gg_retry_wait = pi.get('gg_retry_wait', None)
            if gg_retry_wait is not None:
                meta['gg_retry_wait'] = gg_retry_wait
            retry_http_codes = pi.get('retry_http_codes', None)
            if retry_http_codes is not None:
                meta['retry_http_codes'] = retry_http_codes

            handle_httpstatus_list = pi.get('handle_httpstatus_list', None)
            if handle_httpstatus_list is not None:
                meta['handle_httpstatus_list'] = handle_httpstatus_list
            handle_httpstatus_all = pi.get('handle_httpstatus_all', None)
            if handle_httpstatus_all is not None:
                meta['handle_httpstatus_all'] = handle_httpstatus_all

            mform = pi['mform'] if 'mform' in pi else None
            if mform is not None:
                formdata = {}
                for (k, v) in mform.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                meta['mform'] = mform
                return MultiPartFormRequest(url=req_url, dont_filter=True, callback=pf,
                                            method='POST', headers=headers, formdata=formdata,
                                            meta=meta)

            form = pi['form'] if 'form' in pi else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                meta['form'] = form
                return FormRequest(url=req_url, dont_filter=True, callback=pf,
                                   method='POST', headers=headers, formdata=formdata,
                                   meta=meta)

            body = pi['body'] if 'body' in pi else None
            body = body(pg) if callable(body) else body
            method = 'POST' if body else 'GET'
            meta['body'] = body
            return Request(req_url, dont_filter=True, callback=pf,
                           method=method, headers=headers, body=body,
                           meta=meta)

    def get_last_statistic_date(self, fund_name):
        last_statistic_date = datetime.min
        conn = self.dbPool.acquire()
        cursor = conn.cursor()
        try:
            table = self.dbTable
            cursor.execute(
                'SELECT TOP 1 statistic_date FROM ' + table
                + ' WHERE sitename=%s AND channel=%s AND fund_name=%s ORDER BY statistic_date DESC',
                (self.sitename, self.channel, fund_name))
            row = cursor.fetchone()
            last_statistic_date = row['statistic_date'] if row else last_statistic_date
        finally:
            cursor.close()
            self.dbPool.release(conn)
        return last_statistic_date

    def parse_fund(self, response):
        pass

    def parse_item(self, response):
        pass


# 基金净值Item
class GGFundNavItem(Item):
    hkey = Field()  # 哈希唯一

    groupname = Field()  # 分组名称
    sitename = Field()  # 站点名称
    channel = Field()  # 频道名称

    url = Field()  # 链接地址
    fund_name = Field()  # 基金名称
    statistic_date = Field()  # 统计日期
    fund_code = Field()  # 基金代码
    nav = Field()  # 单位净值(单位: 元)
    added_nav = Field()  # 累计净值(单位: 元)
    nav_2 = Field()  # 含业绩报酬的单位净值(单位: 元)
    added_nav_2 = Field()  # 含业绩报酬的累计单位净值(单位: 元)
    total_nav = Field()  # 总资产净值(单位: 元)
    share = Field()  # 资产份额(单位: 份)
    income_value_per_ten_thousand = Field()  # 每万份计划收益(单位: 元)
    d7_annualized_return = Field()  # 7日年化收益率(单位: %)
    d30_annualized_return = Field()  # 30日年化收益率(单位: %)
    annualized_return = Field()  # 预估收益率(单位: %)
    d7_floating_return = Field()  # 浮动七日收益率(单位: %)


# 基金净值Pipeline
class GGFundNavPipeline(object):
    def process_item(self, item, spider):
        try:
            sitename = item.get('sitename', getattr(spider, 'sitename', None))
            sitename = sitename.strip() if isinstance(sitename, str) else None
            sitename = None if sitename == '' else sitename
            assert sitename is not None

            channel = item.get('channel', getattr(spider, 'channel', None))
            channel = channel.strip() if isinstance(channel, str) else None
            channel = None if channel == '' else channel
            assert channel is not None

            statistic_date = item.get('statistic_date', None)
            assert isinstance(statistic_date, datetime)
            statistic_date = statistic_date.strftime('%Y-%m-%d')

            fund_name = item.get('fund_name', None)
            fund_name = fund_name.strip() if isinstance(fund_name, str) else None
            fund_name = None if fund_name == '' else fund_name
            assert fund_name is not None

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'SELECT TOP 1 hkey,fund_code,url,nav,added_nav,nav_2,added_nav_2,total_nav,share'
                    ',income_value_per_ten_thousand,d7_annualized_return,d30_annualized_return,annualized_return'
                    + ' FROM ' + spider.dbTable
                    + ' WHERE sitename=%s AND channel=%s AND statistic_date=%s AND fund_name=%s ORDER BY tmstamp',
                    (sitename, channel, statistic_date, fund_name,))
                row = cursor.fetchone() or {}

                groupname = item.get('groupname', getattr(spider, 'groupname', row.get('groupname', None)))
                groupname = groupname.strip() if isinstance(groupname, str) else None
                groupname = None if groupname == '' else groupname

                fund_code = item.get('fund_code', row.get('fund_code', None))
                fund_code = fund_code.strip() if isinstance(fund_code, str) else None
                fund_code = None if fund_code == '' else fund_code

                url = item.get('url', row.get('url', None))
                url = url.decode() if isinstance(url, bytes) else url
                url = url.strip() if isinstance(url, str) else None
                url = None if url == '' else url

                nav = item.get('nav', row.get('nav', None))
                nav = Decimal(nav) if isinstance(nav, int) else nav
                nav = Decimal(str(nav)) if isinstance(nav, float) else nav
                nav = nav.normalize() if isinstance(nav, Decimal) else nav
                assert nav is None or isinstance(nav, Decimal)

                added_nav = item.get('added_nav', row.get('added_nav', None))
                added_nav = Decimal(added_nav) if isinstance(added_nav, int) else added_nav
                added_nav = Decimal(str(added_nav)) if isinstance(added_nav, float) else added_nav
                added_nav = added_nav.normalize() if isinstance(added_nav, Decimal) else added_nav
                assert added_nav is None or isinstance(added_nav, Decimal)

                nav_2 = item.get('nav_2', row.get('nav_2', None))
                nav_2 = Decimal(nav_2) if isinstance(nav_2, int) else nav_2
                nav_2 = Decimal(str(nav_2)) if isinstance(nav_2, float) else nav_2
                nav_2 = nav_2.normalize() if isinstance(nav_2, Decimal) else nav_2
                assert nav_2 is None or isinstance(nav_2, Decimal)

                added_nav_2 = item.get('added_nav_2', row.get('added_nav_2', None))
                added_nav_2 = Decimal(added_nav_2) if isinstance(added_nav_2, int) else added_nav_2
                added_nav_2 = Decimal(str(added_nav_2)) if isinstance(added_nav_2, float) else added_nav_2
                added_nav_2 = added_nav_2.normalize() if isinstance(added_nav_2, Decimal) else added_nav_2
                assert added_nav_2 is None or isinstance(added_nav_2, Decimal)

                total_nav = item.get('total_nav', row.get('total_nav', None))
                total_nav = Decimal(total_nav) if isinstance(total_nav, int) else total_nav
                total_nav = Decimal(str(total_nav)) if isinstance(total_nav, float) else total_nav
                total_nav = total_nav.normalize() if isinstance(total_nav, Decimal) else total_nav
                assert total_nav is None or isinstance(total_nav, Decimal)

                share = item.get('share', row.get('share', None))
                share = Decimal(share) if isinstance(share, int) else share
                share = Decimal(str(share)) if isinstance(share, float) else share
                share = share.normalize() if isinstance(share, Decimal) else share
                assert share is None or isinstance(share, Decimal)

                income_value_per_ten_thousand = item.get('income_value_per_ten_thousand',
                                                         row.get('income_value_per_ten_thousand', None))
                income_value_per_ten_thousand = Decimal(income_value_per_ten_thousand) if isinstance(
                    income_value_per_ten_thousand, int) else income_value_per_ten_thousand
                income_value_per_ten_thousand = Decimal(str(income_value_per_ten_thousand)) if isinstance(
                    income_value_per_ten_thousand, float) else income_value_per_ten_thousand
                income_value_per_ten_thousand = income_value_per_ten_thousand.normalize() if isinstance(
                    income_value_per_ten_thousand, Decimal) else income_value_per_ten_thousand
                assert income_value_per_ten_thousand is None or isinstance(income_value_per_ten_thousand, Decimal)

                d7_annualized_return = item.get('d7_annualized_return', row.get('d7_annualized_return', None))
                d7_annualized_return = Decimal(d7_annualized_return) if isinstance(d7_annualized_return, int) \
                    else d7_annualized_return
                d7_annualized_return = Decimal(str(d7_annualized_return)) if isinstance(d7_annualized_return, float) \
                    else d7_annualized_return
                d7_annualized_return = d7_annualized_return.normalize() if isinstance(d7_annualized_return, Decimal) \
                    else d7_annualized_return
                assert d7_annualized_return is None or isinstance(d7_annualized_return, Decimal)

                d30_annualized_return = item.get('d30_annualized_return', row.get('d30_annualized_return', None))
                d30_annualized_return = Decimal(d30_annualized_return) if isinstance(d30_annualized_return, int) \
                    else d30_annualized_return
                d30_annualized_return = Decimal(str(d30_annualized_return)) if isinstance(d30_annualized_return, float) \
                    else d30_annualized_return
                d30_annualized_return = d30_annualized_return.normalize() if isinstance(d30_annualized_return, Decimal) \
                    else d30_annualized_return
                assert d30_annualized_return is None or isinstance(d30_annualized_return, Decimal)

                annualized_return = item.get('annualized_return', row.get('annualized_return', None))
                annualized_return = Decimal(annualized_return) if isinstance(annualized_return, int) \
                    else annualized_return
                annualized_return = Decimal(str(annualized_return)) if isinstance(annualized_return, float) \
                    else annualized_return
                annualized_return = annualized_return.normalize() if isinstance(annualized_return, Decimal) \
                    else annualized_return
                assert annualized_return is None or isinstance(annualized_return, Decimal)

                d7_floating_return = item.get('d7_floating_return', row.get('d7_floating_return', None))
                d7_floating_return = Decimal(d7_floating_return) if isinstance(d7_floating_return, int) \
                    else d7_floating_return
                d7_floating_return = Decimal(str(d7_floating_return)) if isinstance(d7_floating_return, float) \
                    else d7_floating_return
                d7_floating_return = d7_floating_return.normalize() if isinstance(d7_floating_return, Decimal) \
                    else d7_floating_return
                assert d7_floating_return is None or isinstance(d7_floating_return, Decimal)
            finally:
                cursor.close()
                spider.dbPool.release(conn)

            md5 = hashlib.md5()
            seed = 'sitename=' + quote(sitename)
            seed += '&channel=' + quote(channel)
            seed += '&statistic_date=' + quote(statistic_date)
            seed += '&fund_name=' + quote(fund_name)
            if fund_code is not None:
                seed += '&fund_code=' + quote(fund_code)
            if url is not None:
                seed += '&url=' + quote(url)
            if nav is not None:
                seed += '&nav=' + quote(str(nav))
            if added_nav is not None:
                seed += '&added_nav=' + quote(str(added_nav))
            if nav_2 is not None:
                seed += '&nav_2=' + quote(str(nav_2))
            if added_nav_2 is not None:
                seed += '&added_nav_2=' + quote(str(added_nav_2))
            if total_nav is not None:
                seed += '&total_nav=' + quote(str(total_nav))
            if share is not None:
                seed += '&share=' + quote(str(share))
            if income_value_per_ten_thousand is not None:
                seed += '&income_value_per_ten_thousand=' + quote(str(income_value_per_ten_thousand))
            if d7_annualized_return is not None:
                seed += '&d7_annualized_return=' + quote(str(d7_annualized_return))
            if d30_annualized_return is not None:
                seed += '&d30_annualized_return=' + quote(str(d30_annualized_return))
            if annualized_return is not None:
                seed += '&annualized_return=' + quote(str(annualized_return))
            if d7_floating_return is not None:
                seed += '&d7_floating_return=' + quote(str(d7_floating_return))
            md5.update(seed.encode('utf-8'))
            hkey = md5.hexdigest()
            item['hkey'] = hkey

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                if row == {}:
                    cursor.execute(
                        'INSERT INTO ' + spider.dbTable
                        + ' (hkey,groupname,sitename,channel,statistic_date,fund_name,fund_code,url,nav,added_nav,nav_2'
                          ',added_nav_2,total_nav,share,income_value_per_ten_thousand,d7_annualized_return,d30_annualized_return'
                          ',annualized_return,d7_floating_return)'
                        + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (hkey, groupname, sitename, channel, statistic_date, fund_name, fund_code, url, nav, added_nav,
                         nav_2, added_nav_2, total_nav, share, income_value_per_ten_thousand, d7_annualized_return,
                         d30_annualized_return, annualized_return, d7_floating_return))
                elif row['hkey'] != hkey:
                    cursor.execute(
                        'UPDATE ' + spider.dbTable
                        + ' SET hkey=%s,groupname=%s,fund_code=%s,url=%s,nav=%s,added_nav=%s,nav_2=%s,added_nav_2=%s'
                          ',total_nav=%s,share=%s,income_value_per_ten_thousand=%s,d7_annualized_return=%s'
                          ',d30_annualized_return=%s,annualized_return=%s,d7_floating_return=%s,update_time=GETDATE()'
                        + ' WHERE hkey=%s',
                        (hkey, groupname, fund_code, url, nav, added_nav, nav_2, added_nav_2, total_nav, share,
                         income_value_per_ten_thousand, d7_annualized_return, d30_annualized_return, annualized_return,
                         d7_floating_return, row['hkey'],))
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


# 基金(code)净值Pipeline
class GGFundCodeNavPipeline(object):
    def process_item(self, item, spider):
        try:
            sitename = item.get('sitename', getattr(spider, 'sitename', None))
            sitename = sitename.strip() if isinstance(sitename, str) else None
            sitename = None if sitename == '' else sitename
            assert sitename is not None

            channel = item.get('channel', getattr(spider, 'channel', None))
            channel = channel.strip() if isinstance(channel, str) else None
            channel = None if channel == '' else channel
            assert channel is not None

            statistic_date = item.get('statistic_date', None)
            assert isinstance(statistic_date, datetime)
            statistic_date = statistic_date.strftime('%Y-%m-%d')

            fund_code = item.get('fund_code', None)
            fund_code = fund_code.strip() if isinstance(fund_code, str) else None
            fund_code = None if fund_code == '' else fund_code
            assert fund_code is not None

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'SELECT TOP 1 hkey,fund_name,url,nav,added_nav,nav_2,added_nav_2,total_nav,share'
                    ',income_value_per_ten_thousand,d7_annualized_return,d30_annualized_return, annualized_return'
                    + ' FROM ' + spider.dbTable
                    + ' WHERE sitename=%s AND channel=%s AND statistic_date=%s AND fund_code=%s ORDER BY tmstamp',
                    (sitename, channel, statistic_date, fund_code,))
                row = cursor.fetchone() or {}

                groupname = item.get('groupname', getattr(spider, 'groupname', row.get('groupname', None)))
                groupname = groupname.strip() if isinstance(groupname, str) else None
                groupname = None if groupname == '' else groupname

                fund_name = item.get('fund_name', row.get('fund_name', None))
                fund_name = fund_name.strip() if isinstance(fund_name, str) else None
                fund_name = None if fund_name == '' else fund_name
                assert fund_name is not None

                url = item.get('url', row.get('url', None))
                url = url.decode() if isinstance(url, bytes) else url
                url = url.strip() if isinstance(url, str) else None
                url = None if url == '' else url

                nav = item.get('nav', row.get('nav', None))
                nav = Decimal(nav) if isinstance(nav, int) else nav
                nav = Decimal(str(nav)) if isinstance(nav, float) else nav
                nav = nav.normalize() if isinstance(nav, Decimal) else nav
                assert nav is None or isinstance(nav, Decimal)

                added_nav = item.get('added_nav', row.get('added_nav', None))
                added_nav = Decimal(added_nav) if isinstance(added_nav, int) else added_nav
                added_nav = Decimal(str(added_nav)) if isinstance(added_nav, float) else added_nav
                added_nav = added_nav.normalize() if isinstance(added_nav, Decimal) else added_nav
                assert added_nav is None or isinstance(added_nav, Decimal)

                nav_2 = item.get('nav_2', row.get('nav_2', None))
                nav_2 = Decimal(nav_2) if isinstance(nav_2, int) else nav_2
                nav_2 = Decimal(str(nav_2)) if isinstance(nav_2, float) else nav_2
                nav_2 = nav_2.normalize() if isinstance(nav_2, Decimal) else nav_2
                assert nav_2 is None or isinstance(nav_2, Decimal)

                added_nav_2 = item.get('added_nav_2', row.get('added_nav_2', None))
                added_nav_2 = Decimal(added_nav_2) if isinstance(added_nav_2, int) else added_nav_2
                added_nav_2 = Decimal(str(added_nav_2)) if isinstance(added_nav_2, float) else added_nav_2
                added_nav_2 = added_nav_2.normalize() if isinstance(added_nav_2, Decimal) else added_nav_2
                assert added_nav_2 is None or isinstance(added_nav_2, Decimal)

                total_nav = item.get('total_nav', row.get('total_nav', None))
                total_nav = Decimal(total_nav) if isinstance(total_nav, int) else total_nav
                total_nav = Decimal(str(total_nav)) if isinstance(total_nav, float) else total_nav
                total_nav = total_nav.normalize() if isinstance(total_nav, Decimal) else total_nav
                assert total_nav is None or isinstance(total_nav, Decimal)

                share = item.get('share', row.get('share', None))
                share = Decimal(share) if isinstance(share, int) else share
                share = Decimal(str(share)) if isinstance(share, float) else share
                share = share.normalize() if isinstance(share, Decimal) else share
                assert share is None or isinstance(share, Decimal)

                income_value_per_ten_thousand = item.get('income_value_per_ten_thousand',
                                                         row.get('income_value_per_ten_thousand', None))
                income_value_per_ten_thousand = Decimal(income_value_per_ten_thousand) if isinstance(
                    income_value_per_ten_thousand, int) else income_value_per_ten_thousand
                income_value_per_ten_thousand = Decimal(str(income_value_per_ten_thousand)) if isinstance(
                    income_value_per_ten_thousand, float) else income_value_per_ten_thousand
                income_value_per_ten_thousand = income_value_per_ten_thousand.normalize() if isinstance(
                    income_value_per_ten_thousand, Decimal) else income_value_per_ten_thousand
                assert income_value_per_ten_thousand is None or isinstance(income_value_per_ten_thousand, Decimal)

                d7_annualized_return = item.get('d7_annualized_return', row.get('d7_annualized_return', None))
                d7_annualized_return = Decimal(d7_annualized_return) if isinstance(d7_annualized_return, int) \
                    else d7_annualized_return
                d7_annualized_return = Decimal(str(d7_annualized_return)) if isinstance(d7_annualized_return, float) \
                    else d7_annualized_return
                d7_annualized_return = d7_annualized_return.normalize() if isinstance(d7_annualized_return, Decimal) \
                    else d7_annualized_return
                assert d7_annualized_return is None or isinstance(d7_annualized_return, Decimal)

                d30_annualized_return = item.get('d30_annualized_return', row.get('d30_annualized_return', None))
                d30_annualized_return = Decimal(d30_annualized_return) if isinstance(d30_annualized_return, int) \
                    else d30_annualized_return
                d30_annualized_return = Decimal(str(d30_annualized_return)) if isinstance(d30_annualized_return, float) \
                    else d30_annualized_return
                d30_annualized_return = d30_annualized_return.normalize() if isinstance(d30_annualized_return, Decimal) \
                    else d30_annualized_return
                assert d30_annualized_return is None or isinstance(d30_annualized_return, Decimal)

                annualized_return = item.get('annualized_return', row.get('annualized_return', None))
                annualized_return = Decimal(annualized_return) if isinstance(annualized_return, int) \
                    else annualized_return
                annualized_return = Decimal(str(annualized_return)) if isinstance(annualized_return, float) \
                    else annualized_return
                annualized_return = annualized_return.normalize() if isinstance(annualized_return, Decimal) \
                    else annualized_return
                assert annualized_return is None or isinstance(annualized_return, Decimal)

                d7_floating_return = item.get('d7_floating_return', row.get('d7_floating_return', None))
                d7_floating_return = Decimal(d7_floating_return) if isinstance(d7_floating_return, int) \
                    else d7_floating_return
                d7_floating_return = Decimal(str(d7_floating_return)) if isinstance(d7_floating_return, float) \
                    else d7_floating_return
                d7_floating_return = d7_floating_return.normalize() if isinstance(d7_floating_return, Decimal) \
                    else d7_floating_return
                assert d7_floating_return is None or isinstance(d7_floating_return, Decimal)
            finally:
                cursor.close()
                spider.dbPool.release(conn)

            md5 = hashlib.md5()
            seed = 'sitename=' + quote(sitename)
            seed += '&channel=' + quote(channel)
            seed += '&statistic_date=' + quote(statistic_date)
            seed += '&fund_code=' + quote(fund_code)
            seed += '&fund_name=' + quote(fund_name)
            if url is not None:
                seed += '&url=' + quote(url)
            if nav is not None:
                seed += '&nav=' + quote(str(nav))
            if added_nav is not None:
                seed += '&added_nav=' + quote(str(added_nav))
            if nav_2 is not None:
                seed += '&nav_2=' + quote(str(nav_2))
            if added_nav_2 is not None:
                seed += '&added_nav_2=' + quote(str(added_nav_2))
            if total_nav is not None:
                seed += '&total_nav=' + quote(str(total_nav))
            if share is not None:
                seed += '&share=' + quote(str(share))
            if income_value_per_ten_thousand is not None:
                seed += '&income_value_per_ten_thousand=' + quote(str(income_value_per_ten_thousand))
            if d7_annualized_return is not None:
                seed += '&d7_annualized_return=' + quote(str(d7_annualized_return))
            if d30_annualized_return is not None:
                seed += '&d30_annualized_return=' + quote(str(d30_annualized_return))
            if annualized_return is not None:
                seed += '&annualized_return=' + quote(str(annualized_return))
            if d7_floating_return is not None:
                seed += '&d7_floating_return=' + quote(str(d7_floating_return))
            md5.update(seed.encode('utf-8'))
            hkey = md5.hexdigest()
            item['hkey'] = hkey

            conn = spider.dbPool.acquire()
            cursor = conn.cursor()
            try:
                if row == {}:
                    cursor.execute(
                        'INSERT INTO ' + spider.dbTable
                        + ' (hkey,groupname,sitename,channel,statistic_date,fund_code,fund_name,url,nav,added_nav,nav_2'
                          ',added_nav_2,total_nav,share,income_value_per_ten_thousand,d7_annualized_return,d30_annualized_return'
                          ',annualized_return,d7_floating_return)'
                        + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (hkey, groupname, sitename, channel, statistic_date, fund_code, fund_name, url, nav, added_nav,
                         nav_2, added_nav_2, total_nav, share, income_value_per_ten_thousand, d7_annualized_return,
                         d30_annualized_return, annualized_return, d7_floating_return))
                elif row['hkey'] != hkey:
                    cursor.execute(
                        'UPDATE ' + spider.dbTable
                        + ' SET hkey=%s,groupname=%s,fund_name=%s,url=%s,nav=%s,added_nav=%s,nav_2=%s,added_nav_2=%s'
                          ',total_nav=%s,share=%s,income_value_per_ten_thousand=%s,d7_annualized_return=%s'
                          ',d30_annualized_return=%s,annualized_return=%s,d7_floating_return=%s,update_time=GETDATE()'
                        + ' WHERE hkey=%s',
                        (hkey, groupname, fund_name, url, nav, added_nav, nav_2, added_nav_2, total_nav, share,
                         income_value_per_ten_thousand, d7_annualized_return, d30_annualized_return, annualized_return,
                         d7_floating_return, row['hkey'],))
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
