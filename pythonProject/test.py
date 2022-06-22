import re
import time
import requests
import tldextract
from bs4 import BeautifulSoup
import urllib
import distutils.filelist
import chardet

def save_to_db(url,html):
    file = open('de.txt', 'a', encoding='utf-8')
    # 保存网页到数据库，我们暂时用打印相关信息代替
    #url 是网址，html是 网页内容
    print('%s : %s' % (url, len(html)))

    file.write(url)
    file.write('\n')
    r = requests.get(url)
    print(r.apparent_encoding)
    print(r.encoding)
    r.encoding = r.apparent_encoding
    if (len(html)>0 ):
        soup = BeautifulSoup(r.text,"html.parser")
        #if len(soup.find_all('post_recommend_time'))  == 0:

        for tag in soup.find_all( 'p'):
            # print(tag.find(class="post_recommend_time"))
            # if tag.find('class'=="post_recommend_time"):
            #     continue

            if r.apparent_encoding == 'Windows-1254':
                break
            if ((len(tag.get_text()))<=10):
                continue
            else:
                file.write(tag.get_text())
                print(tag.get_text())
                #print(tag)



def crawl():
    # 1\. download baidu news
    #hub_url = 'https://www.baidu.com/s?tn=news&rtt=1&bsst=1&wd=%E5%AE%81%E5%BE%B7%E6%97%B6%E4%BB%A3+%E5%90%88%E4%BD%9C&cl=2'
    #hub_url = 'https://www.baidu.com/s?ie=utf-8&medium=0&rtt=1&bsst=1&rsv_dl=news_t_sk&cl=2&wd=%E5%8D%8E%E4%B8%BA+%E6%8A%95%E8%B5%84&tn=news&rsv_bp=1&oq=&rsv_sug3=23&rsv_sug1=14&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&f=8&inputT=4560&rsv_sug4=4560'
    #hub_url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E7%89%B9%E6%96%AF%E6%8B%89%20%20%E6%8A%95%E8%B5%84'
    hub_url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E7%89%B9%E6%96%AF%E6%8B%89%20%E7%AB%9E%E4%BA%89'
    #hub_url = 'https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%20%E5%90%88%E4%BD%9C'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
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
        #print(tld)
        if tld.domain == 'baidu':
            continue
        # if tld.subdomain == 'passport' or tld.subdomain == 'i' or tld.subdomain == 'cache' or tld.subdomain == 'www' or tld.subdomain == 'tieba' or tld.subdomain == 'map' or tld.subdomain == 'b2b' or tld.subdomain == 'zhidao' or tld.subdomain == 'image' or tld.subdomain == 'wenku':
        #     continue
        news_links.append(link)
    print('find news links:', len(news_links))
    # 3\. download news and save to database
    for link in news_links:
        html = requests.get(link).text
        save_to_db(link, html)
    print('works done!')

def main():

    crawl()


if __name__ == '__main__':
    main()