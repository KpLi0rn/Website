from app import db
from app.main import bp
from flask import render_template,redirect,flash,url_for,request,current_app
from app.main.forms import EditForm,PostForm
from flask_login import current_user,login_required# 登陆框有两种情况 一种是已经登陆了 还有一种是要登陆的
from app.models import User,Post  # 对登陆的用户进行一个数据库检索和校验
from datetime import datetime

@bp.route('/',methods=["GET","POST"])
@bp.route('/index',methods=["GET","POST"])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.post.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("发布成功")
        return redirect(url_for('main.index'))
    # posts = current_user.followed_posts().all()
    page = request.args.get('page',1,type=int)
    posts = current_user.followed_posts().paginate(page,current_app.config['POST_PRE_PAGE'],False)   # paginate 是控制page的范围
    next_url = url_for('main.index',page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index',page=posts.prev_num) \
        if posts.prev_num else None
    return render_template("index.html",posts=posts.items,title="Welcome",form=form,next_url=next_url,prev_url=prev_url)


@bp.route('/user/<username>',methods=['GET','POST'])
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

@bp.before_request
def before_request():   # 将时间 和 表单里面进行一个联系  利用 app.before_request 在试图函数之前进行一个运行
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # 进行数据的提交
        db.session.commit()

@bp.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditForm(current_user.username)     # form 相当于是登陆框的一些后端代码
    if form.validate_on_submit():
        current_user.username = form.username.data   # form.username.data 意思应该是 框框接受到到数据 然后赋值给当前用户到username 其实就是表单的数据
        current_user.about_me = form.about_me.data   # 这里在整理思路的时候想错了 这里应该是表单中获取的数值 赋值到 数据库 也就是 current 数据库的数据是不用data的
        db.session.commit()
        flash("编辑成功")
        return redirect(url_for('main.user',username=current_user.username))   # 进行一个url跳转
    elif request.method == "GET":     # get的话那很有可能就是初始情况 我们把数据库的数据赋值给表单的数据
        form.username.data = current_user.username  # 将数据库中的数据移动到表单的数据
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html",form=form)  # 这里是绑定模版 传参数

@bp.route('/follow/<username>',methods=['GET','POST'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('main.index'))
    if current_user == user:
        flash("你不能关注自己!")
        return redirect(url_for('main.index'))
    current_user.follow(user)
    db.session.commit()
    flash("关注成功!")
    return redirect(url_for('main.user',username=username))

@bp.route('/unfollow/<username>',methods=['GET','POST'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for('main.index'))
    if current_user == user:
        flash("你不能取消关注自己")
        return redirect(url_for('main.index'))
    current_user.unfollow(user)
    db.session.commit()
    flash("取消关注成功")
    return redirect(url_for('main.index'))

@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type=int)   # 首先获取 page的参数
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,current_app.config['POST_PRE_PAGE'],False)
    next_url = url_for('main.explore',page=posts.next_num) \
        if posts.next_num else None
    prev_url = url_for('main.explore',page=posts.prev_num) \
        if posts.prev_num else None
    return render_template('index.html',posts=posts.items,title="Explore",next_url=next_url,prev_url=prev_url)   # 返回的是一个实例 通过items方法获取列表

