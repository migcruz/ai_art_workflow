FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    git \
    wget \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

RUN userdel -r ubuntu && useradd -m -u 1000 -s /bin/bash comfy

WORKDIR /app

RUN git clone https://github.com/Comfy-Org/ComfyUI.git . && \
    chown -R comfy:comfy /app

USER comfy

RUN python3.12 -m venv /app/venv

# Install PyTorch with CUDA 13.0 support for RTX 5090 (Blackwell)
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install torch torchvision torchaudio \
        --extra-index-url https://download.pytorch.org/whl/cu130

RUN /app/venv/bin/pip install -r requirements.txt

EXPOSE 8188

CMD ["/app/venv/bin/python", "main.py", \
     "--listen", "0.0.0.0", \
     "--port", "8188", \
     "--disable-auto-launch", \
     "--highvram", \
     "--extra-model-paths-config", "/app/extra_model_paths.yaml"]
