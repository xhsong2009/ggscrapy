from scrapy import cmdline

# ---------------------------------------------------------------------------------------
# cmdline.execute(['scrapy', 'crawl', 'FundNav_HoldGoodAsset',              '-a', 'jobId=0L'])  # 杭州厚德载富财富
# cmdline.execute(['scrapy', 'crawl', 'FundNav_HaiTongAsset',               '-a', 'jobId=0L'])  # 海通资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_DongHaiSecurities',          '-a', 'jobId=0L'])  # 东海证券
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZczyInvest',                 '-a', 'jobId=0L'])  # 厦门致诚卓远投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_JiShengInvest',              '-a', 'jobId=0L'])  # 季胜投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_QiYaoInvest',                '-a', 'jobId=0L'])  # 上海七曜投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ChiQiFund',                  '-a', 'jobId=0L'])  # 赤祺资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_BeiJingHaiXinAssets',        '-a', 'jobId=0L'])  # 北京海鑫资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YiXinAnAsset',               '-a', 'jobId=0L'])  # 易鑫安资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_DaPuAsset',                  '-a', 'jobId=0L'])  # 大朴资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_XingJuAsset',                '-a', 'jobId=0L'])  # 兴聚投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_LuDengAssets',               '-a', 'jobId=0L'])  # 卢登资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ShangHaiSecurities',         '-a', 'jobId=0L'])  # 上海证券
# cmdline.execute(['scrapy', 'crawl', 'FundNav_TianMaAssets',               '-a', 'jobId=0L'])  # 天马资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_NewCenturyFutures',       '-a', 'jobId=0L'])  # 新世纪期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_DongWuSecurities',        '-a', 'jobId=0L'])  # 东吴证券
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_GuoTouTaiKangTrust',      '-a', 'jobId=0L'])  # 国投泰康信托
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_YinHeCapital',            '-a', 'jobId=0L'])  # 银河资本
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_WesternFuture',           '-a', 'jobId=0L'])  # 西部期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_WanJiAsset',              '-a', 'jobId=0L'])  # 万霁资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_YiDeFuture',              '-a', 'jobId=0L'])  # 一德期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_RongYiInvest',            '-a', 'jobId=0L'])  # 融义投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZhengQianFang',           '-a', 'jobId=0L'])  # 深圳正前方
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_NestInvest',              '-a', 'jobId=0L'])  # 纳斯特投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_HeChengAssets',           '-a', 'jobId=0L'])  # 合晟资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_GuanFuAssets',            '-a', 'jobId=0L'])  # 观富资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_InforeCapital',           '-a', 'jobId=0L'])  # 盈峰资本
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_WanKuiAssets',            '-a', 'jobId=0L'])  # 万葵资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_JingFuAssets',            '-a', 'jobId=0L'])  # 京福资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_JiaShiCapital',           '-a', 'jobId=0L'])  # 嘉实资本
# ------------------------------------------------------------------------------------------------------------------2018-04-02
# cmdline.execute(['scrapy', 'crawl', 'FundNav_LiangDaoAssets',             '-a', 'jobId=0L'])  # 量道投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_LiuHeCapital',               '-a', 'jobId=0L'])  # 六禾投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_LongTengAssets',             '-a', 'jobId=0L'])  # 龙腾资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YuanLanInfo',                '-a', 'jobId=0L'])  # 远澜信息
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_YongYingFund',            '-a', 'jobId=0L'])  # 永赢基金
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZGGuoJiFutures',          '-a', 'jobId=0L'])  # 中银国际期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_DingSaInvest',            '-a', 'jobId=0L'])  # 鼎萨投资
# ------------------------------------------------------------------------------------------------------------------2018-04-09
# cmdline.execute(['scrapy', 'crawl', 'FundNav_XiXianAssets',               '-a', 'jobId=0L'])  # 喜贤资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YingHuaInvest',              '-a', 'jobId=0L'])  # 赢华投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhengMiInvest',              '-a', 'jobId=0L'])  # 正幂投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongYanFutures',            '-a', 'jobId=0L'])  # 中衍期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_SZJingYingAgeFund',       '-a', 'jobId=0L'])  # 深圳菁英时代基金
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_SZZhiFangShiInvest',      '-a', 'jobId=0L'])  # 深圳知方石投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_YuanPuInvest',            '-a', 'jobId=0L'])  # 元普投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_XinHouInvest',            '-a', 'jobId=0L'])  # 鑫厚投资
# ------------------------------------------------------------------------------------------------------------------2018-04-16
# cmdline.execute(['scrapy', 'crawl', 'FundNav_PuErInvest',                 '-a', 'jobId=0L'])  # 普尔投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_WanYiAssets',                '-a', 'jobId=0L'])  # 万屹资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_XiNanFutures',               '-a', 'jobId=0L'])  # 西南期货
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhengLongAssets',            '-a', 'jobId=0L'])  # 正隆财富
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongLiangTrust',            '-a', 'jobId=0L'])  # 中粮信托
# cmdline.execute(['scrapy', 'crawl', 'FundNav_DingSaInvest',               '-a', 'jobId=0L'])  # 鼎萨投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_FuJianKuanKeInvest',         '-a', 'jobId=0L'])  # 福建宽客投资
# ------------------------------------------------------------------------------------------------------------------2018-04-23
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhengQianFang',              '-a', 'jobId=0L'])  # 正前方金融
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhengYanInvest',             '-a', 'jobId=0L'])  # 证研投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongHangSecurities',        '-a', 'jobId=0L'])  # 中航证券
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongHeGongYingAssets',      '-a', 'jobId=0L'])  # 中合共赢资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongTaiTrust',              '-a', 'jobId=0L'])  # 中泰信托
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongXinTrust',              '-a', 'jobId=0L'])  # 中信信托
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZJYiFangBoInvest',           '-a', 'jobId=0L'])  # 浙江亿方博投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZheShangSecurities',         '-a', 'jobId=0L'])  # 浙商证券(净值)
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZheShangSecurities',      '-a', 'jobId=0L'])  # 浙商证券(公告)
# ------------------------------------------------------------------------------------------------------------------2018-05-02
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YongWangAssets',             '-a', 'jobId=0L'])  # 永望资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YuJinFund',                  '-a', 'jobId=0L'])  # 裕晋投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YuanFengFund',               '-a', 'jobId=0L'])  # 源沣资本
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_GuoTaiJunAn',             '-a', 'jobId=0L'])  # 国泰君安
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_GZYinGuoDaCapital',       '-a', 'jobId=0L'])  # 广州银国达资产
# ------------------------------------------------------------------------------------------------------------------2018-05-07
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YiCunInvest',                '-a', 'jobId=0L'])  # 一村投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongGangFutures',           '-a', 'jobId=0L'])  # 中钢期货
# cmdline.execute(['scrapy', 'crawl', 'FundNav_XianTongInvest',             '-a', 'jobId=0L'])  # 仙童投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_RuiYuFund',               '-a', 'jobId=0L'])  # 上海睿豫投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_YiCunInvest',             '-a', 'jobId=0L'])  # 一村投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_JunZeLiCapital',          '-a', 'jobId=0L'])  # 深圳君泽利投资发展企业
# ------------------------------------------------------------------------------------------------------------------2018-05-14
# cmdline.execute(['scrapy', 'crawl', 'FundNav_YuanPuInvest',               '-a', 'jobId=0L'])  # 元普投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_TianHuaFund',                '-a', 'jobId=0L'])  # 杭州添华投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_HuiYuInvest',                '-a', 'jobId=0L'])  # 云南汇誉投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZhongYinGuoJi',           '-a', 'jobId=0L'])  # 中银国际资管
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ChangChengGuoRui',        '-a', 'jobId=0L'])  # 长城国瑞证券
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZhongYouSecurity',        '-a', 'jobId=0L'])  # 中邮证券公告
# ------------------------------------------------------------------------------------------------------------------2018-05-21
# cmdline.execute(['scrapy', 'crawl', 'FundNav_TianTianFund',               '-a', 'jobId=0L'])  # 天天基金
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_BeiJingFuRuiDeInvest',    '-a', 'jobId=0L'])  # 北京福睿德投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZhiChengZhuoYuan',        '-a', 'jobId=0L'])  # 厦门致诚卓远投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_GuanHeAsset',             '-a', 'jobId=0L'])  # 浙江观合资产公告
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZhaoShangSecurity',       '-a', 'jobId=0L'])  # 招商证券公告
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_YueCaiInvest',            '-a', 'jobId=0L'])  # 粤财信托公告
# ------------------------------------------------------------------------------------------------------------------2018-05-21
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_HaiXiShengQianInvest',    '-a', 'jobId=0L'])  # 福建海西晟乾投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ZhongJiuZeInvest',        '-a', 'jobId=0L'])  # 深圳前海中玖泽投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_HuaAnFuture',             '-a', 'jobId=0L'])  # 华安期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ShunShiGuoJi',            '-a', 'jobId=0L'])  # 顺时国际
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_WuXiZhiXinInvest',        '-a', 'jobId=0L'])  # 无锡智信投资
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_ShangHaiYiZhouAsset',     '-a', 'jobId=0L'])  # 上海亿舟资产
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_HeXiInvest',              '-a', 'jobId=0L'])  # 和熙投资
