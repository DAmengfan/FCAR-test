import re
import time
import requests
import tldextract
from bs4 import BeautifulSoup
import urllib
import distutils.filelist
import chardet
def get_text_from_163(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    s = soup.body.find(
        "div", ['wrapper clearfix', 'container post_auto clearfix','a_adtemp a_topad js-topad','content area']).find(
            "div", ['post_main','article-content','article-box l']).find("div",
                                     ['post_content','content','article-text']).find("div", ['post_body','ql-align-justify'])
    return s.get_text()
def get_from_163_3g(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    s = soup.body.find("main").find('article').find(
        'div', class_='article-content').find('div', class_='content').find(
        'div', class_='page js-page on n-platform-android')
    print(s)
    if s is None:
        return
    return s.get_text()

def save_to_db(url, html):
    file = open('link.txt', 'a', encoding='utf-8')
    #url 是网址，html是 网页内容
    print('%s : %s' % (url, len(html)))
    if len(html) == 0:
        return
    file.write(url)
    file.write('\n')
    r = requests.get(url)
    if r.apparent_encoding == 'Windows-1254':
        return
    r.encoding = r.apparent_encoding
    tld = tldextract.extract(url)
    print(tld)
    if tld.subdomain == '3g':
        news_content = get_from_163_3g(r.text)
    if tld.subdomain =='www':
        return
    else:
        news_content = get_text_from_163(r.text)
    if news_content is None:
        file.close()
    else:
        file.write(news_content)
        file.write('\n')
        file.close()

def crawl():
    # 1\. download baidu news
    #hub_url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4+%E5%90%88%E4%BD%9C+site%3A+163.com&tn=news&rsv_bp=1&oq=&rsv_sug3=15&rsv_sug2=0&rsv_btype=t&f=8&inputT=4494&rsv_sug4=4494'
    #阿里巴巴 合作
    hub_url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E7%89%B9%E6%96%AF%E6%8B%89+%E6%8A%95%E8%B5%84site%3A+163.com&tn=news&rsv_bp=1&rsv_sug3=1&rsv_sug2=0&oq=&rsv_btype=t&f=8&inputT=1&rsv_sug4=542'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }
    res = requests.get(hub_url, headers=headers)
    #res = requests.get(hub_url)
    html = res.text
    #print(html)
    # 2\. extract news links
    ## 2.1 extract all links with 'href'
    links = re.findall(r'href=[\'"]?(.*?)[\'"\s]', html)
    print('find links:', len(links))
    news_links = []
    ## 2.2 filter non-news link
    for link in links:
        if not link.startswith('http'):
            continue
        tld = tldextract.extract(link)
        print(tld.domain)
        print(tld.subdomain)
        if tld.domain == 'baidu':
            continue
        #if tld.subdomain == 'passport' or tld.subdomain == 'i' or tld.subdomain == 'cache' or tld.subdomain == 'www' or tld.subdomain == 'tieba'  or tld.subdomain == 'map' or tld.subdomain == 'b2b' or tld.subdomain == 'zhidao' or tld.subdomain == 'image' or tld.subdomain == 'wenku':
        if tld.subdomain == 'i':
            continue
        news_links.append(link)
    print('find news links:', len(news_links))
    # news_links = ['https://www.163.com/dy/article/GTQJKS6J05525UOI.html']
    # 3\. download news and save to database
    news_links = list(set(news_links))
    print(news_links)
    for link in news_links:
        html = requests.get(link).text
        save_to_db(link, html)
    print('works done!')

def main():

    crawl()
if __name__ == '__main__':
    main()