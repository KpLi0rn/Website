from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
import os,logging
from logging.handlers import RotatingFileHandler

# app = Flask(__name__)     # 相当于给人起名字一样 app 具有了flask类的功能
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
# app.config.from_object(Config) # 将配置对象的配置信息转化成app.config的配置
mail = Mail()   # mail 写到config前面了 所以发不出去邮件
login = LoginManager()
login.login_view = 'auth.login'  # 进行强制跳转的页面
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    bootstrap.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    moment.init_app(app)

    from app.errors import bp as erroers_bp   # 这里的蓝图可以理解为微服务框架 我们把一个庞大的项目分割成细小的部分
    app.register_blueprint(erroers_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp,url_prefix="/auth")

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # 如果不是debug模式的话 就进行日志的记录
    # 大致的逻辑是这样的生成一个log文件 然后进行 形式化
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

    return app

from app import models  # 需要导入models 不然就无法进行迁移了
