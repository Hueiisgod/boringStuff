from socket import *
import numpy as np
import cv2


def send_from(arr, dest):
    # view = memoryview(arr).cast('B')
    # while True:
    #     nsent = dest.send(arr)
    #     arr = arr[nsent:]
    #     if arr:
    #         break
    nsent = dest.send(arr)


if __name__ == '__main__':
    c = socket(AF_INET, SOCK_STREAM)
    c.connect(('192.168.0.174', 24000))
    print('connected.')
    # '/mnt/Ubuntu/yolo_ssd/YOLOv3/videos/test/library1.mp4'
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    while cap.isOpened():
        res, frame = cap.read()
        # a = np.ones((200, 300), dtype=int) *1000
        # frame.dtype = 'int'
        send_from(frame, c)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    # print(frame[:10])
    c.close()
