from robotPi import robotPi
from robotpi_serOp import serOp
from Sodiers_client import Client
import cv2
import socket


class Followers(robotPi):
    def __init__(self):
        print("Sir, yes sir!")
        super().__init__()
        self.ser = serOp()
        self.cap = cv2.VideoCapture(0)
        self.frame, self.ok = self.cap.read()

        self.network = '<broadcast>'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.PORT = 13141
        self.s.bind(('', self.PORT))
        print('Listening for broadcast at ', self.s.getsockname())

    def attention(self):
        while True:
            self.s.sendto(self.frame.encode(encoding='utf-8'), (self.network, self.PORT))
            print("Waiting commands!")
            self.client = Client()
            self.order = self.client.listening()
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
            self.take_commands(self.order)
        follower.movement.wave_hands()

    def take_commands(self, order):
        if 'forward' in order:
            follower.movement.move_forward(speed=8, times=1000)
        elif 'left' in order:
            follower.movement.turn_left(speed=8, times=1000)
        elif 'right' in order:
            follower.movement.turn_right(speed=8, times=1000)

    def listening(self):
        if '再见' not in self.message:
            self.message, address = self.s.recvfrom(65535)
            self.s.close()
        return self.message.decode('utf-8')

if __name__ == "__main__":
    follower = Followers()
    follower.attention()
    exit(0)


