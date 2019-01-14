import requests
from requests.exceptions import RequestException
import json
import time
import pymongo


#  获取连接的html数据
def get_page_byurl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(response.status_code, response.text)
            return response.text
        return None
    except RequestException:
        print('网页状态码异常')
        return None


# 将html数据存入数据库中（这里是mongoDB）
def jsons_in_db(html, db_collections):
    rank = json.loads(html)
    for dirt in rank['data']:
        if db_collections.find_one() is None:
            db_collections.insert_one(dirt)
        else:
            result = db_collections.find({'id': dirt['id']}).count()
            if result == 0:
                print('result', result, dirt['id'], dirt)
                db_collections.insert_one(dirt)
            else:
                print('已存在此对象')


def main():
    # 日排行的url'https://api.bilibili.com/x/article/rank/list?cid=3&jsonp=jsonp'
    # 周排行的 jsons_in_db(get_page_byurl('https://api.bilibili.com/x/article/rank/list?cid=2&jsonp=jsonp'), weekdata)

    recommended_data = pymongo.MongoClient('mongodb://localhost:27017/')['test']['recommended']
    for i in range(1, 30):
        url = 'https://api.bilibili.com/x/article/recommends?cid=0&pn=' + str(i) + '&ps=20&jsonp=jsonp&aids=&sort=0'

        jsons_in_db(get_page_byurl(url), recommended_data)
        print(i)


def aest():
    url = 'https://api.bilibili.com/x/relation/followings?vmid=3211302&pn=5&ps=20&order=desc&jsonp=jsonp'
    respons = requests.get(url)
    print(respons.status_code)
    print(respons.text)
    data = json.loads(respons.text)
    print(data)




if __name__ == '__main__':
    main()
