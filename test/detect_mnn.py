import os
import subprocess
import time

import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('../yolov8n.pt')

# Open the video file
source = os.getenv('WDS_SOURCE')
cap = cv2.VideoCapture(source)
video_path = '../static/video/'

# # Loop through the video frames
# while cap.isOpened():
#     # Read a frame from the video
#     success, frame = cap.read()
#     if success:
#         # Run YOLOv8 inference on the frame
#         results = model(frame)
#         # Visualize the results on the frame10
#         annotated_frame = results[0].plot()
#         annotated_frame = cv2.resize(annotated_frame, (1920, 1080))
#         # Display the annotated frame
#         cv2.imshow("YOLOv8 Inference", annotated_frame)
#         # Break the loop if 'q' is pressed
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         # Break the loop if the end of the video is reached
#         break
# # Release the video capture object and close the display window
# cap.release()
# cv2.destroyAllWindows()

print('start_recording')

command = ['ffmpeg',
           '-y',
           '-f', 'rawvideo',
           '-vcodec', 'rawvideo',
           '-pix_fmt', 'bgr24',
           '-s', "{}x{}".format(1920, 1080),
           '-r', str(30),
           '-i', '-',
           '-c:v', 'libx264',
           '-pix_fmt', 'yuv420p',
           '-preset', 'ultrafast',
           '-f', 'flv',
           'rtmp://127.0.0.1:1935/test/wds']

proc = subprocess.Popen(command, stdin=subprocess.PIPE)

i = 0
# video = cv2.VideoWriter(os.path.join(video_path, 'test.flv'), cv2.VideoWriter_fourcc('F', 'L', 'V', '1'), 15,                        (1920, 1080))
while cap.isOpened() and i < 100:
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)
        # Visualize the results on the frame10
        annotated_frame = results[0].plot()
        annotated_frame = cv2.resize(annotated_frame, (1920, 1080))
        proc.stdin.write(annotated_frame.tobytes())
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        # video.write(annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break
#    i = i + 1
cap.release()
# video.release()
cv2.destroyAllWindows()