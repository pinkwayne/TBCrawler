__author__ = '怡炜'


import re
import gzip
import json
import time
import random
import threading
from urllib import request
from bs4 import BeautifulSoup

finish = 0

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


def crawlpage(ids, pageNum, proxy, comments):
    proxy_handler = request.ProxyHandler({'http': proxy})
    null_proxy_handler = request.ProxyHandler({})
    headers = {'Referer': url, 'Connection': 'keep-alive', 'Host': 'rate.taobao.com', 'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip'}
    KsTS = str(int(time.time()*1000))+'_'+str(random.randint(1000, 9999))
    rateUrl = 'http://rate.taobao.com/feedRateList.htm?_ksTS=%(KsTS)s&callback=jsonp_reviews_list&' \
              'userNumId=%(userid)s&auctionNumId=%(auctionNumId)s&siteID=%(siteId)s&currentPageNum=%(pageNum)s&' \
              'rateType=&orderType=sort_weight&showContent=1&attribute=&ua=' \
                 % {'KsTS': KsTS, 'userid': ids['userid'], 'auctionNumId': ids['auctionId'],
                    'siteId': ids['siteId'], 'pageNum': pageNum}
    opener = request.build_opener(null_proxy_handler)
    req = request.Request(url=rateUrl, headers=headers)
    content = gzip.decompress(opener.open(req).read())
    jsonContent = json.loads(content.decode("gbk", "ignore")[23:-3])
    if jsonContent['comments']:
        print('page : %s' % pageNum)
        for i in range(0, len(jsonContent['comments'])):
            comment = jsonContent['comments'][i]['content'].replace('<br/>', '').replace('\n', '')
            print(comment+'    '+str(pageNum))
            comments.write(comment+'\n'*2)
    else:
        global finish
        finish = 1


def crawler(url):
    proxies = open('proxy_ip', 'r').readlines()
    ids = generate_id(url)
    comments = open(r'C:\Users\怡炜\Desktop\comments_%s.txt' % ids['auctionId'], 'w+')
    open(r'C:\Users\怡炜\Desktop\pinkwayne.txt', 'w+').write('pinkwayne')
    i = 1
    while(1):
        threads = []
        for j in range(i, i+50):
            t = threading.Thread(target=crawlpage, args=(ids, j, proxies[j+1-i][:-1], comments))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if finish == 1:
            break
        i += 50

if __name__ == "__main__":
    url = r"http://item.taobao.com/item.htm?spm=a219r.lm893.14.794.Kni2XB&id=41802604226&ns=1&abbucket=19#detail"
    start = time.time()
    crawler(url)
    stop = time.time()
    print("processing time: %s seconds" % str(stop-start))
