from django.conf.urls import patterns, include, url
from gallery.views import *


urlpatterns = patterns('',
    url(r'create_album/$', create_album),
    url(r'create_album_success/$', create_album_success),

#    url(r'album/album_name/$' 
    url(r'upload_photo/$', upload_photo),
    url(r'upload_photo_success/$', upload_photo_success),

    url(r'album_list/$', album_list),
    url(r'album_list/(.+)$', album_detail),
)
