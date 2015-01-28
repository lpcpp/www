#!-*-coding:utf-8-*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from gallery.models import Album, Photo
from gallery.forms import AlbumForm, PhotoForm
import time
import os
import shutil
from PIL import Image
import cStringIO
import logging
from www.settings import MEDIA_ROOT


logger = logging.getLogger('runlog')


# Create your views here.
def create_album(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            name = request.POST['name']
            path = os.path.join(MEDIA_ROOT, name)
            logger.debug('pppppath====%s', path)
            # 防止新建重复的相册
            albums = Album.objects.filter(owner=request.user)

            for album in albums:
                if name in album.name:
                    error = 'album already exist, please choose another name'
                    return render_to_response('create_album.html', {'error': error}, context_instance=RequestContext(request))
            al = Album(name=name, front_cover='', path=path, owner=request.user)
            al.save()
            logger.debug('create_album success')
            return HttpResponseRedirect('/gallery/create_album_success/')

        return render_to_response('create_album.html', {'request': request}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def create_album_success(request):
    logger.debug('enter create_album_success')
    return render_to_response('create_album_success.html', {'request': request})


def album_list(request):
    logger.debug('rrrrrrrrrrrrequset.user==%s', request.user)
    if not request.user.is_authenticated():
        return render_to_response("no_album.html")
    albums = Album.objects.filter(owner=request.user)
    logger.debug('albums:%s', albums) 
    # 如果相册下有图片,使用第一张作为封面，否则使用默认的照片作为封面
    for album in albums:
        if album.photo_set.all():
            logger.debug('photo_set[0]===%s', album.photo_set.all()[0].img)
            album.front_cover = '/'.join(str(album.photo_set.all()[0].img).split('/')[-2: ])
        else:
            album.front_cover = 'no_front_cover.jpg' 

        logger.debug('front_cover8888===%s', album.front_cover)

    return render_to_response('album_list.html', {'albums': albums, 'request': request})


def album_detail(request, album_name):
    logger.debug('enter album_detail')
    logger.debug('album_detail===%s', album_name)
    album = Album.objects.get(name=album_name.rstrip('/'))
    photos = Photo.objects.filter(album=album) 
    if photos:
        url = photos[0].get_absolute_url()
        logger.debug('absolute_url===%s', url)

    logger.debug('photos====%s', photos)
    
    return render_to_response('album_detail.html', {'album': album, 'photos': photos, 'request': request})

    

def handle_upload_photo(f, album, fn): #f:图像文件句柄, album:相册名称, fn:图像文件名称
    """
    上传的图像存储到以相册名称命名的文件夹下,图像名称修改为当前时间,杜绝
    名称重复, 图像文件名后缀和上传前文件名称的后缀一致
    """
    logger.debug('enter handle_upload_photo')
    tm = time.strftime('%Y%m%d%H%M%S')
    path = os.path.join(MEDIA_ROOT, album) + '/'
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
    destination.close()

    return url 


def make_thumbnail(f):
    logger.debug('enter make_thumbnail=%s', f)
    img = Image.open(f)
    img.thumbnail((256, 256), Image.ANTIALIAS)
    suffix_type = f.split('.')[-1]
    fn = f.replace(suffix_type, 'thumbnail.' + suffix_type)
    logger.debug('thumbnail=====%s', fn)
    #img.save(fn, suffix_type)
    img.save(fn)
    return fn


def upload_photo(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            logger.debug('FFFFFFFILES==%s', request.FILES)
            pf = PhotoForm(request.POST, request.FILES)
            logger.debug('pf====%s', pf)
            if pf.is_valid():
                name = pf.cleaned_data['name']
                photos = Photo.objects.filter(name=name)
                if photos:
                    error = 'this photo name has already exist, please use another one'
                    return render_to_response('upload_photo.html', {'pf': pf, 'error': error}, context_instance=RequestContext(request))
                album = pf.cleaned_data['album']
                fn = request.FILES['img'].name
                url = handle_upload_photo(request.FILES['img'], str(album), fn)
                thumbnail = make_thumbnail(url) 
                # thumbnail = make_thumbnail(request.FILES['img']) 
            
                #img字段不再用来存储上传的图像,而是存储生成的缩略图thumbnail
                photo = Photo(name=name, url=url, img=thumbnail, album=album)
                photo.save()
                return HttpResponseRedirect('/gallery/upload_photo_success/')
        else:
            pf = PhotoForm()
            albums = Album.objects.all()
        return render_to_response('upload_photo.html', {'pf': pf, 'request': request}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/login/')


def upload_photo_success(request):
    return render_to_response('upload_photo_success.html', {'request': request})


def photo_detail(request, album_name, photo_name):
    logger.debug('enter photo_detail')
    logger.debug('phhhhhoto==%s', photo_name)
    logger.debug('album_name==%s', album_name)
    photo = Photo.objects.get(name=photo_name)
    album = Album.objects.get(name=album_name)
    return render_to_response('photo_detail.html', {'photo': photo, 'album': album, 'request': request})


def del_photo(request, photo_name):
    logger.debug('enter del_photo')
    photo = Photo.objects.filter(name=photo_name)[0]
    album = photo.album
    url = photo.url
    img = photo.img
    photo.delete()
    os.remove(str(url))
    os.remove(str(img))
    url = '/gallery/' + '/album_list/' + str(album) 
    logger.debug('uuuuuuuuuuurl===%s', url)
    return HttpResponseRedirect(url)


def del_album(reqeuset, album_name):
    logger.debug('enter del_album')
    album = Album.objects.filter(name=album_name)[0]
    path = album.path
    album.delete()
    try:
        shutil.rmtree(path)
    except:
        pass
    
    return HttpResponseRedirect('/gallery/album_list/')
