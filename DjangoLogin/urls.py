"""DjangoLogin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from LoginUser.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',hello),
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('logout/',logout),
    path('base/',base),
    # path('goods_list/',goods_list),
    re_path('goods_list/(?P<status>[01])/(?P<page>\d+)',goods_list),
    re_path('setStatus/(?P<status>\w+)/(?P<id>\d+)',setStatus),
    path('vuedemo/',vuedemo),
    path('api_goods_list/',api_goods_list),    # 页面
]

# api接口
urlpatterns += [
    re_path('goods_list_api/(?P<status>[01])/(?P<page>\d+)',goods_list_api),    # 数据
]