FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

# RUN apt update && apt-get install -y g++ ffmpeg libsm6 libxext6

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
