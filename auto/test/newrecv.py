from socket import *
import numpy as np
import cv2


def recv_into(arr, source):
    view = memoryview(arr).cast('B')
    while len(view):
        nrecv = source.recv_into(view)
        view = view[nrecv:]


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', 24000))
    s.listen(1)
    c, a = s.accept()
    a = np.zeros(shape=480*640*3, dtype=np.uint8)
    # view = memoryview(a).cast('B')
    while True:
        recv_into(a, c)
        a = a.reshape((480, 640, 3))
        # print(a.shape)
        cv2.imshow('frame', a)
        # cv2.waitKey(0)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyWindow('frame')
    s.close()
