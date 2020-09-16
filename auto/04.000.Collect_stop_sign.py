__author__ = 'Avi'

import numpy as np
import cv2
from robotpi_movement import Movement

# import pygame
# from pygame.locals import *

import time
import os


class CollectTrainingData(object):
    """
    input:
        commands and video
    output:
        带有标签的灰度图像集，标签（0, 1, 2, 3）分别代表（前进， 左转，右转，停止）
        每种标签数量上限1000张，像素为H*W = 80×180
    """
    def __init__(self):

        self.raw_height = 480  # 原始视频高度
        self.raw_width = 640  # 原始视频宽度
        self.video_width = 480  # 截取图像宽度
        self.video_height = 180  # 截取图像高度
        self.NUM = 4  # 分类数量：0, 1, 2, 3
        self.range = 100 # 每个分类的图片数
        self.data_path = "dataset"
        self.saved_file_name = 'labeled_img_data_' + str(int(time.time()))

        self.mv = Movement()


        # create labels
        self.k = np.zeros((self.NUM, self.NUM), 'float')
        for i in range(self.NUM):
            self.k[i, i] = 1

        # pygame.init()
        self.collect_image()

    def collect_image(self):

        total_images_collected = 0
        num_list = [0, 0, 0, 0]
        cap = cv2.VideoCapture(0)
        images = np.zeros((1, self.video_height * self.video_width), dtype=float)
        labels = np.zeros((1, self.NUM), dtype=float)

        # Send an action to begin program.
        # command.action()
        self.mv.wave_hands()
        self.mv.set_volume(15)

        while cap.isOpened():
            _, frame = cap.read()
            resized_height = int(self.video_width * 0.75)
            # 计算缩放比例
            frame = cv2.resize(frame, (self.video_width, resized_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # slice the lower part of a frame
            res = frame[resized_height - self.video_height:, :]
            cv2.imshow("review", res)

            command = cv2.waitKey(1) & 0xFF
            if command == ord('q'):
                break
            # forward -- 0
            elif command == ord('w'):
                
                self.mv.move_forward(times=300)
                    
                
                continue

            # forward-left -- 1
            elif command == ord('a'):
            
                self.mv.left_ward()
                
                
                continue

            # forward-right -- 2
            elif command == ord('d'):
                
                self.mv.right_ward()
                
                continue

            # stop-sign -- 3
            elif command == ord('s'):
                if num_list[3] < self.range:
                    num_list[3] += 1
                    total_images_collected += 1
                    self.mv.stop()
                    res = np.reshape(res, [1, -1])
                    images=np.vstack((images, res))
                    labels = np.vstack((labels, self.k[3]))
                else:
                    # Wave rise both hand here.
                    self.mv.play_sound(255, 13)
                    
                    continue
            elif command == ord('x'):
                self.mv.move_backward()
            # ‘z’和‘c’用于辅助收集停止符号数据，机器走到停止符号前，左右平移，调整终止符号的位置再拍照，以获得更丰富的数据样本
            elif command == ord('z'):
                self.mv.move_left()
                continue

            elif command == ord('c'):
                self.mv.move_right()
                continue

            elif num_list[0] == self.range and num_list[1] == self.range and num_list[2] == self.range and num_list[3] == self.range:
                self.mv.wave_hands()
                break
                # exit(0)

        img = images[1:, :]
        lbl = labels[1:, :]
        print("image shape:", img.shape)
        print("label shape:", lbl.shape)
        print("\n")
        print("forward images num:", num_list[0])
        print("forward left images num:", num_list[1])
        print("forward right images num:", num_list[2])
        print("stop sign images num:", num_list[3])
        # 保存数据
        if not os.path.exists(self.data_path):
            os.mkdir(self.data_path)
        try:
            np.savez(self.data_path + '/' + self.saved_file_name + '.npz', train=img, train_labels=lbl, num_list=num_list)
        except IOError as e:
            print(e)


if __name__ == '__main__':
    CollectTrainingData()

