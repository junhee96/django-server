from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views.decorators.csrf import csrf_exempt
from skimage import data, io, filters
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
        test.save()
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
        #a = y_pred[0]
        #a = a.sort(reverse=True)


        # price = dict[0]
        # plantsub = Plantsub()
        # plantsub.plant = get_object_or_404(Plantimage,pk=plantimage.id)
        # plantsub.price = price
        # plantsub.save()
        # plantimage.price = price
        # plantimage.save()
        return render(request, "index.html")
    else:
        plantimage = Plantimage.objects.all
        return render(request, "index.html")
    