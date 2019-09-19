from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect,HttpResponse
import hashlib

def hello(request):
    return HttpResponse('hello world')

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

# 登录拦截装饰器
def loginVaild(func):
    def inner(request,*args,**kwargs):
        email = request.COOKIES.get('email')
        password = request.COOKIES.get('password')
        if email and password:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

def register(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            # 判断邮箱是否存在
            loginuser=LoginUser.objects.filter(email=email).first()
            if not loginuser:
                # 不存在，写库
                user=LoginUser()
                user.email=email
                user.password=setPassword(password)
                user.save()
            else:
                # 存在
                error_msg = '邮箱已经被注册，请登录'
        else:
            error_msg = '邮箱不可为空'
    return render(request,'register.html',locals())

def login(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                if user.password==setPassword(password):
                    response= HttpResponseRedirect('/index/')
                    response.set_cookie('email',email)
                    response.set_cookie('password',password)
                    request.session['email']=email
                    return response
                else:
                    error_msg = '密码错误'
            else:
                error_msg = '该用户不存在，请先注册'
        else:
            error_msg = '邮箱不可为空'
    return render(request,'login.html',locals())

@loginVaild
def index(request):

    return render(request,'index.html')

def logout(request):
    response = HttpResponseRedirect('/login/')
    keys = request.COOKIES.keys()
    for one in keys:
        response.delete_cookie(one)
    del request.session['email']
    return response