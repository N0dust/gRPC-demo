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
            # response.encoding = ('utf8')
            print(response.status_code, response.text)
            return response.text
        return None
    except RequestException:
        print('网页状态码异常')
        return None


def jsons_in_db(html, db_collections):
    pass

def main():
    url = 'https://m.weibo.cn/comments/hotflow?id=4326322916097204&mid=4326322916097204&max_id_type=0'
    get_page_byurl(url)


if __name__ == '__main__':
    main()
