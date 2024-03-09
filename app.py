import os
import subprocess
import uuid
from urllib.parse import urlparse
from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from flask_basicauth import BasicAuth
from flask.logging import logging

logging.getLogger('werkzeug').setLevel('WARNING')
app = Flask(__name__)
scheduler = APScheduler()

app.config['SECRET_KEY'] = str(uuid.uuid4())
if not os.getenv('WDS_USERNAME') or not os.getenv('WDS_PASSWORD'):
    print('NO WDS_USERNAME or WDS_PASSWORD')
    exit(1)
app.config['BASIC_AUTH_USERNAME'] = os.getenv('WDS_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('WDS_PASSWORD')
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

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
           os.getenv('WDS_STREAM_SERVER')]

proc = subprocess.Popen(command, stdin=subprocess.PIPE)


@app.post('/encode')
def encode():
    frame_bytes = request.data
    proc.stdin.write(frame_bytes)
    return {}


@app.route('/')
def index():  # put application's code here
    return render_template('index.html', hls=urlparse(os.getenv('WDS_STREAM_SERVER')).path)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
