from flask_mail import Message
from flask import render_template
from app import mail,app

def send_mail(subject,sender,recipients,text_body,text_html):
    msg = Message(subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = text_html
    mail.send(msg)

def send_reset_pwd_email(user):
    token = user.create_resetpwd_token()
    send_mail("Reset Password",sender=app.config['ADMINS'][0],recipients=[user.email],
              text_body=render_template("email/reset_password.txt",user=user,token=token),
              text_html=render_template("email/reset_password.html",user=user,token=token))
