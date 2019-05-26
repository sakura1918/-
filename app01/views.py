from datetime import datetime
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random,string
from django.core.paginator import Paginator
from django_redis import get_redis_connection

from app01 import models
from app01.captcha.image import ImageCaptcha
import re
import hashlib   # 导入hashlib模块(加密)
from app01.cart import Cart
from app01.models import TCategory, TBook, TUser, TAddress
from project1 import settings

def index(request):
    name=request.COOKIES.get('nuname')
    if name:
        request.session['nuname'] = name
    nuname = request.session.get('nuname')
    print(nuname)
    nuname2 = request.GET.get('nuname')
    print(nuname2)
    if nuname2 == '1':
        nuname = ''
        request.session.clear()
    onec=TCategory.objects.filter(category_pid__isnull=True)
    twoc=TCategory.objects.filter(category_pid__isnull=False)
    num = TBook.objects.all().order_by("-shelves_date")[0:8]
    return render(request,"index.html",{"onec":onec,"twoc":twoc,"num":num,'nuname':nuname})

def bookdetails(requset):
    name = requset.COOKIES.get('nuname')
    if name:
        requset.session['nuname'] = name
    nuname = requset.session.get('nuname')
    nuname2 = requset.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        requset.session.clear()

    id = requset.GET.get("id")
    det = TBook.objects.filter(book_id = id)
    return render(requset,"Book details.html",{"det":det,'nuname':nuname})

def login(request):
    name = request.COOKIES.get('txtUsername')
    password = request.COOKIES.get('txtPassword')
    result = TUser.objects.filter(user_name=name,user_password=password)
    if result:
        request.session['nuname'] = name
        return redirect('app01:index')
    return render(request,'login.html')

def login_logic(request):
    username = request.POST.get("txtUsername")
    pwd = request.POST.get("txtPassword")
    captcha = request.POST.get('txt_vcode')
    code = request.session.get('code')
    print(username,pwd,'121')
    # if not all([username,pwd]):#验证完数据完整性
    #     return render(request,"login.html")
    l = '23567898900fbnjdfnbkdnvlzksfdjgnolkdr!@#$%^&*()'
    salt = ''.join(random.sample(l, 6))
    s1 = hashlib.md5()  # 创建sha1对象
    s1.update(pwd.encode('utf8'))  # 要先编码
    pwd = s1.hexdigest()
    # 验证用户是否正确
    user = TUser.objects.filter(user_email=username,user_password=pwd)  #验证数据的正确性
    print(username,pwd)
    if user and captcha.upper() == code.upper():
        res = redirect('app01:index')
        request.session['nuname'] = username  # 验证成功就添加session状态
        res.set_cookie('txtUsername', username, max_age=7 * 24 * 3600)
        res.set_cookie('txtPassword', pwd, max_age=7 * 24 * 3600)  # 添加cookie
        res.set_cookie('nuname',username,max_age=7 * 24 * 3600)
        return res
    else:
        # return render(request,"login.html")
        return HttpResponse('用户名或密码错误')

def regist(request):
    id = TUser.objects.all().order_by("user_id")
    for i in id:
        print(i)
    return render(request,'register.html')

def getcaptcha(request):
    image = ImageCaptcha()
    rand_code = random.sample(string.ascii_letters+string.digits,4)
    rand_code = ''.join(rand_code)
    request.session['code'] = rand_code
    data = image.generate(rand_code)
    return HttpResponse(data,'image/png')

def regist_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    password2 = request.POST.get('cpwd')
    captcha = request.POST.get('txt_vcode')
    code = request.session.get('code')
    if captcha.upper() == code.upper() and password == password2:
        l = '23567898900fbnjdfnbkdnvlzksfdjgnolkdr!@#$%^&*()'
        salt = ''.join(random.sample(l, 6))
        s1 = hashlib.md5()
        # 加密前，要先编码为比特
        s1.update(password.encode('utf8'))
        password = s1.hexdigest()
        # 存入数据库
        use = TUser.objects.create(user_email=username,
                                   user_password=password)
        # request.session['username']=username ##写入数据库时直接存入session
        print(username,password)
        return redirect('app01:registeok')

def registeok(request):
    return render(request,'register ok.html')

