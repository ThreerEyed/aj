
from flask import Flask
from flask_script import Manager

from Ihome.views import user
from utils.app_creat import create_app

app = create_app()


manage = Manager(app)
app.register_blueprint(blueprint=user, url_prefix='/user')


if __name__ == '__main__':
    manage.run()
