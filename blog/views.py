from forms import UserForm, BlogForm
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from models import Blog
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger('runlog')


def add_blog(request):
    logger.debug('enter add-blog')
    logger.debug('1111' + str(request.user))
    if request.user.is_authenticated():
        logger.debug('add_blog: request.user.is_authenticated')
        return render_to_response('add_blog.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')



def log_in(request):
    logger.debug('enter log_in')
    userform = UserForm(request.POST)
    logger.debug('request.method' + request.method)
    if userform.is_valid():
        logger.debug('userform is valid')
        username = userform.cleaned_data['username']
        password = userform.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/backyard/')
        else:
            logger.debug("username don't match password")
            user = UserForm()
            errors = ["username don't match password"]
            return render_to_response('login.html', {'errors': errors, 'user': user}, context_instance=RequestContext(request))
    else:
        logger.debug('userform is not valid')
        user = UserForm()
        return render_to_response('login.html', {'user': user}, context_instance=RequestContext(request))
                


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def backyard(request):
    logger.debug('enter backyard') 
    if request.user.is_authenticated():
        logger.debug('backyard user is authenticated') 
        blogs = Blog.objects.all()
        return render_to_response('backend.html', {'blogs': blogs}, context_instance=RequestContext(request))
    else:
        logger.debug('bakcyard user is not authenticated')
        return HttpResponseRedirect('/login/')



def index(request):
    blogs = Blog.objects.all()
    return render_to_response('index.html', {'blogs': blogs})



@login_required
def add_blog_success(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            logger.debug('blog form' + str(form))
            form.save()

    return render_to_response('add_blog_success.html', context_instance=RequestContext(request))
