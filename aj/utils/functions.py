import os

from flask import Flask

from App.views import user_blueprint, db


def create_app():

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/aj'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # session 配置
    app.config['SECRET_KEY'] = '\x9dF\x19\xdd#\x8c>K\xeb\xe4k|fq\x96Q\xcd\x05~\xb6'

    db.init_app(app=app)
    return app
