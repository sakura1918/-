import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'project1.settings'

if __name__ == '__main__':
    # send_mail(
    #     'python',
    #     '小九',
    #     'sakura1918@sina.com',
    #     ['sakura1918@163.com'],
    # )
    subject, from_email, to = 'python157', 'sakura1918@sina.com', 'sakura1918@163.com'
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '
    #发送邮件所执行的方法以及所需的参数
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # 发送的heml文本的内容
    msg.attach_alternative(html_content, "text/html")
    msg.send()

