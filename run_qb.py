from scrapy import cmdline


cmdline.execute(['scrapy', 'crawl', 'FundNav_CaiKaFeiFundSales', '-a', 'jobId=0L'])
# --192.168.0.139
# --select
# --select123
# --已配置python抓取的站点
# select distinct sitename,channel
# from funddb.dbo.t_nav_general
# where sitename = '德邦证券'
#
# --192.168.0.141
# --select
# --select123
# --核查私募数据库中是否有该产品
# select fund_id, fund_full_name, fund_name
# from SUNTIME_DB.dbo.t_pf_info
# where entry_class = 1 and entry_status = 3
#  and (fund_full_name like '%%'     --根据产品全称
#   or fund_name like '%%')              --根据产品简称


# TRS现有站点
# 192.168.0.139
# 库名：funddb
# 表名：urlcontent
# select top 100 sitename, channel from urlcontent group by sitename, channel order by sitename


# 入库数据
# --192.168.0.139 funddb urlcontent表
# select select123

# Department : 保障部
# Author : 钱斌
# Create_date : 2018-04-26