FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# Set the working directory
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml .

# Install base utilities
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda
# Download VGG16 PyTorch model
RUN mkdir -p /root/.cache/torch/hub/checkpoints
RUN wget -O /root/.cache/torch/hub/checkpoints/vgg16-397923af.pth https://download.pytorch.org/models/vgg16-397923af.pth
# Install u2net
RUN mkdir -p /root/.u2net
RUN wget --no-check-certificate -O /root/.u2net/u2net.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx


# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

# Initialize conda
RUN conda init bash

# Create a new Conda environment
RUN conda env create -f environment.yml

# # Activate the Conda environment
# SHELL ["conda", "run", "-n", "unicorn", "/bin/bash", "-c"]
RUN echo "conda activate unicorn" > ~/.bashrc
ENV PATH /opt/conda/envs/unicorn/bin:$PATH

RUN /bin/bash -c "source activate unicorn \
    && pip install onnxruntime-gpu\
    && pip install rembg[gpu] \
    && conda clean -afy"

# Copy the remaining files to the container
COPY . .

# FROM continuumio/miniconda3:4.7.10

# WORKDIR /app

# COPY environment.yml .

# RUN conda env create -f environment.yml

# RUN echo "conda activate unicorn" > ~/.bashrc
# ENV PATH /opt/conda/envs/unicorn/bin:$PATH

# RUN /bin/bash -c "source activate unicorn \
#     && pip install rembg \
#     && conda clean -afy"

# COPY . .