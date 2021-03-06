#!-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tm = models.DateTimeField('创建时间', auto_now_add=True)
    front_cover = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.name


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tm = models.DateTimeField('上传时间', auto_now_add=True)
    img = models.ImageField(upload_to="./")
    url = models.CharField(max_length=300)
    album = models.ForeignKey(Album)

    def __unicode__(self):
        return self.name
    
    def get_thumbnail_url(self):
        url = '/'.join(str(self.img).split('/')[-2: ])
        return url 

    def get_absolute_url(self):
        url = '/'.join(self.url.split('/')[-2: ])
        return url 

