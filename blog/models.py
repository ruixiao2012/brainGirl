# -*- coding:utf-8 -*-
# django library
from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)


class Account(models.Model):
    username = models.ForeignKey(User, related_name='user_account')
    account = models.DecimalField(max_digits=30,decimal_places=2)


class Queston(models.Model):
    username = models.ForeignKey(User, related_name='user_question')
    #type={picture，music,idiom}
    type = models.CharField(max_length=50)
    #question title
    title = models.CharField(max_length=5000)
    #question options
    options = models.CharField(max_length=1000)
    #question right answer
    answer = models.CharField(max_length=50)
    #question attachment
    attach = models.CharField(max_length=500)
    #if adopted
    adopt = models.IntegerField()
    #mark1
    mark1= models.CharField(max_length=100)


class PictureFile(models.Model):
    picture= models.FileField(upload_to="picture")

class AudioFile(models.Model):
    music= models.FileField(upload_to="music")

