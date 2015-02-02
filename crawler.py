__author__ = '怡炜'


def crawler():
    import httplib2
    import json
    import bs4
    import re

    url = r"http://item.taobao.com/item.htm?spm=a219r.lm893.14.1.A1oXVV&id=41171239568&ns=1&abbucket=3#detail"
    h = httplib2.Http()
    response, content = h.request(url)
    soup = bs4.BeautifulSoup(content)
    # open(r'C:\Users\怡炜\Desktop\content.txt', 'w').write(content.decode("gbk"))
    content_str = content.decode('gbk')
    microscope_data = re.search(r'pageId=(\d+);prototypeId=(\d+);siteId=(\d+); shopId=(\d+); userid=(\d+)', content_str)
    print(microscope_data)
    meta = soup.meta
    a = meta.find(attrs={'name': 'microscope-data'})
    # print(soup.findAll(name="meta"))
    print(a)
    # print(response, content)


if __name__ == "__main__":
    crawler()