#!-*- coding:utf-8 -*-
from django import forms
from models import Blog
from django.forms import ModelForm


class LoginForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=50)
    password = forms.CharField(label=u"密码", widget=forms.PasswordInput())
    verify_code = forms.CharField(max_length=10)


class RegisterForm(forms.Form):
    username = forms.CharField(label=u"用户名", max_length=50)
    password1 = forms.CharField(label=u"密码", widget=forms.PasswordInput())
    password2 = forms.CharField(label=u"请重复密码", widget=forms.PasswordInput())
    email = forms.EmailField()
    verify_code = forms.CharField(max_length=10)
    

class BlogForm(ModelForm):
    class Meta:
        model = Blog
    
