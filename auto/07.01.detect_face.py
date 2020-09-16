import os
import sys
import cv2
import numpy as np

def read_images(path, sz=None):
    """Reads the images in a given folder, resizes images on the fly if size is given.
 
    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        sz: A tuple with the size Resizes
 
    Returns:
        A list [X,y]
 
            X:  The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
    """
    c = 0
    X,y = [], []
    names=[]
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    if (filename == ".directory"):
                        continue
                    filepath = os.path.join(subject_path, filename)
                    im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
                    if (im is None):
                        print ("image " + filepath + " is none" )
                     
                    # resize to given size (if given)
                    if (sz is not None):
                        im = cv2.resize(im, sz)
                         
                    X.append(np.asarray(im, dtype=np.uint8))
                    y.append(c)
                except:
                    print ("Unexpected error:", sys.exc_info()[0])
                    raise
            c = c+1
            names.append(subdirname)       #添加对应的目录名称
    return [names,X,y]
     
def face_rec():
 
    read_dir = "./data";
 
    # Now read in the image data. This must be a valid path!
    [names,X,y] = read_images(read_dir)
     
    # Convert labels to 32bit integers. This is a workaround for 64bit machines,
    # because the labels will truncated else. This will be fixed in code as
    # soon as possible, so Python users don't need to know about this.
    # Thanks to Leo Dirac for reporting:
    y = np.asarray(y, dtype=np.int32)
         
    # Create the Eigenfaces model. We are going to use the default
    # parameters for this simple example, please read the documentation
    # for thresholding:
     
    #https://docs.opencv.org/3.0-beta/modules/face/doc/facerec/facerec_api.html?highlight=eigenfacerecognizer#Ptr<FaceRecognizer> createEigenFaceRecognizer(int num_components , double threshold)
    #注意:此函数新版发生变化
    model = cv2.face_EigenFaceRecognizer.create()
     
    #Fisherfaces的人脸识别
    #model = cv2.face_FisherFaceRecognizer.create()
     
    # Read
    # Learn the model. Remember our function returns Python lists,
    # so we use np.asarray to turn them into NumPy lists to make
    # the OpenCV wrapper happy:
    model.train(np.asarray(X), np.asarray(y))
     
    camera = cv2.VideoCapture(0)
     
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
     
    while(True):
         
        read, img = camera.read()    
         
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
         
        for (x,y,w,h) in faces:
             
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
             
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
            roi = gray[x:x+w, y:y+h]
             
            try:
                roi = cv2.resize(roi,(200,200),interpolation=cv2.INTER_LINEAR)
                
                # model.predict is going to return the predicted label and the associated confidence:
                [p_label, p_confidence] = model.predict(roi)       
                 
                # Print it:
                print ("Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence))
                 
                #show name
                cv2.putText(img,names[p_label],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
            except:
                continue
        cv2.imshow("camera", img)
        if cv2.waitKey(100) & 0xff == ord("q"):
          break
    camera.release()
    cv2.destroyAllWindows()   
 
if __name__ == "__main__":
    face_rec()