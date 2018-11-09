# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:13:46 2018

@author: Home
"""

import cv2
import numpy as np

# Parameters ################################################################

param_filename = 'webcam_capture_counter.txt'
cv_blue = (255,0,0)
cv_red = (0,0,255)

l1_skin_hsv = np.array([0,0,70], dtype = 'uint8')
h1_skin_hsv = np.array([30,180,255], dtype = 'uint8')

l2_skin_hsv = np.array([165,0,70], dtype = 'uint8')
h2_skin_hsv = np.array([179,180,255], dtype = 'uint8')


cam = cv2.VideoCapture(0)
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
#cv2.resizeWindow('test', 1280, 960)
cv2.resizeWindow('test', 640, 480)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask', 640, 480)

# Methods ####################################################################

def put_text(img, x, y, text, color):
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 1
    boxsize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    cv2.putText(img, text, (x,y + boxsize[1]), fontFace, thickness, color) 
    
def print_avg_color(frame, show_frame):
    #Assumes the frame size is 640x480
    top_left = (200,150)
    bottom_right = (440,330)
    frame_roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    average_color = [frame_roi[:, :, i].mean() for i in range(frame_roi.shape[-1])]
    print(average_color)
    # Draw on image
    cv2.rectangle(show_frame,top_left,bottom_right,cv_red, 1)
    
def select_skin(frame):
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv_img, l1_skin_hsv, h1_skin_hsv)
    mask2 = cv2.inRange(hsv_img, l2_skin_hsv, h2_skin_hsv)
    mask = np.maximum(mask1, mask2)
    
    output = cv2.bitwise_and(frame, frame, mask = mask)
    return output

# Main code ###################################################################
 
# Read the last img_Counter from file if it exists
img_counter = 0
img_name = ''

with open(param_filename) as f:
    img_counter = int(f.read())

while True:
    ret, frame = cam.read()
    if not ret:
        break

    #h,w = frame.shape[:2]
    #frame = cv2.resize(frame, (2*w, 2*h))
    frame = cv2.flip(frame, 1)
    frame_text = frame.copy()
    put_text(frame_text, 10, 10, 'helo', cv_blue)
    put_text(frame_text, 10, 40, img_name, cv_red)
    
    cv2.imshow("test", frame_text)
    hand = select_skin(frame)
    cv2.imshow("mask", hand)
    

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        #save the last counter
        with open(param_filename,'w') as f:
            f.write(str(img_counter))
        break
    if k<0: 
        continue
    c = chr(k)
    if c.isalnum():
        print(k,c)
        #printable key pressed, take a photo
        img_name = '%s_frame_%d.png' % (c,img_counter)
        cv2.imwrite(img_name, frame)
        
        img_name = '%s_skin_%d.png' % (c,img_counter)
        cv2.imwrite(img_name, hand)
        
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()