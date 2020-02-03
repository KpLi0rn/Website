from app import app
from flask import render_template,redirect,flash,url_for
from app.forms import LoginForm
from flask_login import current_user,login_user,logout_user# 登陆框有两种情况 一种是已经登陆了 还有一种是要登陆的
from app.models import User  # 对登陆的用户进行一个数据库检索和校验
@app.route('/')
@app.route('/index')
def index():
    posts = [{
        "author":"KpLi0rn",
        "content":"be happy"
    },
    {
        "author":"kplern",
        "content":"have a good day"
    }]
    return render_template("index.html",posts=posts,title="Welcome")

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:     # 检验用户是否已经登陆
        return redirect(url_for('index'))
    loginform = LoginForm()   # 这里括号没有加 导致出现了错误
    # 如果点击了submit的提交按键 那么进行一个逻辑的判断
    # 1 用户的数据有没有在数据库里 2 用户的输入有没有空
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()   # User.username.data 这里错了 应该是loginform.username.data 因为这里是从登陆框里面获取内容
        flash(user)   # 这里我是为了 看 user 这个的数据是怎么样的 以及 为什么要用 first
        if not user or not user.check_password(loginform.password.data):
            flash("用户名或密码错误")
            return redirect(url_for('login'))
        else:
            login_user(user,remember=loginform.remember_me.data)
            return redirect(url_for('index'))

    return render_template("login.html", title='Login in', loginform=loginform)

@app.route('/logout')
def logout():
    login_user()
    return redirect(url_for('index'))