from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from User.models import db
from utils.app_creat import create_app

app = create_app()


manage = Manager(app)
# 绑定db 和 migrate
migrate = Migrate(app, db)
# 添加迁移脚本的命令到manager 中
manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()
