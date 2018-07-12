import os

import redis
from flask import Flask
from flask_session import Session

from User.models import db
from User.views import user

se = Session()

def create_app():
    """
    生成 app
    :return:
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_folder = os.path.join(BASE_DIR, 'static')
    template_folder = os.path.join(BASE_DIR, 'html')
    app = Flask(__name__,
                template_folder=template_folder,
                static_folder=static_folder)

    # 配置数据库 mysql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ihome'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    SECRET_KEY = "TQ6uZxn+SLqiLgVimX838/VplIsLbEP5jV7vvZ+Ohqw="
    # 创建redis实例用到的参数
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session使用的参数
    SESSION_TYPE = "redis"  # 保存session数据的地方
    SESSION_USE_SIGNER = True  # 为session id进行签名
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 保存session数据的redis配置
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期秒

    app.register_blueprint(blueprint=user, url_prefix='/user')

    se.init_app(app=app)
    db.init_app(app=app)
    return app



