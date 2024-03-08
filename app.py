import os
import uuid

import cv2
from flask import Flask, render_template, request, Response
from flask_basicauth import BasicAuth
from ultralytics import YOLO

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())
if not os.getenv('WDS_USERNAME') or not os.getenv('WDS_PASSWORD'):
    print('NO WDS_USERNAME or WDS_PASSWORD')
    exit(1)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('WDS_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('WDS_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')


def gen_frames(source):
    cap = cv2.VideoCapture(source)
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


@app.get('/video_feed')
def video_feed():
    source = request.args.get('source')
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(source),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
