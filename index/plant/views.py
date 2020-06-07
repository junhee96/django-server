from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from skimage import data, io, filters
from django.views import View
from django.core.serializers import serialize
import json

import cv2
from .serializers import *
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage

import datetime
import tensorflow as tf
import numpy as np

#tf.compat.v1.disable_eager_execution()

#X = tf.compat.v1.placeholder(tf.float32, shape=[None, 4]) #데이터

#Y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1]) #클래스

#W = tf.Variable(tf.compat.v1.random_normal([4, 1]), name="weight") #가중치
#b = tf.Variable(tf.compat.v1.random_normal([1]), name="bias") #바이어스

# 가설을 설정합니다.
#hypothesis = tf.compat.v1.matmul(X, W) + b # 
# 저장된 모델을 불러오는 객체를 선언합니다.
#saver = tf.compat.v1.train.Saver()
#model = tf.compat.v1.global_variables_initializer()
# 세션 객체를 생성합니다.
#sess = tf.compat.v1.Session()
#sess.run(model)

#save_path = "../deep/saved.cpkt"
#saver.restore(sess, save_path)
#################################한번해보기########################################
#img = ""여기에 이미지 담는거 사람이 보내는거
#대충 전처리 하는 코드
model = tf.keras.applications.MobileNet(
    input_shape=(32,32,3), alpha=1.0, depth_multiplier=1, dropout=0.001,
    include_top=True, weights=None, input_tensor=None, pooling=None,
    classes=3, classifier_activation='softmax'
)
model.load_weights("/home/jongminjo/Downloads/flower_weight.h5")


# Create your views here.
class VersionViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.last()
    #     return qs
# class TestViewSet(viewsets.ModelViewSet):
#     queryset = Test.objects.all()
#     serializer_class = TestSerializer

@csrf_exempt
def plant_con(request,name):
    if request.method == "GET":
        query_set = Plantconnect.objects.filter(name=name)
        serializers = PlantconnectSerializer(query_set, many=True)
        return JsonResponse(serializers.data, safe=False)

@csrf_exempt
def plant_result(request,device,date):
    if request.method == "GET":
        # test = get_object_or_404(Test,)
        query_set = Test.objects.filter(device=device) & Test.objects.filter(date=date)
        serializers = TestSerializer(query_set, many=True)
        return JsonResponse(serializers.data, safe=False)


def main(request):
    if request.method == "GET":
        plantimages = Plantsub.objects.last()
        return render(request, "main.html",{"plantimages":plantimages})

import re

# def sorting(a,b,c,dict):
#     if a > c :
#         if b > c:
#             print(a,b)
#             print("군자란,수국")

#         else:
#             print(a,c,b)
#             print("군자란 해바라기")
#     else:
#         print(c,a,b)
#         print("해바라기, 수국")
# else:
#     if b > c:
#         if a > c:
#             print(b,a,c)
#             print("수국, 군자란")
#         else:
#             print(b,c,a)
#             print("수국 해바라기")
#     else:
#         print(c,b,a)
#         print("해바라기 수국")   

# @method_decorator(csrf_exempt,name='dispatch')
# class IndexView(View):
#     def get(self,request):
#         tests = Test.objects.all()
#         data = json.loads(serialize('json', tests))
#         return JsonResponse({'Test':data})

#     def post(self,request):
#         if request.META['CONTENT_TYPE'] == "application/json":
#             request = json.loads(request.body)
#             test = Test(images = request['images'],
#             device = request['device'],
#             date = request['date'])
#             fs = FileSystemStorage()
#             filePathName = fs.save(test.images.name,test.images)
#             print("첫번째",filePathName)
#             filePathName = fs.url(filePathName)
#             testimage = '.'+filePathName
#             print("두번째",filePathName)
#             img_bart = io.imread(testimage)
#             img_resized = cv2.resize(img_bart,(32,32))
#             io.imshow(img_resized)
#             dict = y_pred = model.predict(np.expand_dims(img_resized, axis=0))
#             print("####################################야야야야야야###################",dict)
#             a = dict[0,0]
#             b = dict[0,1]
#             c = dict[0,2]
#         else:
#             test = Test(images = request.FILES['images'],
#             device = request.POST['device'],
#             date = request.POST['date'])
#             fs = FileSystemStorage()
#             filePathName = fs.save(test.images.name,test.images)
#             print("첫번째",filePathName)
#             filePathName = fs.url(filePathName)
#             testimage = '.'+filePathName
#             print("두번째",filePathName)
#             img_bart = io.imread(testimage)
#             img_resized = cv2.resize(img_bart,(32,32))
#             io.imshow(img_resized)
#             dict = y_pred = model.predict(np.expand_dims(img_resized, axis=0))
#             print("####################################야야야야야야###################",dict)
#             a = dict[0,0]
#             b = dict[0,1]
#             c = dict[0,2]
#         test.save()
#         return HttpResponse(status=200)

@csrf_exempt
def index(request):
    if request.method == "POST":
        test = Test()
        # plantimage = Plantimage()
        # plantimage.avg_temp = request.POST["avg_temp"]
        # plantimage.min_temp = request.POST["min_temp"]
        # plantimage.max_temp = request.POST["max_temp"]
        # plantimage.rain_fall = request.POST["rain_fall"]
        # plantimage.save()
        test.images = request.FILES["images"]
        test.device = request.POST["device"]
        test.date = request.POST["date"]
        test.device = re.sub(r'^"|"$','',test.device)
        test.date = re.sub(r'^"|"$','',test.date)
        print("아아아",test.device)
        # test.save()
        fs = FileSystemStorage()
        filePathName = fs.save(test.images.name,test.images)
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
                    test.first_name = first_name
                    test.first_percent = first_accuracy
                    test.second_name = second_name
                    test.second_percent = second_accuracy
                    test.save()
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
                    test.first_name = first_name
                    test.first_percent = first_accuracy
                    test.second_name = second_name
                    test.second_percent = second_accuracy
                    test.save()
                    
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
                test.first_name = first_name
                test.first_percent = first_accuracy
                test.second_name = second_name
                test.second_percent = second_accuracy
                test.save()
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
                    test.first_name = first_name
                    test.first_percent = first_accuracy
                    test.second_name = second_name
                    test.second_percent = second_accuracy
                    test.save()
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
                    test.first_name = first_name
                    test.first_percent = first_accuracy
                    test.second_name = second_name
                    test.second_percent = second_accuracy
                    test.save()
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
                test.first_name = first_name
                test.first_percent = first_accuracy
                test.second_name = second_name
                test.second_percent = second_accuracy
                test.save()

        #a = y_pred[0]
        #a = a.sort(reverse=True)


        # price = dict[0]
        # plantsub = Plantsub()
        # plantsub.plant = get_object_or_404(Plantimage,pk=plantimage.id)
        # plantsub.price = price
        # plantsub.save()
        # plantimage.price = price
        # plantimage.save()
        # context = {'images':test.images,
        #             'device':test.device,
        #             'date':test.date,
        #             'first_name':test.first_name,
        #             'first_percent':test.first_percent,
        #             'second_name':test.second_name,
        #             'second_percent':test.second_percent,
        #             }
        # return HttpResponse(json.dumps(context), content_type="application/json")
        # return render(request, "index.html")
        return HttpResponse(status=200)
    else:
        return render(request, "index.html")
    