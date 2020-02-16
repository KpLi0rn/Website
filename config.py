import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "oasjn$@$%nodIVUsdf90832"
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        "sqlite:///" + os.path.join(basedir,"app.db")  # 这里之前少了一行
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 这一行还是要加的 配置数据变更之后是否需要发给应用
    POST_PRE_PAGE = 3

    MAIL_SERVER = 'smtp.163.com'#os.environ.get('MAIL_SERVER')
    MAIL_PORT = 25#int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_SSL = True#os.environ.get('MAIL_USE_TLS')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['fetino9319@nwesmail.com']

