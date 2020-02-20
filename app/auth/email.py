from flask import render_template
from app import mail
from app.email import send_mail
from app.auth import bp
from flask import current_app

def send_reset_pwd_email(user):
    token = user.create_resetpwd_token()  # 我们先创建用户的token 然后再发送！
    send_mail("Reset Password",sender=current_app.config['ADMINS'][0],recipients=[user.email],
              text_body=render_template("email/reset_password.txt",user=user,token=token),
              text_html=render_template("email/reset_password.html",user=user,token=token))
