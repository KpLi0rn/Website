from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):   # 进行框架的导入 都是基于这个框架的
    username = StringField('账号',validators=[DataRequired()])
    password = PasswordField('密码',validators=[DataRequired()])
    remember_me = BooleanField('Remember')
    submit = SubmitField('Submit')

