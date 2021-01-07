# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


BASE_URL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/'
URL = BASE_URL+'index.html'

SQL_TEMPLATE = "insert into area_info(id,level,code,name,parent_id) values (%s,%s,'%s','%s',%s);\r\n"

# Sql文件生成路径
SQL_FILE = "/home/liupeng/tmp/area_info.sql"

temp_id = 0


def parse_index_html(url):  # 解析首页省级数据
    print(url)
    res = requests.get(url)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, features="html.parser")
    links = soup.find_all("a")
    for link in links:
        if link['href'].endswith("html"):
            id = getNextId()
            genSql(id, 1, id, link.get_text(), 0)
            parse_next_html(2, id, BASE_URL+link['href'])


def parse_next_html(level, id, url):  # 解析市/县级数据
    res = requests.get(url)
    res.encoding = 'gbk'
    print(url)
    if res.status_code != 200:
        print("request fail ,retry", url)
        parse_next_html(level, id, url)
        return
    soup = BeautifulSoup(res.text, features="html.parser")
    links = soup.find_all("a")
    for index in range(0, len(links)-1, 2):
        current_id = getNextId()
        code = links[index].get_text()
        name = links[index+1].get_text()
        genSql(current_id, level, code, name, id)
        if level == 2:
            parse_next_html(3, current_id, BASE_URL+links[index]['href'])


def genSql(id, level, code, name, parent_id):
    s = SQL_TEMPLATE % (id, level, code, name, parent_id)
    writeFile(SQL_FILE, s)


def writeFile(fileName, content):
    file = open(fileName, mode='a')
    file.write(content)
    file.close()


def getNextId():
    global temp_id
    temp_id = temp_id+1
    return temp_id


parse_index_html(URL)
