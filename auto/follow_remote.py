import cv2
import sys

class Track_you():
    def __init__(self):
        self.bias = 0.
        self.tracker = cv2.TrackerKCF_create()
        # Read self.video
        self.video = cv2.VideoCapture(0)
        print(self.video.get(3), self.video.get(4))
        bbox = (int(self.video.get(3)*0.25), int(self.video.get(4)*0.25), int(self.video.get(3)*0.5), int(self.video.get(4)*0.5))

        # Exit if self.video not opened.
        if not self.video.isOpened():
            print("Could not open self.video")
            sys.exit()

        # Read first frame.
        ok, frame = self.video.read()
        if not ok:
            print('Cannot read self.video file')
            sys.exit()
        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(frame, bbox)

    def track(self, frame):

        # Read a new frame
        # frame = self.s.recvfrom(65535)

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = self.tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            self.bias = self.video.get(3)/2. - (bbox[0] + bbox[2]/2.)
            print('bias:', self.bias)
        else:
            # Tracking failure
            self.bias = None
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        cv2.putText(frame, "KCF Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display result
        cv2.imshow("Tracking", frame)
        return self.bias
        # Exit if ESC pressed
        # k = cv2.waitKey(1) & 0xff
        # if k == 27:
        #     break


