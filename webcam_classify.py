# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:13:46 2018

@author: Home
"""

import cv2
import numpy as np
import requests
import base64
from os import startfile
from timeit import default_timer as timer
import imageio

# Parameters ################################################################

cv_blue = (255,0,0)
cv_red = (0,0,255)
cv_purple = (204,0,102)

height = 480
width = 640

# Frame is just a black frame:
background = blank_image = np.zeros((height,width,3), np.uint8)

gif = None
gif_counter = 0

#Set the timer of the last event to 20sec ago
last_event = timer() - 20

'''
Filters to select skin color based on HSV color encoding

color1 = [0, 30=limit_brown] 
color2 = [165=limit_pink, 179]

l = [color, 0, limit_light]
h = [color, limit_dark, 255]
'''

l1_skin_hsv = np.array([0,0,70], dtype = 'uint8')
h1_skin_hsv = np.array([30,180,255], dtype = 'uint8')

l2_skin_hsv = np.array([165,0,70], dtype = 'uint8')
h2_skin_hsv = np.array([179,180,255], dtype = 'uint8')

cam = cv2.VideoCapture(0)
cv2.namedWindow("test", cv2.WINDOW_NORMAL)
cv2.resizeWindow('test', 640, 480)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
cv2.resizeWindow('mask', 640, 480)

# Methods ####################################################################

def put_text(img, x, y, text, color):
    '''Write text on the image
    Modifies the paramter image. No return necessary
    '''
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2 #change thickness
    boxsize, baseline = cv2.getTextSize(text, fontFace, fontScale, thickness)
    cv2.putText(img, text, (x,y + boxsize[1]), fontFace, fontScale, color, thickness)
    

def classify(image, key):
    '''This function will pass your image to the machine learning model
    and return the top result with the highest confidence
    '''
    ok, data = cv2.imencode('.jpg', image)
    encode = base64.b64encode(data).decode('utf-8')
    #The key is kept in a configuration file
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : encode })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

def classify_result(image, key):
    '''Calls image classifier and extract label, confidence
    '''
    demo = classify(image, key)
    label = demo["class_name"]
    confidence = demo["confidence"]
    return label, confidence
        
def print_avg_color(frame, show_frame):
    ''' Assumes the frame size is 640x480
    Compute the HSV color average for all pixels in the center image area
    '''
    top_left = (200,150)
    bottom_right = (440,330)
    frame_roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    average_color = [frame_roi[:, :, i].mean() for i in range(frame_roi.shape[-1])]
    print(average_color)
    # Draw on image
    cv2.rectangle(show_frame,top_left,bottom_right,cv_red, 1)
    
def select_skin(frame):
    ''' Select area with skin color based on HSV filters
    Returns the selected area, black (0) for the remaining image
    '''
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv_img, l1_skin_hsv, h1_skin_hsv)
    mask2 = cv2.inRange(hsv_img, l2_skin_hsv, h2_skin_hsv)
    mask = np.maximum(mask1, mask2)
    
    output = cv2.bitwise_and(frame, frame, mask = mask)
    return output

def insert_into(bigframe, smallframe, width, height, x, y):
    ''' Resizes the smallframe to dimensions (Width,height)
    Inserts smallframe into bigframe at the position x,y
    '''
    #Resize the insert to a specific size
    resized = cv2.resize(smallframe, (width, height)) # width, height
    # Insert the resized into bigframe
    bigframe[y:y+height, x:x+width] = resized

def read_gif(gifname):
    ## Read the gif from disk to `RGB`s using `imageio.miread` 
    gif = imageio.mimread(gifname)
    nums = len(gif)
    print("Total %d frames in the gif!" % nums)
    
    # convert form RGB to BGR 
    gif = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    return gif, nums

# %%
    
# Main code ###################################################################

class_on, sound_on = False, False
# 0 - represents the current classification, 1 - the previous classification
confidence0, confidence1 = 0, 0
label0, label1 = '', ''
text0, text1 = '', '' 
help_text = 'Press space to classify your hand sign'

with open('key.txt') as f:
    key = f.read()

while True:
    # 1 Read frame, break if no frame available
    ret, frame = cam.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)

    # 2 Check user input
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    if k ==  32:
        #space pressed turn on classifier
        class_on =  not class_on

    background_text = background.copy()
    insert_into(background_text, frame, 320, 240, 160, 120)
    '''
    h,w = frame.shape[:2]
    h,w = int(h/4), int(w/4)
    small = cv2.resize(frame, (w, h))
    '''
    
    hand = select_skin(frame)
    
    # 3 Run classifier if needed
    if class_on:
        class_on = False # Only run the classifier once
        # The current classification becomes the previous classification
        label1, confidence1 = label0, confidence0  
        # Get the current classification
        label0, confidence0 = classify_result(hand, key)
        if label0:
            text0 = "Result  : '%s' with %d%% confidence" % (label0, confidence0)
        if label1:
            text1 = "Previous: '%s' with %d%% confidence" % (label1, confidence1)
        sound_on = True
        
        #Download the gif corresponding to the last label:
        c = label0.lower()
        if c in ['a','b','c']:
            gif, nums = read_gif(c + '.gif')
            gif_counter = 0
        
        #Set the time of the last event:
        last_event = timer()
    #END classification block

    # 4 Display images and text 
    put_text(frame, 10, 10, help_text, cv_purple)
    put_text(frame, 10, 40, text0, cv_red)
    put_text(frame, 10, 70, text1, cv_red)

    #Add gif insertion if we have a gif and not too much time passed
    time_passed = timer() - last_event
    if gif and time_passed < 6:  # play gif for 10 seconds
        gif_frame = gif[gif_counter]
        gif_counter = (gif_counter + 1)%nums
        insert_into(frame, gif_frame, 160, 160, 440, 280)
    
    cv2.imshow("test", frame)
    cv2.imshow("mask", hand)
    
    # 5 Play sound file if needed
    #c = chr(k)  # use this instead to test the sound files
    c = label0.lower()
    if sound_on:
        sound_on = False  # only play the audio file once per clasification
        #if confidence0 >= 60:  # use this if we only accept high confidence classifications            
        if c in ['a','b','c']:  # update this if we add new classes       
            #pass
            startfile(c + '.mp4')
            # TODO: For complex signals add elif which tests both label0 and label1 
        elif label1 == 'NO1' and label0 == 'NO2':
            pass
            startfile('no.mp4')
            
    
# Release resources        
cam.release()
cv2.destroyAllWindows()