#!-*-coding:utf-8-*-
from django.db import models

# Create your models here.
class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tm = models.DateTimeField('创建时间', auto_now_add=True)
    front_cover = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name


class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tm = models.DateTimeField('上传时间', auto_now_add=True)
    img = models.ImageField(upload_to="gallery/media/")
    url = models.CharField(max_length=300)
    album = models.ForeignKey(Album)

    def __unicode__(self):
        return self.name
