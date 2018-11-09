# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 18:12:53 2018

@author: Sophia
"""

import requests

# Gets the contents of an image file to be sent to the
# machine learning model for classifying
def getImageFileData(locationOfImageFile):
    with open(locationOfImageFile, "rb") as f:
        data = f.read()
        return data.encode("base64")


# This function will pass your image to the machine learning model
# and return the top result with the highest confidence
def classify(imagefile):
    key = "061f2690-e261-11e8-bd97-538b787f5ee8690968f8-e397-4996-a6f7-ffccd06385bc"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : getImageFileData(imagefile) })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


# CHANGE THIS to the name of the image file you want to classify
demo = classify("c_frame_6.png")

label = demo["class_name"]
confidence = demo["confidence"]


# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))