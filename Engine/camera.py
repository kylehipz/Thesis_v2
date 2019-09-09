import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self, path = 0):
        self.cap = cv2.VideoCapture(path)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        _, frame = self.cap.read()
        return frame
