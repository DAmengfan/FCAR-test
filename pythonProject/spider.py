from bs4 import BeautifulSoup

f = open('特斯拉印度陷“僵局” 马斯克称面临大量挑战 _ 东方财富网.html', encoding='utf-8')
html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
s = soup.body.find("div", 'main').find("div", "contentwrap").find(
    "div", "contentbox").find("div", "mainleft").find("div", "txtinfos")
print(s.get_text())