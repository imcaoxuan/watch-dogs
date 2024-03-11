import os
import time
from datetime import datetime

import cv2
import requests
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO(f'{os.getenv("WDS_MODEL", "model")}.pt')


def start_monitoring():
    print('start_monitoring', datetime.now())
    # session = requests.session()
    while bool(os.getenv('FLAG', True)):
        cap = None
        try:
            source = os.getenv('WDS_SOURCE')
            cap = cv2.VideoCapture(source)
            i = 0
            while bool(os.getenv('FLAG', True)) and cap.isOpened():
                success, frame = cap.read()
                if success:
                    i += 1
                    if i % os.getenv('WDS_STRIDE', 60) != 0:
                        continue
                    results = model.predict(frame, verbose=bool(os.getenv('WDS_YOLO_VERBOSE', True)),
                                            imgsz=int(os.getenv('WDS_YOLO_IMGSZ', 640)),
                                            conf=float(os.getenv('WDS_YOLO_CONF', 0.25)),
                                            max_det=int(os.getenv('WDS_YOLO_MAX_DET', 300)),
                                            classes=eval(os.getenv('WDS_YOLO_CLASSES')))
                    annotated_frame = results[0].plot()
                    # annotated_frame = cv2.resize(annotated_frame, (1920, 1080))
                    if len(results[0].boxes.cls) > 0:
                        annotated_frame_ret, annotated_frame_buffer = cv2.imencode('.jpg', annotated_frame)
                        requests.post(f'{os.getenv("WDS_MASTER")}/report', data=annotated_frame_buffer.tobytes())
                else:
                    print('VideoCapture is not opened')
                    time.sleep(15)
                    break
            cap.release()
        except Exception as e:
            print(e)
        finally:
            if cap:
                cap.release()
    print('stop_monitoring', datetime.now())
