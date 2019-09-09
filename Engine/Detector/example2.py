
import cv2
import os
import numpy as np
from Detector import LPDetector
import tensorflow as tf

def draw(img, p1, p2):
    """
    Parameters
    ----------
    img : numpy array
        The image to be boxed on
    p1 : tuple
        Top left coordinate of the bounding box
    p2 : tuple
        Bottom right coordinate of the bounding box
    Returns
    -------
    """
    cv2.rectangle(img, p1, p2, (0, 255, 0), 2)

#loading our license plate detector
detector = LPDetector('../inference_graphs/license_plate_graph.pb')

cap = cv2.VideoCapture('../../../Desktop/thesis/videos/20190326_073207.mp4')
i = 0

while 1:
    _, img = cap.read()
    # print(_)
    img = cv2.resize(img, (640, 480))
    rows, cols = img.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), -90, 1)
    img = cv2.warpAffine(img, M, (cols, rows))
    i += 1
    # if (i%10 == 0):
    if i%100 == 0:
        lps = detector.detect(img, 0.3)
        i = 0
        for lp in lps:
            p1 = lp[0]
            p2 = lp[1]
            draw(img, p1, p2)
            roi = img[p1[1]:p2[1], p1[0]:p2[0]]
            cv2.imshow('roi', roi)

    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

