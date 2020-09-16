import cv2
from color_bounding import ColorBounding
from robotPi import robotPi
from barcode_scanner_video import QRscan
import time
from rev_cam import rev_cam

class Cleaner:
    def __init__(self):
        self.robot = robotPi()
        self.color_bounding = ColorBounding()
        self.qr = QRscan()
        self.cap = cv2.VideoCapture(0)
        # 画面宽高
        self.width = 640
        self.height = 480
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

    def find_garbage(self, frame):
        x = -1
        self.robot.movement.turn_right(5, 500)
        x, y, w, h = self.color_bounding.bounding(frame)
        if x == 0 and y ==0:
            return -1, -1
        else:
            return x, y, w, h

    def find_bin(self, frame):
        i = -1
        self.robot.movement.turn_right(5, 500)
        name, bbox = self.qr.scan(frame)
        if "sword" in name:
            return bbox
        else:
            return -1, -1, 0, 0

    def going(self, x, y):
        # 目标偏移的最大宽度与高度
        center_x, center_y = int(self.width/2), int(self.height/2)
        self.robot.movement.move_forward()
        vector_x = center_x - x
        vector_y = center_y - y
        if vector_x > 20:
            self.robot.movement.turn_right()
        if vector_x < -20:
            self.robot.movement.turn_left()

    def grab(self):
        time.sleep(3)
        pass

    def put(self):
        time.sleep(3)
        pass


if __name__ == '__main__':
    cc = Cleaner()
    flag = False    # 手上是否有垃圾
    while True:
        ret, raw_frame = cc.cap.read()
        frame = rev_cam(raw_frame)
        frame = cv2.flip(frame, -1)
        # 开始寻找垃圾
        x, y, w, h = cc.find_garbage(frame)

        print("Have garbage:", flag)
        if x != -1 and flag is False:    # 找到垃圾且手上没有垃圾
            # 去垃圾的位置抓取
            cc.going(x+w/2, y+h/2)
            print("going to garbage.")
            cv2.rectangle(frame,(x, y), (x+w, y+h), (255, 0, 0), 5)

            if cc.height - (y+h/2) < 20:
                cc.grab()
                print("grab garbage.")
                flag = True
        (i, j, w, h) = cc.find_bin(frame)
        flag = True
        if i != -1 and flag is True:    # 找到垃圾桶且手上有垃圾
            # 到垃圾桶的位置放下垃圾
            cc.going(i, j)
            print("going to bin.")
            cv2.rectangle(frame, (i, j), (i+w, j+h), (255, 0, 0), 5)
            if w > 300 and cc.height < (j + h):
                cc.put()
                print("put garbage into bin.")
                flag = False
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

