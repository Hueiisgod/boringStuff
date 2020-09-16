import numpy as np
import time
import tensorflow as tf
from robotPi import robotPi
from color_bounding import ColorBounding
from Welcome_face_detector import Face_Detector
from barcode_scanner_video import QRscan

import cv2
import os

# 1:[1,0,0,0] 前
# 2:[0,1,0,0] 左
# 3:[0,0,1,0] 右
# 4:[0,0,0,1] 后


width = 180
height = 80
channel = 1
# 要寻找的目标 1: Color; 2: QR Code; 3: Face
tar = 2
inference_path = tf.Graph()
filepath = os.getcwd() + '/model/auto_drive_model/-49'
temp_image = np.zeros(width * height * channel, 'uint8')


def find_qr(frame):
    qr = QRscan()
    name, bbox = qr.scan(frame)
    if "sword" in name:
        return bbox
    else:
        return -1, -1, 0, 0


def going(x, y):
    # 目标偏移的最大宽度与高度
    robot = robotPi()
    center_x, center_y = int(640 / 2), int(480 / 2)
    robot.movement.move_forward()
    vector_x = center_x - x
    vector_y = center_y - y
    if vector_x > 20:
        robot.movement.turn_right()
    if vector_x < -20:
        robot.movement.turn_left()


def target(number):
    '''
    Searching for target accroding to given number.
    :param number: 1: Color; 2: QR Code; 3: Face
    :return: None
    '''
    robot = robotPi()
    cap = cv2.VideoCapture(0)
    color_bounding = ColorBounding()
    robot.movement.hold()
    x, y, w, h = -1, -1, 0, 0
    it = 0
    T = False  # 是否找到过目标
    while cap.isOpened():
        ret, frame = cap.read()
        # Finding
        robot.movement.turn_right(5, 500)
        x, y, w, h = color_bounding.bounding(frame)
        if x == 0 and y == 0:
            x, y = -1, -1
        else:
            T = True
        # Going to target
        going(x + w/2, y + h/2)
        if it == 100 and T is True:  # 找到目标后，连续100帧丢失目标，认为已经到达目的地
            print("hit.")
            robot.movement.hit()
            break
