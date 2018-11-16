# # -*- coding: utf-8 -*-
# coding:utf-8
# width = 20  # 宽度
# height = 6  # 高度
# array = []  # 数组
# for i in range(0, height):
#     for j in range(0, width):
#         if j == 0:
#             array.append([1])
#         elif j == width - 1:
#             array[i].append(1)
#         else:
#             if i == 0 or i == height-1:
#                 array[i].append(1)
#             else:
#                 array[i].append(0)
# print array
# string = ""
# for i in array:
#     for j in i:
#         string += (j == 1) and "■" or "□"
#     print string
#     string = ""
# import yaml
# f = open('./yaml.ini')
# x = yaml.load(f)
# print x
# def f(x, l=[]):
#     for i in range(x):
#         l.append(i*i)
#     print l
#
# f(3,[3,2,1])


# def read_file(fpath):
#    BLOCK_SIZE = 1024
#    with open(fpath, 'rb') as f:
#        while True:
#            block = f.read(BLOCK_SIZE)
#            if block:
#                yield block
#            else:
#                return
# read_file('/etc')

# import collections
# d = collections.OrderedDict()
# d['a'] = 'a'
# d['b'] = 'b'
# d['c'] = 'c'
# print d
# for k, v in d.items():
#     print '%s %s' % (k, v)

import logging

import subprocess
import time
import os

# def follow(thefile):
#     thefile.seek(0, 2)
#     while True:
#         line = thefile.readline()
#         if not line:
#             time.sleep(0.1)
#             continue
#         yield line
#
#
# if __name__ == '__main__':
#     logfile = open("access.log", "r")
#     loglines = follow(logfile)
#     print type(loglines)
#     print loglines


def watch_log(log):
    max_size = 10*1024*1024
    log = "log/" + log
    line = ""
    while True:
        with open(log, "r") as logfile:
            logfile.seek(-4, 2)
            read_line = logfile.readline()
            if read_line != line:
                line = read_line
                print '改变的行为：', line
                if os.path.getsize(log) >= max_size:
                    for root, dirs, files in os.walk(os.path.dirname(__file__) + "/log", True):
                        last = os.path.join(files[-1]).split('.')[-1]
                        os.rename(log, "%s.%d" % (log, int(last)+1))
        time.sleep(2)
        continue

watch_log("access.log")

# logfile = 'access.log'
# command = 'tail -f '+logfile+' -s 1'
# popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# while True:
#     line = popen.stdout.readline().strip()
#     print line

# import time
# file = open('access.log')
# while 1:
#     where = file.tell()
#     line = file.readline()
#     if not line:
#         time.sleep(1)
#         file.seek(where)
#     else:
#         print type(line),
# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-18 11:52:26

# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-18 11:52:26

from pyspider.libs.base_handler import *
from pyspider.libs.header_switch import HeadersSelector
import sys
import pymysql
import time
import re

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class Handler(BaseHandler):

    # 连接数据库
    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', 'qq123456', 'pachong', charset='utf8')

    def db_add(self, table_name, dic):
        # try:
        if dic['url'][-1] != '/':
            dic['url'] += '/'
        cursor = self.db.cursor()
        sql = 'insert into %s(%s,create_date) values ("%s",%s)' % (
        table_name, ','.join(dic.keys()), '","'.join(dic.values()), 'now()')  # 插入数据库的SQL语句
        cursor.execute(sql)
        self.db.commit()
        # except:
        #     self.db.rollback()

    def db_update(self, table_name, dic):
        try:

            if dic['url'][-1] != '/':
                dic['url'] += '/'
            cursor = self.db.cursor()
            sql = 'update %s set url="%s" where name="%s"' % (table_name, dic['url'], dic['name'])  # 更新数据库的SQL语句
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def db_judge(self, table_name, **kwargs):
        cursor = self.db.cursor()
        sql = 'select * from %s where name="%s"' % (table_name, kwargs['name'])  # 查询数据库的SQL语句
        cursor.execute(sql)
        if cursor.fetchone() == None:
            self.db_add(table_name, kwargs)
        else:
            self.db_update(table_name, kwargs)

    def db_url(self, table_name, url):
        print (re.sub(r'info(.*)$', '', url))
        cursor = self.db.cursor()
        sql = 'select * from %s where url="%s"' % (table_name, re.sub(r'info(.*)$', '', url))  # 查询数据库的SQL语句
        cursor.execute(sql)
        # 返回id
        return str(cursor.fetchone()[0])

    def create_cookie(self, response):
        i = int(time.time()) - 200
        cookie = {
            "__jsluid": response.cookies["__jsluid"],
            "Hm_lvt_9ef8813ed2f6c5ab8be2f11df9c933f5": str(i - 21000),
            "account": "acc=mkcc58",
            "company%5Fid": "15625346",
            "shopDomain": " ",
            "Hm_lpvt_9ef8813ed2f6c5ab8be2f11df9c933f5": str(i)
        }
        cookie_list = ["%s=%s" % (k, cookie[k]) for k in cookie]
        return ";".join(cookie_list)

    def get_header(self, response):
        header_slt = HeadersSelector()
        header = header_slt.select_header()  # 获取一个新的 header
        if response.cookies:
            header["Cookies"] = self.create_cookie(response)
        return header

    @every(minutes=24 * 60)
    def on_start(self):
        header_slt = HeadersSelector()
        header = header_slt.select_header()
        orig_href = 'http://www.fengj.com/'
        header[
            "Cookies"] = "__jsluid=643279edbfca529c4afaaf818a653b43; Hm_lvt_9ef8813ed2f6c5ab8be2f11df9c933f5=1532330720; account=acc=mkcc58; company%5Fid=15625346; shopDomain=; Hm_lpvt_9ef8813ed2f6c5ab8be2f11df9c933f5=1532351450"
        self.crawl(orig_href,
                   callback=self.index_page,
                   headers=header)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        header = self.get_header(response)
        for each in response.doc('.Nav_Left').find('a[href$=".fengj.com"], a[href$=".fengj.com/"]').items():
            if each.text():
                # self.db_judge("first_classify",name = each.text(), url = each.attr.href)
                self.crawl(each.attr.href, callback=self.second_page, headers=header)

    @config(age=10 * 24 * 60 * 60)
    def second_page(self, response):
        header = self.get_header(response)
        self.crawl(response.url + "info/", callback=self.third_page, headers=header, priority=1)

    @config(age=10 * 24 * 60 * 60)
    def third_page(self, response):
        header = self.get_header(response)
        for each in response.doc('.fenlei_erji, .fenlei_er').find('a[href*=".fengj.com/info"]').items():
            text = each.children().text()
            if each.children().text():
                self.db_judge("second_classify", fid=self.db_url("first_classify", response.url), name=text,
                              url=each.attr.href)
                self.crawl(each.attr.href, callback=self.forth_page, headers=header)
                # for page in xrange(2, 11):
                # self.crawl("%spage%d"% (each.attr.href, page), callback=self.forth_page, headers=header)

    @config(age=10 * 24 * 60 * 60)
    def forth_page(self, response):
        header = self.get_header(response)
        for each in response.doc('a[href*=".shop.fengj.com"]').items():
            text = each.children().text()
            if each.children().text():
                self.db_judge("second_classify", fid=self.db_url("first_classify", response.url), name=text,
                              url=each.attr.href)
                self.crawl(each.attr.href, callback=self.detail_page, headers=header)

    @config(priority=2)
    def detail_page(self, response):

        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

