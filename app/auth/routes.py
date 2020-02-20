from app import db
from app.auth import bp
from flask import render_template,redirect,flash,url_for,request
from werkzeug.urls import url_parse      # url 解析
from app.auth.forms import LoginForm,RegisterForm,ResetForm,ResetPasswordForm
from app.auth.email import send_reset_pwd_email
from flask_login import current_user,login_user,logout_user# 登陆框有两种情况 一种是已经登陆了 还有一种是要登陆的
from app.models import User,Post  # 对登陆的用户进行一个数据库检索和校验

@bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:     # 检验用户是否已经登陆
        return redirect(url_for('main.index'))
    loginform = LoginForm()   # 这里括号没有加 导致出现了错误
    # 如果点击了submit的提交按键 那么进行一个逻辑的判断
    # 1 用户的数据有没有在数据库里 2 用户的输入有没有空
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()   # User.username.data 这里错了 应该是loginform.username.data 因为这里是从登陆框里面获取内容
        # 这里的first的意思就是返回元素中的第一个
        if not user or not user.check_password(loginform.password.data):
            flash("用户名或密码错误")
            return redirect(url_for('auth.login'))
        # else:
        login_user(user,remember=loginform.remember_me.data)   # 这一步不能忘的 前面那个只是校验 校验成功之后 通过 login_user 进行登陆
        # 通过 request 进行参数的获取  有参数就跳转到参数的位置 没有参数就默认跳转到 index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template("auth/login.html", title='Login in', loginform=loginform)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    register = RegisterForm()
    if register.validate_on_submit():
        # 这里不是查询数据 这里是 直接把数据写进去
        # user = User.query.filter_by(username=register.username.data,email=register.email.data).first()
        user = User(username=register.username.data,email=register.email.data)
        user.set_password(register.password.data)  # 这里打错了变成check password了  这一步不能忘记 因为我们数据库里面保存的是 哈希数值 这里要用函数 生成一下哈希
        db.session.add(user)    # 这里我变成 User了 但是这里是数据库的提交 需要使用db
        db.session.commit()
        flash("恭喜你注册成功")
        # 注册成功之后跳转到登陆
        return redirect(url_for('auth.login'))
    return render_template("auth/register.html",title="Register",register=register)

@bp.route('/reset',methods=['GET','POST'])
def reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_pwd_email(user)
            flash("点击邮箱中的密码重置链接进行密码重置")
            return redirect(url_for('auth.login'))
    return render_template("auth/reset.html",form=form,title="ResetPassword")

# 重新设置密码的页面
@bp.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.check_reset_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)   # 教程有问题
        db.session.commit()
        flash("密码修改成功")
        return redirect(url_for('auth.login'))
    return render_template("auth/reset_password.html",form=form)
