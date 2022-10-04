import cv2
import numpy as np
import os
import datetime
import time
import threading
from tensorflow.keras.models import load_model
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
"""haar_model = os.path.join(cv2_base_dir,'data/haarcascade_frontalface_default.xml')"""
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
from multiprocessing import Process, Pipe, Event
model=load_model("Model_f2.h5")
def CaptureProcess(pipe, read_ev):

    while True:
        video = None
        def read_th():
            success = False

            while True:
                if(success):
                    read_ev.wait()

                while video is None or not video.isOpened():

                    pass
                success, imageFrame = video.read()
                if(success):

                    pipe.send(imageFrame)
                    print("send")


        r_th = threading.Thread(target=read_th)
        r_th.daemon = True
        r_th.start()

        while True:
            c = (video is None or not video.isOpened())
            if c:
                video = cv2.VideoCapture(0)
            c = (video is None or not video.isOpened())
            if c: 
                time.sleep(0.5)

            elif(not read_ev.is_set()):
                video.grab()
                print("grab")
class InferThread(threading.Thread):
    def __init__(self):
        super(InferThread, self).__init__()
        self.daemon = True
    def run(self):
        global cap_read_ev, cap_pipe
        while True:

            cap_read_ev.set()

            img = cap_pipe.recv()

            cap_read_ev.clear()

            gray=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            faces = face_cascade.detectMultiScale(gray,scaleFactor=1.2, minNeighbors=4)
            print(faces)
            for (x, y, w, h) in faces:
                crop_img = img[y:y+h, x:x+w]
                img_arr = cv2.resize(crop_img,(100,100))
                d=[]
                d.append(img_arr)
                data=np.array(d)
                predictions=model.predict(data)
                classes = np.argmax(predictions, axis = 1)
                if classes[0]==0:
                    cv2.rectangle(img, (x, y), (x+w, y+h),(0,255,0),2)
                else:
                    cv2.rectangle(img, (x, y), (x+w, y+h),(0,0,255), 2)

            cv2.imshow('img', img)
            key=cv2.waitKey(2)
            if key == ord('q'):
                break

cap_pipe, cap_child_pip = Pipe()
cap_read_ev = Event()
cap_read_ev.set()

infer_th=InferThread()

cap_process=Process(target=CaptureProcess, args=(cap_child_pip, cap_read_ev))
cap_process.daemon = False
cap_process.start()

infer_th.start()