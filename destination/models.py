
from django.db import models
import datetime

# Create your models here.
class rating(models.Model):
    rate=models.IntegerField(choices=[(1,1),(2,2),(3,3),(4,4),(5,5)]) 
   

class places(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=30)
    descrption=models.TextField()



class destimages(models.Model):
    place=models.ForeignKey(places,on_delete=models.CASCADE)
    image=models.ImageField()

class hotel(models.Model):
    title=models.CharField(max_length=20)
    contact_info=models.CharField(max_length=15)
    nearby=models.ForeignKey(places,on_delete=models.CASCADE)




        





