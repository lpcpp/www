import logging
from django.shortcuts import render_to_response
from weibo import APIClient


APP_KEY = "381709949"
APP_SECRET = "9cfe955ae9c7967cbe01caf15c46c8ce"
CALLBACK_URL = "http://115.28.15.67/oauth"


client = APIClient(app_key=APP_KEY,
                   app_secret=APP_SECRET,
                   redirect_uri=CALLBACK_URL,
)


logger = logging.getLogger('runlog')


def oauth(request):
   # https://api.weibo.com/2/users/show.json
    logger.info('enter oauth')
    code = request.GET.get('code')
    r = client.request_access_token(code)
    logger.debug(type(r))
    access_token = r.access_token
    expire_in = r.expires_in
    client.set_access_token(access_token, expire_in)
    logger.debug('access_token=%s', access_token)

    uid = client.account.get_uid.get(access_token=access_token)
    logger.debug('uid====%s', uid)
    logger.debug('type(uid)====%s', type(uid))
    uid = uid.get('uid')
    logger.debug('uid====%s', uid)
    userinfo = client.users.show.get(uid = uid)
    logger.debug('userinfo==%s', userinfo)
    return render_to_response(str(userinfo))
