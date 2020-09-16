import os
import json
import sys
# import speech
import wave
from pyaudio import PyAudio, paInt16
os.chdir('/home/avi/Documents/AutoDrive/python_project/auto/Soldiers')
from Sodiers_voice_xunfei import XUNFEI_ASR


class Voice():

    def __init__(self):
        self.path = os.curdir + '/command.wav'
        self.framerate = 16000
        self.NUM_SAMPLES = 2000
        self.channels = 1
        self.sampwidth = 2
        self.TIME = 20
        self.record()
        self.voice2word(path)

    def save_wave_file(self, filename, data):
        '''save the date to the wavfile'''
        wf=wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def record(self):
        pa = PyAudio()
        print("get_default_input_device_info()", pa.get_default_input_device_info())
        stream = pa.open(format=paInt16,
                        channels=1,
                        rate=self.framerate,
                        input=True,
                        frames_per_buffer=self.NUM_SAMPLES)
        my_buf = []
        count = 0
        
        # 开始录音
        while count < self.TIME:#控制录音时间
            string_audio_data = stream.read(self.NUM_SAMPLES)
            if count == 0:
                # speech.say("一秒后请说")
                print("一秒后请说：")
            my_buf.append(string_audio_data)
            count += 1
            # print('.')
        self.save_wave_file(self.path, my_buf)
        stream.close()

    def voice2word(self, path):
        return XUNFEI_ASR(path)




if __name__ == '__main__':
    a = Voice()
    
    print(a) 
    
    exit()
