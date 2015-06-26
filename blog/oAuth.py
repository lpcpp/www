import logging
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from weibo import APIClient
import httplib2


APP_KEY = "381709949"
APP_SECRET = "9cfe955ae9c7967cbe01caf15c46c8ce"
CALLBACK_URL = "http://115.28.15.67/oauth"


client = APIClient(app_key=APP_KEY,
                   app_secret=APP_SECRET,
                   redirect_uri=CALLBACK_URL,
)


logger = logging.getLogger('runlog')


def oauth(request):
    #logger.info('enter oauth')
    code = request.GET.get('code')
    #logger.info('code==========%s', code)

#    import time 
#    time.sleep(10)
#    return HttpResponseRedirect('/index/') 
    
    r = client.request_access_token(code)


    print 'rrrrrrrrrrrrrrrrrrrrr', r.__dict__.keys()
    
    #logger.debug(type(r))
    access_token = r.access_token
    print 'rrrrrrrrrrrrrrrrrrrrr',access_token 
    refresh_token = r.refresh_token
    print 'refresh_token=====', refresh_token
    expire_in = r.expires_in
    client.set_access_token(access_token, expire_in)
    #logger.debug('access_token=%s', access_token)

    uid = client.account.get_uid.get(access_token=access_token)
    #logger.debug('uid====%s', uid)
    #logger.debug('type(uid)====%s', type(uid))
    uid = uid.get('uid')
    #logger.debug('uid====%s', uid)
    userinfo = client.users.show.get(uid = uid)
    logger.debug('userinfo==%s', userinfo)
    #return render_to_response(str(userinfo))

    from django.contrib.auth.models import User
    username = userinfo.domain
    email = 'test@test.com'
    password = 'test'
    if not User.objects.filter(username=userinfo.domain):
        user = User.objects.create_user(username, email, password)
        user.save()
    return HttpResponseRedirect('/index/?domain=%s' % userinfo.domain)

def third_authenticated(request):
    logger.debug('enter third_authencated')
    logger.debug(request)
    

def request_token(request, request_token):
    logger.debug('enter oauth2_code')
    logger.debug('request_token====%s', request_token)

    #return HttpResponseRedirect('/index/') 
    
    
    h = httplib2.Http()
    app_id = '1234567890'
    app_secret = 'iamsecret'

    # url below should be a https
    url = "http://115.28.15.67:8888/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=http://115.28.15.67/&code=%s" % (app_id, app_secret, request_token)
    #logger.debug('url===%s', url)
    resp, content = h.request(url)
    print '---------------------------'
    print content
    import json
    json_data = json.loads(content)
    access_token = json_data['access_token']

    url = 'http://115.28.15.67:8888/api/getinfo/%s/' % access_token
    resp, content = h.request(url)
    print content
    print '---------------------------'
    #return HttpResponseRedirect('/')

    from django.contrib.auth.models import User
    import json
    json_data = json.loads(content) 
    username = json_data.get('username') 
    if username:
       email = ''
       password = 'test'
       if not User.objects.filter(username=username):
           user = User.objects.create_user(username, email, password)
           user.save()
       return HttpResponseRedirect('/index/?domain=%s' % username)

    return HttpResponseRedirect('/')

def access_token(request, access_token):
    #logger.debug('access_token=%s', access_token)
    return HttpResponseRedirect('/index/') 


def test_wenjuan(request):
    code = request.GET.get('code')
    "https://test.wenjuan.com/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI&code=CODE"
    

    return HttpResponseRedirect('/index/') 
