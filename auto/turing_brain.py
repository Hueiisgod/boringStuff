#_*_coding:utf-8_*_

'''
Created by swh on 2017.09.18
'''

import requests
from json import loads

class LoginTic(object):
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }

        self.key = 'b1bca6dd620243eb8313c36c0bbbd55f'
        # 创建一个网络请求session实现登录验证
        self.session = requests.session()

    def talkWithTuling(self, text):
        url = 'http://www.tuling123.com/openapi/api'
        data = {
            'key': self.key,         #key
            'info': text,            #发给图灵的内容
            'userid': 'BCSH'        #用户id,自己设置1-32的字母和数字组合
        }
        response = requests.post(url=url, headers=self.headers, data=data)
        return response.text


if __name__ == '__main__':
    ll = LoginTic()
    userName = input('你想和我聊什么？:')
    while userName != 'q':
        cont = ll.talkWithTuling(userName)
        # print (cont)
        dd = loads(cont)
        if dd['code'] == 100000:
            # 返回的是文本
            print ('-'*10)
            print (dd['text'])
        elif dd['code'] == 200000:
            # '链接类的内容'
            print (dd['text'])
            print (dd['url'])
        elif dd['code'] == 302000:
            # 新闻类的内容
            print (dd['text'])
            print (len(dd['list']))

        elif dd['code'] == 308000:
            # 菜谱类的内容
            pass

        elif dd['code'] == 313000:
            # 儿歌类的
            pass

        elif dd['code'] == 314000:
            #儿童诗词类的
            pass
        userName = input('说话，不要停:')

    print ('程序结束')
