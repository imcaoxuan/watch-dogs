# Ultralytics YOLO 🚀, AGPL-3.0 license
# Builds ultralytics/ultralytics:latest-cpu image on DockerHub https://hub.docker.com/r/ultralytics/ultralytics
# Image is CPU-optimized for ONNX, OpenVINO and PyTorch YOLOv8 deployments

# Start FROM Ubuntu image https://hub.docker.com/_/ubuntu
FROM registry.caoxuan.top:8443/ubuntu:23.10

# Downloads to user config dir
ADD https://github.com/ultralytics/assets/releases/download/v0.0.0/Arial.ttf \
    https://github.com/ultralytics/assets/releases/download/v0.0.0/Arial.Unicode.ttf \
    /root/.config/Ultralytics/

ADD . /root/app/
# Install linux packages
# g++ required to build 'tflite_support' and 'lap' packages, libusb-1.0-0 required for 'tflite_support' package
RUN apt update \
    && apt install --no-install-recommends -y python3-pip git zip curl htop libgl1 libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0

# Create working directory
WORKDIR /usr/src/ultralytics

# Copy contents
# COPY . /usr/src/ultralytics  # git permission issues inside container
RUN git clone https://github.com/ultralytics/ultralytics -b main /usr/src/ultralytics
ADD https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt /usr/src/ultralytics/

# Remove python3.11/EXTERNALLY-MANAGED or use 'pip install --break-system-packages' avoid 'externally-managed-environment' Ubuntu nightly error
RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

# Install pip packages
RUN python3 -m pip install --upgrade pip wheel
RUN pip install --no-cache -e ".[export]" --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -r /root/app/requirements.txt

# Run exports to AutoInstall packages
RUN yolo export model=tmp/yolov8n.pt format=edgetpu imgsz=32
RUN yolo export model=tmp/yolov8n.pt format=ncnn imgsz=32
# Requires <= Python 3.10, bug with paddlepaddle==2.5.0 https://github.com/PaddlePaddle/X2Paddle/issues/991
# RUN pip install --no-cache paddlepaddle>=2.6.0 x2paddle
# Remove exported models
RUN rm -rf tmp

# Creates a symbolic link to make 'python' point to 'python3'
RUN ln -sf /usr/bin/python3 /usr/bin/python

ENTRYPOINT ["python", "-u", "/root/app/app.py"]

EXPOSE 5000

# Usage Examples -------------------------------------------------------------------------------------------------------

# Build and Push
# t=ultralytics/ultralytics:latest-cpu && sudo docker build -f docker/Dockerfile-cpu -t $t . && sudo docker push $t
# t=registry.caoxuan.top:8443/nfools/wathch-dogs:0.0.1 && sudo docker build -f docker/Dockerfile -t $t . && sudo docker push $t

# Run
# t=ultralytics/ultralytics:latest-cpu && sudo docker run -it --ipc=host --name NAME $t

# Pull and Run
# t=ultralytics/ultralytics:latest-cpu && sudo docker pull $t && sudo docker run -it --ipc=host --name NAME $t

# Pull and Run with local volume mounted
# t=ultralytics/ultralytics:latest-cpu && sudo docker pull $t && sudo docker run -it --ipc=host -v "$(pwd)"/datasets:/usr/src/datasets $t