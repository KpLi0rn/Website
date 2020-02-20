from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,length
from app.models import User,Post

# 个人资料的编辑 可以进行user的修改
class EditForm(FlaskForm):   # 这个form 的类也是继承与 flaskform的
    # 用户名修改的时候我们需要进行查看 我们修改后的用户名 有没有重复 但是如果用户不修改的话 那么也应该允许
    username = StringField("用户名",validators=[DataRequired()])
    about_me = TextAreaField("简介",validators=[length(10,150)])
    submit = SubmitField("提交")

    def __init__(self,original_username,*args,**kwargs):  # 构造函数 original_username 代表的是原来的用户名 所以routes.py 里面要进行current_user.username的添加
        # *args 可以传入一系列的数值 数量不定  **kwargs 可以传入字典 一系列
        # 这里为什么要进行一步继承 ?
        # 继承 super(EditForm,self).__init__(*args,**kwargs) 继承父类型的所有参数
        super(EditForm,self).__init__(*args,**kwargs)  # 如果不使用super那么我们就不能调用父类的属性 这里的EditForm相当于 flaskform的子类
        # 这行的代码就是 调用EditForm的父类的方法和属性 因为我们要获取的参数是username  username是父类的参数 也就是flaskform的参数
        self.original_username = original_username

    def validate_username(self,username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError("当前用户名已存在")

class PostForm(FlaskForm):
    post = TextAreaField("说些什么吧!",validators=[DataRequired(),length(1,150)])
    submit = SubmitField("提交")

