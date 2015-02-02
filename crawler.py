__author__ = '怡炜'


def crawler():
    import httplib2
    import json
    import bs4
    import re

    url = r"http://item.taobao.com/item.htm?spm=a219r.lm893.14.38.A1oXVV&id=41239809200&ns=1&abbucket=3#detail"
    h = httplib2.Http()
    response, content = h.request(url)
    soup = bs4.BeautifulSoup(content)
    # open(r'C:\Users\怡炜\Desktop\content.txt', 'w').write(content.decode("gbk"))
    ids = soup.meta.find(attrs={'name': 'microscope-data'}).attrs['content']
    splitid = re.split(';', ids)
    pageId = re.split('=', splitid[0])[1]
    prototypeId = re.split('=', splitid[1])[1]
    siteId = re.split('=', splitid[2])[1]
    shopId = re.split('=', splitid[3])[1]
    userid = re.split('=', splitid[4])[1]
    print('pageId='+pageId)
    print('prototypeId='+prototypeId)
    print('siteId='+siteId)
    print('shopId='+shopId)
    print('userid='+userid)
    print(ids)


if __name__ == "__main__":
    crawler()