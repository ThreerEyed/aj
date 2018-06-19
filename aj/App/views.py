from flask import Blueprint, request, render_template, redirect, url_for, session

from App.models import User, db

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/')
def hello():
    return 'hello, world'


# 创建数据
@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '数据创建成功'


# 删除数据
@user_blueprint.route('/drop_db/')
def drop_db():
    db.drop_all()
    return '数据删除成功'


# 注册
@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return render_template('register.html', msg='两次密码输入不一致')

        user = User()
        user.phone = mobile
        user.password = password2

        user.add_update()

        return redirect(url_for('user.login'))


# 登录
@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        phone = request.form.get('mobile')
        password = request.form.get('password')
        if User.query.filter_by(phone=phone).first():
            user = User.query.filter_by(phone=phone).first()
            if user.check_pwd(password):
                session['user_id'] = user.id
            else:
                return render_template('login.html', msg='用户名或密码错误')

        else:
            return render_template('login.html', msg='没有此用户')

        return redirect(url_for('user.index'))


# 首页
@user_blueprint.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
