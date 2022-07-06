FROM python:3.8

RUN apt update && apt-get install -y g++ ffmpeg libsm6 libxext6
RUN pip install clearml-agent

RUN mkdir /root/.ssh
COPY id_rsa /root/.ssh

CMD sleep infinity
