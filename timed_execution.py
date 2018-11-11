# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 10:16:55 2018

@author: Home
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:21:48 2018

@author: Home
"""
import cv2
from timeit import default_timer as timer
import numpy as np

height = 480
width = 640
cv_blue = (255,0,0)

# Frame is just a black frame:
frame = blank_image = np.zeros((height,width,3), np.uint8)

# MEthods ##############################################################

def put_text(img, x, y, text, color):
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 1
    boxsize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    cv2.putText(img, text, (x,y + boxsize[1]), fontFace, thickness, color) 


# Main code ############################################################
# Run and press space.
# Each time, a rectagle will display for 3 seconds after pressing space
# Could be a  gif or an insert also :P

# Set the last event 20 seconds ago
# timer() gets the current time, in seconds
last_event = timer() - 20

while True:
    key = cv2.waitKey(1)
    if key % 256 == 27:
        break    
    if key == 32:
        #Set the last event to now
        last_event = timer()

    #Draw a rectangle if the last event was less than 3 secodns ago:

    frame_text = frame.copy()
    time_passed = timer() - last_event
    if time_passed < 3:
        #IMPORTANT: we can insert an image or play a gif instead of drawing a rectangle
        text = 'Time passed: %f seconds' % time_passed
        put_text(frame_text, 10, 10, text, cv_blue)


        #cv2.rectangle(img,top_left,bottom_right,color,thickness)
        cv2.rectangle(frame_text,(240,180), (400,300), cv_blue, 1)


    # Show the current frame (the frame number gif_counter) from the gif
    cv2.imshow("gif", frame_text)

    
cv2.destroyAllWindows()