from flask_mail import Message
from flask import render_template
from app import mail
from app.auth import bp
from threading import Thread
from flask import current_app

# current_user
def send_async_email(app,msg):
    with app.app_content():  # 调用上下文来进行使用
        mail.send(msg)

def send_mail(subject,sender,recipients,text_body,text_html):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = text_html
    mail.send(msg)
    # Thread(target=send_reset_pwd_email,args=(current_app._get_current_object(),msg,)).start()

def send_reset_pwd_email(user):
    token = user.create_resetpwd_token()  # 我们先创建用户的token 然后再发送！
    send_mail("Reset Password",sender=current_app.config['ADMINS'][0],recipients=[user.email],
              text_body=render_template("email/reset_password.txt",user=user,token=token),
              text_html=render_template("email/reset_password.html",user=user,token=token))
