import datetime
import os
import queue
import uuid
from urllib.parse import urlparse

from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth

import utils

import time

# logging.getLogger('werkzeug').setLevel('WARNING')
app = Flask(__name__)

app.config['SECRET_KEY'] = str(uuid.uuid4())
if not os.getenv('WDS_USERNAME') or not os.getenv('WDS_PASSWORD'):
    print('NO WDS_USERNAME or WDS_PASSWORD')
    exit(1)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('WDS_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('WDS_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True
scheduler = APScheduler()
scheduler.init_app(app)

basic_auth = BasicAuth(app)

# command = ['D:/cxs/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe',
#            '-y',
#            '-f', 'rawvideo',
#            '-vcodec', 'rawvideo',
#            '-pix_fmt', 'bgr24',
#            '-s', "{}x{}".format(1920, 1080),
#            '-r', str(30),
#            '-i', '-',
#            '-c:v', 'libx264',
#            '-pix_fmt', 'yuv420p',
#            '-preset', 'ultrafast',
#            '-f', 'flv',
#            os.getenv('WDS_STREAM_SERVER')]
#
# proc = subprocess.Popen(command, stdin=subprocess.PIPE)

q = queue.Queue()


def takeN(n):
    ls = []
    for _ in range(n):
        item = q.get()
        if item:
            ls.append(item)
    return ls


@scheduler.task('interval', id='check', seconds=30, misfire_grace_time=900)
def check():
    n = q.qsize()
    print(f'check {n}')
    if n > 0:
        utils.send_email('Intrusion Warning!!!', takeN(n))


@app.post('/report')
def report():
    frame = request.data
    # proc.stdin.write(frame_bytes)
    q.put(frame)
    n = int(os.getenv('WDS_N', 10))
    if q.qsize() >= n:
        utils.send_email('Intrusion Warning!!!', takeN(n))
    # winsound.Beep(500, 1000)
    return {}


@app.route('/')
def index():  # put application's code here
    return render_template('index.html', hls=urlparse(os.getenv('WDS_STREAM_SERVER')).path)


if __name__ == '__main__':
    scheduler.start()
    app.run('0.0.0.0', 5000)
