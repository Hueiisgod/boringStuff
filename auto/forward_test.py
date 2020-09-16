import numpy as np
import time

from robotPi import robotPi
import cv2
import os

def auto_pilot():
    #datetime = datetime()
    robot = robotPi()
    t1 = time.time()
    i1=0
    i2=0
    t2=t1+1
    #endtime = time.ctime() + 5
    while t2 >= time.time():
         #print (time.ctime())
        #robot = robotPi()
         robot.movement.move_forward()
         print(1)
    
    while i1  < 282:
        robot.movement.right_ward()
        i1 = i1 + 1
        print(i1)
    
    t3=time.time()
    t4=t3+2.5
    while t4 >= time.time():
        robot.movement.move_forward()
    
    while i2  < 287:
        robot.movement.right_ward()
        i2= i2 + 1
        print(i2)
    #print(2)
        
    t5=time.time()
    t6=t5+1
    while t6 >= time.time():
        robot.movement.move_forward(85)
        
        
    
    i2=0
    while i2  < 280:
        robot.movement.left_ward()
        i2= i2 + 1
        print(i2)
    
    
    t6=0
    t5=time.time()
    t6=t5+1
    while t6 >= time.time():
        robot.movement.move_forward(35)
        
    i2=0
    while i2  < 140:
        robot.movement.left_ward()
        i2= i2 + 1
        print(i2)
   
        #break;
#while(1):
 #   robot.movement.right_ward()

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






