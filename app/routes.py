from app import app
from flask import render_template,redirect,flash,url_for
from app.forms import LoginForm

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
    return render_template("index.html",posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    loginform = LoginForm()   # 这里括号没有加 导致出现了错误
    if loginform.validate_on_submit():
        flash("user{},password{}".format(loginform.username.data,loginform.remember_me.data))
        return redirect(url_for("index"))
    return render_template("login.html",loginform=loginform,title="Login in")
