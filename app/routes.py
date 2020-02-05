from app import app,db
from flask import render_template,redirect,flash,url_for,request
from werkzeug.urls import url_parse      # url 解析
from app.forms import LoginForm,RegisterForm,EditForm
from flask_login import current_user,login_user,logout_user,login_required# 登陆框有两种情况 一种是已经登陆了 还有一种是要登陆的
from app.models import User  # 对登陆的用户进行一个数据库检索和校验
from datetime import datetime
@app.route('/')
@app.route('/index')
@login_required
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
        # 这里的first的意思就是返回元素中的第一个
        if not user or not user.check_password(loginform.password.data):
            flash("用户名或密码错误")
            return redirect(url_for('login'))
        # else:
        login_user(user,remember=loginform.remember_me.data)   # 这一步不能忘的 前面那个只是校验 校验成功之后 通过 login_user 进行登陆
        # 通过 request 进行参数的获取  有参数就跳转到参数的位置 没有参数就默认跳转到 index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title='Login in', loginform=loginform)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",register=register)

@app.route('/user/<username>',methods=['GET','POST'])
@login_required
def user(username):
    # 既然是用户的个人页面 那么数据我们肯定要从数据库里面进行搜索
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{
        "author": "KpLi0rn",
        "content": "be happy"
    },
        {
            "author": "kplern",
            "content": "have a good day"
        }]
    return render_template("profile.html",user=user,posts=posts)

@app.before_request
def before_request():   # 将时间 和 表单里面进行一个联系  利用 app.before_request 在试图函数之前进行一个运行
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # 进行数据的提交
        db.session.commit()

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditForm(current_user.username)     # form 相当于是登陆框的一些后端代码
    if form.validate_on_submit():
        current_user.username = form.username.data   # form.username.data 意思应该是 框框接受到到数据 然后赋值给当前用户到username 其实就是表单的数据
        current_user.about_me = form.about_me.data   # 这里在整理思路的时候想错了 这里应该是表单中获取的数值 赋值到 数据库 也就是 current 数据库的数据是不用data的
        db.session.commit()
        flash("编辑成功")
        return redirect(url_for('user',username=current_user.username))   # 进行一个url跳转
    elif request.method == "GET":     # get的话那很有可能就是初始情况 我们把数据库的数据赋值给表单的数据
        form.username.data = current_user.username  # 将数据库中的数据移动到表单的数据
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html",form=form)  # 这里是绑定模版 传参数



