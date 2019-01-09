import requests
from requests.exceptions import RequestException
import json
import time
import pymongo


# 投稿视频链接
# https://space.bilibili.com/ajax/member/getSubmitVideos?mid=16151010&pagesize=30&tid=0&page=1&keyword=&order=pubdate
# 评论连接
# 第一页
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925331&jsonp=jsonp&pn=1&type=1&oid=40232658&sort=0&_=1547008926833
# 第二页
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925335&jsonp=jsonp&pn=2&type=1&oid=40232658&sort=0&_=1547009121899
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925342&jsonp=jsonp&pn=2&type=1&oid=40232658&sort=2&_=1547009383089
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925344&jsonp=jsonp&pn=2&type=1&oid=40232658&sort=2&_=1547009800063
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925346&jsonp=jsonp&pn=2&type=1&oid=40232658&sort=2&_=1547009806573
# 第三页
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925336&jsonp=jsonp&pn=3&type=1&oid=40232658&sort=0&_=1547009176432
# 对照组
# https://api.bilibili.com/x/article/recommends?cid=0&pn=1&ps=20&jsonp=jsonp&aids=&sort=0'
# 尝试组
# https://api.bilibili.com/x/v2/reply?callback=jQuery17207233102631476498_1547008925346&jsonp=jsonp&pn=2&type=1&oid=40232658&sort=2


#  获取连接的html数据
def get_page_byurl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # response.encoding = ('utf8')
            print(response.status_code, response.text)
            return response.text
        return None
    except RequestException:
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                # response.encoding = ('utf8')
                print(response.status_code, response.text)
                return response.text
        except RequestException:
            print('网页状态码异常')
            return None


def jsons_in_db(html, db_collections):
    pass


def get_comment():
    url1 = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=1&type=1&oid=40232658&sort=2'
    url2 = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=2&type=1&oid=40232658&sort=2'
    url3 = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=3&type=1&oid=40232658&sort=2'
    pn1 = json.loads(get_page_byurl(url1))
    pn2 = json.loads(get_page_byurl(url2))
    pn3 = json.loads(get_page_byurl(url3))
    print(pn1['data']['replies'])
    for comment in pn1['data']['replies']:
        print(comment['content']['message'])


def main():
    # https://space.bilibili.com/ajax/member/getSubmitVideos?mid=326246517&pagesize=30&tid=0&page=1&keyword=&order=pubdate
    get_page_byurl('https://space.bilibili.com/ajax/member/getSubmitVideos?mid=16151010&pagesize=30&tid=0&page=1&keyword=&order=pubdate')


if __name__ == '__main__':
    main()
