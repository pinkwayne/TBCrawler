# -*- coding: utf8 -*-
__author__ = '怡炜'


import re
import sys
import gzip
import json
import time
import random
import urllib2
import BeautifulSoup


def generate_id(url):
    auctionId = re.search('id=(\d+)', url).group(1)
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(content)
    ids = soup.find('meta', {'name': 'microscope-data'})['content']
    splitid = re.split(';', ids)
    siteId = re.split('=', splitid[2])[1]
    userid = re.split('=', splitid[4])[1]
    return {'userid': userid, 'auctionId': auctionId, 'siteId': siteId}


def crawler(url):
    ids = generate_id(url)
    comments = open(r'comments_data/comments_%s.txt' % ids['auctionId'], 'w+')
    headers = {'Referer': url, 'Connection': 'keep-alive', 'Host': 'rate.taobao.com', 'User-Agent': 'Mozilla/5.0'}
    pageNum = 1
    review_id = 1
    segmentor = u'[ ，,.。！!？?：:；、~～="“”（）()/〓【】★☆…\[\]\*]'
    while(1):
        KsTS = str(int(time.time()*1000))+'_'+str(random.randint(1000, 9999))
        rateUrl = 'http://rate.taobao.com/feedRateList.htm?_ksTS=%(KsTS)s&callback=jsonp_reviews_list&' \
                  'userNumId=%(userid)s&auctionNumId=%(auctionNumId)s&siteID=%(siteId)s&currentPageNum=%(pageNum)s&' \
                  'rateType=&orderType=sort_weight&showContent=1&attribute=&ua=' \
                  % {'KsTS': KsTS, 'userid': ids['userid'], 'auctionNumId': ids['auctionId'],
                     'siteId': ids['siteId'], 'pageNum': pageNum}
        # print rateUrl
        opener = urllib2.build_opener()
        req = urllib2.Request(url=rateUrl, headers=headers)
        content = opener.open(req).read()
        jsonContent = json.loads(content.decode("gbk", "ignore")[23:-3])
        if jsonContent['comments']:
            print('page %d' % pageNum)
            for i in range(0, len(jsonContent['comments'])):
                comment = jsonContent['comments'][i]['content'].replace('<br/>', '').replace('\n', '').replace('&hellip;', '')
                comment = re.sub(segmentor, ' ', comment)
                print review_id
                comment = 'id:%d ' % review_id + comment.strip()
                # print(comment)
                comments.write(comment)
                comments.write('\n')
                review_id += 1
            pageNum += 1
            if pageNum % 25 == 0:
                time.sleep(0.5)
            if pageNum == 101:
                break
        else:
            break


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    url = r"http://item.taobao.com/item.htm?id=42180621470&ns=1&abbucket=0#detail"
    start = time.time()
    crawler(url)
    stop = time.time()
    print("processing time: %s seconds" % str(stop-start))
