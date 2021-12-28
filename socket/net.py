import torch
from torchvision import transforms
import cv2
import numpy as np
from time import time as t

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
#torch.set_num_threads(4)
#torch.set_grad_enabled(False)

def get_segment_labels(image, model, device):
    image = image.to(DEVICE)
    model.eval()
    outputs = model(image)
    return outputs['out'][0]

def get_colored_img(_image_, size=(256, 256)):
    img = cv2.cvtColor(_image_, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, size)
    preprocess = transforms.Compose([
        transforms.ToTensor(),
    ])
    norm_img = preprocess(img / 255)
    input_tensor = norm_img.to(torch.float)
    input_batch = input_tensor.unsqueeze(0)
    start = t()
    pred = get_segment_labels(input_batch, net, DEVICE)
    curr_fps = 1/(t()-start)
    labels = pred.detach().cpu().numpy()
    labels = np.where(labels > 0.5, 1, 0)

    #img[:, :, 0] = np.where(labels[1, :, :] == 1, 0, img[:, :, 0])
    #img[:, :, 1] = np.where(labels[1, :, :] == 1, 0, img[:, :, 1])
    # img[:, :, 2] = np.where(labels[1, :, :] == 
    #np.where(labels[0, :, :] == 1, 0, img[:, :, 0])
    img[:, :, 1] = np.where(labels[0, :, :] == 1, 0, img[:, :, 1])
    img[:, :, 2] = np.where(labels[0, :, :] == 1, 0, img[:, :, 2])
    return img, curr_fps

net = torch.load('model.t', map_location=DEVICE)
print("Model loaded")
