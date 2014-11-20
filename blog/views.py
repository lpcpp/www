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

logger = logging.getLogger('runlog')


@login_required
def add_category(request):
    logger.debug('enter add category')
    return render_to_response('add_category.html', context_instance=RequestContext(request))


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
        logger.debug('category======%s', str(dir(category)))
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

@login_required
def backyard(request):
    logger.debug('enter backyard') 
    if request.user.is_authenticated():
        logger.debug('backyard user is authenticated') 
        blogs = Blog.objects.all().order_by('-tm')
        paginator = Paginator(blogs, 10)
        page = request.GET.get('page')
        logger.debug('paginator.num_pages:%s', paginator.num_pages)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        return render_to_response('backend.html', {'blogs': blogs}, context_instance=RequestContext(request))
    else:
        logger.debug('bakcyard user is not authenticated')
        return HttpResponseRedirect('/login/')



def index(request):
    blogs = Blog.objects.all().order_by('-tm')
    paginator = Paginator(blogs, 5)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    logger.debug('request.user=%s', request.user)
    return render_to_response('index.html', {'blogs': blogs, 'request': request})


def detail(request, id):
    logger.debug('enter detail')
    blog = Blog.objects.get(id=int(id))
    logger.debug('blog tail====%s', blog)
    return render_to_response('detail.html', {'blog': blog, 'request': request})


def about(request):
    return render_to_response('about.html')


def del_blog(request, id):
    logger.debug('enter del_blog')
    Blog.objects.get(id=int(id)).delete()
    return HttpResponseRedirect('/del_blog_success/')


def del_blog_success(request):
    logger.debug('enter del blog success')
    return render_to_response('del_blog_success.html')


def del_category(request, id):
    logger.debug('enter del_category')
    Category.objects.get(id=int(id)).delete()
    return HttpResponseRedirect('/del_category_success/')


def del_category_success(request):
        logger.debug('enter del category success')
        return render_to_response('del_blog_success.html')


def category_list(request):
    categorys = Category.objects.all().order_by('-tm')
    return render_to_response('category_list.html', {'categorys': categorys, 'request': request})


def category_detail(request, id):
    category = Category.objects.get(id=int(id))
    return render_to_response('category_detail.html', {'category': category, 'request': request})