def checkname(request):
    name = request.GET.get('user_name')
    print(name,'11')
    result2 = TUser.objects.filter(user_email = name)
    print(result2,'11')
    if result2:
        return HttpResponse('该账号已被注册')
    elif not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',name) and not re.match(r'^1(3|4|5|7|8)\d{9}$',name):
        return HttpResponse('输入格式不正确')
    else:
        return HttpResponse(' ')

def checkpwd(request):
    userpwd1 = request.GET.get('pwd')
    userpwd2 = request.GET.get('cpwd')
    print(userpwd1,userpwd2,'22')
    if userpwd1 == userpwd2:
        return HttpResponse(' ')
    else:
        return HttpResponse('两次密码不一致请再次输入')

def checknum(request):
    number = request.GET.get('txt_vcode')

    code = request.session.get('code')
    print(number, code)
    if number.upper() == code.upper():
        return HttpResponse(' ')
    else:
        return HttpResponse('验证码有误')

def checkallow(request):
    allow = request.GET.get('chb_agreement')
    print(allow)
    if allow == 'on':
        return HttpResponse('协议没有被同意')

def list(request):
    name = request.COOKIES.get('nuname')
    if name:
        request.session['nuname'] = name
    nuname = request.session.get('nuname')
    print(nuname)
    nuname2 = request.GET.get('nuname')
    print(nuname2)
    if nuname2 == '1':
        nuname = ''
        request.session.clear()
    onec=TCategory.objects.filter(category_pid__isnull=True)
    twoc=TCategory.objects.filter(category_pid__isnull=False)
    num = TBook.objects.all().order_by("-shelves_date")
    number = request.GET.get("num")
    print(number,'146')
    e = TBook.objects.all()
    pagtor = Paginator(e,per_page=3)
    try:
        number = int(number)
    except Exception as e:
        number = 1
    # if number >= pagtor.num_pages:
    #     number = 1
    s_page = pagtor.page(number)
    print(number,'157')
    num_pages = pagtor.num_pages
    if num_pages <5:
        pages = range(1,num_pages+1)
    elif number <= 3:
        pages = range(1,6)
    elif num_pages-number <= 2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(number-2,number+3)
    return render(request, "booklist.html", {"s_page":s_page,"pages":pages,"onec": onec, "twoc": twoc, "num": num,'nuname':nuname})

##########购物车设计###########
#添加商品至购物车的view设计#接收参数
def add_book(request):
    count = request.GET.get("count")
    id = request.GET.get("id")
    information = request.session.get('informate')
    request.session['carid'] = id
    if information:
        for i in information:
            if int(i['id']) == int(id):
                c = int(i['count']) + int(count)
                sums = c * int(i['book_price'])
                i['count'] = c
                i['sums'] = sums
                # information[b]=i
                request.session['informate'] = information
                # print(information,'000000')
                return redirect("app01:bookdetails")
        table = TBook.objects.get(book_id=int(id))
        book_name = table.book_name
        book_price = table.book_price
        count = count
        sums = int(count) * int(book_price)
        l_sku = {"id": id, "book_name": book_name, "book_price": book_price, "count": count, 'sums': sums}
        information.append(l_sku)
        # b += 1
        request.session['informate'] = information
        return redirect("app01:bookdetails")
    else:
        information = []
        table = TBook.objects.get(book_id=int(id))
        book_name = table.book_name
        book_price = table.book_price
        count = count
        sums = int(count) * int(book_price)
        l_sku = {"id": id, "book_name": book_name, "book_price": book_price, "count": count, "sums": sums}
        information.append(l_sku)
        # print(information,'22222222')
        request.session['informate'] = information
        return redirect("app01:bookdetails")
    request.session['informate'] = information
    return redirect("app01:bookdetails")

def shoppingcar(request):
    name = request.COOKIES.get('nuname')
    if name:
        request.session['nuname'] = name
    nuname = request.session.get('nuname')
    print(nuname)
    nuname2 = request.GET.get('nuname')
    print(nuname2)
    if nuname2 == '1':
        nuname = ''
        request.session.clear()
    information=request.session.get('informate')
    #判断
    if information is None:
        return render(request,"dis_car.html")
    s_sums = 0
    for i in information:
        s_sums += int(i['sums'])
    s_sums = s_sums
    return render(request,'car.html',{"information":information,'s_sums':s_sums,'nuname':nuname})

