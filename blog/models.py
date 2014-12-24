#!-*-coding:utf-8-*-
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    tm = models.DateTimeField('创建时间', auto_now_add=True)
    description = models.TextField()

    def __unicode__(self):
        return self.name


#class User(models.Model):
#    username = models.CharField(max_length=50)
#    password = models.CharField(max_length=50)
#    email = models.EmailField()

#    def __unicode__(self):
#        return self.username
        

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    tm = models.DateTimeField('发表时间', auto_now_add=True)

    def __unicode__(self):
        return self.caption
