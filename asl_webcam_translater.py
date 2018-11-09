# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:18:33 2018

@author: Sophia
"""

import cv2, requests, base64

# Gets an image from the webcam
def getWebcamImageData():
    cam = cv2.VideoCapture(0)
    try:
        ok, image = cam.read()
        if ok != True:
            raise ValueError("Problem using the webcam")
        ok, data = cv2.imencode('.jpg', image)
        if ok != True:
            raise ValueError("Problem getting image data")
        return base64.b64encode(data).decode('utf-8')
    finally:
        cam.release()


# This function will pass your image to the machine learning model
# and return the top result with the highest confidence
def classify(image):
    ok, data = cv2.imencode('.jpg', image)
    encode = base64.b64encode(data).decode('utf-8')

    key = "061f2690-e261-11e8-bd97-538b787f5ee8690968f8-e397-4996-a6f7-ffccd06385bc"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : encode })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

def classify_result(image):
    demo = classify(image)
    label = demo["class_name"]
    confidence = demo["confidence"]
    
    
    # CHANGE THIS to do something different with the result
    return "result: '%s' with %d%% confidence" % (label, confidence)
            
