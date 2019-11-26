from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Information_portal.settings')
django.setup()

# 创建一个Celery类的实例对象
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/2')


#安装命令：redis-server.exe --service-install redis.windows.conf --loglevel verbose

#启动服务命令：redis-server.exe  --service-start/stup
#
#D:\Information_portal>celery -A celery_task.task worker -l info -P eventlet  启动异步任务


# 定义任务函数
@app.task
def send_register_active_email(to_email, username,userno ):
    active_url = '<h1>{}欢迎使用，点击激活</h1><br/><a href="http://127.0.0.1:8000/Information_portal/active/?usename={}&userid={}"></a>'.format(
        username, username, userno)
    send_mail(subject='请注意这是Django邮件测试', message=active_url, from_email=settings.EMAIL_HOST_USER,
              recipient_list=[to_email])
