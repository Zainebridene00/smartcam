import tkinter as tk
import os
from PIL import Image, ImageTk

import sys


root = tk.Tk()
def alg1():
   os.system('python algo1.py')
def alg2():
   os.system("source test/bin/activate")
   os.system("python detect_mask_video.py")
def alg3():
   os.system('python door.py')
def alg4():
   sys.exit(0)



   signal.signal(signal.SIGINT, signal_handler)

root.title("Smart-Cam GUI")
canvas = tk.Canvas(root,height = 530,width = 530)
canvas.pack()

bgimg = Image.open('are.png')
img = ImageTk.PhotoImage(bgimg)
bglabel = tk.Label(root, image = img)
bglabel.place(relwidth = 1,relheight = 1)



frame = tk.Frame(root, bg ="#1d1c18")
frame.place(relx = 0.1, rely = 0.55,relwidth = 0.8,relheight=0.3)
button1 = tk.Button(frame, text ="Face Recognition", command = alg1, bg = "#1d1c18", fg = "#ffd148")
button1.place(relx = 0.025,rely = 0.1,relwidth = 0.3,relheight = 0.3)
button2 = tk.Button(frame, text ="Mask Detection", command = alg2, bg = "#1d1c18", fg = "#ffd148")
button2.place(relx = 0.35,rely = 0.1,relwidth = 0.3,relheight = 0.3)
button3 = tk.Button(frame, text ="Door State", command = alg3 , bg = "#1d1c18", fg = "#ffd148")
button3.place(relx = 0.675,rely = 0.1,relwidth = 0.3,relheight = 0.3)
button4 = tk.Button(frame, text ="Stop", command = alg4, bg = "#1d1c18", fg = "#ffd148")
button4.place(relx = 0.35,rely = 0.7,relwidth = 0.3,relheight = 0.3)

root.mainloop()