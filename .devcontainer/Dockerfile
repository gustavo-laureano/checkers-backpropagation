FROM mcr.microsoft.com/devcontainers/python:3.11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libsmpeg-dev \
    libportmidi-dev \
    libavformat-dev \
    libswscale-dev \
    libjpeg-dev \
    libfreetype6-dev \
    xvfb \
    x11-utils \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*


ENV DISPLAY=:99

WORKDIR /workspace

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    pylint \
    mypy

RUN pip install --no-cache-dir pygame numpy

CMD ["sleep", "infinity"]