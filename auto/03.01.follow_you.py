from follow_remote import Track_you
import socket
import cv2


class Tracker:
    def __init__(self):
        self.tracking = Track_you()
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
        self.bias = 0.

    def sending_command(self):
        cap = cv2.VideoCapture(0)

        while True:
            # print('wait for frame.')
            # self.message = self.s.recvfrom(65535)
            # self.frame = self.message.decode('utf-8')
            # print('Waiting for connection...')

            _, self.frame = cap.read()
            self.bias = self.tracking.track(self.frame)
            if self.bias is None:
                print("lost tracking.")
                break
            elif self.bias > 10:
                self.message = 'left'
                print('left')
                self.s.sendto(self.message.encode(encoding='utf-8'), (self.network, self.port))
            elif self.bias < -10:
                self.message = 'right'
                print('right')
                self.s.sendto(self.message.encode(encoding='utf-8'), (self.network, self.port))
            else:
                self.message = 'forward'
                print('forward')
                self.s.sendto(self.message.encode(encoding='utf-8'), (self.network, self.port))
            # 发送数据
            print('...send message to :', self.addr)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        self.s.close()


if __name__ == '__main__':
    s = Tracker()
    s.sending_command()