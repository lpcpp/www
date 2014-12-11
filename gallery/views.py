#!-*-coding:utf-8-*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from gallery.models import Album, Photo
from gallery.forms import AlbumForm, PhotoForm
import time
import os
import Image
import logging

logger = logging.getLogger('runlog')


# Create your views here.
def create_album(request):
    if request.method == "POST":
        af = AlbumForm(request.POST)
        if af.is_valid():
            name = af.cleaned_data['name']
            # 防止新建重复的相册
            albums = Album.objects.all()
            for album in albums:
                if name in album.name:
                    error = 'album already exist, please choose another name'
                    return render_to_response('create_album.html', {'af': af, 'error': error}, context_instance=RequestContext(request))
            al = Album(name=name, front_cover='')
            al.save()
            return HttpResponseRedirect('/gallery/create_album_success/')
    else:
        af = AlbumForm()

    return render_to_response('create_album.html', {'af': af}, context_instance=RequestContext(request))


def create_album_success(request):
    return render_to_response('create_album_success.html')


def album_list(request):
    albums = Album.objects.all()
    logger.debug('albums:%s', albums) 
    # 如果相册下有图片,使用第一张作为封面，否则使用默认的照片作为封面
    for album in albums:
        if album.photo_set.all():
            logger.debug('photo_set[0]===%s', album.photo_set.all()[0])
            album.front_cover = album.photo_set.all()[0].img
        else:
            fn = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'static/', 'no_front_cover.jpg')
            album.front_cover = fn 


        logger.debug('front_cover8888===%s', album.front_cover)

    return render_to_response('album_list.html', {'albums': albums})


def album_detail(request, album_name):
    logger.debug('enter album_detail')

    

def handle_upload_photo(f, album, fn): #f:图像文件句柄, album:相册名称, fn:图像文件名称
    """
    上传的图像存储到以相册名称命名的文件夹下,图像名称修改为当前时间,杜绝
    名称重复, 图像文件名后缀和上传前文件名称的后缀一致
    """
    logger.debug('enter handle_upload_photo')
    tm = time.strftime('%Y%m%d%H%M%S')
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'media', album + '/', )
    logger.debug('ppppppath===%s', path)
    suffix_type = fn.split('.')[-1]
    logger.debug('suffix_type:%s', suffix_type)
    if not os.path.exists(path):
        os.makedirs(path)
    url = path + tm + '.' + suffix_type
    logger.debug('88888:%s', url)
    destination = open(url, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)

    return url 


def make_thumbnail(f):
    logger.debug('ffffff===%s', f)
    img = Image.open(f)
    img.thumbnail((256, 256), Image.ANTIALIAS)
    suffix_type = f.split('.')[-1]
    fn = f.replace(suffix_type, 'thumbnail.' + suffix_type)
    logger.debug('thumbnail=====%s', fn)
    #img.save(fn, suffix_type)
    img.save(fn)
    return fn


def upload_photo(request):
    if request.method == "POST":
        logger.debug('FFFFFFFILES==%s', request.FILES)
        pf = PhotoForm(request.POST, request.FILES)
        logger.debug('pf====%s', pf)
        if pf.is_valid():
            name = pf.cleaned_data['name']
            album = pf.cleaned_data['album']
            fn = request.FILES['img'].name
            url = handle_upload_photo(request.FILES['img'], str(album), fn)
            thumbnail = make_thumbnail(url) 
            
            #img字段不再用来存储上传的图像,而是存储生成的缩略图thumbnail
            photo = Photo(name=name, url=url, img=thumbnail, album=album)
            photo.save()
            return HttpResponseRedirect('/gallery/upload_photo_success/')
    else:
        pf = PhotoForm()
        albums = Album.objects.all()
    return render_to_response('upload_photo.html', {'pf': pf}, context_instance=RequestContext(request))


def upload_photo_success(request):
    return render_to_response('upload_photo_success.html')
