from django.shortcuts import render,redirect
from .models import Plantimage,Test
from django.views.decorators.csrf import csrf_exempt
# from .serializers import *
# from rest_framework import viewsets

import datetime
import tensorflow as tf
import numpy as np
tf.compat.v1.disable_eager_execution()

X = tf.compat.v1.placeholder(tf.float32, shape=[None, 4])

Y = tf.compat.v1.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.compat.v1.random_normal([4, 1]), name="weight")
b = tf.Variable(tf.compat.v1.random_normal([1]), name="bias")

# 가설을 설정합니다.
hypothesis = tf.compat.v1.matmul(X, W) + b
# 저장된 모델을 불러오는 객체를 선언합니다.
saver = tf.compat.v1.train.Saver()
model = tf.compat.v1.global_variables_initializer()
# 세션 객체를 생성합니다.
sess = tf.compat.v1.Session()
sess.run(model)

save_path = "../deep/saved.cpkt"
saver.restore(sess, save_path)

# Create your views here.
# class PlantimageViewSet(viewsets.ModelViewSet):
#     queryset = Plantimage.objects.all()
#     serializer_class = PlantimageSerializer
    

# class TestViewSet(viewsets.ModelViewSet):
#     queryset = Test.objects.all()
#     serializer_class = TestSerializer

def main(request):
    return render(request, "main.html")

@csrf_exempt
def index(request):
    if request.method == "POST":
        # test = Test()
        plantimage = Plantimage()
        plantimage.avg_temp = request.POST["avg_temp"]
        plantimage.min_temp = request.POST["min_temp"]
        plantimage.max_temp = request.POST["max_temp"]
        plantimage.rain_fall = request.POST["rain_fall"]
        plantimage.save()
        # test.images = request.POST["images"]
        # test.save()
        price = 0
        data = ((plantimage.avg_temp, plantimage.min_temp, plantimage.max_temp, plantimage.rain_fall), (0, 0, 0, 0))
        print(plantimage.avg_temp)
        arr = np.array(data, dtype=np.float32)
        x_data = arr[0:4]
        dict = sess.run(hypothesis, feed_dict={X: x_data})
        price = dict[0]
        return render(request, "index.html",{"price":price})
    else:
        return render(request, "index.html")
    