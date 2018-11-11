# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:21:48 2018

@author: Home
"""
import cv2
#Need to install this module by opening a anaconda prompt as administrator and
#executing
#conda install imageio
import imageio

# Methods #############################################################

def read_gif(gifname):
    ## Read the gif from disk to `RGB`s using `imageio.miread` 
    gif = imageio.mimread(gifname)
    nums = len(gif)
    print("Total %d frames in the gif!" % nums)
    
    # convert form RGB to BGR 
    gif = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    return gif, nums

# Main code ############################################################
# Run: you'll see a played gif 
    
# Read the gif and number of frames in the gif
gif, nums = read_gif('A.gif')  # Put the name of the gif file you want to load
gif_counter = 0 

while True:
    # VERY IMPORTANT: must wait 100 miliseconds or the gif will play too fast
    key = cv2.waitKey(100) 
    if key % 256 == 27:
        break    


    # Sohw the current frame (the frame number gif_counter) from the gif
    cv2.imshow("gif", gif[gif_counter])
    # Increment the counter to the next gif frame. IF reached last frame, reset to 0
    gif_counter = (gif_counter + 1)%nums
    
cv2.destroyAllWindows()