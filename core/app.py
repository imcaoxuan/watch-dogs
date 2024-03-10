import os

import cv2
from flask import Flask, render_template, Response
from flask_apscheduler import APScheduler
from ultralytics import YOLO

import yolov8

app = Flask(__name__)
scheduler = APScheduler()


def get_frames():
    cap = cv2.VideoCapture(os.getenv('WDS_SOURCE'))
    model = YOLO(f'{os.getenv("WDS_MODEL")}.pt')
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        if success:
            # Run YOLOv8 inference on the frame

            results = model(frame)
            # Visualize the results on the frame10
            annotated_frame = results[0].plot()
            annotated_frame_ret, annotated_frame_buffer = cv2.imencode('.jpg', annotated_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + annotated_frame_buffer.tobytes() + b'\r\n')  # concat frame one by one and show result
        else:
            # Break the loop if the end of the video is reached
            break


@app.route('/start')
def start():
    scheduler.add_job(func=yolov8.start_monitoring, id='yolov8', replace_existing=True)
    if scheduler.running:
        scheduler.shutdown()
        print('shutdown')
    scheduler.start()
    print('start')
    return {}


@app.route('/shutdown')
def shutdown():
    if scheduler.running:
        scheduler.shutdown()
        print('shutdown')
    return {}


@app.get('/video-feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(get_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run('0.0.0.0', 5001)
