# from django.contrib.sessions.models import Session
# from django.conf import settings
# from django import VERSION as DJANGO_VERSION
from django.utils import deprecation
# from importlib import import_module
from catalog.models import Visitor1, OldSession, OldIp
from catalog.models import Visitors

# engine = import_module(settings.SESSION_ENGINE)


# def is_authenticated(user):
#     """
#     Check if user is authenticated, consider backwards compatibility
#     """
#     if DJANGO_VERSION >= (1, 10, 0):
#         return user.is_authenticated
#     else:
#         return user.is_authenticated()


class PreventConcurrentLoginsMiddleware(deprecation.MiddlewareMixin):
    """
    Django middleware that prevents multiple concurrent logins..
    Adapted from http://stackoverflow.com/a/1814797 and https://gist.github.com/peterdemin/5829440
    """

    def process_request(self, request):
        if request.user.is_authenticated:
            key_from_cookie = request.session.session_key
            if hasattr(request.user, 'visitors'):
                # print('zzzz1')
                # print(hasattr(request.user, 'visitor'))
                session_key_in_visitor_db = request.user.visitors.session_key
                request.session['sessionid'] = session_key_in_visitor_db
                # print(request.session.get('sessionid'))
                # print(obj,create)
                (obj, created) = OldSession.objects.get_or_create(session_key=session_key_in_visitor_db,
                                                                  defaults={'session_key': session_key_in_visitor_db})

                if not OldSession.objects.filter(session_key=request.session.session_key).exists():
                    if session_key_in_visitor_db != key_from_cookie:
                        # Delete the Session object from database and cache

                        # engine.SessionStore(session_key_in_visitor_db).delete()
                        # print(key_from_cookie)
                        request.user.visitors.session_key = key_from_cookie
                        request.user.visitors.save()
                        # print(request.user.visitor.session_key)
                        # (obj, created) = OldSession.objects.get_or_create(session_key=key_from_cookie,
                        # defaults={'session_key': key_from_cookie})

            else:
                # print('zzzz2')
                request.session['sessionid'] = key_from_cookie
                (obj, created) = OldSession.objects.get_or_create(
                    session_key=key_from_cookie, defaults={'session_key': key_from_cookie})
                Visitors.objects.create(user=request.user,
                                        session_key=key_from_cookie)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
            else:
                ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
            # print(str(ip))
            if hasattr(request.user, 'visitor1'):
                # print('zzzz3')
                request.session['oldip'] = request.user.visitor1.ip
                session_ip = request.user.visitor1.ip
                # print(session_key_in_visitor_db)
                # print(session_key_in_visitor_db != key_from_cookie)
                # print(key_from_cookie)
                (obj, created) = OldIp.objects.get_or_create(ip=str(ip),
                                                             defaults={'ip': session_ip})
                if not OldIp.objects.filter(ip=str(ip)).exists():
                    if session_ip != str(ip):
                        request.user.visitor1.ip = str(ip)
                        request.user.visitor1.save()
            else:
                # print('zzzz4')
                (obj, created) = OldIp.objects.get_or_create(ip=str(ip),
                                                             defaults={'ip': str(ip)})
                # print(request.session.get('sessionid'))
                request.session['oldip'] = str(ip)
                Visitor1.objects.create(
                    user=request.user, session_key=request.session.get('sessionid'), ip=str(ip))
        else:
            request.session['zz'] = 'zz'
