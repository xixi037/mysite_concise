from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

import os

from account.decorators import home_required, index_required, userinfo_required
from account.forms import LoginForm, UserInfoForm, UserProInfoForm
from account.models import UserProInfo, UserInfo
from manager.models import Status
from mysite.settings import BASE_PATH


def get_apply_year():
    status_obj = Status.objects.all()[0]
    apply_year = (status_obj.apply_year).split("-")[0]
    return apply_year


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            print(cd)
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                if UserInfo.objects.filter(user=user):
                    userinfo = UserInfo.objects.filter(user=user)
                    for i in userinfo:
                        if i.status != "1":
                            return HttpResponse("您的身份已过期!如有疑问可咨询管理员492195925@qq.com")
                if user.has_perm('account.add_userproinfo'):
                    return HttpResponseRedirect(reverse('manager:manager_home'))
                if not UserProInfo.objects.filter(user=user):
                    return HttpResponseRedirect(reverse('account:account_index'))
                return HttpResponseRedirect(reverse('account:account_home'))
            else:
                return render(request, "account/login_wrong.html")
                # return HttpResponse("账号或密码错误！")
        else:
            return HttpResponse("无效登录！")
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


@login_required(login_url='/account/login/')
@home_required
def account_home(request):
    print("我进来了呀")
    return render(request, "account/home.html")


@login_required(login_url='/account/login/')
@index_required
def account_index(request):
    return render(request, "account/index.html")


