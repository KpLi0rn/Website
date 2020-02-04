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
# id username password email
class User(UserMixin,db.Model):   # User 继承 db.Model 是所有类型的基类  UserMixin 这个是基类包含了四种校验属性
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(length=10),index=True,unique=True)
    password_hash = db.Column(db.String(length=128))
    email = db.Column(db.String(length=50),index=True,unique=True)
    posts = db.relationship("Post",backref="author",lazy="dynamic")    # backref 有点类似快捷方式

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)


class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  # 这里对应的是相关联的表 user的id 和user——id 进行绑定 所以是 user.id
    timestamp = db.Column(db.DateTime,default=datetime.utcnow(),index=True)
    content = db.Column(db.String(length=150))

    def __repr__(self):
        return "<Post {}>".format(self.content)

