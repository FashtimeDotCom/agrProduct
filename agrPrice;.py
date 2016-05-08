# coding:utf-8
import urllib2
from bs4 import BeautifulSoup
import sys
import pymongo

reload(sys)
sys.setdefaultencoding("utf-8")

connection = pymongo.MongoClient()
tdb = connection.o2o
post_info = tdb.good


def find_data(tmp_url, tmp_city):
    for pageNum in range(1, 10):

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

            print "{\"species\":\"%s\", \"price\":\"%s\",\"market\":\"%s\",\"date\":\"%s\"}" % (
                species_str, price_str, market_str, date_str)

            data = {"city": tmp_city, "species": species_str, "price": float(price_str), "market": market_str,
                    "date": date_str}

            post_info.save(data)
    return


url = "http://nc.mofcom.gov.cn/channel/gxdj/jghq/sc_list.shtml"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, "html.parser")

div_soup = soup.find('div', {'class': 'z_map'})
div_list = div_soup.findAll('div', {'class': 'k_txtBoxP_01'})
for div in div_list:
    city = div.find('h4')
    city_str = city.string[:len(city.string) - 4]
    a_list = div.findAll('a')
    print "city:%s" % city_str
    for a in a_list:
        find_data(a['href'], city_str)
