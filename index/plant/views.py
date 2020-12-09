from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from skimage import data, io, filters
from django.views import View
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import re

import cv2
from .serializers import *
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage

import datetime
import tensorflow as tf
import numpy as np

# Create your views here.
@csrf_exempt
def plant_con(request,name):
    if request.method == "GET":
        query_set = Plantconnect.objects.filter(name=name)
        serializers = PlantconnectSerializer(query_set, many=True)
        return JsonResponse(serializers.data, safe=False)

@csrf_exempt
def plant_result(request,device,date):
    if request.method == "GET":
        query_set = MyCamera.objects.filter(device=device) & MyCamera.objects.filter(date=date)
        serializers = MyCameraSerializer(query_set, many=True)
        return JsonResponse(serializers.data, safe=False)

@csrf_exempt
def index(request):
    model = tf.keras.applications.MobileNet(
        input_shape=(32,32,3), alpha=1.0, depth_multiplier=1, dropout=0.001,
        include_top=True, weights=None, input_tensor=None, pooling=None,
        classes=3, classifier_activation='softmax'
    )
    model.load_weights("/home/jongminjo/Downloads/flower_weight.h5")

    if request.method == "POST":
        mycamera = MyCamera()
        mycamera.images = request.FILES["images"]
        mycamera.device = request.POST["device"]
        mycamera.date = request.POST["date"]
        mycamera.device = re.sub(r'^"|"$','',mycamera.device)
        mycamera.date = re.sub(r'^"|"$','',mycamera.date)
        print("아아아",mycamera.device)
        fs = FileSystemStorage()
        filePathName = fs.save(mycamera.images.name,mycamera.images)
        print("첫번째",filePathName)
        filePathName = fs.url(filePathName)
        testimage = '.'+filePathName
        print("두번째",filePathName)
    
        # price = 0
        # data = ((plantimage.avg_temp, plantimage.min_temp, plantimage.max_temp, plantimage.rain_fall), (0, 0, 0, 0))
        # arr = np.array(data, dtype=np.float32)
        # x_data = arr[0:4]
        # #dict = sess.run(hypothesis, feed_dict={X: x_data})
        img_bart = io.imread(testimage)
        img_resized = cv2.resize(img_bart,(32,32))
        io.imshow(img_resized)
        dict = y_pred = model.predict(np.expand_dims(img_resized, axis=0))
        print("####################################야야야야야야###################",dict)
        a = dict[0,0]
        b = dict[0,1]
        c = dict[0,2]

        if a > b:
            if a > c:
                if b > c:
                    #군자란 수국
                    first_name = "군자란"
                    first_accuracy = a
                    second_name = "수국"
                    second_accuracy = b
                    first_name = re.sub(r'^"|"$','',first_name)
                    second_name = re.sub(r'^"|"$','',second_name)
                    print(first_name,first_accuracy)
                    print(second_name,second_accuracy)
                    mycamera.first_name = first_name
                    mycamera.first_percent = first_accuracy
                    mycamera.second_name = second_name
                    mycamera.second_percent = second_accuracy
                    mycamera.save()
                else:
                    #군자란 해바라기
                    first_name = "군자란"
                    first_accuracy = a
                    second_name = "해바라기"
                    second_accuracy = c
                    first_name = re.sub(r'^"|"$','',first_name)
                    second_name = re.sub(r'^"|"$','',second_name)
                    print(first_name,first_accuracy)
                    print(second_name,second_accuracy)
                    mycamera.first_name = first_name
                    mycamera.first_percent = first_accuracy
                    mycamera.second_name = second_name
                    mycamera.second_percent = second_accuracy
                    mycamera.save()
                    
            else:
                #해바라기 수국
                first_name = "해바라기"
                first_accuracy = c
                second_name = "수국"
                second_accuracy = b
                first_name = re.sub(r'^"|"$','',first_name)
                second_name = re.sub(r'^"|"$','',second_name)
                print(first_name,first_accuracy)
                print(second_name,second_accuracy)
                mycamera.first_name = first_name
                mycamera.first_percent = first_accuracy
                mycamera.second_name = second_name
                mycamera.second_percent = second_accuracy
                mycamera.save()
        else:
            if b > c:
                if a > c:
                    #수국 군자란
                    first_name = "수국"
                    first_accuracy = b
                    second_name = "군자란"
                    second_accuracy = a
                    first_name = re.sub(r'^"|"$','',first_name)
                    second_name = re.sub(r'^"|"$','',second_name)
                    print(first_name,first_accuracy)
                    print(second_name,second_accuracy)
                    mycamera.first_name = first_name
                    mycamera.first_percent = first_accuracy
                    mycamera.second_name = second_name
                    mycamera.second_percent = second_accuracy
                    mycamera.save()
                else:
                    #수국 해바라기
                    first_name = "수국"
                    first_accuracy = b
                    second_name = "해바라기"
                    second_accuracy = c
                    first_name = re.sub(r'^"|"$','',first_name)
                    second_name = re.sub(r'^"|"$','',second_name)
                    print(first_name,first_accuracy)
                    print(second_name,second_accuracy)
                    mycamera.first_name = first_name
                    mycamera.first_percent = first_accuracy
                    mycamera.second_name = second_name
                    mycamera.second_percent = second_accuracy
                    mycamera.save()
            else:
                #해바라기 수국
                first_name = "해바라기"
                first_accuracy = c
                second_name = "수국"
                second_accuracy = b
                first_name = re.sub(r'^"|"$','',first_name)
                second_name = re.sub(r'^"|"$','',second_name)
                print(first_name,first_accuracy)
                print(second_name,second_accuracy)
                mycamera.first_name = first_name
                mycamera.first_percent = first_accuracy
                mycamera.second_name = second_name
                mycamera.second_percent = second_accuracy
                mycamera.save()
        return HttpResponse(status=200)
    else:
        return render(request, "index.html")

@csrf_exempt
def book_post(request):
    if request.method == "POST":
        plantadd = Plantadd()
        # plantadd.number = request.POST["number"]
        plantadd.device = request.POST["device"]
        plantadd.name = request.POST["name"]
        plantadd.flower = request.POST["flower"]
        plantadd.content = request.POST["content"]
        plantadd.image = request.POST["image"]
        plantadd.save()
        return HttpResponse(status=200)
    else:
        return render(request,"book_add.html")


@csrf_exempt
def book_list(request,device):
    if request.method == "GET":
        query_set = Plantadd.objects.filter(device=device)
        # query_set = Plantadd.objects.filter(device=device) & Plantadd.objects.filter(number=number)
        serializers = PlantaddSerializer(query_set, many=True)
        return JsonResponse(serializers.data, safe=False)


@csrf_exempt
def my_book_detail(request,device,id):
    if request.method == "GET":
        query_set = Plantadd.objects.filter(device=device) & Plantadd.objects.filter(id=id)
        serializers = PlantaddSerializer(query_set, many=True)
        return JsonResponse(serializers.data, safe=False)
    

@api_view(['GET','DELETE'])
def my_book_delete(request,id):
    try:
        plantadd =Plantadd.objects.get(pk=id)
    except Plantadd.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PlantaddSerializer(plantadd)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        plantadd.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
