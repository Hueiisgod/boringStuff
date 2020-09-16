import json
import time
import requests
import base64
import urllib.parse
import hashlib
from Sodiers_voice import Voice
from turing_brain import LoginTic
from word2voice import Talk


def Asr_Ques():
    ''' 图灵问答系统

    :param _path:
    :return:
    '''
    # Input voice and turn to word.
    q = Voice()
    ll = LoginTic()
    tt = Talk()
    tt.toVoice("嗨，你好！")

    while True:

        question = q.getword()
        cont = ll.talkWithTuling(question)
        print(cont)
        dd = json.loads(cont)
        if dd['code'] == 100000:
            # 返回的是文本
            print('-'*10)
            print(dd['text'])
            tt.toVoice(dd['text'])
        elif dd['code'] == 200000:
            # '链接累的内容'
            print(dd['text'])
            print(dd['url'])
            tt.toVoice(dd['text'])

        elif dd['code'] == 302000:
            # 新闻类的内容
            print(dd['text'])
            print(len(dd['list']))
            tt.toVoice(dd['text'])
            tt.toVoice(dd['list'])
        elif dd['code'] == 308000:
            # 菜谱类的内容
            pass

        elif dd['code'] == 313000:
            # 儿歌类的
            pass

        elif dd['code'] == 314000:
            #儿童诗词类的
            tt.toVoice(dd['text'])
        if "再见" in question:
            break
        tt.toVoice("你说吧！")


if __name__ == '__main__':
    qna = Asr_Ques()