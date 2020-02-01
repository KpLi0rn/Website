from flask import Flask
from config import Config

app = Flask(__name__)     # 相当于给人起名字一样 app 具有了flask类的功能
app.config.from_object(Config) # 将配置对象的配置信息转化成app.config的配置

from app import routes