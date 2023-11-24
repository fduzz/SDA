# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 20:32:05 2023

@author: Lenovo
"""
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime, date # needed to retrieve the date of publication 

year = [2023,2020,2018,2015,2013,2010,2008,2005,2003]

anhui = {2023:'https://www.ah.gov.cn/public/1681/564207141.html',
         2020:'https://www.ah.gov.cn/public/1681/8254221.html',
         2018:'https://www.ah.gov.cn/public/1681/7965141.html',
         2015:'https://www.ah.gov.cn/public/1681/7965171.html',
         2013:'https://www.ah.gov.cn/public/1681/7965191.html',
         2010:'https://www.ah.gov.cn/public/1681/7965221.html',
         2008:'https://www.ah.gov.cn/public/1681/7965241.html',
         2005:'https://www.ah.gov.cn/public/1681/7965271.html',
         2003:'https://www.ah.gov.cn/public/1681/7965291.html'}

shanxi = {2023:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/202301/t20230131_7894563.shtml',
            2020:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/202001/t20200117_6090390.shtml',
            2018:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/201802/t20180205_6090388.shtml',
            2015:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/201502/t20150204_6090385.shtml',
            2013:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/201302/t20130205_6090383.shtml',
            2010:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/201712/t20171220_6090380.shtml',
            2008:'http://www.shanxi.gov.cn/szf/zfgzbg/szfgzbg/201712/t20171220_6090378.shtml',
            2005:'https://www.gov.cn/test/2006-02/10/content_185027.htm',
            2003:'https://www.gov.cn/test/2006-02/17/content_202874.htm'}

hunan = {2023:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/202301/t20230128_29191509.html',
         2020:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/202001/t20200123_11163610.html',
         2018:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201802/t20180224_4960623.html',
         2015:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201711/t20171111_4676644.html',
         2013:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201302/t20130206_4676642.html',
         2010:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201711/t20171111_4676639.html',
         2008:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201711/t20171111_4676637.html',
         2005:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201711/t20171111_4676634.html',
         2003:'http://www.hunan.gov.cn/hnszf/szf/zfgzbg/201711/t20171111_4676632.html'}


for i in year:

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = anhui[i]
    url_request = requests.get(url, headers=headers)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'lxml') # 'html.parser' or 'lxml'
    print(parsed_content)
    # 定位到<div class="Custom_UnionStyle">
    news_elements = parsed_content.find('div', class_ = r'wzcon j-fontContent')
# 提取并打印所有文本
    text = news_elements.get_text()
 
    with open('C:/Users/Lenovo/Desktop/SDA/安徽/安徽'+str(i)+'.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    
for i in {2008,2010,2013,2015,2018,2020,2023}:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = shanxi[i]
    url_request = requests.get(url, headers=headers)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'lxml') # 'html.parser' or 'lxml'
    print(parsed_content)
    # 定位到<div class="Custom_UnionStyle">
    news_elements = parsed_content.find('div', class_ = r'article-body clearfix')
    # 提取并打印所有文本

    text = news_elements.get_text()
      
    with open('C:/Users/Lenovo/Desktop/SDA/山西/山西'+str(i)+'.txt', 'w', encoding='utf-8') as file:
             file.write(text)   
             
for i in {2003,2005}:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = shanxi[i]
    url_request = requests.get(url, headers=headers)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'lxml') # 'html.parser' or 'lxml'
    print(parsed_content)
    # 定位到<div class="Custom_UnionStyle">
    news_elements = parsed_content.find('td', class_=r'p1')
    # 提取并打印所有文本

    text = news_elements.get_text()
      
    with open('C:/Users/Lenovo/Desktop/SDA/山西/山西'+str(i)+'.txt', 'w', encoding='utf-8') as file:
             file.write(text)   
             

for i in year:

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = hunan[i]
    url_request = requests.get(url, headers=headers)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'lxml') # 'html.parser' or 'lxml'
    print(parsed_content)
    # 定位到<div class="Custom_UnionStyle">
    news_elements = parsed_content.find('div', class_ = r'xly_Box')
# 提取并打印所有文本
    text = news_elements.get_text()
 
    with open('C:/Users/Lenovo/Desktop/SDA/湖南/湖南'+str(i)+'.txt', 'w', encoding='utf-8') as file:
        file.write(text)
    
    
    
        


