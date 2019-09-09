from flask import Flask, render_template, Response, session, redirect, url_for, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
from copy import deepcopy
import numpy as np
import cv2
import tensorflow as tf
import pytesseract as ts
from PIL import Image
from Detector.Detector import LPDetector
from camera import VideoCamera
import imgproc as proc
from models import *
from datetime import datetime

detector = LPDetector('inference_graphs/license_plate_graph.pb')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SSS.db'
app.secret_key = b'AKO ANG HARI NG TUGMA'
db = SQLAlchemy(app)

def hanash(string):
    h = hashlib.md5(bytes(string, encoding='utf-8'))
    return h.hexdigest()


def gen(camera, entrance):
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
                    datenow = datetime.now()
                    image_path = "".join(str(datenow).split(" "))
                    image_path = "".join(image_path.split("-"))
                    image_path = "".join(image_path.split(":"))
                    image_path = "".join(image_path.split("."))
                    image_path = f"{image_path}.jpg"
                    log = Logs(plate_number=prev_text, date_time=datenow, image_path=image_path, entrance=entrance)
                    db.session.add(log)
                    db.session.commit()
                    prev_text = ""
                    ctr = 0
                    cv2.imwrite(f"license_plates/{image_path}", frame)

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
