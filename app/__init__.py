from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask_mail import Mail,Message
from flask_moment import Moment
import logging
import os

app = Flask(__name__)     # 相当于给人起名字一样 app 具有了flask类的功能
bootstrap = Bootstrap(app)
app.config.from_object(Config) # 将配置对象的配置信息转化成app.config的配置
db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)   # mail 写到config前面了 所以发不出去邮件
login = LoginManager(app)
moment = Moment(app)
login.login_view = 'login'  # 进行强制跳转的页面

from app import routes,models,errors # 需要导入models 不然就无法进行迁移了

# # 如果不是debug模式的话 就进行日志的记录
# # 大致的逻辑是这样的生成一个log文件 然后进行 形式化
# if not app.debug:
#     # 如果没有日志文件夹那么就创建一个
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/website.log',maxBytes=10240,backupCount=10)
#     # 时间 等级名字 错误信息 错误路径 行数
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s in [%(filename)s %(lineno)s]'))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)  # 这里的方法是 Handler
#     app.logger.setLevel(logging.INFO)
#     app.logger.info("Website Starts up")
#
