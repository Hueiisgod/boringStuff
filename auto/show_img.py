import numpy as np
import time
import os


data = np.load('/mnt/Ubuntu/AutoDrive/python_project/auto/dataset/labeled_img_data_1550453606.npz')

num=data['train'].shape[0]

print("image:")
for i in range(num):
    print(data['train'][i])

print("labels:")
for i in range(num):
    print(data['train_labels'][i])

data.close()