def shopadd(request):
    id = request.GET.get("id")
    information=request.session.get("informate")
    print(information)
    s_sum = 0
    for i in information:
        if i['id'] == id:
            count = int(i['count'])+1
            sums = int(i['book_price']) * count
            # print(count,sums,'11111')
            i['sums']=sums
            i['count']=count
        s_sum += int(i['sums'])
    s_sums=s_sum
    request.session['informate'] = information
    return JsonResponse({'count':count,'sums':sums,'s_sums':s_sums})

def shopdel(request):
    id = request.GET.get("id")
    information = request.session.get('informate')
    s_sum = 0
    for i in information:
        if i['id'] == id:
            count = int(i['count']) - 1
            sums = int(i['book_price']) * count
            # print(count, sums, '11111')
            i['sums'] = sums
            i['count'] = count
        s_sum += int(i['sums'])
    s_sums = s_sum
    request.session['informate'] = information
    # return render(request,'car.html',{'count':count, 'sums':sums,'s_sums':s_sums})
    return JsonResponse({'count':count, 'sums':sums,'s_sums':s_sums})

def delete_s(request):
    id = request.GET.get("id")
    information = request.session.get('informate')
    if information[0] is None:
        return render(request,"dis_car.html")
    for i in information:
        if i['id'] == id:
            information.remove(i)
            # print(information,1111)
            request.session['informate']=information
            # return redirect('app01:shoppingcar')
    return redirect('app01:shoppingcar')

