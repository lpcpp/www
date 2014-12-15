from django.conf.urls import patterns, include, url
from gallery.views import *


urlpatterns = patterns('',
    url(r'create_album/$', create_album),
    url(r'create_album_success/$', create_album_success),

#    url(r'album/album_name/$' 
    url(r'upload_photo/$', upload_photo),
    url(r'upload_photo_success/$', upload_photo_success),

    url(r'album_list/$', album_list),

    url(r'album_list/(?P<album_name>.+)/(?P<photo_name>.+)/$', photo_detail),
    url(r'album_list/(?P<album_name>.+)/$', album_detail),

    url(r'del_album/(?P<album_name>.+)/$', del_album),
    url(r'del_photo/(?P<photo_name>.+)/$', del_photo),
)
