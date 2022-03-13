import datetime

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from web import models
from django.db.models import Avg,Max,Min,Count,Sum  #   引入函数

def basePerform(request):
    return render(request, 'index.html')
def customerLogin(request):
    return render(request, 'login.html')
# def managerLogin(request):
#     return render(request, 'ad_login.html')
def customerindex(request):
    return render(request, 'customerindex.html')
def dagongrenindex(request):
    return render(request, 'dagongren.html')
def managerindex(request):
    return render(request, 'managerindex.html')
userno=['']
def login(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        userno[0] = username
        if username == '' or password == '':
            return HttpResponse('<script>alert("用户名密码不能为空");location.href="/login";</script>')
        #通过filter(相当于select sno,spassword from sign where sno='web post的账号'),查询数据库是否存在用户
        inDb = models.sign.objects.filter(sno=username).first()
        if inDb:
            if password == inDb.spassword and inDb.sbz == 1:            #1-客户标志
                return redirect('/customerindex')
            elif password == inDb.spassword and inDb.sbz == 2:          #2-雇员标志
                return redirect('/dagongren')
            elif password == inDb.spassword and inDb.sbz == 3:          #3-管理层标志
                return redirect('/managerindex')
            else:
                return HttpResponse('<script>alert("用户名或密码错误");location.href="/login";</script>')
        else:
            return HttpResponse('<script>alert("用户名或密码错误");location.href="/login";</script>')
    return render(request, 'login.html')
# def clickregister(request):
#     return render(request, 'register.html')
def register(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        againpassword = request.POST.get('againpass')
        if username == '' or password == '':
            return HttpResponse('<script>alert("用户名密码不能为空哦！");location.href="/register";</script>')
        elif username.isdigit() == False:
            return HttpResponse('<script>alert("账号必须是数字哦！");location.href="/register";</script>')
        elif password != againpassword:
            return HttpResponse('<script>alert("两次密码输入不一致！");location.href="/register";</script>')
        #将post来的表单数据添加到数据库并作前端反馈
        try:
            adduser = models.sign.objects.create(sno=username, spassword=password, sbz=1)
            #重定向至登录
            return HttpResponse('<script>alert("注册成功，欢迎登录！");location.href="/login";</script>')
        except Exception as err:
            errStr = err.args[1]
            if 'PRIMARY' in errStr:
                return HttpResponse('<script>alert("账号重复");location.href="/register";</script>')
    return render(request, 'register.html')
#显示房间信息
#预订跳转
yudingroom=['']
def display(request):
    # if request.method == 'GET':
    #     allrooms = models.rooms.all()
    #     print(allrooms)
    if request.POST:
        yudingroom[0] = request.POST.get('fanghao')
        print(yudingroom)
        if yudingroom[0] != '':
            return redirect('/bookdetail')
    allrooms = models.rooms.objects.all()
    people = models.sign.objects.all()
    return render(request, 'customerbook.html', {'rooms':allrooms,'users': people})
alterroom=['']
def displaybooked(request):

    if request.POST:
        alterroom[0] = request.POST.get('fanghao')
        print(alterroom)
        if alterroom[0] != '':
            if 'genggai' in request.POST:
                return redirect('/alterdetail')
            elif 'quxiao' in request.POST:
                quxiaorow = models.bookrecord.objects.get(id=int(alterroom[0]))
                quxiaorow2 = models.bookrecord.objects.filter(id=int(alterroom[0]))
                #预付金预订不退款
                if quxiaorow.btype == 1:
                    quxiaorow2.update(iscancel=1)
                    return HttpResponse('<script>alert("取消预付金预订成功，无退款！");location.href="/bookedroom";</script>')
                elif quxiaorow.btype == 2:
                    yudingtime = quxiaorow.bdate
                    if (yudingtime.replace(tzinfo=None)-datetime.datetime.now()).days > 3 :
                        quxiaorow2.update(iscancel=1)
                        return HttpResponse('<script>alert("取消常规预订成功！");location.href="/bookedroom";</script>')
                    else:
                        #先根据房型查价格
                        mtemp = models.rooms.objects.get(rno=quxiaorow.bcno_id)

                        money=mtemp.rprice
                        #生成付款记录
                        nowtime = datetime.datetime.now()
                        models.moneyrecord.objects.create(mtype=3, mrno=quxiaorow.bcno_id, money=money,
                                                          mdate=nowtime, mdays=quxiaorow.bdays,
                                                          mrtype=quxiaorow.broomtype)
                        return HttpResponse('<script>alert("请支付第一天的房费！"'+str(money)+'元);location.href="/bookedroom";</script>')

    allrooms = models.bookrecord.objects.filter(bcno_id=int(userno[0]),iscancel=0)
    return render(request, 'bookedroom.html', {'rooms':allrooms})
allocateroom=['']
ydbh=['']
def allocate(request):
    if request.POST:
        allocateroom[0] = request.POST.get('fanghao')           #得到前端发来的房号
        ydbh[0] = request.POST.get('bianhao')
        if allocateroom[0] != '' and ydbh[0] != '':
            allo1 = models.rooms.objects.get(rno=int(allocateroom[0]))
            allo2 = models.rooms.objects.filter(rno=int(allocateroom[0]))
            print(allocateroom[0],ydbh[0])
            yd = models.bookrecord.objects.get(id=int(ydbh[0]))
            if allo1.rin == 1:
                return HttpResponse('<script>alert("分配失败！该房间已被分配");location.href="/allbooked";</script>')
            elif yd.broomtype != allo1.rtype:
                return HttpResponse('<script>alert("分配失败！与用户预订房型不一样！");location.href="/allbooked";</script>')
            else:
                #房间入住
                allo2.update(rin=1)
                #生成入住记录
                addrecord = models.checkedrecord.objects.create(crno=allo1.rno, cdate=yd.bdate, ccno=yd.bcno_id, cdays=yd.bdays)
                #更新收入记录中的房号
                temp = models.moneyrecord.objects.filter(mtype=1,mdate=yd.bdate,mdays=yd.bdays)
                temp.update(mrno=allo1.rno)
                return HttpResponse('<script>alert("分配成功！");location.href="/allbooked";</script>')

    allrooms = models.bookrecord.objects.filter(iscancel=0)
    allfangjians = models.rooms.objects.all()
    return render(request, 'allbooked.html', {'rooms':allrooms,'fangjians':allfangjians})

def bookdetail(request):
    # 客户post了预订需求后
    if request.method == 'POST' and request.POST:
        # 得到前端发来的预订类型
        bookno = yudingroom[0]          #预订的房号
        booktype1 = request.POST.get('ck1')         #选中为on ,未选中未None
        booktype2 = request.POST.get('ck2')
        bookbegintime = datetime.datetime(int(request.POST.get('beginyear')),int(request.POST.get('beginmonth')),
                                          int(request.POST.get('beginday')))
        nowtime = datetime.datetime.now()
        # bookbegintime = request.POST.get('beginyear') + '-'\
        #                 +request.POST.get('beginmonth') + '-'\
        #                 +request.POST.get('beginday') +' 00:00'
        bookdays = request.POST.get('bookdays')
        print(bookbegintime)
        # 得到预订类型向数据库中插入记录
        if booktype1 == 'on':  # 预付金预订
            # try:
            #至少提前30天
            if (bookbegintime-nowtime).days>=30:
                #生成预订记录
                addrecord = models.bookrecord.objects.create(broomtype=bookno, btype=1, bdate=bookbegintime, bcno_id=userno[0],bdays=bookdays)
                # 重定向至预付金付款（生成付款记录）
                #后端算钱,天数*基价*0.75
                room = models.rooms.objects.get(rtype=bookno)
                allmoney = int(bookdays) * int(room.rprice) * 0.75
                models.moneyrecord.objects.create(mtype=1, mrno=999, money=allmoney, mrtype=bookno,
                                                  mdate=bookbegintime, mdays=bookdays)
                return HttpResponse('<script>alert("预订成功，期待您的光临！请给我打钱，打'+str(allmoney)+'元");location.href="/bookdetail";</script>')
            else:
                return HttpResponse('<script>alert("预付金预订必须提前30天预订！");location.href="/bookdetail";</script>')
        if booktype2 == 'on': #普通预订
            addrecord = models.bookrecord.objects.create(broomtype=bookno, btype=2, bdate=bookbegintime, bcno_id=userno[0],
                                                         bdays=bookdays)
            return HttpResponse('<script>alert("预订成功，期待您的光临！信用卡or打钱？");location.href="/bookdetail";</script>')

    return render(request,'bookdetail.html')
def alterdetail(request):
    # 客户post了更改需求后
    if request.method == 'POST' and request.POST:
        # 得到前端发来的预订类型
        bookno = alterroom[0]  # 更改的编号
        booktype1 = request.POST.get('ck1')  # 选中为on ,未选中未None
        booktype2 = request.POST.get('ck2')
        bookbegintime = datetime.datetime(int(request.POST.get('beginyear')), int(request.POST.get('beginmonth')),
                                          int(request.POST.get('beginday')))
        roomtype = request.POST.get('fangxing')
        nowtime = datetime.datetime.now()
        # bookbegintime = request.POST.get('beginyear') + '-'\
        #                 +request.POST.get('beginmonth') + '-'\
        #                 +request.POST.get('beginday') +' 00:00'
        bookdays = request.POST.get('bookdays')
        # 得到预订类型向数据库中插入记录
        if booktype1 == 'on':  # 预付金预订
            # try:
            # 至少提前30天
            if (bookbegintime - nowtime).days >= 30:
                alterrow = models.bookrecord.objects.filter(id=int(bookno))
                altertemp = models.bookrecord.objects.get(id=int(bookno))
                roomtemp = models.rooms.objects.get(rno=altertemp.bcno_id)
                alterrow.update(btype=1,bdate = bookbegintime,bdays = bookdays,broomtype=roomtype)
                #金额减少不退款，金额增加退款
                allmoney = int(bookdays) * int(roomtemp.rprice) * 0.75
                #查金额有无减少
                mt = models.moneyrecord.objects.get(mdate=bookbegintime,mtype=1)
                moneyed = mt.money
                if allmoney <= moneyed:
                    return HttpResponse(
                        '<script>alert("修改预订成功，期待您的光临！");location.href="/alterdetail";</script>')
                else:
                    # 生成预付金更改付款记录
                    models.moneyrecord.objects.create(mtype=4, mrno=altertemp.bcno_id, money=moneyed-allmoney,
                                                      mdate=nowtime, mdays=bookdays,mrtype=roomtemp)
                    return HttpResponse(
                        '<script>alert("修改预订成功，您还得支付'+str(moneyed-allmoney)+'元！");location.href="/alterdetail";</script>')
            else:
                return HttpResponse('<script>alert("预付金预订必须提前30天预订！");location.href="/alterdetail";</script>')
        if booktype2 == 'on':  # 普通预订
            alterrow = models.bookrecord.objects.filter(id=int(bookno))
            alterrow.update(btype=2,bdate = bookbegintime,bdays = bookdays,broomtype=roomtype)
            return HttpResponse('<script>alert("修改成功，期待您的光临！信用卡or打钱？");location.href="/alterdetail";</script>')

    return render(request, 'alterdetail.html')

def givemoney(request):
    if request.POST:
        checkno = request.POST.get('bianhao')
        if checkno != '':
            checkrow = models.checkedrecord.objects.get(id=int(checkno))
            roomtemp = models.rooms.objects.get(rno=checkrow.crno)
            checktemp = models.checkedrecord.objects.filter(id=int(checkno))
            print(allocateroom[0],ydbh[0])
            if checkrow.cpaid == 1:
                return HttpResponse('<script>alert("结账失败！该客户已结账");location.href="/givemoney";</script>')
            else:
                #结账
                checktemp.update(cpaid=1)
                #查房价
                tt = models.rooms.objects.get(rno=checkrow.crno)
                allmoney = checkrow.cdays*tt.rprice
                #生成正常常规付款记录
                models.moneyrecord.objects.create(mtype=2,mrno=checkrow.crno,money=allmoney,
                                                  mdate=checkrow.cdate,mdays=checkrow.cdays,mrtype=roomtemp.rtype)
                # models.checkedrecord.objects.create(crno=allo1.rno, cdate=yd.bdate, ccno=yd.bcno_id, cdays=yd.bdays)
                return HttpResponse('<script>alert("请刷卡支付'+str(allmoney)+'元，结账成功！");location.href="/givemoney";</script>')

    checks = models.checkedrecord.objects.all()
    return render(request, 'givemoney.html', {'checks':checks})

def pricemanage(request):
    if request.POST:
        nowprice = request.POST.get('nowprice')
        nowtype = request.POST.get('fangxing')
        if nowprice != '':
            roomsrow = models.rooms.objects.filter(rtype=nowtype)
            roomsrow.update(rprice=int(nowprice))
            return HttpResponse('<script>alert("修改基价成功！");location.href="/alterprice";</script>')

    room1 = models.rooms.objects.get(rtype='大床房')
    room2 = models.rooms.objects.get(rtype='双床房')
    room3 = models.rooms.objects.get(rtype='商务房')
    room4 = models.rooms.objects.get(rtype='家庭房')
    room5 = models.rooms.objects.get(rtype='六人豪华房')

    return render(request, 'alterprice.html',{'room1':room1,'room2':room2,'room3':room3,'room4':room4,'room5':room5})

def myform(request):
    yuding = models.bookrecord.objects.all()
    shouru = models.moneyrecord.objects.all()
    allprice = models.moneyrecord.objects.aggregate(Sum('money'))
    return render(request, 'baobiao.html', {'rooms': yuding,'fangjians':shouru,'allmoney':allprice})

def gform(request):
    nowform1 = models.bookrecord.objects.all()
    nowform2 = models.checkedrecord.objects.all()
    nowdate = datetime.datetime(2021,12,23)

    return render(request, 'formguyuan.html', {'rooms': nowform1,'fangjians':nowform2,'nowdate':nowdate})






