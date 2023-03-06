from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse
from PIL import Image
import base64
from io import BytesIO
import os
import time
from .models import TextPrediction
from django.http import JsonResponse
import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import re
from PIL import Image, ImageDraw
from torchvision import transforms
import json
import torch.nn as nn
from torch import optim
import gc

"""
device = torch.device("cpu")
#device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
print(device)
model1 = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=None)
num_classes = 2
in_features = model1.roi_heads.box_predictor.cls_score.in_features
model1.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model2 = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(weights=None)
model3 = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(weights=None)
model1.load_state_dict(torch.load("./linemodelv2.pth"))
in_features = model2.roi_heads.box_predictor.cls_score.in_features
model2.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model2.load_state_dict(torch.load("./worddetectionmodelv2.pth"))
model2.eval()
in_features = model3.roi_heads.box_predictor.cls_score.in_features
model3.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model3.load_state_dict(torch.load("./letterdetectionmodelv2.pth"))
model3.eval()
model1.eval()"""

def index(request):
    context = {}
    return render(request,"upload.html",context)

@api_view(['POST'])
def uploaded(request):
    device = torch.device("cpu")
#device = (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
    print(device)
    model1 = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=None)
    num_classes = 2
    in_features = model1.roi_heads.box_predictor.cls_score.in_features
    model1.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    model2 = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(weights=None)
    model3 = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(weights=None)
    model1.load_state_dict(torch.load("./linemodelv2.pth"))
    in_features = model2.roi_heads.box_predictor.cls_score.in_features
    model2.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    model2.load_state_dict(torch.load("./worddetectionmodelv2.pth"))
    model2.eval()
    in_features = model3.roi_heads.box_predictor.cls_score.in_features
    model3.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    model3.load_state_dict(torch.load("./letterdetectionmodelv2.pth"))
    model3.eval()
    model1.eval()
    st = time.time()
    dt = request.data
    img = dt["image_data"]
    image_data = img.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    img = image.convert("RGB")
    img = transforms.ToTensor()(img)
    img = img.unsqueeze(0)
    testout = model1(img)
    j = 0
    for i in range(len(testout[0]["boxes"])):
        if testout[0]["scores"][i] > 0.8:
            li = testout[0]["boxes"][i].cpu().detach().numpy()
            j += 1
            cropimg = transforms.functional.crop(img,int(li[1]),int(li[0]),int(li[3]-li[1]),int(li[2]-li[0]))
            gc.collect()
            senout = model2(cropimg)
            for k in senout:
                for c,f in zip(k["boxes"],k["scores"]):
                    print("ok")
                    if f.item() > 0.8:
                        wordimg = transforms.functional.crop(cropimg,int(c[1]),int(c[0]),int(c[3]-c[1]),int(c[2]-c[0]))
                        letout = model3(wordimg)
                        print(letout)
    et = time.time()
    text = "Right Time --> "+str(et-st)
    k = TextPrediction.objects.filter(id=1)
    k.update(textdata=text)
    return Response("Nice")

@api_view(['GET'])
def textd(request):
    g = TextPrediction.objects.get(id=1)
    td = {"textdata":g.textdata}
    return JsonResponse(td)

def text(request):
    context = {}
    return render(request,"editor.html",context)

