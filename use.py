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


# 全国农产品商务信息公共服务平台
def find_data_1(tmp_url, tmp_city, tmp_num):
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


# 上海农业
def find_data_2(tmp_url):
    f_url = tmp_url
    f_page = urllib2.urlopen(f_url)
    f_soup = BeautifulSoup(f_page, "html.parser")

    a_soup_list = f_soup.findAll('a')[1:]

    for a in a_soup_list:
        a_onclick = a.attrs['onclick']
        cut_1 = a_onclick.index("'")
        cut_2 = a_onclick[cut_1 + 1:len(a_onclick) - 1].index("'")
        product_number = a_onclick[cut_1 + 1:cut_1 + cut_2 + 1]
        cut_3 = a_onclick[cut_1 + cut_2 + 2:len(a_onclick) - 1].index("'")
        cut_4 = a_onclick[cut_1 + cut_2 + cut_3 + 3:len(a_onclick) - 1].index("'")
        product_name = a_onclick[cut_1 + cut_2 + cut_3 + 3:cut_1 + cut_2 + cut_3 + cut_4 + 3]

        new_url = tmp_url + product_number
        new_page = urllib2.urlopen(new_url)
        new_soup = BeautifulSoup(new_page, "html.parser")
        table_soup = new_soup.findAll('table')[1:]

        use_table = table_soup[0]
        proxy_list = use_table.findAll('tr')[0:]
        for tr in proxy_list:
            td_list = tr.findAll('td')
            current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            print "{\"species\":\"%s\", \"price\":\"%s\",\"market\":\"%s\",\"date\":\"%s\"}" % (
            product_name, td_list[2].string, td_list[0].string, current_date)
            data = {"city": "上海市", "species": product_name, "price": float(td_list[2].string),
                    "market": td_list[0].string, "date": current_date}
            post_info.save(data)
    return


# 中国惠农网
def find_data_3(tmp_url, tmp_num):
    tmp_page = 1
    f_url = tmp_url + tmp_num + '/'
    f_page = urllib2.urlopen(f_url)
    f_soup = BeautifulSoup(f_page, "html.parser")

    page_soup = f_soup.find('div', class_="page mt_40")
    pageNumALabel = page_soup.findAll('a')[1:]
    pageNum = pageNumALabel[len(pageNumALabel) - 2].get_text()
    print(pageNum)

    while (tmp_page < int(pageNum)):
        f_url = tmp_url + tmp_num + '/' + str(tmp_page)
        f_page = urllib2.urlopen(f_url)
        f_soup = BeautifulSoup(f_page, "html.parser")

        table_soup = f_soup.find('div', class_="column-other")

        proxy_list = table_soup.findAll('ul')[1:]

        for tr in proxy_list:
            td_list = tr.findAll('li')[0:]
            species = td_list[0].find('a').get_text()
            dateIndex = td_list[1].get_text().index("20")
            date = td_list[1].get_text()[dateIndex:dateIndex + 10]
            market = td_list[2].get_text()
            max_price = td_list[3].get_text()
            min_price = td_list[4].get_text()
            avg_price = td_list[5].get_text()

            print(species + " " + date + " " + market + " " + max_price + " " + min_price + " " + avg_price)
        tmp_page += 1
    print("end")


find_data_3('http://news.cnhnb.com/hangqing/0/key%3d/', '9')

while True:
    current_time = time.localtime(time.time())
    if ((current_time.tm_hour == 21) and (current_time.tm_min == 51) and (current_time.tm_sec == 0)):
        find_data_1('/channel/gxdj/jghq/jg_detail.shtml?id=20969', "江苏", 247)
        find_data_1('/channel/gxdj/jghq/jg_detail.shtml?id=2576431', "江苏", 11)
        find_data_2('http://116.228.18.49:8888/jgjcDemo/sqkd-pfjg.jsp?pfjfl=')
    time.sleep(1)
