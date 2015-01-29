from blog.models import Blog
from blog.serializer import BlogSerializer
from django.http import Http404
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json; charset=utf8'
        super(JSONResponse, self).__init__(content, **kwargs)


#class Blog_list(APIView):
#    """
#    List all snippets
#    """
#    def get(self, request, format=None):
#        blogs = Blog.objects.all()
#        serial = BlogSerializer(blogs, many=True)
#        return Response(serial.data)


class Blog_list(APIView):
    def get(self, request, format=None):
        blogs = Blog.objects.all()
        serial = BlogSerializer(blogs, many=True)
#        return Response(serial.data)
        return JSONResponse(serial.data)

    
