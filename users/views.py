from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views import View
from .models import Users_message, Users
import json, re
from Encryption.encry import AesEcb
from django.core.mail import send_mail
from django.conf import settings
from celery_task.task import send_register_active_email

# Create your views here.



class Login_view(View):
    def get(self, request):
        return render(request, 'login.html', {'error_message': ''})

    def post(self, request):
        # if Users.objects.get(users_isactive=1):
            name = request.POST.get('users_name')  # 从html的post请求里拿到
            userpwd1 = request.POST.get('users_password')  # 从html的post请求里拿到
            aes1 = AesEcb()  # 实例化加密模块

            name = aes1.encryption(name)
            userpwd1 = aes1.encryption(userpwd1)
            print(name,userpwd1)
            # print(users_no,users_password1)
            try:
                # 验证用户是否存在数据库中 select * from 用户信息表 where   用户id users_no=users_no, users_password=users_password1
                Users.objects.get(users_name=name, users_password=userpwd1)  # 判断数据库内容是否与输入的相同
                res = redirect('/Information_portal/message/')  # 重定项对象（跳转页面）
                res.set_cookie('username', name)  # 给重定项对象设置cookie
                return res
            except Exception as e:
                print(e)
                # 如果没找到报错 重新返回html文件和错误信息
                return render(request, 'login.html', {'error_message': '账号或者密码错误！'})


class Message(View):
    def get(self, request):
        return render(request, 'message.html')

    def post(self, request):
        # if Users.objects.get(users_isactive=1):
            name1 = request.POST.get('test')
            name1 = name1[10:-1]

            # name1 = request.POST.get('name')
            # major1 = request.POST.get('major')
            print(name1)


            try:
                user1 = Users.objects.get(users_name=name1)
                # name1 = Users.objects.get(users_name=name1)
                # major1 = Users.objects.get(users_major=major1)
                aes1 = AesEcb()


                dict_message = {'name': aes1.unencryption(user1.users_name), 'user_no': aes1.unencryption(user1.users_no),
                                'major': aes1.unencryption(user1.users_major),'img': '/static/imags/{}'.format(user1.users_image)}
                send_message = json.dumps(dict_message)
                return  HttpResponse(send_message)
            except Exception as e:
                print(e)
                return render(request, 'login.html', {'error_message': '信息显示错误！'})


class Register(View):##邮箱功能尚未完成

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('name')  # 接收从HTML端输入的数据
        userpwd = request.POST.get('pwd')
        userpwd1 = request.POST.get('pwd1')
        user_no = request.POST.get('users_no')
        email = request.POST.get('email')
        usermajor = request.POST.get('major')

        if username == None:  # 判断数据是否完整，不完整返回报错
            return render(request, 'register.html', {'error_infor': "姓名数据不完整！"})
        if userpwd == None and userpwd1 == None:  # 判断数据是否完整，不完整返回报错
            return render(request, 'register.html', {'error_infor': "密码数据不完整！"})
        if user_no == None:  # 判断数据是否完整，不完整返回报错
            return render(request, 'register.html', {'error_infor': "id据不完整！"})
        if usermajor == None:  # 判断数据是否完整，不完整返回报错
            return render(request, 'register.html', {'error_infor': "专业数据不完整！"})
        if not re.match(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$',email):
            return render(request, 'register.html', {'error_infor':"邮箱格式错误"})
        try:
            user=Users.objects.get(users_no=user_no)
        except Users.DoesNotExist:
            user=None

        if user:
            return render(request,'register.html',{'error_id':"用户名已存在！"})
        if userpwd != userpwd1:
            return render(request,{"error_password": "两次密码不一样！"})

        try:
            aes1 = AesEcb()                          #实例化加密模块
            usermajor1 = aes1.encryption(usermajor)  #加密方法
            username1 = aes1.encryption(username)
            user_no1 = aes1.encryption(user_no)
            userpwd1 = aes1.encryption(userpwd)
            # print('加密前',usermajor1)
            user = Users.objects.create(users_name=username1, users_no=user_no1, users_password=userpwd1,
                                        users_major=usermajor1)
            user.users_image = '0'
            user.save()
            res1 = aes1.unencryption(usermajor1)  #解密
            res2 = aes1.encryption(username1)
            res3 = aes1.encryption(user_no1)
            res4 = aes1.encryption(userpwd1)

            # print('解密后',res1,)
            id = aes1.encryption(user_no)
            # active_url = '<h1>{}欢迎使用，点击激活</h1><br/><a href="http://127.0.0.1:8000/Information_portal/active/?usename={}&userid={}"></a>'.format(usersname,usersname,id)
            # send_mail(subject='请注意这是Django邮件测试', message=active_url, from_email=settings.EMAIL_HOST_USER, recipient_list=["2257429315@qq.com"])
            to_email = ""                      #目标地址
            send_register_active_email(to_email,username,res1)  #异步发送邮件

            return redirect('/Information_portal/')
        except Exception as e:

            print(e)
            return render(request,'register.html',{'error_infor':"信息保存错误！"})


class Active(View):#邮箱验证

    def get(self, request):

        name = request.GET.get('usename')
        id = request.GET.get('userid')
        print(name, id)
        try:
            user_out = Users.objects.get(users_name=name,users_no=id)
            Users.objects.get(users_isactive = 1)
            return render(request, 'login.html')
        except:
            return HttpResponse('false')
