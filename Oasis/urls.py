"""Oasis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from web import views
from . import testdb
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/',views.index),
    # path('login/',views.customerLogin, name="customerlogin"),       #载入login页面
    # path('ad_login/',views.managerindex, name="managerlogin"),
    path('',views.basePerform),
    path('login/',views.login),
    path('customerindex',views.customerindex),
    path('dagongren',views.dagongrenindex),
    # path('customerindex/',views.customerindex),
    # path('find_accout/',views.find_accout),
    # path('testdb/', testdb.testdb),
    # path('register/',views.clickregister,name="clickregister"),
    path('login/register/',views.register),
    path('managerindex/', views.managerindex),
    path('register/',views.register),
    # path('customerbook/bookdetail/', views.bookdetail,name='bookdetail'),
    url(r'customerbook/',views.display),
    url(r'bookedroom/',views.displaybooked),
    url(r'allbooked/',views.allocate),
    url(r'givemoney/',views.givemoney),
    url(r'alterprice/',views.pricemanage),
    url(r'baobiao/',views.myform),
    url(r'formguyuan/',views.gform),
    path('bookdetail/',views.bookdetail),
    path('alterdetail/',views.alterdetail),
    # url('customerbook/bookdetail/',views.bookdetail),
]
