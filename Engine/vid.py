import cv2
import numpy as np
import tensorflow as tf
import imgproc as proc
import pytesseract as ts
from PIL import Image
from Detector.Detector import LPDetector

graph_path = 'inference_graphs/license_plate_graph.pb'
detector = LPDetector(graph_path)

video_path = 'videos/20190325_161049.mp4'
cap = cv2.VideoCapture(video_path)

# speed up
frameCtr = 0

while cap.isOpened():
    _, frame = cap.read()
    frameCtr += 1
    frame = proc.rotate(frame)
    if frameCtr % 10 == 0:
        frameCtr = 0
        license_plates = detector.detect(frame, 0.3)

        for lp in license_plates:
            p1, p2 = lp
            roi = proc.getROI(frame, p1, p2)
            cv2.imshow('orig', roi)
            # proc.draw(frame, p1, p2)
            roi = proc.unlock(roi)
            roi = proc.findLargestContour(roi)

            s = ts.image_to_string(Image.fromarray(roi))
            print(s)
            cv2.imshow('roi', roi)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

cap.release()
cv2.destroyAllWindows()
