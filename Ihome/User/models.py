from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 基础类
class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


# 用户类
class User(BaseModel, db.Model):

    # 用户id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名称
    name = db.Column(db.String(30))
    # 用户手机号
    phone = db.Column(db.String(11), unique=True)
    # 用户性别
    sex = db.Column(db.Boolean, default=0)
    # 用户真实姓名
    id_name = db.Column(db.String(30))
    # 用户身份证号码
    id_card = db.Column(db.String(255), unique=True)
    # 用户头像
    avatar = db.Column(db.String(255))
    # 用户的密码
    pw_hash = db.Column(db.String(255))


