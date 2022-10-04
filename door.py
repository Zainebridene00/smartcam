import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
import cv2
import time
import threading
from multiprocessing import Process, Pipe, Event

image_size = (180, 180)
model = load_model("door.h5")


def CaptureProcess(pipe, read_ev):
    while True:
        video = None

        def read_th():
            success = False
            while True:
                if (success): read_ev.wait()
                while video is None or not video.isOpened(): pass
                success, imageFrame = video.read()
                if (success):
                    pipe.send(imageFrame)

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

            elif (not read_ev.is_set()):
                video.grab()


class InferThread(threading.Thread):
    def __init__(self):
        super(InferThread, self).__init__()
        self.daemon = True

    def run(self):
        global cap_read_ev, cap_pipe
        while True:
            cap_read_ev.set()
            frame = cap_pipe.recv()
            cap_read_ev.clear()


            door = cv2.resize(frame, image_size)

            # Afficher le cadre résultant
            cv2.imshow('frame', frame)
            """img = keras.preprocessing.image.load_img("testDoor/testopen7.jpeg", target_size=image_size)"""

            img_array = keras.preprocessing.image.img_to_array(door)
            img_array = tf.expand_dims(img_array, 0)

            predictions = model.predict(img_array)
            score = predictions[0]
            print(
                "This image is %.2f percent Closed and %.2f percent Open."
                % (100 * (1 - score), 100 * score)
            )
            # Si vous appuyez sur Q, quittez le script
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break




cap_pipe, cap_child_pip = Pipe()
cap_read_ev = Event()
cap_read_ev.set()

infer_th = InferThread()

cap_process = Process(target=CaptureProcess, args=(cap_child_pip, cap_read_ev))
cap_process.daemon = False
cap_process.start()

infer_th.start()
