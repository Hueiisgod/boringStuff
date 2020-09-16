import json
import time
import requests
import base64
import urllib.parse
import hashlib
def XUNFEI_ASR(_path):
    ''' 讯飞语音转文字
    
    :param _path: 
    :return: 
    '''
    f = open(_path, 'rb')
    #rb表示以二进制格式只读打开文件

    file_content = f.read()

    base64_audio = base64.b64encode(file_content)
    
    body = urllib.parse.urlencode({'audio': base64_audio})
    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    APP_ID = '5ba0483a'
    API_KEY = '0aee7c2a8895d58988d56b2c9a57d38c'
    param = {"engine_type": "sms16k", "aue": "raw"}
    
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    _str = API_KEY + str(x_time) + x_param.decode('utf-8')
    x_checksum = hashlib.md5(_str.encode('utf-8')).hexdigest()
    x_header = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'X-Appid': APP_ID,
                'X-CurTime': str(x_time),
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    res = requests.post(url, body, headers = x_header)
    res = res.content.decode('utf-8')
    answer = json.loads(res)
    if answer['code'] == '0':
        return answer['data']
    else:
        return answer['code']

