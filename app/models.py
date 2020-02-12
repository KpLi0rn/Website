# 这里是数据库表的模型
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from app import login

# 进行用户登陆的功能编写的时候 需要用到 flask-login 的 loginManager 并且在 文件中进行注册 给app添加用户登陆的属性 / 对象
# 将注册后的登陆对象 导入到 models 由于要对密码进行加密 所以先书写 哈希加密 和 哈希密码的校验
# 还有一个就是 登陆成功之后 需要进行后续的跟踪这个用户的行为
# 每当已登录的用户导航到新页面时，flask需要进行权限的校验 校验这个这个用户有没有权限进入到这个页面
# 所以需要从数据库中进行检索 id Flask-Login将从会话中检索用户的ID，然后将该用户实例加载到内存中。

# 目的是进行用户的跟踪 这是一个用户加载的功能
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# 创建一个 我关注的人 和关注的人 的关联性的表 】
# 这是自关联的多对多 显示的是 列名是
# 粉丝  关注的人  通过看别人关注的人有几个是自己来判断自己的粉丝情况
# 由于这里是自关联多对多 所有两个实例都是user 所以我们这里两个字段关联的主键都是user.id
followers = db.Table('followers',
                     db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
                     db.Column('followed_id',db.Integer,db.ForeignKey('user.id')))
# 我们这张followers的中间表就是为了 follower_id 就是当前用户的id
""" follower_id  followed_id(表示关注的人)   这里我们只有一种关系 那就是关注 
        1           2       一号关注了二号      这里需要这样进行理解 followed_id 被几个人关注  follower_id关注了几个人 
        1           4       一号关注了四号      所以右边就相当于粉丝 左边就相当于关注
        2           1       二号关注了一号
        3           4       三号关注了四号
"""
# id username password email
# 这里 follow需要这样来进行理解
class User(UserMixin,db.Model):   # User 继承 db.Model 是所有类型的基类  UserMixin 这个是基类包含了四种校验属性
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(length=10),index=True,unique=True)
    password_hash = db.Column(db.String(length=128))
    email = db.Column(db.String(length=50),index=True,unique=True)
    posts = db.relationship("Post",backref="author",lazy="dynamic")    # backref 有点类似快捷方式 这里是一对多关系 因为一个人可以发多个post 我们在post里面建立一个联系到user
    about_me = db.Column(db.String(150))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    # 这个是返回一个列表 返回当前用户 比如说 1 所关注的人的名单 可以用sql语句这样表示
    # select fan_id from user where follow_id = 1（用sql语句比较直白) 然后返回的结果是 [2,4]
    # 返回当前用户关注的所有的人的列表
    followed = db.relationship('User',secondary=followers,
                               primaryjoin=(followers.c.follow_id == id),
                               secondaryjoin=(followers.c.fan_id == id),
                               backref=db.backref('followers',lazy='dynamic'),lazy='dynamic')  # 返回的类型是一个列表 对followers表进行了一个关联  返回对数据是列表

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def is_following(self,user):    # follower是数据表 举个例子这里就是 我有没有关注4 那么就去看fan_id 里面有没有4
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0  # 对关联表进行一个过滤返回符合结果 这里的user_id 相当于4
        # 前面的 self.followed 这个很关键 这个是返回我这个用户所关注的所有的人 然后我们再用过滤器过滤我关注的人里面有没有 4

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        # 关注的人的动态 + 自己的动态                 关注的人的动态                                加了一个限定 我关注的人的动态
        # 一定要加限定 因为之前返回的是 a关注的人 和 b关注的人的合集 后面的过滤就是加一个限定 比如我是a用户 那么就返回 a关注的人的动态
        # 不加限定的sql语句就像这样  select followed_id from user
        # 加了限定的sql语句是这样    select followed_id from user where follower_id = "a"
        followed = Post.query.join(followers,(Post.user_id == followers.c.followed_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)   # user_id是post的外键 我们要保证我们可以看到自己的动态
        return followed.union(own).order_by(Post.timestamp.desc())



class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  # 这里对应的是相关联的表 user的id 和user——id 进行绑定 所以是 user.id
    timestamp = db.Column(db.DateTime,default=datetime.utcnow(),index=True)
    content = db.Column(db.String(length=150))

    def __repr__(self):
        return "<Post {}>".format(self.content)
