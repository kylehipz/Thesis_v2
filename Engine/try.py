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

@app.route('/live_feed')
def live_feed():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))
    return render_template('live_feed.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("admin") is not None:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html')

    else:
        username = request.form.get("username")
        password = request.form.get("password")

        password = hanash(password)
        admin = Admin.query.filter_by(username=username).first()
        if admin is None or password != admin.password:
            flash("Incorrect Credentials")
            return redirect(url_for('login'))
        else:
            session['admin'] = username
            return redirect(url_for('dashboard'))
    
@app.route('/dashboard')
def dashboard():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))

    return render_template('dashboard.html')

@app.route('/logs')
def logs():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))
    return render_template('logs.html')

@app.route('/logs/<_id>')
def see_log(_id):
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))
    
    log = Logs.query.filter_by(id=_id).first()
    return render_template('see_log.html', log=log)


@app.route('/admin')
def admin():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))
    
    admins = Admin.query.all()

    return render_template('admin.html', admins=admins)

@app.route('/admin/add', methods=['GET', 'POST'])
def add_admin():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('add_admin.html')
    else:
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if confirm != password:
            flash("Passwords do not match")
            return redirect(url_for('add_admin'))

        else:
            new_admin = Admin(name=name,
                              username=username,
                              password=hanash(password),
                              date_created=datetime.now())

            db.session.add(new_admin)
            db.session.commit()

            flash("Administrator account successfully created!")
            return redirect(url_for('admin'))

@app.route('/homeowners')
def homeowners():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))

    homeowners = db.session.query(Homeowners, VehicleTypes).join(VehicleTypes, Homeowners.vehicle_type==VehicleTypes.id).all()

    return render_template('homeowners.html', homeowners=homeowners)

@app.route('/homeowners/add', methods=['GET', 'POST'])
def add_homeowner():
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))

    if request.method == 'GET':
        vehicle_types = VehicleTypes.query.all()
        return render_template('add_homeowner.html', vehicle_types=vehicle_types)
    else:
        name = request.form.get("name")
        address = request.form.get("address")
        contact_number = request.form.get("contact_number")
        conduction_number = request.form.get("conduction_number")
        plate_number = request.form.get("plate_number")
        vehicle_type = request.form.get("vehicle_type")
        model = request.form.get("model")

        homeowner = Homeowners(name=name,
                               address=address,
                               plate_number=plate_number,
                               contact_number=contact_number,
                               conduction_number=conduction_number,
                               vehicle_type=int(vehicle_type),
                               model=model,
                               date_registered=datetime.now())

        db.session.add(homeowner)
        db.session.commit()
        flash("Homeowner successfully added!")
        return redirect(url_for('homeowners'))


@app.route('/homeowners/<name>')
def homeowner(name):
    if session.get("admin") is None:
        flash('You need to log in first')
        return redirect(url_for('login'))

    return render_template('homeowner.html')

@app.route('/logout')
def logout():
    session.pop("admin")
    return redirect(url_for('login'))

@app.route('/get_logs')
def get_logs():
    # instantiate data
    LOGS = []
    # get logs
    logs = Logs.query.order_by(db.desc(Logs.date_time)).all()

    for log in logs:
        data = dict()
        owner = Homeowners.query.filter_by(plate_number=log.plate_number).first()
        data['plate_number'] = log.plate_number
        if owner is None:
            data['visitor'] = 'Yes'
            data['owner'] = 'Unknown'
        else:
            data['visitor'] = 'No'
            data['owner'] = owner.name
        data['status'] = 'Entrance' if log.entrance else 'Exit'
        data['date'] = log.date_time
        LOGS.append(data)

    return jsonify(LOGS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



