from bs4 import BeautifulSoup

f = open('关注 _ 与特斯拉在新战场竞争？华为将于3月在日本销售大型电池_储能_网易订阅.html', encoding='utf-8')
html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
s = soup.body.find("div", 'wrapper clearfix').find("div", "post_main").find(
    "div", "post_content").find("div", "post_body")
print(s.get_text())