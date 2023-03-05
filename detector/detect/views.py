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

def index(request):
    context = {}
    return render(request,"upload.html",context)

@api_view(['POST'])
def uploaded(request):
    dt = request.data
    img = dt["image_data"]
    image_data = img.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))

    cwd = os.getcwd()
    text = "Right Time --> "+str(time.time())
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

