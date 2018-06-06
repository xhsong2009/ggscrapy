# -*- coding: utf-8 -*-
# Department : 保障部
# Author : 袁龚浩
# Create_date : 2018-05-30

from datetime import datetime
from FundNavSpiders import GGFundNavItem
from FundNavSpiders import GGFundNavSpider
import json
import scrapy


class ShangHaiJiaKenAssetSpider(GGFundNavSpider):
    name = 'FundNav_ShangHaiJiaKenAsset'
    sitename = '上海嘉恳资产'
    channel = '投资顾问'
    allowed_domains = ['www.jiakenzichan.com']

    def start_requests(self):
        yield scrapy.Request(url='http://www.jiakenzichan.com/jjjz/lsjz/article%20', callback=self.pars_pre_login)

    def pars_pre_login(self, response):
        f_codes = response.xpath('//select//option//@value').extract()
        for f_code in f_codes[1:]:
            a = 'field_name_tid=' + f_code + '&view_name=lishijingzhi&view_display_id=default&view_args=&view_path=node%2F64&view_base_path=null&view_dom_id=7b904809e3ce3eb73b6f4dc7de374a16&pager_element=0&ajax_html_ids%5B%5D=skip-link&ajax_html_ids%5B%5D=page&ajax_html_ids%5B%5D=main&ajax_html_ids%5B%5D=content&ajax_html_ids%5B%5D=main-content&ajax_html_ids%5B%5D=views-exposed-form-lishijingzhi-default&ajax_html_ids%5B%5D=edit-field-name-tid-wrapper&ajax_html_ids%5B%5D=edit-field-name-tid&ajax_html_ids%5B%5D=edit-submit-lishijingzhi&ajax_page_state%5Btheme%5D=jiaken&ajax_page_state%5Btheme_token%5D=XP00iUWtqI4Uo-1WPaIFASp2YHxFKWZra2SYQlhEtlY&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.base.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.messages.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsystem%2Fsystem.theme.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Ffield%2Ftheme%2Ffield.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Flogintoboggan%2Flogintoboggan.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fnode%2Fnode.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fsearch%2Fsearch.css%5D=1&ajax_page_state%5Bcss%5D%5Bmodules%2Fuser%2Fuser.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fviews%2Fcss%2Fviews.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fckeditor%2Fcss%2Fckeditor.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fmodules%2Fctools%2Fcss%2Fctools.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fsystem.menus.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fsystem.messages.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fsystem.theme.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fcss%2Fstyles.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fcss%2Fstyle.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fcss%2Fcommon.css%5D=1&ajax_page_state%5Bcss%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fcss%2Fcustom.css%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Freplace%2Fjquery%2F1.7%2Fjquery.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fjquery.once.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fdrupal.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Freplace%2Fui%2Fexternal%2Fjquery.cookie.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Freplace%2Fjquery.form%2F3%2Fjquery.form.min.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fajax.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fjquery_update%2Fjs%2Fjquery_update.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fadmin_menu%2Fadmin_devel%2Fadmin_devel.js%5D=1&ajax_page_state%5Bjs%5D%5Bpublic%3A%2F%2Flanguages%2Fzh-hans_ZWeqD1PUdTBQbYzTSP2OLHA8dqDtVr-QDqpvBwMCzA8.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fctools%2Fjs%2Fauto-submit.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fviews%2Fjs%2Fbase.js%5D=1&ajax_page_state%5Bjs%5D%5Bmisc%2Fprogress.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fmodules%2Fviews%2Fjs%2Fajax_view.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fjs%2Fscript.js%5D=1&ajax_page_state%5Bjs%5D%5Bsites%2Fall%2Fthemes%2Fjiaken%2Fjs%2Fjquery.slideBox.js%5D=1&ajax_page_state%5Bjquery_version%5D=1.7'
            data = {}
            cks = a.split('&')
            for ck in cks:
                ck = ck.split('=', 1)
                key = ck[0].strip()
                value = ck[1].strip()
                data[key] = value
            yield scrapy.FormRequest(url='http://www.jiakenzichan.com/views/ajax',
                                     formdata=data,
                                     callback=self.parse_item)

    def parse_item(self, response):
        funds = json.loads(response.text)[2]['data']
        f_list = scrapy.Selector(text=funds).xpath('//table//tr')
        for i in f_list[1:]:
            t = i.xpath('td//text()').extract()
            fund_name = t[0]
            nav = t[1]
            added_nav = t[2]
            statistic_date = t[3]
            item = GGFundNavItem()
            item['sitename'] = self.sitename
            item['channel'] = self.channel
            item['url'] = response.url
            item['fund_name'] = fund_name
            item['statistic_date'] = datetime.strptime(statistic_date,
                                                       '%Y-%m-%d')
            item['nav'] = float(nav) if nav is not None else None
            item['added_nav'] = float(added_nav) if added_nav is not None else None
            yield item
