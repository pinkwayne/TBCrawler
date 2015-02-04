__author__ = '怡炜'


import re
import gzip
import json
import time
import random
from urllib import request
from bs4 import BeautifulSoup


def generate_id(url):
    auctionId = re.search('id=(\d+)', url).group(1)
    content = request.urlopen(url).read()
    soup = BeautifulSoup(content)
    open(r'C:\Users\怡炜\Desktop\content.txt', 'w').write(content.decode("gbk"))
    ids = soup.meta.find(attrs={'name': 'microscope-data'}).attrs['content']
    splitid = re.split(';', ids)
    siteId = re.split('=', splitid[2])[1]
    userid = re.split('=', splitid[4])[1]
    return {'userid': userid, 'auctionId': auctionId, 'siteId': siteId}


def crawler(url):
    ids = generate_id(url)
    comments = open(r'C:\Users\怡炜\Desktop\comments_%s.txt' % ids['userid'], 'w+')
    proxy_handler = request.ProxyHandler({'http': r'183.207.237.11:83'})
    headers = {'Referer': url, 'Connection': 'keep-alive', 'Host': 'rate.taobao.com', 'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'}
    for pageNum in range(1, 100):
        print("page %s" % pageNum)
        KsTS = str(int(time.time()*1000))+'_'+str(random.randint(1000, 9999))
        rateUrl = 'http://rate.taobao.com/feedRateList.htm?_ksTS=%(KsTS)s&callback=jsonp_reviews_list&' \
                  'userNumId=%(userid)s&auctionNumId=%(auctionNumId)s&siteID=%(siteId)s&currentPageNum=%(pageNum)s&' \
                  'rateType=&orderType=sort_weight&showContent=1&attribute=&ua=' \
                  % {'KsTS': KsTS, 'userid': ids['userid'], 'auctionNumId': ids['auctionId'],
                     'siteId': ids['siteId'], 'pageNum': pageNum}
        # print(rateUrl)
        # h = httplib2.Http()
        opener = request.build_opener(proxy_handler)
        req = request.Request(url=rateUrl, headers=headers)
        content = gzip.decompress(opener.open(req).read())
        # response, content = h.request(rateUrl, headers=headers)
        # open(r'C:\Users\怡炜\Desktop\content2.txt', 'w').write(content.decode("gbk"))
        jsonContent = json.loads(content.decode("gbk", "ignore")[23:-3])
        for i in range(0, 20):
            comment = jsonContent['comments'][i]['content'].replace('<br/>', '').replace('\n', '')
            # print(comment)
            comments.write(comment+'\n'*2)
if __name__ == "__main__":
    url = r"http://item.taobao.com/item.htm?spm=a219r.lm893.14.35.YyNnUx&id=41239809200&ns=1&abbucket=3#detail"
    start = time.time()
    crawler(url)
    stop = time.time()
    print("processing time: %s seconds" % str(stop-start))
