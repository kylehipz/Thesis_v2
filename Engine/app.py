from flask import Flask, render_template, Response, session, redirect, url_for, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import numpy as np
import cv2
import tensorflow as tf
import pytesseract as ts
from PIL import Image
from Detector.Detector import LPDetector
from camera import VideoCamera
import imgproc as proc
from datetime import datetime
import pymongo
import string
import random

# load detector
detector = LPDetector('inference_graphs/license_plate_graph.pb')


# add database connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.test

app = Flask(__name__)

def rand():
    return random.choice(string.ascii_letters)

def hanash(string):
    # hashing for password
    h = hashlib.md5(bytes(string, encoding='utf-8'))
    return h.hexdigest()


def gen(camera, entrance):
    """
    Camera live feed
    """
    prev_text = ""
    ctr = 0
    frame_ctr = 0
    while True:
        frame = camera.get_frame()
        frame = proc.rotate(frame)
        # frame = cv2.resize(frame, (640, 480))
        frame_ctr += 1
        
        # every 10 frames predict
        if frame_ctr > 1:
            lps = detector.detect(frame, 0.3)
            if len(lps) > 0:
                if ctr == 4:

                    # if prev_text is blank, continue
                    if prev_text == '':
                        ctr = 0
                        continue

                    # add to the database
                    image_path = ""

                    for i in range(11):
                        image_path += rand()

                    image_path = hanash(image_path)

                    # check if homeowner
                    owner = db.homeowners.find_one({"plate_number":prev_text})
                    visitor = "No" if owner else "Yes"

                    Log = {"plate_number": prev_text,
                            "image_path": image_path,
                           "entrance": 1,
                           "visitor": visitor,
                           "owner": owner.name if owner else "Unknown",
                           "date_recorded": datetime.now()}

                    db.logs.insert_one(Log)
                    prev_text = ""
                    ctr = 0

                    # save image
                    cv2.imwrite(f'../Infra/public/license_plates/{image_path}.jpg', frame)

            # reset frame counter to 0
            frame_ctr = 0

            for lp in lps:
                p1, p2 = lp;
                cur_text = proc.process(frame, p1, p2)
                print(cur_text)
                cv2.putText(frame, cur_text, p1, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                if prev_text == "":
                    prev_text = cur_text
                elif prev_text == cur_text:
                    ctr += 1
                else:
                    ctr = 0
                    prev_text = cur_text
                proc.draw(frame, p1, p2)
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen(VideoCamera('videos/20190325_161049.mp4'), 1),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(gen(VideoCamera('videos/20190325_161205.mp4'), 0),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
