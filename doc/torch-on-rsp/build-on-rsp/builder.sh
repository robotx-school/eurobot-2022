git clone -b v1.10.0 --depth=1 --recursive https://github.com/pytorch/pytorch.git
cd pytorch

sudo pip3 install -r requirements.txt
export BUILD_CAFFE2_OPS=OFF
export USE_FBGEMM=OFF
export USE_FAKELOWP=OFF
export BUILD_TEST=OFF
export USE_MKLDNN=OFF
export USE_NNPACK=ON
export USE_XNNPACK=ON
export USE_QNNPACK=ON
export MAX_JOBS=4
export USE_OPENCV=OFF
export USE_NCCL=OFF
export USE_SYSTEM_NCCL=OFF
PATH=/usr/lib/ccache:$PATH

#python3 setup.py clean - After Error
python3 setup.py bdist_wheel
cd dist
