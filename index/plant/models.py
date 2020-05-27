from django.db import models

# Create your mo(dels here.
class Plantimage(models.Model):
    avg_temp = models.FloatField(blank="null")
    min_temp = models.FloatField(blank="null")
    max_temp = models.FloatField(blank="null")
    rain_fall = models.FloatField(blank="null")
    
class Test(models.Model):
    images = models.ImageField(upload_to="",blank="null")