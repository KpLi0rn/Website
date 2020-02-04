from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Email,ValidationError,length
from app.models import User,Post

class LoginForm(FlaskForm):   # 进行框架的导入 都是基于这个框架的
    username = StringField('账号',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('账号',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    password_repeat = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password')])
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    submit = SubmitField('立即注册')

    def validate_username(self,username):    #  以validate开头的 wtforms 会把这种函数方法自定义为默认的验证器 并进行调用他们 这就是为什么 为之前名字不对 500 了

        user= User.query.filter_by(username=username.data).first()   # 这是两种查询方式 中的一种 一种是 first 返回列表中的第一个元素  一种是 all
        if user is not None:
            raise ValidationError('用户名已经被注册')  #生成一个错误

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已被注册')

# 个人资料的编辑 可以进行user的修改
class EditForm(FlaskForm):
    username = StringField("用户名",validators=[DataRequired()])
    about_me = TextAreaField("简介",validators=[length(10,150)])
    submit = SubmitField("提交")


