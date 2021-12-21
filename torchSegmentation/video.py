import torch
#import torch.optim as optim
#import torch.nn as nn
#from torch.utils.data.dataset import Dataset
from torchvision import transforms
#from torchvision import models
#import torchvision
#import glob
#import albumentations as A
import cv2
import numpy as np
#from matplotlib import pyplot as plt
from time import time as t

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

def get_segment_labels(image, model, device):
    image = image.to(DEVICE)
    model.eval()
    outputs = model(image)
    return outputs['out'][0]

def get_colored_img(_image_):
    img = cv2.cvtColor(_image_, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (256, 256))

    preprocess = transforms.Compose([
        transforms.ToTensor(),
    ])

    # input_tensor = preprocess(img)

    norm_img = preprocess(img / 255)
    input_tensor = norm_img.to(torch.float)
    input_batch = input_tensor.unsqueeze(0)
    start = t()
    pred = get_segment_labels(input_batch, net, DEVICE)
    print('fps:',1/(t()-start))
    labels = pred.detach().cpu().numpy()
    labels = np.where(labels > 0.5, 1, 0)

    #img[:, :, 0] = np.where(labels[1, :, :] == 1, 0, img[:, :, 0])
    #img[:, :, 1] = np.where(labels[1, :, :] == 1, 0, img[:, :, 1])
    # img[:, :, 2] = np.where(labels[1, :, :] == 1, 0, img[:, :, 2])

    # img[:, :, 0] = np.where(labels[0, :, :] == 1, 0, img[:, :, 0])
    img[:, :, 1] = np.where(labels[0, :, :] == 1, 0, img[:, :, 1])
    img[:, :, 2] = np.where(labels[0, :, :] == 1, 0, img[:, :, 2])
    return img


net = torch.load('model.t', map_location=DEVICE)

cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = get_colored_img(img)
    img = cv2.resize(img, (512, 512))
    #cv2.imshow('cam.png', img)
    #ch = cv2.waitKey(5)
    #if ch == 27:
    #    break
cv2.destroyAllWindows()
cap.release()
