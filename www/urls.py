from django.conf.urls import patterns, include, url
from blog.views import *

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'www.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', log_in, name="login"),
    url(r'^logout/$', log_out, name="logout"),

    url(r'^backyard/$', backyard, name="backyard"),
    url(r'^index/$', index),

    url(r'^add_blog/$', add_blog),
    url(r'^add_blog_success/$', add_blog_success, name="add_blog_success"),

    url(r'^add_category/$', add_category, name="add_category"),
    url(r'^add_category_success/$', add_category_success, name="add_category_success"),
)
