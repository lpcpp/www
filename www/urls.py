from django.conf.urls import patterns, include, url
from blog import views
from blog.verifycode import verify_code
from blog.oAuth import oauth, request_token, access_token
import auth.views
import settings

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^login/$', auth.views.log_in, name="login"),
    url(r'^logout/$', auth.views.log_out, name="logout"),

    url(r'^oauth2/request_token/(.+)/$', request_token, name="request_token"),
    url(r'^oauth2/access_token/(.+)/$', access_token, name="access_token"),

    url(r'^oauth?', oauth),

    url(r'^backyard/$', views.backyard, name="backyard"),
    url(r'^index/$', views.index),
    url(r'^$', views.index),
    url(r'^blog/$', views.blog),

    url(r'^add_blog/$', views.add_blog),
    url(r'^add_blog_success/$', views.add_blog_success, name="add_blog_success"),

    url(r'^add_category/$', views.add_category, name="add_category"),
    url(r'^add_category_success/$', views.add_category_success, name="add_category_success"),

    url(r'^detail/(?P<id>\d+)/$', views.detail),
    url(r'^about/$', views.about),

    url(r'^del_blog/(?P<id>\d+)/$', views.del_blog),
    url(r'^del_blog_success/$', views.del_blog_success),

    url(r'^category_list/$', views.category_list),
    url(r'^category_detail/(?P<id>\d+)/$', views.category_detail),

    url(r'^del_category/(?P<id>\d+)/$', views.del_category),
    url(r'^del_category_success/$', views.del_category_success),

    url(r'^gallery/', include('gallery.urls')),

    url(r'^videoplay/$', views.play_video),

    url(r'^blog/search/$', views.search),

    url(r'^contact/$', views.contact),
    url(r'^contact/send_mail_success/$', views.send_mail_success),

    url(r'^verify_code/$', verify_code),
    url(r'^register/$', auth.views.register),
    url(r'^register/success/$', auth.views.register_success),
    url(r'^register/activation_error/$', auth.views.activate_error),
    url(r'^register/activation/$', auth.views.activate_state),
    url(r'register/activate/(?P<username>\w+)/(?P<activation_key>\w+)/$', auth.views.activate),

    # url(r'^ckeditor/', include('ckeditor.urls')),
)

urlpatterns += (
    url(r'^', include('blog.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('', url(r'^media/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),)
