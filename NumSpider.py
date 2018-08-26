# -*- coding: utf-8 -*-
import os
#import sys
#import urllib2
import requests
import re
import json
from lxml import etree

def AllPageListSave(url):
    pagelists = []
    i = 1
    while i < 117:
        newurl = url + "_" + str(i) + ".html"
        i += 1
        print("downloading ", newurl)
        new_page = requests.get(newurl).content.decode("utf8")
        newpagelist = Page_Info(new_page)
        pagelists.extend(newpagelist)

    StringListSave(pagelists)
def StringListSave(slist):
    save_path = "spider"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    fname = "num.json"
    path = save_path+"/"+fname
    '''with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0], s[1])) #.encode("utf8")
    '''

    try:
        with open(path, 'w+') as f_obj:
            #j_nums = json.load(f_obj)
            #print(j_nums)
            #for value in j_nums.values():
             #   print(value)
            json.dump(slist, f_obj)
    except IOError:#FileNotFoundError（py3)
        pass
    else:

        print("file exists")
def Page_Info(myPage):
    '''Regex'''
    mypage_Info = re.findall(r'<td align="center">(\d+)</td>.*?<em class="rr">(.*?)</em>.*?<em class="rr">(.*?)</em>.*?<em class="rr">(.*?)</em>.*?<em class="rr">(.*?)</em>.*?<em class="rr">(.*?)</em>.*?<em class="rr">(.*?)</em>.*?<em>(.*?)</em>', myPage, re.S)
    #</td>.*?<strong>(.*?)</strong></td>
    print(mypage_Info)

    return mypage_Info

def New_Page_Info(new_page):
    '''Regex(slowly) or Xpath(fast)'''
    # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)\.html".*?>(.*?)</a></td>', new_page, re.S)
    # # new_page_Info = re.findall(r'<td class=".*?">.*?<a href="(.*?)">(.*?)</a></td>', new_page, re.S) # bugs
    # results = []
    # for url, item in new_page_Info:
    #     results.append((item, url+".html"))
    # return results
    dom = etree.HTML(new_page)
    new_items = dom.xpath('//tr/td/a/text()')
    new_urls = dom.xpath('//tr/td/a/@href')
    assert(len(new_items) == len(new_urls))
    return zip(new_items, new_urls)

def GetNewPageList(url):
    url0 = url + ".html"
    print("downloading ", url0)
    myPage = requests.get(url0).content.decode("utf8")
    # myPage = urllib2.urlopen(url).read().decode("gbk")
    mypageresults = Page_Info(myPage)

def GetFileList():

    path = "spider/num.json"
    '''with open(path, "w+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\n" % (s[0], s[1])) #.encode("utf8")
    '''

    try:
        with open(path, 'w+') as f_obj:
            #j_nums = json.load(f_obj)
            #print(j_nums)
            #for value in j_nums.values():
             #   print(value)
            json.dump(slist, f_obj)
    except IOError:#FileNotFoundError（py3)
        pass
    else:

        print("file exists")

def Spider(url):
    GetNewPageList(url)

    '''
    for item, url in myPageResults:
        print("downloading ", url)
        new_page = requests.get(url).content.decode("gbk")
        # new_page = urllib2.urlopen(url).read().decode("gbk")
        newPageResults = New_Page_Info(new_page)
        filename = str(i)+"_"+item
        StringListSave(save_path, newPageResults)
        i += 1
    '''
    #一次性获取并保存
    #AllPageListSave(url)


if __name__ == '__main__':
    print("start")
    start_url = "http://kaijiang.zhcw.com/zhcw/html/ssq/list"
    Spider(start_url)
    print("end")