# Ultralytics YOLO 🚀, AGPL-3.0 license
# Builds ultralytics/ultralytics:latest-cpu image on DockerHub https://hub.docker.com/r/ultralytics/ultralytics
# Image is CPU-optimized for ONNX, OpenVINO and PyTorch YOLOv8 deployments

# Start FROM Ubuntu image https://hub.docker.com/_/ubuntu
FROM registry.caoxuan.top:8443/ultralytics/ultralytics:8.1.24-cpu

ADD . /root/app/
# Create working directory
WORKDIR /root/app

RUN pip install --no-cache -i https://public:public@mirrors.caoxuan.top:8443/repository/pypi-proxy/simple -r /root/app/requirements.txt

ENTRYPOINT ["python", "-u", "predict.py"]

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