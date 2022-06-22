# import urllib.request
# from bs4 import BeautifulSoup
# class Scraper:
#     def __init__(self,site):
#         self.site=site
#
#     def scrape(self):
#         r=urllib.request.urlopen(self.site)
#         html=r.read()
#         parser="html.parser"
#         sp=BeautifulSoup(html,parser)
#         for tag in sp.find_all("a"):
#             url=tag.get("href")
#             if url is None:
#                 continue
#             if "html" in url:
#                 print("\n"+url)
#
#
# if __name__ == '__main__':
#     news = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&rsv_dl=ns_pc&word=%E5%AE%81%E5%BE%B7%E6%97%B6%E4%BB%A3%E5%8A%A8%E5%8A%9B%E7%94%B5%E6%B1%A0"
#     Scraper(news).scrape()


import requests
from bs4 import BeautifulSoup


if __name__=='__main__':
    url = "http://news.baidu.com/ns?cl=2&rn=20&tn=news&word=%E4%B8%8A%E6%B5%B7%E6%B5%B7%E4%BA%8B%E5%A4%A7%E5%AD%A6"
    response = requests.get(url)  #对获取到的文本进行解析
    html = response.text
    soup=BeautifulSoup(html,features='lxml')  #根据HTML网页字符串创建BeautifulSoup对象
    news=soup.find_all('div', {"class": "result"})

    for t in news:
        data = {
            "标题":t.find('a').text,
            "链接":t.find('a')['href'],
            "时间":t.find('p').get_text()
        }
        print(data)

