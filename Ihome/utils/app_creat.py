import os

from flask import Flask


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

    return app



