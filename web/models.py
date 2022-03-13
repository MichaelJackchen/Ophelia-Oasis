from django.db import models

# Create your models here.
class sign(models.Model):
    sno = models.AutoField(primary_key=True)
    spassword = models.CharField(max_length=15)
    sbz = models.IntegerField()
class rooms(models.Model):
    rno = models.AutoField(primary_key=True)        #房间号
    rtype = models.CharField(max_length=10)         #房间类型,大床房/双床房/商务房等...
    rprice = models.IntegerField()
    rin = models.BooleanField()         #是否入住
class bookrecord(models.Model):
    bdate = models.DateTimeField()
    btype = models.IntegerField()       #预订类型
    broomtype = models.CharField(max_length=10)             #预订的房间类型
    bdays = models.IntegerField(default=1)       #预订天数
    bcno = models.ForeignKey('sign',on_delete=models.CASCADE)       #预订客户编号
    iscancel = models.IntegerField(default=0)        #取消记录，默认为0
class checkedrecord(models.Model):
    crno = models.IntegerField()
    cdate = models.DateTimeField()
    ccno = models.IntegerField()
    cdays = models.IntegerField(default=1)
    cpaid = models.IntegerField(default=0)          #是否结账
class moneyrecord(models.Model):
    mtype = models.IntegerField()               #收入来自3中类型：1-预付金 2-常规 3-常规取消预订（3天内支付第一天）
    mrno = models.IntegerField()                #收入来自哪个房间
    mrtype = models.CharField(max_length=10)
    money = models.IntegerField()               #单次收入记录
    mdate = models.DateTimeField()              #收入来自哪天
    mdays = models.IntegerField()               #收入的天数（根据收入类型1、2-预订天数，3-默认为1）


