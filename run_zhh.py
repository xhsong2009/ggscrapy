from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'FundNav_HuoLiAsset', '-a', 'level=0', '-a', 'debug=1', '-a', 'jobId=0L'])
