FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt update && apt-get install -y g++ ffmpeg libsm6 libxext6
