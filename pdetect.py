import numpy as np
from matplotlib import pyplot as plt
import cv2
import io
import time
import random

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# Camera stream
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
# Video stream (optional, not tested)
# cap = cv2.VideoCapture("video.mp4")
# Image crop
# x, y, w, h = 800, 500, 100, 100
# x, y, w, h = 950, 300, 100, 100
heartbeat_count = 128
heartbeat_values = [0]*heartbeat_count
heartbeat_times = [time.time()]*heartbeat_count
# Matplotlib graph surface
# fig = plt.figure()
# ax = fig.add_subplot(111)
#while True:
def out(cap,heartbeat_values,heartbeat_times):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # print('x,y',x,y)
    # print(w,h)
    try:
        crop_img = img[y:y+50,x+50:x+100] #[y:y + h, x:x + w]
    except:
        crop_img = img
    # Update the data
    heartbeat_values = heartbeat_values[1:] + [np.average(crop_img)]
    heartbeat_times = heartbeat_times[1:] + [time.time()]
    # Draw matplotlib graph to numpy array
    #heartbeat_values = [random.uniform(68,72) for i in range(128)]
    #print(heartbeat_values)
    # ax.plot(heartbeat_times, heartbeat_values)
    # fig.canvas.draw()
    # plot_img_np = np.fromstring(fig.canvas.tostring_rgb(),dtype=np.uint8, sep='')
    # plot_img_np = plot_img_np.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    # plt.cla()
    cv2.putText(img=img, text='BPM:'+str(heartbeat_values[-1]), org=(450,27), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
    ret, jpeg = cv2.imencode('.jpg', img)
    # cv2.imshow('Graph', plot_img_np)
    return jpeg.tobytes()
    # Display the frames
    cv2.imshow('orignal', img)
    cv2.imshow('Crop', crop_img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
cap.release()
cv2.destroyAllWindows()