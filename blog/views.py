# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from models import Blog, Category
from django.contrib.auth.decorators import login_required
import logging
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.mail import send_mail
from www.settings import EMAIL_USER_TO, EMAIL_HOST_USER
import oauth2 as oauth


logger = logging.getLogger('runlog')


app_key = '123456789'
app_secret = '987654321'
consumer = oauth.Consumer(app_key, app_secret)
client = oauth.Client(consumer)

request_token_url = 'https://api.weibo.com/oauth2/authorize'


def add_category(request):
    logger.debug('enter add category')
    if request.user.is_authenticated():
        return render_to_response('blog/add_category.html', {'request': request}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


@login_required
def add_category_success(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        c = Category(name=name, description=description)
        c.save()
    return render_to_response('blog/add_category_success.html', context_instance=RequestContext(request))


def add_blog(request):
    logger.debug('enter add-blog')
    logger.debug('1111' + str(request.user))
    if request.user.is_authenticated():
        logger.debug('add_blog: request.user.is_authenticated')
        categorys = Category.objects.all()
        logger.debug('categorys:%s', categorys)
        return render_to_response('blog/add_blog.html', {'categorys': categorys, 'request': request}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def modify_blog(request):
    logger.debug('enter modify blog')


@login_required
def add_blog_success(request):
    logger.debug('enter success')
    if request.method == "POST":
        logger.debug('request.POST:' + str(request.POST))

        caption = request.POST['caption']
        content = request.POST['content']
        category = request.POST['category']
#        logger.debug('category======%s', str(dir(category)))
        c = Category.objects.get(name=category)
        b = Blog(caption=caption, content=content, category=c, user=request.user)
        b.save()

    return render_to_response('blog/add_blog_success.html', context_instance=RequestContext(request))


def paginator(blogs, page, num=1):
    logger.debug('page=%s, blogs=%s', page, blogs)
    paginator = Paginator(blogs, num)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    logger.debug('bbloooogs=%s', blogs)
    return blogs


def backyard(request):
    logger.debug('enter backyard')
    logger.error('enter backyard')
    if request.user.is_authenticated():
        logger.debug('backyard user is authenticated')
        print '88888888888user', request.user, type(request.user)
        blogs = Blog.objects.filter(user=request.user).order_by('-tm')
        page = request.GET.get('page')
        blogs = paginator(blogs, page, num=10)

        return render_to_response('blog/backend.html', {'blogs': blogs, 'request': request}, context_instance=RequestContext(request))
    else:
        logger.debug('bakcyard user is not authenticated')
        return HttpResponseRedirect('/login/')


def index(request):
    logger.debug('enter index')
    logger.error('enter index')
    blogs = Blog.objects.all().order_by('-tm')
    logger.debug('blogs==%s', blogs)
    page = request.GET.get('page')
    blogs = paginator(blogs, page, num=10)
    logger.debug('request.user=%s', request.user)
    logger.debug('blogs==%s', blogs)
    if request.GET.get('domain'):
        user = authenticate(username=request.GET.get('domain'), password='test')
        login(request, user)

    x = RequestContext(request)
    logger.debug('context_instance===%s', x)
    return render_to_response('blog/index.html', {'blogs': blogs, 'request': request}, context_instance=RequestContext(request))


def blog(request):
    logger.debug('enter blog')
    if request.user.is_authenticated():
        blogs = Blog.objects.filter(user=request.user).order_by('-tm')
    else:
        blogs = Blog.objects.all().order_by('-tm')
    logger.debug('blogs==%s', blogs)
    page = request.GET.get('page')
    blogs = paginator(blogs, page, num=10)
    logger.debug('request.user=%s', request.user)
    logger.debug('blogs==%s', blogs)
    return render_to_response('blog/index.html', {'blogs': blogs, 'request': request})


def detail(request, id):
    logger.debug('enter detail')
    blog = Blog.objects.get(id=int(id))
    logger.debug('blog tail====%s', blog)
    return render_to_response('blog/detail.html', {'blog': blog, 'request': request})


def about(request):
    return render_to_response('blog/about.html', {'request': request})


def del_blog(request, id):
    if request.user.is_authenticated():
        logger.debug('enter del_blog')
        Blog.objects.get(id=int(id)).delete()
        return HttpResponseRedirect('/del_blog_success/')
    else:
        return HttpResponseRedirect('/login/')


def del_blog_success(request):
    logger.debug('enter del blog success')
    return render_to_response('blog/del_blog_success.html', {'request': request})


def del_category(request, id):
    if request.user.is_authenticated():
        logger.debug('enter del_category')
        Category.objects.get(id=int(id)).delete()
        return HttpResponseRedirect('/del_category_success/')
    else:
        return HttpResponseRedirect('/login/')


def del_category_success(request):
        logger.debug('enter del category success')
        return render_to_response('blog/del_blog_success.html', {'request': request})


def category_list(request):
    categorys = Category.objects.all().order_by('-tm')
    return render_to_response('blog/category_list.html', {'categorys': categorys, 'request': request})


def category_detail(request, id):
    category = Category.objects.get(id=int(id))
    return render_to_response('blog/category_detail.html', {'category': category, 'request': request})


def play_video(request):
    return render_to_response('gallery/video.html', {'request': request})


def search(request):
    logger.debug('enter request')
    logger.debug('request.get==%s', request.GET)
    logger.debug('request.user==%s', request.user)
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            q = 'theweatherisgood'
            blogs = []
            return render_to_response('blog/index.html', {'blogs': blogs, 'query': q, 'request': request})

        else:
            q = request.GET.get('q')
            if '?' in q:
                page = int(q.split('=')[-1])
                q = q.split('?')[0]
            else:
                page = 1
            blogs = Blog.objects.filter(caption__icontains=q)
            if blogs:
                length = len(blogs)
            else:
                length = 0
            blogs = paginator(blogs, page, num=10)
    return render_to_response('blog/index.html', {'blogs': blogs, 'query': q, 'len': length, 'request': request})


def contact(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        sender = request.POST['sender']
        logger.info('sender=%s', sender)
        send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_USER_TO], fail_silently=True)
        return HttpResponseRedirect('/contact/send_mail_success/')

    return render_to_response('blog/contact.html', {'request': request}, context_instance=RequestContext(request))


def send_mail_success(request):
    return render_to_response('blog/send_mail_success.html')


def test(request):
    return render_to_response('blog/test.html')
