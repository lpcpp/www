from forms import UserForm, BlogForm
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from models import Blog, Category
from django.contrib.auth.decorators import login_required
import logging
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.mail import send_mail
from www.settings import EMAIL_USER_TO, EMAIL_HOST_USER

logger = logging.getLogger('runlog')


def add_category(request):
    logger.debug('enter add category')
    if request.user.is_authenticated():
        return render_to_response('add_category.html', context_instance=RequestContext(request))
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
        return render_to_response('add_blog.html', {'categorys': categorys}, context_instance=RequestContext(request))
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
        b = Blog(caption=caption, content=content, category=c)
        b.save()

    return render_to_response('add_blog_success.html', context_instance=RequestContext(request))


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
    if request.user.is_authenticated():
        logger.debug('backyard user is authenticated') 
        blogs = Blog.objects.all().order_by('-tm')
        page = request.GET.get('page')
        blogs = paginator(blogs, page, num=10)

        return render_to_response('backend.html', {'blogs': blogs}, context_instance=RequestContext(request))
    else:
        logger.debug('bakcyard user is not authenticated')
        return HttpResponseRedirect('/login/')


def index(request):
    blogs = Blog.objects.all().order_by('-tm')
    logger.debug('blogs==%s', blogs)
    page = request.GET.get('page')
    blogs = paginator(blogs, page)
    logger.debug('request.user=%s', request.user)
    logger.debug('blogs==%s', blogs)
    return render_to_response('index.html', {'blogs': blogs, 'request': request})


def detail(request, id):
    logger.debug('enter detail')
    blog = Blog.objects.get(id=int(id))
    logger.debug('blog tail====%s', blog)
    return render_to_response('detail.html', {'blog': blog, 'request': request})


def about(request):
    return render_to_response('about.html')


def del_blog(request, id):
    if request.user.is_authenticated():
        logger.debug('enter del_blog')
        Blog.objects.get(id=int(id)).delete()
        return HttpResponseRedirect('/del_blog_success/')
    else:
        return HttpResponseRedirect('/login/')


def del_blog_success(request):
    logger.debug('enter del blog success')
    return render_to_response('del_blog_success.html')


def del_category(request, id):
    if request.user.is_authenticated():
        logger.debug('enter del_category')
        Category.objects.get(id=int(id)).delete()
        return HttpResponseRedirect('/del_category_success/')
    else:
        return HttpResponseRedirect('/login/')


def del_category_success(request):
        logger.debug('enter del category success')
        return render_to_response('del_blog_success.html')


def category_list(request):
    categorys = Category.objects.all().order_by('-tm')
    return render_to_response('category_list.html', {'categorys': categorys, 'request': request})


def category_detail(request, id):
    category = Category.objects.get(id=int(id))
    return render_to_response('category_detail.html', {'category': category, 'request': request})


def play_video(request):
    return render_to_response('video.html')


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
            blogs = paginator(blogs, page)
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
