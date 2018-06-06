from scrapy import cmdline

#cmdline.execute(['scrapy', 'crawl', 'FundNav_AnXinStock', '-a', 'jobId=0L'])             # 安信证券
#cmdline.execute(['scrapy', 'crawl', 'FundNotice_DiyichuangyeQiHuo', '-a', 'jobId=0L'])   # 第一创业期货
#cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongLiangTrust', '-a', 'jobId=0L'])        # 中粮信托

#cmdline.execute(['scrapy', 'crawl', 'FundNav_ZunDaoAsset', '-a', 'jobId=0L'])        #尊道资产
#cmdline.execute(['scrapy', 'crawl', 'FundNav_YuanCeAsset', '-a', 'jobId=0L'])        #远策投资
#cmdline.execute(['scrapy', 'crawl', 'FundNotice_XiNanFuture', '-a', 'jobId=0L'])     #西南期货
#cmdline.execute(['scrapy', 'crawl', 'FundNotice_XiYuInvest', '-a', 'jobId=0L'])  #西域投资
cmdline.execute(['scrapy', 'crawl', 'FundNav_YuanXinYongFengFund', '-a', 'jobId=0L'])  #圆信永丰基金
