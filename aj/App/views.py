import os
import re

from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

from App.models import User, db
from utils import status_code
from utils.decorator import is_login

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
@user_blueprint.route('/register/', methods=['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')


@user_blueprint.route('/register/', methods=['POST'])
def user_register():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 1. 验证数据完整性
        if not all([mobile, password, password2]):
            return jsonify(status_code.USER_REGISTER_DATA_NOT_NONE)

        # 2，验证手机号码的正确
        mobile_reg = re.match(r'^1[3,4,5,7,8]\d{9}$', mobile)
        if not mobile_reg:
            return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

        # 3, 验证密码
        if password != password2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_IS_NOT_VALID)

        # 4，验证用户
        user1 = User.query.filter_by(phone=mobile).first()
        if user1:
            return jsonify(status_code.USER_EXISTS)

        user = User()
        user.phone = mobile
        user.password = password2
        user.name = mobile

        user.add_update()

        # return redirect(url_for('user.login'))
        return jsonify(status_code.OK)


# 登录
@user_blueprint.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    if request.method == 'POST':
        phone = request.form.get('mobile')
        password = request.form.get('password')

        # 验证数据完整性
        if not all([phone, password]):
            return jsonify(status_code.USER_REGISTER_DATA_NOT_NONE)
        if User.query.filter_by(phone=phone).first():
            user = User.query.filter_by(phone=phone).first()
            if user.check_pwd(password):
                session['user_id'] = user.id
            else:
                return jsonify(status_code.USER_PASSWORD_ERROR)

        else:
            return jsonify(status_code.USER_NO_USER)

        return jsonify(status_code.OK)


# 退出
@user_blueprint.route('/logouts/', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'data': '200'})


# 退出
@user_blueprint.route('/logout/')
def user_logout():
    session.clear()
    return redirect(url_for('user.login'))


# 首页
@user_blueprint.route('/index/', methods=['GET', 'POST'])
@is_login
def index():
    if request.method == 'GET':
        return render_template('index.html')


# 个人中心
@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 用户信息
@user_blueprint.route('/user/', methods=['GET'])
@is_login
def user_info():
    user = User.query.filter_by(id=session['user_id']).first()
    if user:
        return jsonify({'code': '200', 'user_info': user.to_basic_dict()})
    else:
        return jsonify(status_code.USER_NOT_LOGIN_ERROR)


# 我的订单
@user_blueprint.route('/orders/', methods=['GET'])
@is_login
def orders():
    return render_template('orders.html')


# 实名认证
@user_blueprint.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


# 实名认证post
@user_blueprint.route('/auth/', methods=['PATCH'])
@is_login
def user_auth():
    real_name = request.form.get('real-name')
    id_card = request.form.get('id-card')

    if not all([real_name, id_card]):
        return jsonify(status_code.USER_AUTH_DATA_IS_NULL)

    reg = re.match(r'^[1-9]\d{17}', id_card)
    if not reg:
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_INVALID)

    user = User.query.filter_by(id=session['user_id']).first()
    user.id_name = real_name
    user.id_card = id_card

    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify({'code': '200', 'msg': user.to_auth_dict()})


# 用户实名验证
@user_blueprint.route('/auths/', methods=['GET'])
@is_login
def auths():
    user = User.query.filter_by(id=session['user_id']).first()
    return jsonify({'code': '200', 'msg': user.to_auth_dict()})


# 客户订单
@user_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# 修改
@user_blueprint.route('/profile/', methods=['GET'])
def profile():
    return render_template('profile.html')


# 上传图片
@user_blueprint.route('/profile/', methods=['POST'])
@is_login
def user_profile():
    file = request.files.get('avatar')
    # 校验上传图片的格式的正确性
    if not re.match(r'image/.*', file.mimetype):
        return jsonify(status_code.USER_IMAGE_ERROR)
    # 保存
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'static/upload', secure_filename(file.filename))
    file.save(file_path)

    user = User.query.filter_by(id=session.get('user_id')).first()
    user.avatar = file.filename

    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': '0', 'msg': '数据库错误'})
    return jsonify({'code': '200', 'img_url': '/static/upload/' + file.filename})


# 名字修改
@user_blueprint.route('/profile/', methods=['PATCH'])
@is_login
def user_name_profile():
    user_name = request.form.get('user-name')
    if User.query.filter_by(name=user_name).first():
        return jsonify(status_code.USER_NAME_EXISTS)
    user = User.query.filter_by(id=session.get('user_id')).first()
    user.name = user_name

    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify({'code': '200', 'msg': '修改名字成功'})



