import random

from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
import hashlib
from django.core.paginator import Paginator

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

def base(request):
    return render(request,'base.html')

def goods_list(request,status,page):
    if status == '0':
        goods = Goods.objects.filter(goods_status=0).order_by('goods_number')
    else:
        goods = Goods.objects.filter(goods_status=1).order_by('goods_number')
    paginator = Paginator(goods,10)
    page_obj = paginator.page(int(page))
    return render(request,'vue_goods_list.html',locals())

# 批量生成数据
def add_goods(request):
    goods_name = '大叶生，紫叶生，罗马生，直立生，紫菊，苦苣，菊花菜，鸡毛菜，蒿子杆，茼蒿，菠菜，大白菜，圆白菜，小白菜，筷菜，油麦菜，盖菜，奶白菜，韭菜，油菜，香菜，空心菜，黄心菜，菜心，芥兰，豌豆苗，豌豆尖，丝瓜尖，南瓜尖，青蒜，红苋菜，绿苋菜，棒菜，抱子甘蓝，羽衣甘蓝，芦荟，老黄瓜，芦笋，苦菜，霸王花，南瓜花，茴香，芝麻菜，麦苗，玉米苗，荆芥，尖椒，青椒，红彩椒，黄彩椒，小米椒，青小米椒，美人椒，青美人椒，红尖椒，线椒，螺丝椒，杭椒，西兰花，娃娃菜，莲藕，紫甘蓝，山药，大芋头，小芋头，洋葱，红洋葱，干葱头，沙姜，南姜，牛蒡，章丘大葱，水芹，菠菜苗，面条菜，马齿菜，茴香球，黄花菜，紫苏叶，玉米'
    goods_address = '北京市，天津市，上海市，重庆市，河北省，山西省，辽宁省，吉林省，黑龙江省，江苏省，浙江省，安徽省，福建省，江西省，山东省，河南省，湖北省，湖南省，广东省，海南省，四川省，贵州省，云南省，陕西省，甘肃省，青海省，台湾省'
    goods_name = goods_name.split('，')
    goods_address = goods_address.split('，')

    for x in range(1,100):
        goods = Goods()
        goods.goods_number = str(x).zfill(4)
        goods.goods_name = random.choice(goods_address)+random.choice(goods_name)
        goods.goods_price = random.random()*100
        goods.goods_count = random.randint(1,100)
        goods.goods_location = random.choice(goods_address)
        goods.goods_safe_date = random.randint(1,36)
        goods.save()
    return HttpResponse('生成数据')

# 商品状态
def setStatus(request,status,id):
    good = Goods.objects.get(id=int(id))
    if status == 'up':
        good.goods_status=1
    else:
        good.goods_status=0
    good.save()
    url=request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(url)

# 提供数据的api接口
# 返回的是一个json对象
def goods_list_api(request,status='1',page='1'):
    if status == '0':    # 下架商品
        goods = Goods.objects.filter(goods_status=0).order_by('goods_number')
    else:    # 在售商品
        goods = Goods.objects.filter(goods_status=1).order_by('goods_number')
    paginator = Paginator(goods,10)
    page_obj = paginator.page(int(page))

    res=[]
    for one in page_obj:
        res.append({
            'goods_number':one.goods_number,
            'goods_name':one.goods_name,
            'goods_price':one.goods_price,
            'goods_count':one.goods_count,
            'goods_location':one.goods_location,
            'goods_safe_date':one.goods_safe_date,
            'goods_status':one.goods_status,
            'goods_pro_time':one.goods_pro_time,
        })
    result = {
        'data':res,
        'page_range':list(paginator.page_range)
    }
    return JsonResponse(result)

# 提供页面
def api_goods_list(request):
    return render(request,'api_goods_list.html')

def vuedemo(request):
    return render(request,'vuedemo.html')