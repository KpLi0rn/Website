import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "oasjn$@$%nodIVUsdf90832"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        "sqlite:///" + os.path.join(basedir,"app.db")  # 这里之前少了一行

    SQLALCHEMY_TRACK_MODIFICATIONS = False # 这一行还是要加的 配置数据变更之后是否需要发给应用
