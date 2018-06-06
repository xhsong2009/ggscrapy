# -*- coding: utf-8 -*-

# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-28


from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json


class HuaTaiSecuritySpider(GGFundNavSpider):
    name = 'FundNav_HuaTaiSecurity'
    sitename = '华泰证券'
    channel = '券商资管净值'
    allowed_domains = ['htamc.htsc.com.cn']

    ips = [
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941239&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B66.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '定增6号（风险级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941183&t=5&start=0&limits=1000&name=.C2.BB.C3.95.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE1.C3.86.C3.9A',
            'ext': '徽华1号A份额1期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941199&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B02.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940025&t=3&start=0&limits=1000&name=.C2.BD.C3.9A.C2.BC.C3.99.C3.88.C3.95.C3.80.C3.AD.C2.B2.C3.86',
            'ext': '节假日理财'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941160&t=5&start=0&limits=1000&name=.C2.BE.C2.A9.C2.BB.C2.AA1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '京华1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941434&t=4&start=0&limits=1000&name=.C3.84.C3.8F.C2.B3.C3.A41.C2.BA.C3.85A2',
            'ext': '南充1号A2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941109&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE3.C3.86.C3.9A',
            'ext': '浦华1号A份额3期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941412&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA3.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6A1',
            'ext': '浦华3号优先级A1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF8156&t=5&start=0&limits=1000&name=.C3.88.C3.BC.C3.81.C3.AC.C3.81.C3.AC.C2.BA.C2.BD1.C2.BA.C3.85',
            'ext': '赛领领航1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940008&t=5&start=0&limits=1000&name=.C3.8F.C3.96.C2.BD.C3.B0.C2.B9.C3.9C.C2.BC.C3.92',
            'ext': '现金管家'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941163&t=5&start=0&limits=1000&name=.C3.93.C2.AF.C3.8C.C2.A91.C2.BA.C3.85',
            'ext': '盈泰1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941219&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB4.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见4号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941251&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB5.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见5号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940344&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X16',
            'ext': '月月优先6月X16'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940321&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.97.C2.A8.C3.8F.C3.ADX1',
            'ext': '月月优先专享X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940083&t=4&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C2.B1.C2.A61.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '质押宝1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940042&t=5&start=0&limits=1000&name=.C2.B8.C3.9F.C3.8A.C3.95.C3.92.C3.A6.C3.95.C2.AE',
            'ext': '高收益债'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940210&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X10',
            'ext': '季季优先X10'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940213&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X13',
            'ext': '季季优先X13'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941430&t=5&start=0&limits=1000&name=.C2.BD.C2.A1.C3.90.C3.901.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '健行1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941113&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE7.C3.86.C3.9A',
            'ext': '浦华1号A份额7期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941107&t=5&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85B.C2.B7.C3.9D.C2.B6.C3.AE',
            'ext': '浦华1号B份额'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940085&t=5&start=0&limits=1000&name=.C3.8E.C3.88.C3.80.C3.BB1.C2.BA.C3.85',
            'ext': '稳利1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940013&t=5&start=0&limits=1000&name=.C3.90.C3.82.C3.90.C3.8B.C2.B2.C3.BA.C3.92.C2.B5',
            'ext': '新兴产业'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941220&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB4.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见4号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941254&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB6.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见6号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940332&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X3',
            'ext': '月月优先1月X3'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940312&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX12',
            'ext': '月月优先半年X12'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940319&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX19',
            'ext': '月月优先半年X19'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941156&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE1.C3.86.C3.9A',
            'ext': '质押易1号A份额1期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941158&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE3.C3.86.C3.9A',
            'ext': '质押易1号A份额3期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940053&t=5&start=0&limits=1000&name=.C2.B0.C3.AB.C3.84.C3.AA.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '半年发（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941152&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF0585&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE2.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢2号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941235&t=5&start=0&limits=1000&name=.C2.BB.C3.9B.C3.94.C3.B31.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '慧泽1号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941234&t=5&start=0&limits=1000&name=.C2.BB.C3.9B.C3.94.C3.B31.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '慧泽1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940030&t=5&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '季季发（风险级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941232&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B010.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园10号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941190&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B01.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941199&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B02.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S75566&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B03.C2.BA.C3.85',
            'ext': '家园3号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940004&t=5&start=0&limits=1000&name=.C2.B2.C2.BD.C2.B2.C2.BD.C3.8E.C2.AA.C3.93.C2.AF',
            'ext': '步步为盈'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941184&t=5&start=0&limits=1000&name=.C2.BB.C3.95.C2.BB.C2.AA1.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6A2',
            'ext': '徽华1号优先级A2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940029&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '季季发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941211&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A67.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力7号（中间级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941115&t=5&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE9.C3.86.C3.9A',
            'ext': '浦华1号A份额9期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941280&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A91.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941256&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB7.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见7号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940181&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X8',
            'ext': '月月优先1月X8'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940341&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X13',
            'ext': '月月优先6月X13'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940252&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX7',
            'ext': '月月优先新享X7'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940305&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.885.C2.BA.C3.85',
            'ext': '增强债券优先5号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940048&t=5&start=0&limits=1000&name=.C2.B2.C3.86.C2.B8.C2.BB2.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '财富2号（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940209&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X9',
            'ext': '季季优先X9'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941206&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力2号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941411&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA3.C2.BA.C3.85.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6B',
            'ext': '浦华3号风险级B'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941162&t=5&start=0&limits=1000&name=.C3.88.C3.99.C3.8C.C2.A91.C2.BA.C3.85',
            'ext': '荣泰1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941219&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB4.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见4号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941253&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB6.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见6号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940281&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.883.C3.94.C3.82X1',
            'ext': '月月优先3月X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940263&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.884.C3.94.C3.82X3',
            'ext': '月月优先4月X3'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940311&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX11',
            'ext': '月月优先半年X11'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940255&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX10',
            'ext': '月月优先新享X10'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941258&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.BF.C3.86.C2.BD.C3.B0.C2.B2.C3.861.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中科金财1号（中间级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941173&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.856.C2.B8.C3.B6.C3.94.C3.821.C3.86.C3.9A',
            'ext': '中银1号6个月1期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941152&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941182&t=5&start=0&limits=1000&name=.C2.BB.C3.95.C2.BB.C2.AA1.C2.BA.C3.85B.C2.B7.C3.9D.C2.B6.C3.AE',
            'ext': '徽华1号B份额'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940201&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X1',
            'ext': '季季优先X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941431&t=5&start=0&limits=1000&name=.C2.BD.C2.A1.C3.90.C3.901.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '健行1号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941241&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A614.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力14号（中间级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941205&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力2号（中间级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941205&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力2号（中间级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941111&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE5.C3.86.C3.9A',
            'ext': '浦华1号A份额5期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940028&t=1&start=0&limits=1000&name=.C3.8C.C3.AC.C3.8C.C3.AC.C2.B7.C2.A2B',
            'ext': '天天发B'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940038&t=1&start=0&limits=1000&name=.C3.8C.C3.AC.C3.8C.C3.AC.C2.B7.C2.A2C',
            'ext': '天天发C'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940087&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.88.C3.9A.C2.B1.C2.A6C.C2.BC.C2.B6',
            'ext': '投融宝C级'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940253&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX8',
            'ext': '月月优先新享X8'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941226&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B08.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园8号（次级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941161&t=5&start=0&limits=1000&name=.C2.BE.C2.A9.C2.BB.C2.AA1.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '京华1号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941241&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A614.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力14号（中间级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941203&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A63.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力3号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941432&t=5&start=0&limits=1000&name=.C3.84.C3.8F.C2.B3.C3.A41.C2.BA.C3.85B',
            'ext': '南充1号B'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941413&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA3.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6A2',
            'ext': '浦华3号优先级A2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941281&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A91.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰1号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941506&t=5&start=0&limits=1000&name=.C3.88.C3.B0.C3.93.C2.AF1.C2.BA.C3.85A',
            'ext': '瑞盈1号A'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940007&t=5&start=0&limits=1000&name=.C3.93.C3.85.C3.95.C2.AE.C2.BE.C2.AB.C3.91.C2.A1',
            'ext': '优债精选'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940180&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X7',
            'ext': '月月优先1月X7'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940282&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.883.C3.94.C3.82X2',
            'ext': '月月优先3月X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940310&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX10',
            'ext': '月月优先半年X10'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940318&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX18',
            'ext': '月月优先半年X18'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940306&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.886.C2.BA.C3.85',
            'ext': '增强债券优先6号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941179&t=5&start=0&limits=1000&name=.C3.96.C3.87.C2.B7.C3.89.C3.89.C3.BA.C3.8E.C3.AF1.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '智飞生物1号（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940054&t=5&start=0&limits=1000&name=.C3.92.C3.97.C3.88.C3.9A.C2.B1.C2.A61.C2.BA.C3.85',
            'ext': '易融宝1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940033&t=5&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '月月发（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940246&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX1',
            'ext': '月月优先新享X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940256&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX11',
            'ext': '月月优先新享X11'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940248&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX3',
            'ext': '月月优先新享X3'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940249&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX4',
            'ext': '月月优先新享X4'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941259&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.BF.C3.86.C2.BD.C3.B0.C2.B2.C3.861.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中科金财1号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941239&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B66.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '定增6号（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940099&t=4&start=0&limits=1000&name=.C2.B7.C3.A1.C3.8C.C2.A9.C2.B4.C3.B3.C2.B7.C3.A1A1',
            'ext': '丰泰大丰A1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940210&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X10',
            'ext': '季季优先X10'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941191&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B01.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园1号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941161&t=5&start=0&limits=1000&name=.C2.BE.C2.A9.C2.BB.C2.AA1.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '京华1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941204&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941164&t=5&start=0&limits=1000&name=.C3.8A.C2.A2.C3.8C.C2.A91.C2.BA.C3.85',
            'ext': '盛泰1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF5284&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.94.C3.B61.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '投增1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940013&t=5&start=0&limits=1000&name=.C3.90.C3.82.C3.90.C3.8B.C2.B2.C3.BA.C3.92.C2.B5',
            'ext': '新兴产业'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941251&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB5.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见5号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940341&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X13',
            'ext': '月月优先6月X13'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940315&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX15',
            'ext': '月月优先半年X15'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940256&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX11',
            'ext': '月月优先新享X11'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941325&t=4&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85X21',
            'ext': '尊享1号X21'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941326&t=4&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85X22',
            'ext': '尊享1号X22'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940053&t=5&start=0&limits=1000&name=.C2.B0.C3.AB.C3.84.C3.AA.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '半年发（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941224&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B07.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园7号（次级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941215&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A68.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力8号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941110&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE4.C3.86.C3.9A',
            'ext': '浦华1号A份额4期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941283&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A92.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰2号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940087&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.88.C3.9A.C2.B1.C2.A6C.C2.BC.C2.B6',
            'ext': '投融宝C级'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941248&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB15.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见15号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941178&t=5&start=0&limits=1000&name=.C3.96.C3.87.C2.B7.C3.89.C3.89.C3.BA.C3.8E.C3.AF1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '智飞生物1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941172&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中银1号（风险级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940057&t=5&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '尊享季季发（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S78688&t=5&start=0&limits=1000&name=.C2.B2.C2.A2.C2.B9.C2.BA.C2.BB.C3.B9.C2.BD.C3.B01.C2.BA.C3.85',
            'ext': '并购基金1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940048&t=5&start=0&limits=1000&name=.C2.B2.C3.86.C2.B8.C2.BB2.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '财富2号（风险级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941245&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B6.C2.B9.C2.B2.C2.BD.C3.B81.C2.BA.C3.85',
            'ext': '定增共进1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941153&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE1.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢1号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941200&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B02.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园2号（次级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941223&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B07.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6',
            'ext': '家园7号优先级'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941160&t=5&start=0&limits=1000&name=.C2.BE.C2.A9.C2.BB.C2.AA1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '京华1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941246&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A616.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力16号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941212&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A67.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力7号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941213&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A68.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力8号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941433&t=4&start=0&limits=1000&name=.C3.84.C3.8F.C2.B3.C3.A41.C2.BA.C3.85A1',
            'ext': '南充1号A1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S78988&t=5&start=0&limits=1000&name=.C2.B2.C2.A2.C2.B9.C2.BA.C2.BB.C3.B9.C2.BD.C3.B02.C2.BA.C3.85',
            'ext': '并购基金2号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF0585&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE2.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢2号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940213&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X13',
            'ext': '季季优先X13'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940207&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X7',
            'ext': '季季优先X7'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S75566&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B03.C2.BA.C3.85',
            'ext': '家园3号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941203&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A63.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力3号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941411&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA3.C2.BA.C3.85.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6B',
            'ext': '浦华3号风险级B'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941283&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A92.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰2号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941164&t=5&start=0&limits=1000&name=.C3.8A.C2.A2.C3.8C.C2.A91.C2.BA.C3.85',
            'ext': '盛泰1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940041&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.88.C3.9A.C2.B1.C2.A6B.C2.BC.C2.B6',
            'ext': '投融宝B级'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941400&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.88.C3.9A.C3.94.C3.B6.C3.80.C3.BB1.C2.BA.C3.85',
            'ext': '投融增利1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF5284&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.94.C3.B61.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '投增1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940056&t=4&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '尊享季季发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940052&t=4&start=0&limits=1000&name=.C2.B0.C3.AB.C3.84.C3.AA.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '半年发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940027&t=5&start=0&limits=1000&name=.C2.B1.C3.9C.C3.8F.C3.95',
            'ext': '避险'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940019&t=2&start=0&limits=1000&name=.C2.B6.C2.A8.C2.B4.C3.A6.C2.B1.C2.A6',
            'ext': '定存宝'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S76682&t=5&start=0&limits=1000&name=.C2.BB.C2.AA.C3.93.C2.AF1.C2.BA.C3.85',
            'ext': '华盈1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940211&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X11',
            'ext': '季季优先X11'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940208&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X8',
            'ext': '季季优先X8'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SG1665&t=5&start=0&limits=1000&name=.C2.BE.C2.AD.C3.8E.C2.B34.C3.86.C3.9A',
            'ext': '经纬4期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941211&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A67.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力7号（中间级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941213&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A68.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力8号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940085&t=5&start=0&limits=1000&name=.C3.8E.C3.88.C3.80.C3.BB1.C2.BA.C3.85',
            'ext': '稳利1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941194&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941220&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB4.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见4号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941198&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B63.C2.BA.C3.85',
            'ext': '定增3号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940212&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X12',
            'ext': '季季优先X12'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940205&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X5',
            'ext': '季季优先X5'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940205&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X5',
            'ext': '季季优先X5'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941224&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B07.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园7号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940025&t=3&start=0&limits=1000&name=.C2.BD.C3.9A.C2.BC.C3.99.C3.88.C3.95.C3.80.C3.AD.C2.B2.C3.86',
            'ext': '节假日理财'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941204&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941201&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A63.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力3号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941201&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A63.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力3号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941214&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A68.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力8号（中间级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941111&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE5.C3.86.C3.9A',
            'ext': '浦华1号A份额5期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940052&t=4&start=0&limits=1000&name=.C2.B0.C3.AB.C3.84.C3.AA.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '半年发（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940047&t=4&start=0&limits=1000&name=.C2.B2.C3.86.C2.B8.C2.BB2.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '财富2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940101&t=5&start=0&limits=1000&name=.C2.B7.C3.A1.C3.8C.C2.A9.C2.B4.C3.B3.C2.B7.C3.A1B',
            'ext': '丰泰大丰B'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940067&t=5&start=0&limits=1000&name=.C2.BA.C3.AA.C2.B9.C3.9B.C2.BB.C3.98.C2.B1.C2.A81.C2.BA.C3.85.C2.A3.C2.A8.C3.86.C3.95.C3.8D.C2.A8.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '宏观回报1号（普通级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940214&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X14',
            'ext': '季季优先X14'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941225&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B08.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园8号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940126&t=5&start=0&limits=1000&name=.C2.BD.C2.A1.C2.BF.C2.B5.C3.96.C3.90.C2.B9.C3.BA',
            'ext': '健康中国'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941212&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A67.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力7号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941210&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A67.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力7号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941434&t=4&start=0&limits=1000&name=.C3.84.C3.8F.C2.B3.C3.A41.C2.BA.C3.85A2',
            'ext': '南充1号A2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941285&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A93.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰3号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941412&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA3.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6A1',
            'ext': '浦华3号优先级A1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941282&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A92.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰2号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940018&t=1&start=0&limits=1000&name=.C3.8C.C3.AC.C3.8C.C3.AC.C2.B7.C2.A2A',
            'ext': '天天发A'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940232&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X2',
            'ext': '月月优先1月X2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940181&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X8',
            'ext': '月月优先1月X8'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940314&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX14',
            'ext': '月月优先半年X14'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940246&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX1',
            'ext': '月月优先新享X1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940251&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX6',
            'ext': '月月优先新享X6'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940300&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AFC.C2.BC.C2.B6',
            'ext': '增强债券C级'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941257&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.BF.C3.86.C2.BD.C3.B0.C2.B2.C3.861.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中科金财1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941258&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.BF.C3.86.C2.BD.C3.B0.C2.B2.C3.861.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中科金财1号（中间级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940097&t=4&start=0&limits=1000&name=.C3.92.C3.97.C3.88.C3.9A.C2.B1.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '易融宝2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941243&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB2.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见2号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940342&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X14',
            'ext': '月月优先6月X14'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940316&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX16',
            'ext': '月月优先半年X16'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941500&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.B5.C3.8D.C3.86.C3.80.C2.BC.C2.B6.C3.95.C2.AE1.C2.BA.C3.85',
            'ext': '中低评级债1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941171&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中银1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940039&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.96.C2.A4800.C3.94.C3.B6.C3.87.C2.BF',
            'ext': '中证800增强'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941300&t=2&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85Z',
            'ext': '尊享1号Z'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941255&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB7.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见7号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940261&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.884.C3.94.C3.82X1',
            'ext': '月月优先4月X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940310&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX10',
            'ext': '月月优先半年X10'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940247&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX2',
            'ext': '月月优先新享X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940249&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX4',
            'ext': '月月优先新享X4'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940325&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.97.C2.A8.C3.8F.C3.ADX5',
            'ext': '月月优先专享X5'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941169&t=5&start=0&limits=1000&name=.C3.AE.C2.A3.C3.8C.C2.A9.C2.A1.C2.A4.C2.B2.C3.86.C2.B8.C2.BBFOF2.C2.BA.C3.85',
            'ext': '睿泰·财富FOF2号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941248&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB15.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见15号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941243&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB2.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941195&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB3.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见3号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941196&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB3.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见3号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940261&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.884.C3.94.C3.82X1',
            'ext': '月月优先4月X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940343&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X15',
            'ext': '月月优先6月X15'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940311&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX11',
            'ext': '月月优先半年X11'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940321&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.97.C2.A8.C3.8F.C3.ADX1',
            'ext': '月月优先专享X1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941156&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE1.C3.86.C3.9A',
            'ext': '质押易1号A份额1期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941172&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中银1号（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941165&t=5&start=0&limits=1000&name=.C3.88.C2.AB.C3.87.C3.B2.C3.95.C2.AE.C3.88.C2.A8.C2.BB.C3.BA.C2.BB.C3.A11.C2.BA.C3.85',
            'ext': '全球债权机会1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940041&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.88.C3.9A.C2.B1.C2.A6B.C2.BC.C2.B6',
            'ext': '投融宝B级'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940032&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '月月发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940132&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X1',
            'ext': '月月优先1月X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940232&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X2',
            'ext': '月月优先1月X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940344&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X16',
            'ext': '月月优先6月X16'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940315&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX15',
            'ext': '月月优先半年X15'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941174&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.8512.C2.B8.C3.B6.C3.94.C3.822.C3.86.C3.9A',
            'ext': '中银1号12个月2期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940012&t=5&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B0.C3.81.C3.BA.C2.A3.C2.A8QDII.C2.A3.C2.A9',
            'ext': '紫金龙（QDII）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941326&t=4&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85X22',
            'ext': '尊享1号X22'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940003&t=5&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B03.C2.BA.C3.85',
            'ext': '紫金3号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940002&t=5&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B02.C2.BA.C3.85',
            'ext': '紫金2号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940057&t=5&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '尊享季季发（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941245&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B6.C2.B9.C2.B2.C2.BD.C3.B81.C2.BA.C3.85',
            'ext': '定增共进1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940208&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X8',
            'ext': '季季优先X8'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941226&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B08.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园8号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SG1665&t=5&start=0&limits=1000&name=.C2.BE.C2.AD.C3.8E.C2.B34.C3.86.C3.9A',
            'ext': '经纬4期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941432&t=5&start=0&limits=1000&name=.C3.84.C3.8F.C2.B3.C3.A41.C2.BA.C3.85B',
            'ext': '南充1号B'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941108&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE2.C3.86.C3.9A',
            'ext': '浦华1号A份额2期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941110&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE4.C3.86.C3.9A',
            'ext': '浦华1号A份额4期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941115&t=5&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE9.C3.86.C3.9A',
            'ext': '浦华1号A份额9期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941282&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A92.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941507&t=5&start=0&limits=1000&name=.C3.88.C3.B0.C3.93.C2.AF1.C2.BA.C3.85B',
            'ext': '瑞盈1号B'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940018&t=1&start=0&limits=1000&name=.C3.8C.C3.AC.C3.8C.C3.AC.C2.B7.C2.A2A',
            'ext': '天天发A'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940038&t=1&start=0&limits=1000&name=.C3.8C.C3.AC.C3.8C.C3.AC.C2.B7.C2.A2C',
            'ext': '天天发C'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940066&t=4&start=0&limits=1000&name=.C2.BA.C3.AA.C2.B9.C3.9B.C2.BB.C3.98.C2.B1.C2.A81.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '宏观回报1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940202&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X2',
            'ext': '季季优先X2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941225&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B08.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园8号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941240&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A614.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力14号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941106&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE1.C3.86.C3.9A',
            'ext': '浦华1号A份额1期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941113&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE7.C3.86.C3.9A',
            'ext': '浦华1号A份额7期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF5283&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.94.C3.B61.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '投增1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940098&t=5&start=0&limits=1000&name=.C3.92.C3.97.C3.88.C3.9A.C2.B1.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '易融宝2号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940098&t=5&start=0&limits=1000&name=.C3.92.C3.97.C3.88.C3.9A.C2.B1.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '易融宝2号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941163&t=5&start=0&limits=1000&name=.C3.93.C2.AF.C3.8C.C2.A91.C2.BA.C3.85',
            'ext': '盈泰1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940132&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X1',
            'ext': '月月优先1月X1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941195&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB3.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见3号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941252&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB5.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见5号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940032&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '月月发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940335&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.883.C3.94.C3.82X10',
            'ext': '月月优先3月X10'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940255&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX10',
            'ext': '月月优先新享X10'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940248&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX3',
            'ext': '月月优先新享X3'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940301&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.881.C2.BA.C3.85',
            'ext': '增强债券优先1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940058&t=6&start=0&limits=1000&name=.C3.97.C3.8A.C3.88.C2.AF.C3.8D.C2.A8.C2.B7.C3.96.C2.BC.C2.B6A',
            'ext': '资券通分级A'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941019&t=2&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B01.C2.BA.C3.85B.C2.BC.C2.B6',
            'ext': '紫金1号B级'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940250&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX5',
            'ext': '月月优先新享X5'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940006&t=5&start=0&limits=1000&name=.C3.94.C3.AC.C2.B8.C2.A3.C3.89.C2.A3.C3.A8.C3.B7',
            'ext': '造福桑梓'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941157&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE2.C3.86.C3.9A',
            'ext': '质押易1号A份额2期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941158&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE3.C3.86.C3.9A',
            'ext': '质押易1号A份额3期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941155&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85B.C2.B7.C3.9D.C2.B6.C3.AE',
            'ext': '质押易1号B份额'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941259&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.BF.C3.86.C2.BD.C3.B0.C2.B2.C3.861.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中科金财1号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940039&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.96.C2.A4800.C3.94.C3.B6.C3.87.C2.BF',
            'ext': '中证800增强'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF0581&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE2.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941182&t=5&start=0&limits=1000&name=.C2.BB.C3.95.C2.BB.C2.AA1.C2.BA.C3.85B.C2.B7.C3.9D.C2.B6.C3.AE',
            'ext': '徽华1号B份额'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940207&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X7',
            'ext': '季季优先X7'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941200&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B02.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园2号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940005&t=5&start=0&limits=1000&name=.C2.BD.C3.B5.C3.89.C3.8F.C3.8C.C3.AD.C2.BB.C2.A8',
            'ext': '锦上添花'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941114&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE8.C3.86.C3.9A',
            'ext': '浦华1号A份额8期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941244&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB2.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见2号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940335&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.883.C3.94.C3.82X10',
            'ext': '月月优先3月X10'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940262&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.884.C3.94.C3.82X2',
            'ext': '月月优先4月X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940345&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X17',
            'ext': '月月优先6月X17'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940312&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX12',
            'ext': '月月优先半年X12'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940251&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX6',
            'ext': '月月优先新享X6'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940308&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.888.C2.BA.C3.85',
            'ext': '增强债券优先8号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941179&t=5&start=0&limits=1000&name=.C3.96.C3.87.C2.B7.C3.89.C3.89.C3.BA.C3.8E.C3.AF1.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '智飞生物1号（风险级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940011&t=5&start=0&limits=1000&name=.C3.96.C3.9C.C3.86.C3.9A.C3.82.C3.96.C2.B6.C2.AF',
            'ext': '周期轮动'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF5968&t=5&start=0&limits=1000&name=.C2.BB.C2.AA.C3.94.C3.B61.C2.BA.C3.85',
            'ext': '华增1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941183&t=5&start=0&limits=1000&name=.C2.BB.C3.95.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE1.C3.86.C3.9A',
            'ext': '徽华1号A份额1期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941235&t=5&start=0&limits=1000&name=.C2.BB.C3.9B.C3.94.C3.B31.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '慧泽1号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940201&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X1',
            'ext': '季季优先X1'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941233&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B010.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园10号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941114&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE8.C3.86.C3.9A',
            'ext': '浦华1号A份额8期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941284&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A93.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰3号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941169&t=5&start=0&limits=1000&name=.C3.AE.C2.A3.C3.8C.C2.A9.C2.A1.C2.A4.C2.B2.C3.86.C2.B8.C2.BBFOF2.C2.BA.C3.85',
            'ext': '睿泰·财富FOF2号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940008&t=5&start=0&limits=1000&name=.C3.8F.C3.96.C2.BD.C3.B0.C2.B9.C3.9C.C2.BC.C3.92',
            'ext': '现金管家'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941194&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941254&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB6.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见6号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S78688&t=5&start=0&limits=1000&name=.C2.B2.C2.A2.C2.B9.C2.BA.C2.BB.C3.B9.C2.BD.C3.B01.C2.BA.C3.85',
            'ext': '并购基金1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940047&t=4&start=0&limits=1000&name=.C2.B2.C3.86.C2.B8.C2.BB2.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '财富2号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S76682&t=5&start=0&limits=1000&name=.C2.BB.C2.AA.C3.93.C2.AF1.C2.BA.C3.85',
            'ext': '华盈1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF5968&t=5&start=0&limits=1000&name=.C2.BB.C2.AA.C3.94.C3.B61.C2.BA.C3.85',
            'ext': '华增1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940209&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X9',
            'ext': '季季优先X9'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941112&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE6.C3.86.C3.9A',
            'ext': '浦华1号A份额6期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941107&t=5&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85B.C2.B7.C3.9D.C2.B6.C3.AE',
            'ext': '浦华1号B份额'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941413&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA3.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6A2',
            'ext': '浦华3号优先级A2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941284&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A93.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰3号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941162&t=5&start=0&limits=1000&name=.C3.88.C3.99.C3.8C.C2.A91.C2.BA.C3.85',
            'ext': '荣泰1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941506&t=5&start=0&limits=1000&name=.C3.88.C3.B0.C3.93.C2.AF1.C2.BA.C3.85A',
            'ext': '瑞盈1号A'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941507&t=5&start=0&limits=1000&name=.C3.88.C3.B0.C3.93.C2.AF1.C2.BA.C3.85B',
            'ext': '瑞盈1号B'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940247&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX2',
            'ext': '月月优先新享X2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941171&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中银1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940058&t=6&start=0&limits=1000&name=.C3.97.C3.8A.C3.88.C2.AF.C3.8D.C2.A8.C2.B7.C3.96.C2.BC.C2.B6A',
            'ext': '资券通分级A'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940002&t=5&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B02.C2.BA.C3.85',
            'ext': '紫金2号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940037&t=2&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B0.C2.BB.C3.B5.C2.B1.C3.92.C3.94.C3.B6.C3.87.C2.BF',
            'ext': '紫金货币增强'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940056&t=4&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '尊享季季发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S78988&t=5&start=0&limits=1000&name=.C2.B2.C2.A2.C2.B9.C2.BA.C2.BB.C3.B9.C2.BD.C3.B02.C2.BA.C3.85',
            'ext': '并购基金2号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941238&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B66.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '定增6号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940214&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X14',
            'ext': '季季优先X14'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941206&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力2号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941215&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A68.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力8号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941280&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A91.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940097&t=4&start=0&limits=1000&name=.C3.92.C3.97.C3.88.C3.9A.C2.B1.C2.A62.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '易融宝2号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940007&t=5&start=0&limits=1000&name=.C3.93.C3.85.C3.95.C2.AE.C2.BE.C2.AB.C3.91.C2.A1',
            'ext': '优债精选'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940318&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX18',
            'ext': '月月优先半年X18'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940325&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.97.C2.A8.C3.8F.C3.ADX5',
            'ext': '月月优先专享X5'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940302&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.882.C2.BA.C3.85',
            'ext': '增强债券优先2号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF8156&t=5&start=0&limits=1000&name=.C3.88.C3.BC.C3.81.C3.AC.C3.81.C3.AC.C2.BA.C2.BD1.C2.BA.C3.85',
            'ext': '赛领领航1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941176&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB11.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见11号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941253&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB6.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见6号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940281&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.883.C3.94.C3.82X1',
            'ext': '月月优先3月X1'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940282&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.883.C3.94.C3.82X2',
            'ext': '月月优先3月X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940346&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X18',
            'ext': '月月优先6月X18'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940254&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX9',
            'ext': '月月优先新享X9'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940254&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX9',
            'ext': '月月优先新享X9'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940300&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AFC.C2.BC.C2.B6',
            'ext': '增强债券C级'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940084&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C2.B1.C2.A61.C2.BA.C3.85.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '质押宝1号（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941178&t=5&start=0&limits=1000&name=.C3.96.C3.87.C2.B7.C3.89.C3.89.C3.BA.C3.8E.C3.AF1.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '智飞生物1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940304&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.884.C2.BA.C3.85',
            'ext': '增强债券优先4号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941257&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.BF.C3.86.C2.BD.C3.B0.C2.B2.C3.861.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '中科金财1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940011&t=5&start=0&limits=1000&name=.C3.96.C3.9C.C3.86.C3.9A.C3.82.C3.96.C2.B6.C2.AF',
            'ext': '周期轮动'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940059&t=7&start=0&limits=1000&name=.C3.97.C3.8A.C3.88.C2.AF.C3.8D.C2.A8.C2.B7.C3.96.C2.BC.C2.B6B',
            'ext': '资券通分级B'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940037&t=2&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B0.C2.BB.C3.B5.C2.B1.C3.92.C3.94.C3.B6.C3.87.C2.BFA',
            'ext': '紫金货币增强A'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940003&t=5&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B03.C2.BA.C3.85',
            'ext': '紫金3号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941300&t=2&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85Z',
            'ext': '尊享1号Z'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940019&t=2&start=0&limits=1000&name=.C2.B6.C2.A8.C2.B4.C3.A6.C2.B1.C2.A6',
            'ext': '定存宝'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940067&t=5&start=0&limits=1000&name=.C2.BA.C3.AA.C2.B9.C3.9B.C2.BB.C3.98.C2.B1.C2.A81.C2.BA.C3.85.C2.A3.C2.A8.C3.86.C3.95.C3.8D.C2.A8.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '宏观回报1号（普通级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941184&t=5&start=0&limits=1000&name=.C2.BB.C3.95.C2.BB.C2.AA1.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6A2',
            'ext': '徽华1号优先级A2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941191&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B01.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园1号（次级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941190&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B01.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941430&t=5&start=0&limits=1000&name=.C2.BD.C2.A1.C3.90.C3.901.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '健行1号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940005&t=5&start=0&limits=1000&name=.C2.BD.C3.B5.C3.89.C3.8F.C3.8C.C3.AD.C2.BB.C2.A8',
            'ext': '锦上添花'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941246&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A616.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力16号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941285&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A93.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰3号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941400&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.88.C3.9A.C3.94.C3.B6.C3.80.C3.BB1.C2.BA.C3.85',
            'ext': '投融增利1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941197&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB1.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940027&t=5&start=0&limits=1000&name=.C2.B1.C3.9C.C3.8F.C3.95',
            'ext': '避险'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941238&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B66.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '定增6号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940100&t=4&start=0&limits=1000&name=.C2.B7.C3.A1.C3.8C.C2.A9.C2.B4.C3.B3.C2.B7.C3.A1A2',
            'ext': '丰泰大丰A2'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S76681&t=5&start=0&limits=1000&name=.C2.BB.C2.AA.C3.8E.C3.881.C2.BA.C3.85',
            'ext': '华稳1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941234&t=5&start=0&limits=1000&name=.C2.BB.C3.9B.C3.94.C3.B31.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '慧泽1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940030&t=5&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '季季发（风险级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940206&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X6',
            'ext': '季季优先X6'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941202&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A63.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力3号（中间级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941108&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE2.C3.86.C3.9A',
            'ext': '浦华1号A份额2期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941281&t=5&start=0&limits=1000&name=.C3.86.C3.96.C3.8C.C2.A91.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '浦泰1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941165&t=5&start=0&limits=1000&name=.C3.88.C2.AB.C3.87.C3.B2.C3.95.C2.AE.C3.88.C2.A8.C2.BB.C3.BA.C2.BB.C3.A11.C2.BA.C3.85',
            'ext': '全球债权机会1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940004&t=5&start=0&limits=1000&name=.C2.B2.C2.BD.C2.B2.C2.BD.C3.8E.C2.AA.C3.93.C2.AF',
            'ext': '步步为盈'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941198&t=5&start=0&limits=1000&name=.C2.B6.C2.A8.C3.94.C3.B63.C2.BA.C3.85',
            'ext': '定增3号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941153&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE1.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940029&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C2.B7.C2.A2.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '季季发（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940211&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X11',
            'ext': '季季优先X11'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940202&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X2',
            'ext': '季季优先X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941233&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B010.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园10号（次级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941242&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A614.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力14号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941242&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A614.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力14号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941247&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A616.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力16号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941214&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A68.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力8号（中间级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940042&t=5&start=0&limits=1000&name=.C2.B8.C3.9F.C3.8A.C3.95.C3.92.C3.A6.C3.95.C2.AE',
            'ext': '高收益债'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF0581&t=5&start=0&limits=1000&name=.C2.B9.C2.B2.C3.93.C2.AE2.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '共赢2号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941262&t=5&start=0&limits=1000&name=.C2.B9.C3.89.C3.88.C2.A8.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85',
            'ext': '股权尊享1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940066&t=4&start=0&limits=1000&name=.C2.BA.C3.AA.C2.B9.C3.9B.C2.BB.C3.98.C2.B1.C2.A81.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '宏观回报1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=S76681&t=5&start=0&limits=1000&name=.C2.BB.C2.AA.C3.8E.C3.881.C2.BA.C3.85',
            'ext': '华稳1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941223&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B07.C2.BA.C3.85.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6',
            'ext': '家园7号优先级'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941247&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A616.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力16号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941210&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A67.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力7号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941112&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE6.C3.86.C3.9A',
            'ext': '浦华1号A份额6期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=SF5283&t=5&start=0&limits=1000&name=.C3.8D.C2.B6.C3.94.C3.B61.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '投增1号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941244&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB2.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见2号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940212&t=4&start=0&limits=1000&name=.C2.BC.C2.BE.C2.BC.C2.BE.C3.93.C3.85.C3.8F.C3.88X12',
            'ext': '季季优先X12'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941232&t=5&start=0&limits=1000&name=.C2.BC.C3.92.C3.94.C2.B010.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '家园10号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940126&t=5&start=0&limits=1000&name=.C2.BD.C2.A1.C2.BF.C2.B5.C3.96.C3.90.C2.B9.C3.BA',
            'ext': '健康中国'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941431&t=5&start=0&limits=1000&name=.C2.BD.C2.A1.C3.90.C3.901.C2.BA.C3.85.C2.A3.C2.A8.C2.B4.C3.8E.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '健行1号（次级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941240&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A614.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力14号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941202&t=5&start=0&limits=1000&name=.C2.BE.C3.9B.C3.81.C2.A63.C2.BA.C3.85.C2.A3.C2.A8.C3.96.C3.90.C2.BC.C3.A4.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '聚力3号（中间级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941106&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE1.C3.86.C3.9A',
            'ext': '浦华1号A份额1期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940054&t=5&start=0&limits=1000&name=.C3.92.C3.97.C3.88.C3.9A.C2.B1.C2.A61.C2.BA.C3.85',
            'ext': '易融宝1号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941177&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB11.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见11号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941176&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB11.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见11号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941249&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB15.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见15号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941196&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB3.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见3号（优先级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940262&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.884.C3.94.C3.82X2',
            'ext': '月月优先4月X2'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940317&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX17',
            'ext': '月月优先半年X17'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940253&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX8',
            'ext': '月月优先新享X8'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940012&t=5&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B0.C3.81.C3.BA.C2.A3.C2.A8QDII.C2.A3.C2.A9',
            'ext': '紫金龙（QDII）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940028&t=1&start=0&limits=1000&name=.C3.8C.C3.AC.C3.8C.C3.AC.C2.B7.C2.A2B',
            'ext': '天天发B'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941177&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB11.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见11号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941197&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB1.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见1号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941252&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB5.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见5号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940332&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X3',
            'ext': '月月优先1月X3'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940343&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X15',
            'ext': '月月优先6月X15'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940345&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X17',
            'ext': '月月优先6月X17'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940314&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX14',
            'ext': '月月优先半年X14'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940316&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX16',
            'ext': '月月优先半年X16'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940319&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX19',
            'ext': '月月优先半年X19'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940006&t=5&start=0&limits=1000&name=.C3.94.C3.AC.C2.B8.C2.A3.C3.89.C2.A3.C3.A8.C3.B7',
            'ext': '造福桑梓'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941249&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB15.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见15号（进取级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940180&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.881.C3.94.C3.82X7',
            'ext': '月月优先1月X7'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941500&t=5&start=0&limits=1000&name=.C3.96.C3.90.C2.B5.C3.8D.C3.86.C3.80.C2.BC.C2.B6.C3.95.C2.AE1.C2.BA.C3.85',
            'ext': '中低评级债1号'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941174&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.8512.C2.B8.C3.B6.C3.94.C3.822.C3.86.C3.9A',
            'ext': '中银1号12个月2期'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941325&t=4&start=0&limits=1000&name=.C3.97.C3.B0.C3.8F.C3.AD1.C2.BA.C3.85X21',
            'ext': '尊享1号X21'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941256&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB7.C2.BA.C3.85.C2.A3.C2.A8.C2.BD.C3.B8.C3.88.C2.A1.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见7号（进取级）'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941255&t=5&start=0&limits=1000&name=.C3.94.C2.B6.C2.BC.C3.BB7.C2.BA.C3.85.C2.A3.C2.A8.C3.93.C3.85.C3.8F.C3.88.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '远见7号（优先级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940033&t=5&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C2.B7.C2.A2.C2.A3.C2.A8.C2.B7.C3.A7.C3.8F.C3.95.C2.BC.C2.B6.C2.A3.C2.A9',
            'ext': '月月发（风险级）'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940263&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.884.C3.94.C3.82X3',
            'ext': '月月优先4月X3'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940346&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X18',
            'ext': '月月优先6月X18'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940313&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX13',
            'ext': '月月优先半年X13'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940317&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX17',
            'ext': '月月优先半年X17'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940303&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.883.C2.BA.C3.85',
            'ext': '增强债券优先3号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940307&t=2&start=0&limits=1000&name=.C3.94.C3.B6.C3.87.C2.BF.C3.95.C2.AE.C3.88.C2.AF.C3.93.C3.85.C3.8F.C3.887.C2.BA.C3.85',
            'ext': '增强债券优先7号'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941157&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE2.C3.86.C3.9A',
            'ext': '质押易1号A份额2期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941173&t=5&start=0&limits=1000&name=.C3.96.C3.90.C3.92.C3.B81.C2.BA.C3.856.C2.B8.C3.B6.C3.94.C3.821.C3.86.C3.9A',
            'ext': '中银1号6个月1期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941109&t=4&start=0&limits=1000&name=.C3.86.C3.96.C2.BB.C2.AA1.C2.BA.C3.85A.C2.B7.C3.9D.C2.B6.C3.AE3.C3.86.C3.9A',
            'ext': '浦华1号A份额3期'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940342&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.886.C3.94.C3.82X14',
            'ext': '月月优先6月X14'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940313&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C2.B0.C3.AB.C3.84.C3.AAX13',
            'ext': '月月优先半年X13'},
        {
            'url': 'http://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940250&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX5',
            'ext': '月月优先新享X5'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940252&t=4&start=0&limits=1000&name=.C3.94.C3.82.C3.94.C3.82.C3.93.C3.85.C3.8F.C3.88.C3.90.C3.82.C3.8F.C3.ADX7',
            'ext': '月月优先新享X7'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940037&t=2&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B0.C2.BB.C3.B5.C2.B1.C3.92.C3.94.C3.B6.C3.87.C2.BFA',
            'ext': '紫金货币增强A'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941155&t=5&start=0&limits=1000&name=.C3.96.C3.8A.C3.91.C2.BA.C3.92.C3.971.C2.BA.C3.85B.C2.B7.C3.9D.C2.B6.C3.AE',
            'ext': '质押易1号B份额'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=941019&t=2&start=0&limits=1000&name=.C3.97.C3.8F.C2.BD.C3.B01.C2.BA.C3.85B.C2.BC.C2.B6',
            'ext': '紫金1号B级'},
        {
            'url': 'https://htamc.htsc.com.cn/jhcp/JhcpJzgx/jhjzList.do?productCode=940059&t=7&start=0&limits=1000&name=.C3.97.C3.8A.C3.88.C2.AF.C3.8D.C2.A8.C2.B7.C3.96.C2.BC.C2.B6B',
            'ext': '资券通分级B'},
    ]

    def parse_item(self, response):
        fund_name = response.meta['ext']
        f_list = json.loads(response.text)["items"]
        for i in f_list:
            item = GGFundNavItem()
            statistic_date = i['JZRQ']
            if 'VAL3' in response.text:
                d7_annualized = i['VAL1'].replace('--', '')
                income_value_per_ten_thousand = i['VAL3'].replace('--', '')
                item['d7_annualized_return'] = float(
                    d7_annualized) if d7_annualized is not None and d7_annualized != '' else None
                item['income_value_per_ten_thousand'] = float(
                    income_value_per_ten_thousand) if income_value_per_ten_thousand is not None and income_value_per_ten_thousand != '' else None
            elif 'VAL4' in response.text:
                annualized_return = i['VAL4'].replace('--', '').replace('%', '')
                item['annualized_return'] = float(
                    annualized_return) if annualized_return is not None and annualized_return != '' else None
            else:
                if 'VAL1' in i and 'VAL2' in i:
                    nav = i['VAL1'].replace('--', '')
                    added_nav = i['VAL2'].replace('--', '')
                    item['nav'] = float(nav) if nav is not None and nav != '' else None
                    item['added_nav'] = float(added_nav) if added_nav is not None and added_nav != '' else None
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date, '%Y-%m-%d')
            yield item
