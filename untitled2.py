# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 08:45:26 2018

@author: Sophia
"""
import cv2
import numpy as np
import urllib
url = r'https://larspsyll.files.wordpress.com/2018/06/unicorn.jpg?w=270&h=270'
req = urllib.request.urlopen(url)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr,-1)
cv2.imshow('image',img)
cv2.waitKey(0)