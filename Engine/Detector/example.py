import cv2
import os
import numpy as np
from Detector import LPDetector
import tensorflow as tf

def draw(img, p1, p2):
    cv2.rectangle(img, p1, p2, (0, 255, 0), 2)

#loading our license plate detector
detector = LPDetector('../inference_graphs/license_plate_graph.pb')

#iterate over images in the test_images directory and then detect
for pic in os.listdir('test_images'):
    img = cv2.imread(os.path.join('test_images', pic))

    # Actual detector object
    license_plates = detector.detect(img, 0.3)
    
    for lp in license_plates:

        draw(img, lp[0], lp[1])
        # cv2.rectangle(img, (tlx, tly), (brx, bry), (0, 255, 0), 2)
        # roi = img[tly:bry, tlx:brx]

    cv2.imshow('Detected', img)
    cv2.waitKey()

cv2.destroyAllWindows()

