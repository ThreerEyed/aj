import os

import redis
from flask import Flask
from flask_session import Session

from App.house_views import house_blueprint
from App.views import user_blueprint, db

se = Session()


def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')

    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/aj'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # session 配置
    app.config['SECRET_KEY'] = '\x9dF\x19\xdd#\x8c>K\xeb\xe4k|fq\x96Q\xcd\x05~\xb6'
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

    # 初始化
    db.init_app(app=app)
    se.init_app(app=app)
    return app
