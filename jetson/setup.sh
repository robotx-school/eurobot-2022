#!/bin/bash
sudo apt update && sudo apt upgrade && sudo apt autoremove
sudo apt install nano tmux htop

sudo -H pip3 install --upgrade pip
sudo -H pip3 install protobuf==3.3.0

sudo apt-get install python3-pip libjpeg-dev libopenblas-dev libopenmpi-dev libomp-dev
sudo -H pip3 install future
sudo pip3 install -U --user wheel mock pillow
sudo -H pip3 install testresources setuptools==58.3.0 Cython gdown
gdown "https://drive.google.com/uc?id=1TqC6_2cwqiYacjoLhLgrZoap6-sVL2sd"
sudo -H pip3 install torch-1.10.0a0+git36449ea-cp36-cp36m-linux_aarch64.whl
rm torch-1.10.0a0+git36449ea-cp36-cp36m-linux_aarch64.whl

sudo -H pip3 install opencv-contrib-python

sudo systemctl disable lightdm

reboot
