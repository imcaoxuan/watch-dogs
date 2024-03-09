import os
import time
from datetime import datetime

import cv2
import requests
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO(f'{os.getenv("WDS_MODEL")}.pt')


def start_pushing():
    dt = datetime.now()
    print('start_recording', dt)
    session = requests.session()
    while True:
        try:
            source = os.getenv('WDS_SOURCE')
            cap = cv2.VideoCapture(source)
            while cap.isOpened():
                success, frame = cap.read()
                if success:
                    results = model(frame, verbose=False)
                    annotated_frame = results[0].plot()
                    annotated_frame = cv2.resize(annotated_frame, (1920, 1080))
                    session.post(os.getenv('WDS_CODING_SERVER'), data=annotated_frame.tobytes())
                else:
                    print('VideoCapture is not opened')
                    time.sleep(15)
                    cap = cv2.VideoCapture(source)
            cap.release()
        except:
            print()