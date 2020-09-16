import socket
import cv2
import numpy as np

class Tracker:
    def __init__(self):
        self.host = ''  # 监听所有的ip
        self.port = 13141  # 接口必须一致
        self.bufsize = 1024
        self.addr = (self.host, self.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.network = '<broadcast>'
        self.s.bind(('', self.port))  # 开始监听
        self.frame = ''
        self.message = 'waiting for connection....'

    def sending_command(self):
        while True:
            print('wait for frame.')
            self.message = self.s.recvfrom(65535)
            self.frame = self.message[0].decode('utf-8')
            self.frame = list(self.frame)
            print(type(self.frame))
            print('frame received.')
            print(len(self.frame))
            print(self.frame[:])
            cv2.imshow('frame', self.frame)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        self.s.close()


if __name__ == '__main__':
    s = Tracker()
    s.sending_command()