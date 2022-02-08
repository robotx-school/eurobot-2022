#!/bin/bash
cd
sudo apt update && sudo apt -y upgrade && sudo apt -y autoremove
sudo apt -y install nano tmux htop

sudo -H pip3 install --upgrade pip
sudo -H pip3 install protobuf==3.3.0 opencv-contrib-python

sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev libavcodec-dev libavformat-dev libavutil-dev libswresample-dev libswscale-dev
sudo -H pip3 install future
sudo -H pip3 install -U --user wheel mock pillow
sudo -H pip3 install testresources setuptools==58.3.0 Cython gdown
gdown "https://drive.google.com/uc?id=1TqC6_2cwqiYacjoLhLgrZoap6-sVL2sd"
sudo -H pip3 install torch-1.10.0a0+git36449ea-cp36-cp36m-linux_aarch64.whl
rm torch-1.10.0a0+git36449ea-cp36-cp36m-linux_aarch64.whl

git clone --branch release/0.11 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.11.0
sudo -H python3 setup.py install --user
cd

sudo systemctl disable lightdm
reboot
