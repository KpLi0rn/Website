# 这里是数据库表的模型
from datetime import datetime
from app import db
# id username password email
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(length=10),index=True,unique=True)
    password_hash = db.Column(db.String(length=128))
    email = db.Column(db.String(length=50),index=True,unique=True)
    posts = db.relationship("Post",backref="author",lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))  # 这里对应的是相关联的表 user的id 和user——id 进行绑定 所以是 user.id
    timestamp = db.Column(db.DateTime,default=datetime.utcnow(),index=True)
    content = db.Column(db.String(length=150))

    def __repr__(self):
        return "<Post {}>".format(self.content)