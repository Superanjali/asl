# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:47:40 2018

@author: Home
"""

import cv2
import numpy as np

# Parameters ############################################################## 

cv_blue = (255,0,0)
height = 480
width = 640

# Frame is just a black frame:
frame = blank_image = np.zeros((height,width,3), np.uint8)

# Insert is a blue frame: create a black frame
insert = np.zeros((height,width,3), np.uint8)
#fill it with blue color
insert[:] = cv_blue

# Methods #################################################################

def insert_into(bigframe, smallframe, width, height, x, y):
    ''' Resizes the smallframe to dimensions (Width,height)
    Inserts smallframe into bigframe at the position x,y
    '''
    #Resize the insert to a specific size
    resized = cv2.resize(smallframe, (width, height)) # width, height
    # Insert the resized into bigframe
    bigframe[y:y+height, x:x+width] = resized
    

# Main code ###############################################################
# Run, you'll see a small image (blue) inserted into a bigger image (black)

while True:
    # This function the image 'insert' into the background image 'frame'
    frame_text = frame.copy()
    insert_into(frame_text, insert, 320, 240, 160, 120)
    
    cv2.imshow("demo", frame_text)
    key = cv2.waitKey(1) 
    if key % 256 == 27:
        break    

cv2.destroyAllWindows()
