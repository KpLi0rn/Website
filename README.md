# Website
按照https://github.com/luhuisicnu/The-Flask-Mega-Tutorial-zh/blob/master/docs/进行学习 不懂的地方会添加上自己的注释 后续熟练之后会对代码进行修改 刚刚开始写每天都会写一些 学习flask框架中自己日常练习的项目代码 想着放到github上更加有动力学习
后续会根据自己的理解加入一些新的东西 打算把这个项目做成一个博客
### 目前进度
实现的功能 登陆 注册 个人主页 个人主页的信息修改 自定义错误页面 错误日志 粉丝和关注 邮箱 忘记密码 时间显示 
对结构进行优化(蓝图)

遇到的一个错误 
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user

解决方案：
运行flask shell
from app import User
db.create_all()


