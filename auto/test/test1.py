import cv2

cap = cv2.VideoCapture(0)
#cap.set(3, 1600)
#cap.set(4, 1200)
# 140 degree cap size:639*479


while cap.isOpened():
    _, res = cap.read()
    cv2.imshow('frame', res)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):

        break

cap.release()
cv2.destroyAllWindows()