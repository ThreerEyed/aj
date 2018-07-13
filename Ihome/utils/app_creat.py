import os

import redis
from flask import Flask
from flask_session import Session

from User.house_views import house
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

    app.config['SECRET_KEY'] = '\x9dF\x19\xdd#\x8c>K\xeb\xe4k|fq\x96Q\xcd\x05~\xb6'

    # 创建redis实例用到的参数
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask-session使用的参数
    app.config['SESSION_TYPE'] = "redis"  # 保存session数据的地方
    app.config['SESSION_USE_SIGNER'] = True  # 为session id进行签名
    app.config['SESSION_REDIS'] = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 保存session数据的redis配置
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期秒

    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=house, url_prefix='/house')

    se.init_app(app=app)
    db.init_app(app=app)
    return app



