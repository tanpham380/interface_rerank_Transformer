FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

WORKDIR /app

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1


# Upgrade pip and setuptools
RUN pip3 install --upgrade pip setuptools

# Install torch first
RUN pip3 install --extra-index-url https://download.pytorch.org/whl/cu121 torch

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install --ignore-installed -r requirements.txt
# RUN pip3 install --extra-index-url https://download.pytorch.org/whl/cu121 torch

# Download the model
COPY download.py .
ARG MODEL_NAME
RUN python3 download.py

# Copy the rest of the application code
COPY . .

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
# ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--trust-remote-code"]
