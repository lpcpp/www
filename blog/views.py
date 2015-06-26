#!-*-coding:utf-8-*-
from forms import LoginForm, BlogForm, RegisterForm
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from models import Blog, Category
from django.contrib.auth.decorators import login_required
import logging
import hashlib
import random
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.mail import send_mail
from django.contrib.auth.models import User
from www.settings import EMAIL_USER_TO, EMAIL_HOST_USER
import oauth2 as oauth
import cgi
from blog.models import Profile


logger = logging.getLogger('runlog')


app_key = '123456789'
app_secret = '987654321'
consumer = oauth.Consumer(app_key, app_secret)
client = oauth.Client(consumer)

request_token_url = 'https://api.weibo.com/oauth2/authorize'


def add_category(request):
    logger.debug('enter add category')
    if request.user.is_authenticated():
        return render_to_response('add_category.html', {'request': request}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


@login_required
def add_category_success(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        c = Category(name=name, description=description)
        c.save()
    return render_to_response('add_category_success.html', context_instance=RequestContext(request))


def add_blog(request):
    logger.debug('enter add-blog')
    logger.debug('1111' + str(request.user))
    if request.user.is_authenticated():
        logger.debug('add_blog: request.user.is_authenticated')
        categorys = Category.objects.all()
        logger.debug('categorys:%s', categorys)
        return render_to_response('add_blog.html', {'categorys': categorys, 'request': request}, context_instance=RequestContext(request))
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
        #logger.debug('category======%s', str(dir(category)))
        c = Category.objects.get(name=category)
        b = Blog(caption=caption, content=content, category=c, user=request.user)
        b.save()

    return render_to_response('add_blog_success.html', context_instance=RequestContext(request))


def validate_login(request, username, password):
    user = authenticate(username=username, password=password)
    logger.debug('uuuuuuser=%s', user)
    logger.debug('type_uuuuuuser=%s', type(user))
    if user:
        logger.debug('user.is_active==%s', user.is_active)
        if user.is_active:
                login(request, user)
                logger.debug('after register')
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
                return render_to_response('register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))
            username = rf.cleaned_data["username"]
            if User.objects.filter(username=username):
                errors.append("用户名已存在")
                return render_to_response('register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))
            password1 = rf.cleaned_data["password1"]
            password2 = rf.cleaned_data["password2"]
            if password1 != password2:
                errors.append("两次输入的密码不一致")
                return render_to_response('register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))
            logger.debug('user create')
            email = rf.cleaned_data['email']
            user = User.objects.create_user(username, email, password1)
#            user = User.objects.create_user(username, email, password1, is_active=False)
            user.is_active = False
            user.save()
            salt  = hashlib.sha1(str(random.random())).hexdigest()[:5]
            logger.debug('salt====%s', salt)
            activation_key = hashlib.sha1(salt + username).hexdigest()
            logger.debug('activation_key====%s', activation_key)
#            logger.debug('validate_login')
#            validate_login(request, username, password1)
            subject = "test reigster"
            message = '127.0.0.1:8000/register/activate/' + username + '/' + activation_key + '/'
            request.session['activation_key'] = activation_key
            send_mail(subject, message, EMAIL_HOST_USER, [rf.cleaned_data['email']], fail_silently=True)
            return HttpResponseRedirect('/register/activation/')

    rf = RegisterForm()
    return render_to_response('register.html', {'errors': errors, 'rf': rf}, context_instance=RequestContext(request))


def activate_state(request):
    logger.debug('enter activate_state')
    msg = "请进入邮箱认证"
    return render_to_response('register_feedback.html', {'msg': msg})

def activate(request, username, activation_key):
    logger.debug('enter activate')
    logger.debug('username==%s', username)
    logger.debug('activation11=%s', activation_key)

    if not request.session['activation_key']:
        User.objects.get(name=username).delete()
        return HttpResponseRedirect('/register/activation_error/')
    if request.session['activation_key'] == activation_key:
        logger.debug('eeeee')
        user = User.objects.get(username=username)
        logger.debug('uuuuuu=%s', user.username)
        user.is_active = True
        user.save()
        #request.user = user
        logger.debug('request.user2222===%s', request.user)
        return HttpResponseRedirect('/register/success/')


def activate_error(request):
    logger.debug('enter activate error')
    msg = '该链接已失效，请重新注册'
    render_to_response('register_feedback.html', {'msg': msg})

def register_success(request):
    msg = '激活成功'
    return render_to_response('register_feedback.html', {'msg': msg})
    

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
                return render_to_response('login.html', {'errors': errors, 'lf': lf}, context_instance=RequestContext(request))
            logger.debug('userform is valid')
            username = lf.cleaned_data['username']
            password = lf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    errors.append('该用户尚未激活')
                    return render_to_response('login.html', {'errors': errors, 'lf': lf}, context_instance=RequestContext(request))
                login(request, user)
                return HttpResponseRedirect('/backyard/')
            else:
                logger.debug("username don't match password")
                lf = LoginForm()
                errors = ["username don't match password"]
                return render_to_response('login.html', {'errors': errors, 'lf': lf}, context_instance=RequestContext(request))
        else:
            logger.debug('userform is not valid')
            lf = LoginForm()

    lf = LoginForm()
    url = "http://115.28.15.67:8888/oauth2/authorize?client_id=1234567890&response_type=code&redirect_uri=http://115.28.15.67/oauth2/request_token/"
    return render_to_response('login.html', {'lf': lf, 'url': url}, context_instance=RequestContext(request))

                


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def paginator(blogs, page, num=1):
    logger.debug('page=%s, blogs=%s',page, blogs)
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

        return render_to_response('backend.html', {'blogs': blogs, 'request': request}, context_instance=RequestContext(request))
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

    return render_to_response('index.html', {'blogs': blogs, 'request': request})

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
    return render_to_response('index.html', {'blogs': blogs, 'request': request})


def detail(request, id):
    logger.debug('enter detail')
    blog = Blog.objects.get(id=int(id))
    logger.debug('blog tail====%s', blog)
    return render_to_response('detail.html', {'blog': blog, 'request': request})


def about(request):
    return render_to_response('about.html', {'request': request})


def del_blog(request, id):
    if request.user.is_authenticated():
        logger.debug('enter del_blog')
        Blog.objects.get(id=int(id)).delete()
        return HttpResponseRedirect('/del_blog_success/')
    else:
        return HttpResponseRedirect('/login/')


def del_blog_success(request):
    logger.debug('enter del blog success')
    return render_to_response('del_blog_success.html', {'request': request})


def del_category(request, id):
    if request.user.is_authenticated():
        logger.debug('enter del_category')
        Category.objects.get(id=int(id)).delete()
        return HttpResponseRedirect('/del_category_success/')
    else:
        return HttpResponseRedirect('/login/')


def del_category_success(request):
        logger.debug('enter del category success')
        return render_to_response('del_blog_success.html', {'request': request})


def category_list(request):
    categorys = Category.objects.all().order_by('-tm')
    return render_to_response('category_list.html', {'categorys': categorys, 'request': request})


def category_detail(request, id):
    category = Category.objects.get(id=int(id))
    return render_to_response('category_detail.html', {'category': category, 'request': request})


def play_video(request):
    return render_to_response('video.html', {'request': request})


def search(request):
    logger.debug('enter request')
    logger.debug('request.get==%s', request.GET)
    logger.debug('request.user==%s', request.user)
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            q = 'theweatherisgood' 
            blogs = []
            return render_to_response('index.html', {'blogs': blogs, 'query':q, 'request': request})

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
            logger.debug('pppppppppage=%s', page)
            logger.debug('bxxxxxxe=%s', blogs)
            blogs = paginator(blogs, page, num=10)
            logger.debug('bbbbbbe=%s', blogs)
    return render_to_response('index.html', {'blogs': blogs, 'query':q, 'len': length, 'request': request})


def contact(request):
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        sender = request.POST['sender']
        logger.info('sender=%s', sender)
        send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_USER_TO], fail_silently=True)
        return HttpResponseRedirect('/contact/send_mail_success/')
         
    return render_to_response('contact.html', {'request': request}, context_instance=RequestContext(request))


def send_mail_success(request):
    return render_to_response('send_mail_success.html')
