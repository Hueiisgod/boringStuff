import cv2


def rev_cam(frame):
    (h, w) = frame.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 180, 1)  # 旋转缩放矩阵：(旋转中心，旋转角度，缩放因子)
    rotated = cv2.warpAffine(frame, M, (w, h))
    return rotated

if __name__ == '__main__':
    import cv2

    cap = cv2.VideoCapture(0)
    # cap.set(3, 1600)
    # cap.set(4, 1200)
    # 140 degree cap size:639*479


    while cap.isOpened():
        _, res = cap.read()
        res = rev_cam(res)
        cv2.imshow('frame', res)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('q'):

            break
    cv2.destroyAllWindows()
    exit(0)
