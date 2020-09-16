import cv2
from Welcome_face_detector import Face_Detector
from robotPi import robotPi
from robotpi_movement import Movement
import numpy as np

# give the name of the input video file
class welguy():
    def __init__(self):
        self.CAM_NUM = 0
        self.cap = cv2.VideoCapture(self.CAM_NUM)
        self.face = Face_Detector()
        self.robot = robotPi()
        self.mv = Movement()
    #self.mv.Movement.MoveModeSet(2)
    

        while self.cap.isOpened():
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            faceflow, faces = self.face.find_faces(frame, ret)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            retval,dst = cv2.threshold(gray,0,255,cv2.THRESH_OTSU)
            dst = cv2.dilate(dst,None,iterations=2)
            color = dst[400]
            cv2.imshow('frame',frame)
            white_count = np.sum(color == 255)
            white_index = np.where(color == 255)

            if white_count == 0:
               white_count = 1

            center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
              
            direction = center - 320
            print(direction)
            

            if abs(direction) > 150:
                self.robot.movement.turn_left()
                
            elif direction >= 180:
                self.robot.movement.turn_right(speed=3)
                if direction > 50:
                    direction = 50
                    self.mv.move_forward(times=3500)
                    self.robot.movement.turn_right()

            elif direction < -0:
                self.robot.movement.turn_left(speed=3)
                self.mv.move_forward(times=3500)

            # Display the resulting frame
            #cv2.imshow('Video', faceflow)
            #if len(faces) != 0:
                #print("Aholla~!!")
                #self.robot.movement.wave_hands()
            #elif len(faces) == 0:
                #print("move left and right to find people")
                #self.robot.movement.turn_right(speed=3)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break

        # When everything is done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    welcome_guy = welguy()
    exit(0)
