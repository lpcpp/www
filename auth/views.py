# -*- coding: utf-8 -*-
from forms import LoginForm, RegisterForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
import logging
import hashlib
import time
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from www.settings import EMAIL_HOST_USER
from www.settings import DOMAIN


logger = logging.getLogger('auth')


def validate_login(request, username, password):
    user = authenticate(username=username, password=password)
    logger.debug('validate_login.user=%s', user)
    if user:
        logger.debug('user.is_active==%s', user.is_active)
        if user.is_active:
                login(request, user)
        else:
            logger.error('此用户尚未激活')


def register(request):
    logger.debug('enter register')
    errors = []
    if request.method == "POST":
        rf = RegisterForm(request.POST)
        if rf.is_valid():
            logger.debug('session_verify_code===%s', str(request.session['verifycode']))
            if str(rf.cleaned_data['verify_code']).lower() != str(request.session['verifycode']).lower():
                errors.append("验证码错误")
                return render_to_response('auth/register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))

            username = rf.cleaned_data["username"]
            if User.objects.filter(username=username):
                errors.append("用户名已存在")
                return render_to_response('auth/register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))

            password1 = rf.cleaned_data["password1"]
            password2 = rf.cleaned_data["password2"]
            if password1 != password2:
                errors.append("两次输入的密码不一致")
                return render_to_response('auth/register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))

            email = rf.cleaned_data['email']
            user = User.objects.create_user(username, email, password1)
            user.is_active = False
            user.save()

            activation_key = hashlib.sha1(''.join((str(random.random()), username, str(time.time())))).hexdigest()
            logger.debug('activation_key====%s', activation_key)
            subject = "test reigster"
            message = DOMAIN + '/register/activate/' + username + '/' + activation_key + '/'
            request.session['activation_key'] = activation_key
            send_mail(subject, message, EMAIL_HOST_USER, [rf.cleaned_data['email']], fail_silently=True)
            return HttpResponseRedirect('/register/activation/')

    rf = RegisterForm()
    return render_to_response('auth/register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))


def activate_state(request):
    logger.debug('enter activate_state')
    msg = "请进入邮箱认证"
    return render_to_response('auth/register_feedback.html', {'msg': msg})


def activate(request, username, activation_key):
    logger.debug('enter activate')

    if not request.session['activation_key']:
        User.objects.get(name=username).delete()
        return HttpResponseRedirect('/register/activation_error/')
    if request.session['activation_key'] == activation_key:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        logger.debug('activate.request.user===%s', request.user)
        return HttpResponseRedirect('/register/success/')


def activate_error(request):
    logger.debug('enter activate error')
    msg = '该链接已失效，请重新注册'
    render_to_response('auth/register_feedback.html', {'msg': msg})


def register_success(request):
    msg = '激活成功'
    index_url = DOMAIN
    return render_to_response('auth/register_feedback.html', {'msg': msg, 'index_url': index_url})


def log_in(request):
    logger.info('enter log_in')
    logger.error('enter log_in')
    logger.debug('request.method' + request.method)
    errors = []
    if request.method == "POST":
        lf = LoginForm(request.POST)
        if lf.is_valid():
            if str(lf.cleaned_data['verify_code']).lower() != str(request.session['verifycode']).lower():
                errors.append("验证码错误")
                return render_to_response('auth/login.html', {'errors': errors, 'lf': lf}, context_instance=RequestContext(request))
            logger.debug('userform is valid')
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    errors.append('该用户尚未激活')
                    return render_to_response('auth/login.html', {'errors': errors, 'lf': lf}, context_instance=RequestContext(request))
                login(request, user)
                return HttpResponseRedirect('/backyard/')
            else:
                logger.debug("username don't match password")
                lf = LoginForm()
                errors = ["username don't match password"]
                return render_to_response('auth/login.html', {'errors': errors, 'lf': lf}, context_instance=RequestContext(request))
        else:
            logger.debug('userform is not valid')
            lf = LoginForm()

    lf = LoginForm()
    url = "http://115.28.15.67:8888/oauth2/authorize?client_id=1234567890&response_type=code&redirect_uri=http://115.28.15.67/oauth2/request_token/"
    return render_to_response('auth/login.html', {'lf': lf, 'url': url}, context_instance=RequestContext(request))


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')
