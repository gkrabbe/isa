# coding: utf-8

print("1")


import os
import sys 
import time
import torch
import random
import datetime

from utils import utils
from models import *

import matplotlib.pyplot as plt
from torch.autograd import Variable
import matplotlib.patches as patches

from PIL import Image
from requests import Session
from signalr import Connection
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


print("2")


class_path='config/coco.names'
config_path='config/yolov3.cfg'
weights_path='config/yolov3.weights'

img_size=416
nms_thres=0.4
conf_thres=0.8

# Load model and weights
model = Darknet(config_path, img_size=img_size)
model.load_weights(weights_path)
model.cuda()
model.eval()
classes = utils.load_classes(class_path)
Tensor = torch.cuda.FloatTensor


print("3")

input("press ENTER to start VISIO")

session = Session()
connection = Connection("http://127.0.0.1:8088/signalr", session)
chat = connection.register_hub('isaHub')
connection.start()

print("started")

print("4")


def detect_image(img):
    # scale and pad image
    ratio = min(img_size/img.size[0], img_size/img.size[1])
    imw = round(img.size[0] * ratio)
    imh = round(img.size[1] * ratio)
    img_transforms=transforms.Compose([transforms.Resize((imh,imw)),
         transforms.Pad((max(int((imh-imw)/2),0), 
              max(int((imw-imh)/2),0), max(int((imh-imw)/2),0),
              max(int((imw-imh)/2),0)), (128,128,128)),
         transforms.ToTensor(),
         ])
    # convert image to Tensor
    image_tensor = img_transforms(img).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input_img = Variable(image_tensor.type(Tensor))
    # run inference on the model and get detections
    with torch.no_grad():
        detections = model(input_img)
        detections = utils.non_max_suppression(detections, 80, 
                        conf_thres, nms_thres)
    return detections[0]


print("5")


import cv2
from sort import *
from IPython.display import clear_output

cmap = plt.get_cmap('tab20b')
colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

vid = cv2.VideoCapture(0)
mot_tracker = Sort() 

status = False



while(True):
#for ii in range(40):
    ret, frame2 = vid.read()
    width = int(frame2.shape[1] * 2)
    height = int(frame2.shape[0] * 2)
    
    #frame2 = cv2.resize(frame2, (width, height), interpolation = cv2.INTER_AREA)
    frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    pilimg = Image.fromarray(frame)
    detections = detect_image(pilimg)

    img = np.array(pilimg)
    pad_x = max(img.shape[0] - img.shape[1], 0) * (img_size / max(img.shape))
    pad_y = max(img.shape[1] - img.shape[0], 0) * (img_size / max(img.shape))
    unpad_h = img_size - pad_y
    unpad_w = img_size - pad_x
    detect_person = 0
    if detections is not None:
        tracked_objects = mot_tracker.update(detections.cpu())

        unique_labels = detections[:, -1].cuda().unique()
        n_cls_preds = len(unique_labels)
        for x1, y1, x2, y2, obj_id, cls_pred in tracked_objects:
            if(cls_pred == 0.0):
                detect_person += 1
            box_h = int(((y2 - y1) / unpad_h) * img.shape[0])
            box_w = int(((x2 - x1) / unpad_w) * img.shape[1])
            y1 = int(((y1 - pad_y // 2) / unpad_h) * img.shape[0])
            x1 = int(((x1 - pad_x // 2) / unpad_w) * img.shape[1])

            color = colors[int(obj_id) % len(colors)]
            color = [i * 255 for i in color]
            try:
                cls = classes[int(cls_pred)]
            except:
                cls = "desconhecido"
            cv2.rectangle(frame2, (x1, y1), (x1+box_w, y1+box_h), color, 4)
            cv2.rectangle(frame2, (x1, y1-35), (x1+len(cls)*19+60, y1), color, -1)
            cv2.putText(frame2, cls + "-" + str(int(obj_id)), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
    if(detect_person >=1):
        chat.server.invoke('sendlocalization', 'cquarto1', True)

    else:
        chat.server.invoke('sendlocalization', 'cquarto1', False)
            
            
    cv2.imshow('Camera',  frame2)
    if cv2.waitKey(1) != -1:
        cv2.waitKey(0)
    cls_pred
vid.release()
cv2.destroyAllWindows()

