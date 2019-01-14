import requests
from requests.exceptions import RequestException
import json
import time
import pymongo


#  获取连接的html数据
def get_page_by_url(url, encode):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding = (encode)
            return response.text
        return None
    except RequestException:
        try:
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                # response.encoding = ('utf8')
                print(response.status_code)
                return response.text
        except RequestException:
            print('网页状态码异常' + response.status_code)
            return None


def data_insert_db(data, db_collections):
    if db_collections.find_one() is None:
        db_collections.insert_one(data)
    else:
        result = db_collections.find({'rpid': data['rpid']}).count()
        if result == 0:
            print('result', result, data['rpid'], data)
            db_collections.insert_one(data)
        else:
            print('已存在此对象')


# 获取用户的所有视频id
def get_video_list(space_id):
    video_list = set()
    for pn in (1, 3):
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + str(space_id) + '&pagesize=30&tid=0&page=' + str(pn) + '&keyword=&order=pubdate'
        string = get_page_by_url(url, 'unicode_escape')
        if len(string) == 67:
            print('获取视频列表循环：结束')
            break
        string.encode('utf-8')
        data = json.loads(string.replace('\n', '').replace('\r', ''))
        for item in data['data']['vlist']:
            # print(item['aid'])
            video_list.add(item['aid'])

    print(video_list)
    print('获取视频列表循环：结束')
    return video_list


# 保存评论
def save_comment(av_number, MongoClient):
    for pn in range(1, 9):
        url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=' + str(pn) + '&type=1&oid=' + str(av_number)
        page = get_page_by_url(url, 'utf-8')
        if page is None:
            print('获取评论循环：结束（页面空）')
            break
        if pn > 1:
            print('比对NoneType:page')
            print(page)
            print('比对NoneType:page_before')
            print(page_before)
            if len(page) == len(page_before):
                print('获取评论循环：结束（到达最后一页）')
                break
        if len(page) == 39:
            print('获取评论循环：结束（关闭评论）')
            break
        data = json.loads(page)
        print('------------------' + str(av_number) + '-----------------------获取第' + str(
            pn) + '页评论-----------------------------------------------------')
        if data['data']['replies'] is None:
            pass
        else:
            for comment in data['data']['replies']:
                data_insert_db(comment, MongoClient)
                print(comment['content']['message'])
        page_before = page


def main():
    reply_DB = pymongo.MongoClient('mongodb://localhost:27017/')['test']['reply']
    # 5128788是用户id
    video_list = get_video_list(5128788)
    for av_number in video_list:
        save_comment(av_number, reply_DB)


if __name__ == '__main__':
    main()
