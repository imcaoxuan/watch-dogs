FROM registry.caoxuan.top:8443/ultralytics/ultralytics:8.1.24-cpu

ADD . /root/app/
# Create working directory
WORKDIR /root/app

RUN pip install --no-cache -i https://public:public@mirrors.caoxuan.top:8443/repository/pypi-proxy/simple -r /root/app/requirements.txt

ENTRYPOINT ["python", "-u", "/root/app/app.py"]

EXPOSE 5001

