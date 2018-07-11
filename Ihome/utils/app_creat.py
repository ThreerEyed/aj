import os

from flask import Flask

from User.models import db
from User.views import user


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

    app.register_blueprint(blueprint=user, url_prefix='/user')

    db.init_app(app=app)
    return app



