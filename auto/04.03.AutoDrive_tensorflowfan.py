import numpy as np
import time
import tensorflow as tf
from robotPi import robotPi
import cv2
import os
from rev_cam import rev_cam


# 1:[1,0,0,0]
# 2:[0,1,0,0]
# 3:[0,0,1,0]
# 4:[0,0,0,1]


width = 480
height = 180
channel = 1
inference_path = tf.Graph()
#filepath = os.getcwd() + '/model/auto_drive_model/_983'
filepath = os.getcwd() + '/model/auto_drive_model/-24'


temp_image = np.zeros(width * height * channel, 'uint8')


def auto_pilot():
    # a = np.array(frame, dtype=np.float32)
    # _, prediction = model.predict(a.reshape(1, width * height))
    cap = cv2.VideoCapture(0)
    robot = robotPi()

    with tf.Session(graph=inference_path) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        saver = tf.train.import_meta_graph(filepath + '.meta')
        saver.restore(sess, filepath)

        tf_X = sess.graph.get_tensor_by_name('input:0')
        pred = sess.graph.get_operation_by_name('pred')
        number = pred.outputs[0]
        prediction = tf.argmax(number, 1)

        stop_count=0
        while cap.isOpened():
            ret, frame = cap.read()
            frame = rev_cam(frame)
            resized_height = int(width * 0.75)
            
            frame = cv2.resize(frame, (width, resized_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # slice the lower part of a frame
            res = frame[resized_height - height:, :]
            cv2.imshow("frame", res)
            #cv2.waitKey(1)
            frame = np.array(res, dtype=np.float32)
            value = prediction.eval(feed_dict={tf_X: np.reshape(frame, [-1, height, width, channel])})
            print('img_out:', value)
    
            if value == 0:
                print("forward")
                robot.movement.move_forward(36,times=300)
            elif value == 1:
                print("left")
                robot.movement.left_ward()
            elif value == 2:
                print("right")
                robot.movement.right_ward()
            elif value == 3:
                print("stop sign")
                stop_count += 1
                if stop_count == 20:
                    robot.movement.hit()
                    robot.movement.move_forward(0,times=500)
#                    robot.movement.hit()
                    break
                else:
                    robot.movement.move_forward(36,times=300)
            
            elif cv2.waitKey(1) & 0xFF ==ord('q'):
                break
            else:
        #cv2.destroyAllWindows()
            #elif value == 4:
                #print("Banner forward")
                #robot.movement.move_forward(25,times=300)                
            #elif value == 5:
                #print("Banner left")
                #robot.movement.left_ward()                
            #elif value == 6:
                #print("Banner right")   
                #robot.movement.right_ward()               
            #elif cv2.waitKey(1) & 0xFF ==ord('q'):
                break
        cv2.destroyAllWindows()
            
        

if __name__ == '__main__':

    ###############################################################
    # startTime=datetime.datetime.now()
    ###############################################################
    auto_pilot()
    # time.sleep(0.5)
    ##############################################################
    # endTime=datetime.datetime.now()
    # print(endTime-startTime)
    ###############################################################





