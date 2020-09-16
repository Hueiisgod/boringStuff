import base64
import json
import time
import hashlib
import urllib.request
import urllib.parse
import wave
import pyaudio


class Talk():
    # API请求地址、API KEY、APP ID等参数，提前填好备用、
    def __init__(self):
        self.api_url = "http://api.xfyun.cn/v1/service/v1/tts"
        self.API_KEY = "ca619127512012f31a12c3c13641fee5"
        self.APP_ID = "5bda5bda"
        self.OUTPUT_FILE = "/mnt/Ubuntu/AutoDrive/python_project/auto/test/output.wav"  # 输出音频的保存路径，请根据自己的情况替换
        TEXT = ""
        self.CHUNK = 1024

        # 构造输出音频配置参数
        self.Param = {
            "auf": "audio/L16;rate=16000",  # 音频采样率
            "aue": "raw",  # 音频编码，raw(生成wav)或lame(生成mp3)
            "voice_name": "xiaoyan",
            "speed": "50",  # 语速[0,100]
            "volume": "77",  # 音量[0,100]
            "pitch": "50",  # 音高[0,100]
            "engine_type": "aisound"  # 引擎类型。aisound（普通效果），intp65（中文），intp65_en（英文）
        }
        # 配置参数编码为base64字符串，过程：字典→明文字符串→utf8编码→base64(bytes)→base64字符串
        Param_str = json.dumps(self.Param)  # 得到明文字符串
        Param_utf8 = Param_str.encode('utf8')  # 得到utf8编码(bytes类型)
        Param_b64 = base64.b64encode(Param_utf8)  # 得到base64编码(bytes类型)
        Param_b64str = Param_b64.decode('utf8')  # 得到base64字符串

        # 构造HTTP请求的头部
        time_now = str(int(time.time()))
        checksum = (self.API_KEY + time_now + Param_b64str).encode('utf8')
        checksum_md5 = hashlib.md5(checksum).hexdigest()
        self.header = {
            "X-Appid": self.APP_ID,
            "X-CurTime": time_now,
            "X-Param": Param_b64str,
            "X-CheckSum": checksum_md5
        }

    def toVoice(self, txt):

        # 构造HTTP请求Body
        body = {
            "text": txt
        }
        body_urlencode = urllib.parse.urlencode(body)
        self.body_utf8 = body_urlencode.encode('utf8')


        # 发送HTTP POST请求

        req = urllib.request.Request(self.api_url, data=self.body_utf8, headers=self.header)
        response = urllib.request.urlopen(req)

        # 读取结果
        response_head = response.headers['Content-Type']
        if (response_head == "audio/mpeg"):
            out_file = open(self.OUTPUT_FILE, 'wb')
            data = response.read()  # a 'bytes' object
            out_file.write(data)
            out_file.close()
            # print('输出文件: ' + self.OUTPUT_FILE)

            wf = wave.open(self.OUTPUT_FILE, 'rb')
            p = pyaudio.PyAudio()

            # Open voice stream
            stream = p.open(format=pyaudio.paInt16,#format=p.get_format_from_width(wf.getsampwidth()),
                        channels=1,#wf.getnchannels(),
                        rate=16000,#wf.getframerate(),
                        output=True)
            data = wf.readframes(self.CHUNK)
            while data != b'':
                stream.write(data)
                data = wf.readframes(self.CHUNK)
            time.sleep(1)
            stream.stop_stream()
            stream.close()
            p.terminate()
        else:
            print(response.read().decode('utf8'))


if __name__ == '__main__':
    v = Talk()
    v.toVoice('刘备，即汉昭烈帝，又称先主，字玄德，东汉末年幽州涿郡涿县（今河北省涿州市）人，西汉中山靖王刘胜之后，三国时期蜀汉开国皇帝、政治家。刘备少年时拜卢植为师；早年颠沛流离，备尝艰辛，投靠过多个诸侯，曾参与镇压黄巾起义。先后率军救援北海相孔融、徐州牧陶谦等。陶谦病亡后，将徐州让与刘备。赤壁之战时，刘备与孙权联盟击败曹操，趁势夺取荆州。而后进取益州。于章武元年（221年）在成都称帝，国号汉，史称蜀或蜀汉。《三国志》评刘备的机权干略不及曹操，但其弘毅宽厚，知人待士，百折不挠，终成帝业。刘备也称自己做事“每与操反，事乃成尔”。')
