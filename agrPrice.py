# coding:utf-8
import urllib2

import time
from bs4 import BeautifulSoup
import sys
import pymongo

reload(sys)
sys.setdefaultencoding("utf-8")

connection = pymongo.MongoClient()
tdb = connection.o2o
post_info = tdb.good


def find_data(tmp_url, tmp_city, tmp_num):
    for pageNum in range(1, tmp_num):

        page_num_str = str(pageNum)
        print "Getting data for Page " + page_num_str
        f_url = "http://nc.mofcom.gov.cn" + tmp_url + "&page=" + page_num_str
        f_page = urllib2.urlopen(f_url)
        f_soup = BeautifulSoup(f_page, "html.parser")

        table_soup = f_soup.find('table')

        proxy_list = table_soup.findAll('tr')[1:]

        for tr in proxy_list:
            td_list = tr.findAll('td')
            species = td_list[0]
            species_str = species.string
            price = td_list[1]
            price_str = price.string
            market = td_list[2].find('a')
            market_str = "".join(market.string.split())
            date = td_list[3]
            date_str = date.string

            # if date_str == tmp_time:

            print "{\"species\":\"%s\", \"price\":\"%s\",\"market\":\"%s\",\"date\":\"%s\"}" % (
                species_str, price_str, market_str, date_str)

            data = {"city": tmp_city + "市", "species": species_str, "price": float(price_str), "market": market_str,
                    "date": date_str}

            post_info.save(data)
    return


find_data('/channel/gxdj/jghq/jg_detail.shtml?id=20969', "无锡", 247)
find_data('/channel/gxdj/jghq/jg_detail.shtml?id=2576431', "无锡", 11)

# url = "http://nc.mofcom.gov.cn/channel/gxdj/jghq/sc_list.shtml"
# page = urllib2.urlopen(url)
# soup = BeautifulSoup(page, "html.parser")
#
# now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
# print now_time
#
# div_soup = soup.find('div', {'class': 'z_map'})
# div_list = div_soup.findAll('div', {'class': 'k_txtBoxP_01'})
# for div in div_list:
#     city = div.find('h4')
#     city_str = city.string[:len(city.string) - 4]
#     a_list = div.findAll('a')
#     print "city:%s" % city_str
#     if city_str == "上海":
#         for a in a_list:
#             print a['href']
#             # find_data(a['href'], city_str, now_time)
