from django.db import models
    
class MyCamera(models.Model):
    images = models.FileField(upload_to="",blank="null")
    device = models.TextField(blank="null")
    date = models.TextField(blank="null")
    first_name = models.CharField(max_length=30, blank="null")
    first_percent = models.FloatField(blank="null")
    second_name = models.CharField(max_length=30, blank="null")
    second_percent = models.FloatField(blank="null")

class Plantconnect(models.Model):
    name = models.CharField(max_length=30, blank="null")
    flower = models.TextField(blank="null")
    content = models.TextField(blank="null")
    image = models.FileField(upload_to="",blank="null")

class Plantadd(models.Model):
    # number = models.IntegerField(blank="null")
    device = models.TextField(blank="null")
    name = models.CharField(max_length=30,blank="null")
    flower = models.TextField(blank="null")
    content = models.TextField(blank="null")
    image = models.TextField(blank="null")