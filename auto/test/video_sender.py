
import cv2
import socket


class Followers():
    def __init__(self):
        print("Sir, yes sir!")
        self.cap = cv2.VideoCapture(0)
        self.ok, self.frame = self.cap.read()

        self.network = '<broadcast>'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.PORT = 13141
        self.s.bind(('', self.PORT))
        print('Listening for broadcast at ', self.s.getsockname())

    def attention(self):
        while True:
            self.s.sendto(self.frame, (self.network, self.PORT))
            print("Waiting commands!")
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break






if __name__ == "__main__":
    follower = Followers()
    follower.attention()
    exit(0)