@login_required(login_url='/account/login/')
@home_required
def user_info(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/userinfo.html", {"user": user, "userinfo": userinfo})


@login_required(login_url='/account/login/')
def user_info_edit(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == "POST":
        userinfo_form = UserInfoForm(request.POST)

        if userinfo_form.is_valid():
            userinfo_cd = userinfo_form.cleaned_data
            userinfo.phone = userinfo_cd['phone']
            userinfo.email = userinfo_cd['email']
            userinfo.save()
        return HttpResponseRedirect(reverse('account:my_information'))
    else:
        userinfo_form = UserInfoForm(initial={"phone": userinfo.phone, "email": userinfo.email})
        return render(request, "account/userinfo_edit.html",
                      {"user": user, "userinfo": userinfo, "userinfo_form": userinfo_form})


@login_required(login_url='/account/login/')
@home_required
def user_pro_info(request):
    user = User.objects.get(username=request.user.username)
    userproinfo = UserProInfo.objects.get(user=user, apply_year=get_apply_year())
    return render(request, "account/proinfo.html", {"user": user, "userproinfo": userproinfo})


@login_required(login_url='/account/login/')
@home_required
def user_pro_info_edit(request):
    user = User.objects.get(username=request.user.username)
    apply_year = get_apply_year()
    userproinfo = UserProInfo.objects.get(user=user, apply_year=apply_year)
    if request.method == "POST":
        userproinfo_form = UserProInfoForm(request.POST)

        if userproinfo_form.is_valid():
            userproinfo_cd = userproinfo_form.cleaned_data
            userproinfo.tutor = userproinfo_cd['tutor']
            userproinfo.pro_name = userproinfo_cd['pro_name']
            userproinfo.result_type = userproinfo_cd['result_type']
            userproinfo.lab = userproinfo_cd['lab']
            userproinfo.mem_num = userproinfo_cd['mem_num']
            userproinfo.apply_year = apply_year  # request.POST.get("apply_year")
            print(userproinfo.apply_year)
            userproinfo.save()
        return HttpResponseRedirect(reverse('account:my_pro_information'))
    else:
        userproinfo_form = UserProInfoForm(initial={"tutor": userproinfo.tutor, "pro_name": userproinfo.pro_name,
                                                    "result_type": userproinfo.result_type, "lab": userproinfo.lab,
                                                    "mem_num": userproinfo.mem_num})
        return render(request, "account/proinfo_edit.html", {"user": user, "userproinfo_form": userproinfo_form})


@login_required(login_url='/account/login/')
@index_required
def index_user_info(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/index_userinfo.html", {"user": user, "userinfo": userinfo})


@login_required(login_url='/account/login/')
@index_required
def index_user_info_edit(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == "POST":
        userinfo_form = UserInfoForm(request.POST)

        if userinfo_form.is_valid():
            userinfo_cd = userinfo_form.cleaned_data
            userinfo.phone = userinfo_cd['phone']
            userinfo.email = userinfo_cd['email']
            userinfo.save()
        # return HttpResponseRedirect('/account/index/my-information/')
        return HttpResponseRedirect(reverse('account:index_my_information'))
    else:
        userinfo_form = UserInfoForm(initial={"phone": userinfo.phone, "email": userinfo.email})
        return render(request, "account/index_userinfo_edit.html",
                      {"user": user, "userinfo": userinfo, "userinfo_form": userinfo_form})


@login_required(login_url='/account/login/')
@index_required
@userinfo_required
def index_user_pro_info_edit(request):
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        userproinfo_form = UserProInfoForm(request.POST)

        if userproinfo_form.is_valid():
            try:
                userproinfo = UserProInfo.objects.create(user=user)
                userproinfo_cd = userproinfo_form.cleaned_data
                userproinfo.tutor = userproinfo_cd['tutor']
                userproinfo.pro_name = userproinfo_cd['pro_name']
                userproinfo.result_type = userproinfo_cd['result_type']
                userproinfo.lab = userproinfo_cd['lab']
                userproinfo.mem_num = userproinfo_cd['mem_num']
                userproinfo.apply_year = request.POST.get("apply_year")
                print(userproinfo.apply_year)
                userproinfo.save()
            except Exception as e:
                print(e)
                userproinfo_form = UserProInfoForm()
                return render(request, "account/index_proinfo_edit.html",
                              {"user": user, "userproinfo_form": userproinfo_form})
        return HttpResponseRedirect(reverse('account:account_home'))
    else:
        userproinfo_form = UserProInfoForm()
        return render(request, "account/index_proinfo_edit.html", {"user": user, "userproinfo_form": userproinfo_form})


def get_status(request):
    status_obj = Status.objects.all()[0]
    mode = status_obj.mode
    date = str(status_obj.date).replace("-", "")
    apply_year = (status_obj.apply_year).split("-")[0]
    status_dic = {'mode': mode, 'date': date, 'apply_year': apply_year}
    return JsonResponse(status_dic)


@login_required(login_url='/account/login/')
@home_required
def upload_apply(request):
    print(request.method)
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    apply_year = get_apply_year()
    userproinfo = UserProInfo.objects.get(user=user, apply_year=apply_year)
    apply_status = userproinfo.apply_status
    status = ""
    tutor = userproinfo.tutor
    name = userinfo.name
    pro_name = userproinfo.pro_name
    path = BASE_PATH + os.sep + 'apply' + apply_year
    savename = '申请报告_' + tutor + '_' + name + '_' + pro_name + '.doc'
    filepath = os.path.join(path, savename)
    if apply_status == "1":
        status = "注意：你已上传过该文件，再次提交会覆盖原先文件"
    if request.method == "POST":

        if not os.path.exists(path):
            os.makedirs(path)
        if request.FILES.get('apply', '') != '':
            file_obj = request.FILES.get('apply')
            print(filepath)
            dest = open(filepath, 'wb')
            dest.write(file_obj.read())
            dest.close()
            UserProInfo.objects.filter(user=user, apply_year=apply_year).update(apply_status="1", comment="合格")
            status = "上传成功！"
            # return render(request, 'account/apply_upload.html', {'status': '上传成功！'})

            # return render(request, "account/apply_upload.html",{"status":status})
    file_list = []
    if os.path.exists(filepath):
        path_dir = {}
        path_dir['fullpath'] = filepath
        path_dir['filename'] = savename
        file_list.append(path_dir)
    return render(request, "account/apply_upload.html", {"status": status,"filelist":file_list})


@login_required(login_url='/account/login/')
@home_required
def upload_middle(request):
    print(request.method)
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    apply_year = get_apply_year()
    userproinfo = UserProInfo.objects.get(user=user, apply_year=apply_year)
    middle_status = userproinfo.middle_status
    status = ""
    tutor = userproinfo.tutor
    name = userinfo.name
    pro_name = userproinfo.pro_name
    path = BASE_PATH + os.sep + 'middle' + apply_year
    savename = '中期报告_' + tutor + '_' + name + '_' + pro_name + '.doc'
    filepath = os.path.join(path, savename)
    if middle_status == "1":
        status = "注意：你已上传过该文件，再次提交会覆盖原先文件"
    if request.method == "POST":
        if not os.path.exists(path):
            os.makedirs(path)
        if request.FILES.get('middle', '') != '':
            file_obj = request.FILES.get('middle')
            print(filepath)
            dest = open(filepath, 'wb')
            dest.write(file_obj.read())
            dest.close()
            UserProInfo.objects.filter(user=user, apply_year=apply_year).update(middle_status="1")
            status = "上传成功！"
    file_list=[]
    if os.path.exists(filepath):
        path_dir={}
        path_dir['fullpath']=filepath
        path_dir['filename']=savename
        file_list.append(path_dir)
    return render(request, "account/middle_upload.html", {"status": status,"filelist":file_list})


@login_required(login_url='/account/login/')
@home_required
def upload_conclude_file(request):
    print(request.method)
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    apply_year = get_apply_year()
    userproinfo = UserProInfo.objects.get(user=user, apply_year=apply_year)
    status = ""
    status1 = ""
    status2 = ""
    status3 = ""
    conclude_status = userproinfo.conclude_status
    file_status = userproinfo.file_status
    file_list = file_status.split("+")
    if conclude_status == "1":
        status = "注意：你已上传过该文件，再次提交会覆盖原先文件"
    if "1" in file_list:
        status1 = "注意：你已上传过该文件，再次提交会覆盖原先文件"
    if "2" in file_list:
        status2 = "注意：你已上传过该文件，再次提交会覆盖原先文件"
    if "3" in file_list:
        status3 = "注意：你已上传过该文件，再次提交会覆盖原先文件"
    tutor = userproinfo.tutor
    name = userinfo.name
    pro_name = userproinfo.pro_name
    if request.method == "POST":
        path = BASE_PATH + os.sep + 'other' + apply_year
        if not os.path.exists(path):
            os.makedirs(path)
        conclude_path = BASE_PATH + os.sep + 'conclude' + apply_year
        if not os.path.exists(conclude_path):
            os.makedirs(conclude_path)
        if request.FILES.get('conclude', '') != '':
            file_obj = request.FILES.get('conclude')
            savename = '结题报告_' + tutor + '_' + name + '_' + pro_name + '.doc'
            filepath = os.path.join(conclude_path, savename)
            print(filepath)
            dest = open(filepath, 'wb')
            dest.write(file_obj.read())
            dest.close()
            UserProInfo.objects.filter(user=user, apply_year=apply_year).update(conclude_status="1")
            status = "上传成功！"
            # return render(request, 'account/conclude_file_upload.html', {'status': '上传成功！'})
        elif request.FILES.get('experiment_file', '') != '':
            file_obj = request.FILES.get('experiment_file')
            savename = '实验报告_' + tutor + '_' + name + '_' + pro_name + '.doc'
            filepath = os.path.join(path, savename)
            print(filepath)
            dest = open(filepath, 'wb')
            dest.write(file_obj.read())
            dest.close()
            if "1" not in file_list:
                file_status += "1+"
            UserProInfo.objects.filter(user=user, apply_year=apply_year).update(file_status=file_status)
            status1 = "上传成功！"
            # return render(request, 'account/conclude_file_upload.html', {'status1': '上传成功！'})
        elif request.FILES.get('research_file', '') != '':
            file_obj = request.FILES.get('research_file')
            savename = '研究报告_' + tutor + '_' + name + '_' + pro_name + '.doc'
            filepath = os.path.join(path, savename)
            print(filepath)
            dest = open(filepath, 'wb')
            dest.write(file_obj.read())
            dest.close()
            if "2" not in file_list:
                file_status += "2+"
            UserProInfo.objects.filter(user=user, apply_year=apply_year).update(file_status=file_status)
            status2 = "上传成功！"
            # return render(request, 'account/conclude_file_upload.html', {'status2': '上传成功！'})
        elif request.FILES.get('compressed_file', '') != '':
            file_obj = request.FILES.get('compressed_file')
            savename = '压缩文件_' + tutor + '_' + name + '_' + pro_name + '.zip'
            filepath = os.path.join(path, savename)
            print(filepath)
            dest = open(filepath, 'wb')
            dest.write(file_obj.read())
            dest.close()
            if "3" not in file_list:
                file_status += "3+"
            UserProInfo.objects.filter(user=user, apply_year=apply_year).update(file_status=file_status)
            status3 = "上传成功！"
            # return render(request, 'account/conclude_file_upload.html', {'status3': '上传成功！'})
    file_list = []

    savename = '结题报告_' + tutor + '_' + name + '_' + pro_name + '.doc'
    conclude_path = BASE_PATH + os.sep + 'conclude' + apply_year
    path = os.path.join(conclude_path,savename)
    if os.path.exists(path):
        path_dir = {}
        path_dir["fullpath"] = path
        path_dir["filename"] = savename
        file_list.append(path_dir)
    other_path = BASE_PATH + os.sep + 'other' + apply_year
    savename_list = ['实验报告_' + tutor + '_' + name + '_' + pro_name + '.doc',
                     '研究报告_' + tutor + '_' + name + '_' + pro_name + '.doc',
                     '压缩文件_' + tutor + '_' + name + '_' + pro_name + '.zip']
    for i in savename_list:
        path = os.path.join(other_path, i)
        if os.path.exists(path):
            path_dir = {}
            path_dir["fullpath"] = path
            path_dir["filename"] = i
            file_list.append(path_dir)
    return render(request, "account/conclude_file_upload.html",
                  {'status': status, 'status1': status1, 'status2': status2, 'status3': status3,"filelist":file_list})
