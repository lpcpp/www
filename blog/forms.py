#!-*- coding:utf-8 -*-
from django import forms
from models import User
from models import Blog
from django.forms import ModelForm


class UserForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=50)
    password = forms.CharField(label=u"密码", widget=forms.PasswordInput())


class BlogForm(ModelForm):
    class Meta:
        model = Blog
    
