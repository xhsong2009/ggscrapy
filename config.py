SPIDER_MODULES = [
    'spiders',
    'FundNavSpiders',
    'FundNoticeSpiders',
]

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/66.0.3359.139 Safari/537.36',
}

proxies = [
    None,  # http://user:pass@addr:port
    None,
    None,
    None,
    None,
    None,
]

fund_nav = {
    'db': {
        'host': '192.168.0.53',
        'name': 'scrapy_debug_db',
        'port': 1433,
        'user': 'sql_scrapy',
        'pswd': 'sql_scrapy123',
        'table': 't_nav_general',
        'timeout': 60,
    },
}

fund_notice = {
    'db': {
        'host': '192.168.0.53',
        'name': 'scrapy_debug_db',
        'port': 1433,
        'user': 'sql_scrapy',
        'pswd': 'sql_scrapy123',
        'table': 't_fund_announcement',
        'timeout': 60,
    },
}
