from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.urls import reverse

from account.models import UserProInfo, UserInfo
from manager.models import Status


def home_required(func):

    def wrapper(*args,**kwargs):
        for a in args:
            if isinstance(a,WSGIRequest):
                user = a.user
                user_obj = User.objects.get(username=user.username)
                status_obj = Status.objects.all()[0]
                apply_year = (status_obj.apply_year).split("-")[0]
                if not UserProInfo.objects.filter(user=user_obj,apply_year=apply_year):
                    # return HttpResponseRedirect('/account/index')
                    return HttpResponseRedirect(reverse('account:account_index'))

        return func(*args,**kwargs)
    return wrapper


def index_required(func):

    def wrapper(*args,**kwargs):
        for a in args:
            if isinstance(a,WSGIRequest):
                user = a.user
                print(user.username)
                user_obj = User.objects.get(username=user.username)
                status_obj = Status.objects.all()[0]
                apply_year = (status_obj.apply_year).split("-")[0]
                if UserProInfo.objects.filter(user=user_obj,apply_year=apply_year):
                    # return HttpResponseRedirect('/account/home')
                    return HttpResponseRedirect(reverse('account:account_home'))

        return func(*args,**kwargs)
    return wrapper

def userinfo_required(func):

    def wrapper(*args,**kwargs):
        for a in args:
            if isinstance(a,WSGIRequest):
                user = a.user
                user_obj = User.objects.get(username=user.username)
                if UserInfo.objects.filter(user=user_obj):
                    userinfo = UserInfo.objects.get(user=user_obj)
                    if userinfo.phone.strip() == "":
                        # return HttpResponseRedirect('/account/index/edit-my-information/')
                        return HttpResponseRedirect(reverse('account:index_edit_my_information'))

        return func(*args,**kwargs)
    return wrapper

# 会频繁重定向
# def upload_required(func):
#     def wrapper(*args,**kwargs):
#         for a in args:
#             if isinstance(a,WSGIRequest):
#                 status_obj = Status.objects.all()[0]
#                 mode = status_obj.mode
#                 print(mode)
#                 if mode == 1:
#                     return HttpResponseRedirect(reverse('account:upload_apply'))
#                 elif mode == 2:
#                     return HttpResponseRedirect(reverse('account:upload_middle'))
#                 elif mode == 3:
#                     return HttpResponseRedirect(reverse('account:upload_conclude'))
#
#         return func(*args,**kwargs)
#     return wrapper
#

