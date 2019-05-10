import requests
from requests.exceptions import RequestException
import json
import  re


def getMagnetUrl(id):
    # 拼接链接
    url = 'https://www.javbus.com/' + id
    # 构建头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'referer': url
    }
    # 先获取gid
    response_tem = requests.get(url, headers=headers)
    gid = re.search('(\d{11})(?=;)', response_tem.text).group()
    # 通过gid来拼接请求url获取种子链接
    magnet_request_url = 'https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=' + gid + '&uc=0'
    response = requests.get(magnet_request_url, headers=headers)
    magnetUrl = list(set(re.findall('href="(.*?)"\>', response.text)))
    for each in magnetUrl:
        print(each)


def main():
    # id即番号
    id = 'IPX-292'
    getMagnetUrl(id)


if __name__ == '__main__':
    main()