def shoudong(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    print(id,count,'333')
    information = request.session.get('informate')
    s_sum = 0
    for i in information:
        if i['id'] == id:
            count = count
            print(count,'666')
            sums = int(count)*int(i['book_price'])
            i['sums'] = sums
            i['count'] = count
        s_sum += int(i['sums'])
    s_sums = s_sum
    request.session['informate'] = information
    return JsonResponse({'count': count, 'sums': sums, 's_sums': s_sums})


def indentok(request):
    name = request.COOKIES.get('nuname')
    if name:
        request.session['nuname'] = name
    nuname = request.session.get('nuname')
    nuname2 = request.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()
    name = request.POST.get('ship_man')
    address = request.POST.get("ship_add")
    num = request.POST.get("ship_num")
    mp = request.POST.get("ship_mp")
    tp = request.POST.get("ship_tp")
    n = TUser.objects.get(user_email=nuname)
    n.taddress_set.create(name=name, detail_address=address, telphone=tp, addr_mobile=mp)
    information = request.session.get('informate')
    s_sums = 0
    for i in information:
        s_sums += int(i['sums'])
    s_sums = s_sums
    return render(request, 'indent ok.html', {'nuname': nuname, 's_sums': s_sums})

def indent(request):
    name = request.COOKIES.get('txtUsername')
    if name:
        request.session['nuname'] = name
    nuname = request.session.get('nuname')
    nuname2 = request.GET.get('nuname')
    if nuname2 == '1':
        nuname = ''
        request.session.clear()
    nuname = request.session.get('nuname')
    print(nuname,'111')
    #检测用户是否登录
    if nuname: #已登录
        information = request.session.get('informate')
        s_sums = 0
        for i in information:
            s_sums += int(i['sums'])
        s_sums = s_sums
        m = TUser.objects.filter(user_email=nuname)
        se_add = m[0].taddress_set.all()
        va = request.GET.get('value_s')
        for s in se_add:
            name = s.name
            deta = s.detail_address
            telphone = s.telphone
            mobile = s.addr_mobile
            addid = str(s.id)
            id = s.user_id
            if addid == va:
                return JsonResponse({'name': name, 'deta': deta, 'telphone': telphone, 'mobile': mobile})

        return render(request, 'indent.html', {"information": information, 's_sums': s_sums,'nuname':nuname})
    else:  #未登录
        return render(request,'login.html')



# ########邮箱############
def arrive_form(request):
    return render(request, 'register.html')

def hash_code(name, now):
    """
    谁调此方法就为谁返回一个随机的验证码
    :param name:
    :param now:
    :return:
    """
    h = hashlib.md5()
    name += now
    h.update(name.encode())
    return h.hexdigest()

def make_confirm_string(new_user):
    """
    为用户生成随机验证码并将验证码保存在数据库中
    :param new_user:
    :return:
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code = hash_code(new_user.username, now)
    models.Confirm_string.objects.create(code=code, user=new_user)
    return code

def send_email(email, code):
    subject = 'python157'
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1', code)
    #发送邮件所执行的方法以及所需的参数
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    # 发送的heml文本的内容
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def user_register(request):
    """
    处理用户注册请求的view
    :param request: 用户的表单参数
    :return:
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    new_user = models.User.objects.create(username=username, password=password, email=email)
    code = make_confirm_string(new_user)
    send_email(email, code)
    return HttpResponse('')

def user_confirm(request):
    """
    用户处理用户发起邮箱验证的请求
    :param request: 用户发来的验证码
    :return:
    """
    user_code = request.GET.get('code')
    confirm = models.Confirm_string.objects.get(code=user_code)
    if confirm:
        # 将用户状态改为可登陆
        pass
        # 删除验证码
    else:
        pass















#
# def carview(request):
#     cart=request.session.get('cart')
#     c_book=cart.cartltems
#     print(c_book)
#     d_book=cart.dustbin
#     cart.c_sums()
#     sum_price=cart.sum_price
#     total_price=cart.total_price
#     return render(request,'car.html',{'c_book':c_book,'total_price':total_price,'sum_price':sum_price,'d_book':d_book})
# def addajax(request):
#     b_id=int(request.GET.get('b_id'))
#     amount1=int(request.GET.get('amount'))
#     cart=request.session.get('cart')
#     if cart is None:
#        cart=Cart()
#        cart.c_add(b_id,amount1)
#        request.session['cart'] = cart
#     else:
#         cart.c_add(b_id,amount1)
#         request.session['cart'] = cart
#     return HttpResponse('1')
# def updateajax(request):
#     b_id = int(request.GET.get('b_id'))
#     amount1 = int(request.GET.get('amount'))
#     cart = request.session.get('cart')
#     cart.c_update(b_id,amount1)
#     cart.c_sums()
#     sums=cart.sum_price
#     total=cart.total_price
#     request.session['cart'] = cart
#     return HttpResponse(str(sums)+'+'+str(total))
# def removeajax(request):
#     order=request.GET.get('order')
#     b_id=int(request.GET.get('b_id'))
#     amount1 = request.GET.get('amount')
#     cart=request.session.get('cart')
#     cart.c_remove(b_id,order,amount1)
#     request.session['cart'] = cart
#     return HttpResponse('1')
# def recoverajax(request):
#     order=request.GET.get('order')
#     b_id=int(request.GET.get('b_id'))
#     amount1 = request.GET.get('amount')
#     cart=request.session.get('cart')
#     cart.c_recover(b_id,order,amount1)
#     request.session['cart'] = cart
#     return HttpResponse('1')
# def pay(request):
#     loginflag=request.session.get('login')
#     if loginflag=='ok':
#         usersname=request.session.get('usersname')
#         u_id=TUser.objects.filter(name=usersname).values('id')[0]['id']
#         addres=TAddress.objects.filter(user_id=u_id)[0]
#         cart=request.session.get('cart')
#         c_book = cart.cartltems
#         cart.c_sums()
#         sum_price = cart.sum_price
#         total_price = cart.total_price
#         return render(request,'indent.html',{'usersname':usersname,'addres':addres,'c_book':c_book,'sum_price':sum_price,'total_price':total_price})
#     else:
#         return redirect('app01:login')
#
# # def shoppingcar(request):
# #     information=request.session.get('informate')
# #     # print(information,'666')
# #
# #     return render(request,'car.html',{"information":information})
# #
# # def shopadd(request):
# #     id = request.GET.get("id")
# #     # print(id,'274')
# #     information=request.session.get("informate")
# #     print(information)
# #     s_sum = 0
# #     for i in information:
# #         if i['id'] == id:
# #             count = int(i['count'])+1
# #             sums = int(i['book_price']) * count
# #             # print(count,sums,'11111')
# #             i['sums']=sums
# #             i['count']=count
# #         request.session['informate'] = information
# #     # information = request.session.get('informate')
# #     # print(information,'3333')
# #
# #     return JsonResponse({'count':count,'sums':sums})
# #
# # def shopdel(request):
# #     id = request.GET.get("id")
# #     information = request.session.get('informate')
# #     for i in information:
# #         if i['id'] == id:
# #             count = int(i['count']) - 1
# #             sums = int(i['book_price']) * count
# #             # print(count, sums, '11111')
# #             i['sums'] = sums
# #             i['count'] = count
# #             request.session['informate'] = information
# #
# #     return JsonResponse({'count':count, 'sums':sums})
# #
# # def delete_s(request):
# #     id = request.GET.get("id")
# #     information = request.session.get('informate')
# #     for i in information:
# #         if i['id'] == id:
# #             information.remove(i)
# #             print(information,1111)
# #             request.session['informate']=information
# #             # return redirect('app01:shoppingcar')
# #     return redirect('app01:shoppingcar')
#
# #修改购物车的view
# # def update_cart(request):
# #     #接收参数
# #     name = request.COOKIES.get('nuname')
# #     if name:
# #         request.session['nuname'] = name
# #     nuname = request.session.get('nuname')
# #     print(nuname)
# #     nuname2 = request.GET.get('nuname')
# #     print(nuname2)
# #     if nuname2 == '1':
# #         nuname = ''
# #         request.session.clear()
# #     information = request.session.get('informate')
# #     # 调用方法
# #     # 相应模板
# #     return render(request, 'car.html',{"information": information,'nuname': nuname})
# #
# # def get(request):
# #     '''显示'''
# #     # 获取登录的用户
# #     user = request.user
# #     # 获取用户购物车中商品的信息
# #     conn = get_redis_connection('default')
# #     cart_key = 'cart_%d'%user.id
# #     # {'商品id':商品数量, ...}
# #     cart_dict = conn.hgetall(cart_key)
# #     books = []
# #     # 保存用户购物车中商品的总数目和总价格
# #     book_count = 0
# #     book_price = 0
# #     # 遍历获取商品的信息
# #     for book_id, count in cart_dict.items():
# #         # 根据商品的id获取商品的信息
# #         book = TBook.objects.get(id=book_id)
# #         # 计算商品的小计
# #         amount = book.price*int(count)
# #         # 动态给book对象增加一个属性amount, 保存商品的小计
# #         book.amount = amount
# #         # 动态给book对象增加一个属性count, 保存购物车中对应商品的数量
# #         book.count = count
# #         # 添加
# #         books.append(book)
# #         # 累加计算商品的总数目和总价格
# #         book_count += int(count)
# #         book_price += amount
# #     # 组织上下文
# #     context = {'book_count':book_count,
# #                 'book_price':book_price,
# #                 'books':books}
# #     # 使用模板
# #     return render(request, 'car.html', context)
# #
# #
# # #删除购物车
# # def delete_book(request):
# #     return
# #
# #


##########邮箱#########
# def arrive_form(request):
#     return render(request, 'register.html')
#
# def hash_code(name, now):
#     """
#     谁调此方法就为谁返回一个随机的验证码
#     :param name:
#     :param now:
#     :return:
#     """
#     h = hashlib.md5()
#     name += now
#     h.update(name.encode())
#     return h.hexdigest()
#
# def make_confirm_string(new_user):
#     """
#     为用户生成随机验证码并将验证码保存在数据库中
#     :param new_user:
#     :return:
#     """
#     now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     code = hash_code(new_user.username, now)
#     models.Confirm_string.objects.create(code=code, user=new_user)
#     return code
#
# def send_email(email, code):
#     subject = 'python157'
#     text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
#     html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1', code)
#     #发送邮件所执行的方法以及所需的参数
#     msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
#     # 发送的heml文本的内容
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#
# def user_register(request):
#     """
#     处理用户注册请求的view
#     :param request: 用户的表单参数
#     :return:
#     """
#     username = request.POST.get('user_name')
#     password = request.POST.get('password')
#     email = request.POST.get('email')
#     new_user = models.TUser.objects.create(username=username, password=password, email=email)
#     code = make_confirm_string(new_user)
#     send_email(email, code)
#     return HttpResponse('')
#
# def user_confirm(request):
#     """
#     用户处理用户发起邮箱验证的请求
#     :param request: 用户发来的验证码
#     :return:
#     """
#     user_code = request.GET.get('code')
#     confirm = models.Confirm_string.objects.get(code=user_code)
#     if confirm:
#         # 将用户状态改为可登陆
#         pass
#         # 删除验证码
#     else:
#         pass
#
# def shoppingcar(request):
#     information=request.session.get('informate')
#     # print(information,'666')
#
#     return render(request,'car.html',{"information":information})
#
# def shopadd(request):
#     id = request.GET.get("id")
#     # print(id,'274')
#     information=request.session.get("informate")
#     print(information)
#     s_sum = 0
#     for i in information:
#         if i['id'] == id:
#             count = int(i['count'])+1
#             sums = int(i['book_price']) * count
#             # print(count,sums,'11111')
#             i['sums']=sums
#             i['count']=count
#         request.session['informate'] = information
#     # information = request.session.get('informate')
#     # print(information,'3333')
#
#     return JsonResponse({'count':count,'sums':sums})
#
#
# def shopdel(request):
#     id = request.GET.get("id")
#     information = request.session.get('informate')
#     for i in information:
#         if i['id'] == id:
#             count = int(i['count']) - 1
#             sums = int(i['book_price']) * count
#             # print(count, sums, '11111')
#             i['sums'] = sums
#             i['count'] = count
#             request.session['informate'] = information
#
#     return JsonResponse({'count':count, 'sums':sums})
#
#
# def delete_s(request):
#     id = request.GET.get("id")
#     information = request.session.get('informate')
#     for i in information:
#         if i['id'] == id:
#             information.remove(i)
#             print(information,1111)
#             request.session['informate']=information
#             # return redirect('app01:shoppingcar')
#     return redirect('app01:shoppingcar')
#
# #修改购物车的view
# # def update_cart(request):
# #     #接收参数
# #     name = request.COOKIES.get('nuname')
# #     if name:
# #         request.session['nuname'] = name
# #     nuname = request.session.get('nuname')
# #     print(nuname)
# #     nuname2 = request.GET.get('nuname')
# #     print(nuname2)
# #     if nuname2 == '1':
# #         nuname = ''
# #         request.session.clear()
# #     information = request.session.get('informate')
# #     # 调用方法
# #     # 相应模板
# #     return render(request, 'car.html',{"information": information,'nuname': nuname})
# #
# # def get(request):
# #     '''显示'''
# #     # 获取登录的用户
# #     user = request.user
# #     # 获取用户购物车中商品的信息
# #     conn = get_redis_connection('default')
# #     cart_key = 'cart_%d'%user.id
# #     # {'商品id':商品数量, ...}
# #     cart_dict = conn.hgetall(cart_key)
# #     books = []
# #     # 保存用户购物车中商品的总数目和总价格
# #     book_count = 0
# #     book_price = 0
# #     # 遍历获取商品的信息
# #     for book_id, count in cart_dict.items():
# #         # 根据商品的id获取商品的信息
# #         book = TBook.objects.get(id=book_id)
# #         # 计算商品的小计
# #         amount = book.price*int(count)
# #         # 动态给book对象增加一个属性amount, 保存商品的小计
# #         book.amount = amount
# #         # 动态给book对象增加一个属性count, 保存购物车中对应商品的数量
# #         book.count = count
# #         # 添加
# #         books.append(book)
# #         # 累加计算商品的总数目和总价格
# #         book_count += int(count)
# #         book_price += amount
# #     # 组织上下文
# #     context = {'book_count':book_count,
# #                 'book_price':book_price,
# #                 'books':books}
# #     # 使用模板
# #     return render(request, 'car.html', context)
# #
# #
# # #删除购物车
# # def delete_book(request):
# #     return
# #
# #
# def indent(request):
#     name = request.COOKIES.get('nuname')
#     if name:
#         request.session['nuname'] = name
#     nuname = request.session.get('nuname')
#     print(nuname)
#     nuname2 = request.GET.get('nuname')
#     print(nuname2)
#     if nuname2 == '1':
#         nuname = ''
#         request.session.clear()
#     return  render(request,'indent.html',{'nuname': nuname})
#
# def indentok(request):
#     name = request.COOKIES.get('nuname')
#     if name:
#         request.session['nuname'] = name
#     nuname = request.session.get('nuname')
#     print(nuname)
#     nuname2 = request.GET.get('nuname')
#     print(nuname2)
#     if nuname2 == '1':
#         nuname = ''
#         request.session.clear()
#     return  render(request,'indent ok.html',{'nuname': nuname})



