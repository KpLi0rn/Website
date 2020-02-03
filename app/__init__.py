from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)     # 相当于给人起名字一样 app 具有了flask类的功能
app.config.from_object(Config) # 将配置对象的配置信息转化成app.config的配置
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)

from app import routes,models # 需要导入models 不然就无法进行迁移了
