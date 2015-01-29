from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from restful import views


urlpatterns = (
    url(r'api/blog_list/$', views.Blog_list.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
