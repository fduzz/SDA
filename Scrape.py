import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime, date # needed to retrieve the date of publication 

year = [2023,2020,2018,2015,2013,2010,2008,2005,2003]

jilin = {2023:'https://www.jl.gov.cn/zw/jcxxgk/gzbg/szfgzbg/202301/t20230120_8662908.html',
         2020:'https://www.jl.gov.cn/zw/jcxxgk/gzbg/szfgzbg/202001/t20200120_6625530.html',
         2018:'https://www.jl.gov.cn/zw/jcxxgk/gzbg/szfgzbg/201802/t20180220_6625528.html',
         2015:'https://www.jl.gov.cn/zw/jcxxgk/gzbg/szfgzbg/201502/t20150226_6625525.html',
         2013:'https://www.jl.gov.cn/zw/jcxxgk/gzbg/szfgzbg/201411/t20141119_6625524.html',
         2010:'https://www.jl.gov.cn/zw/jcxxgk/gzbg/szfgzbg/201411/t20141119_6625522.html',
         2008:'https://www.gov.cn/test/2008-02/18/content_892280.htm',
         2005:'https://web.archive.org/web/20100419114341/https://www.gov.cn/test/2006-02/10/content_185038.htm',
         2003:'https://www.gov.cn/test/2006-02/17/content_202877.htm'}

liaoning = {2023:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/EE9395E0C27941F89E476E1B07369A44/index.shtml',
            2020:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/26D9FA7CDBF44CB483B6C802E1ED8B97/index.shtml',
            2018:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/D50B292BB1AE4BAD90B43B18C784DA35/index.shtml',
            2015:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/D1039EF913204A529A8B69B0B2746536/index.shtml',
            2013:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/95C48360165548BC8676DEA95B16D45F/index.shtml',
            2010:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/AE17AF0FE4B64C61BA4E8A915FF78E51/index.shtml',
            2008:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/65CBDA21C27340AAB96130C7782E9228/index.shtml',
            2005:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/01BA958037BD42FABDAA51DC89259A68/index.shtml',
            2003:'https://www.ln.gov.cn/web/zwgkx/zfgzbg/szfgzbg/E58CE56F7E974584AC4BF9D32FF742A0/index.shtml'}

heilongjiang = {2023:'https://www.hlj.gov.cn/hlj/c108465/202302/c00_31524958.shtml',
                2020:'https://www.hlj.gov.cn/hlj/c108465/202001/c00_30603044.shtml',
                2018:'https://www.hlj.gov.cn/hlj/c108465/201801/c00_30597244.shtml',
                2015:'https://www.hlj.gov.cn/hlj/c108465/201502/c00_30657828.shtml',
                2013:'https://www.hlj.gov.cn/hlj/c108465/201302/c00_30657826.shtml',
                2010:'https://www.hlj.gov.cn/hlj/c108465/201601/c00_30657832.shtml',
                2008:'https://www.hlj.gov.cn/hlj/c108465/200801/c00_30657824.shtml',
                2005:'https://www.hlj.gov.cn/hlj/c108465/200708/c00_30657830.shtml',
                2003:'https://www.hlj.gov.cn/hlj/c108465/200708/c00_30657821.shtml'}


for i in year:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = jilin[i]
    url_request = requests.get(url)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'html.parser') # or 'lxml'
    # 定位到<div class="Custom_UnionStyle">
    if i > 2016:
        news_elements = parsed_content.find('div', class_ = "Custom_UnionStyle")
    elif i > 2009:
        news_elements = parsed_content.find('div', class_ = "TRS_Editor")
    else:
        news_elements = parsed_content.find('td', class_ = "p1")

    # 提取并打印所有文本
    text = news_elements.get_text()

    with open('/Users/zhou/Library/Mobile Documents/com~apple~CloudDocs/SDA/Scrape/吉林/吉林'+str(i)+'.txt', 'w', encoding='utf-8') as file:
        file.write(text)


for i in year:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = liaoning[i]
    url_request = requests.get(url, headers=headers)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'lxml') # 'html.parser' or 'lxml'
    # 定位到<div class="Custom_UnionStyle">
    news_elements = parsed_content.find('div', class_ = "TRS_Editor")

    # 提取并打印所有文本
    text = news_elements.get_text()

    with open('/Users/zhou/Library/Mobile Documents/com~apple~CloudDocs/SDA/Scrape/辽宁/辽宁'+str(i)+'.txt', 'w', encoding='utf-8') as file:
        file.write(text)


for i in year:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = heilongjiang[i]
    url_request = requests.get(url, headers=headers)

    # Returns the content of the response,  …
    url_content = url_request.content # … in bytes
    # Using BeautifulSoup to parse webpage source code
    parsed_content = soup(url_content, 'lxml') # 'html.parser' or 'lxml'
    # 定位到<div class="Custom_UnionStyle">
    news_elements = parsed_content.find('div', class_ = r'article_content article_content_body')

    # 提取并打印所有文本
    text = news_elements.get_text()

    with open('/Users/zhou/Library/Mobile Documents/com~apple~CloudDocs/SDA/Scrape/黑龙江/黑龙江'+str(i)+'.txt', 'w', encoding='utf-8') as file:
        file.write(text)

