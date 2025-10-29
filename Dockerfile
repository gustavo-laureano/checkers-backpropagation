FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
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
    && rm -rf /var/lib/apt/lists/*



WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir pygame \
    && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY . /app

CMD ["python", "-m", "src.infra.main"]
