import os
import re

from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename

from App.models import User, db, House, Order, Area
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
@user_blueprint.route('/index/', methods=['GET'])
@is_login
def index():
    if request.method == 'GET':
        return render_template('index.html')


# 搜索
@user_blueprint.route('/search/', methods=['GET'])
def search():

    return render_template('search.html')


# 搜索接口
@user_blueprint.route('/user_search/', methods=['GET'])
def user_search():
    sort_key = request.args.get('sk')
    a_id = request.args.get('aid')
    begin_date = request.args.get('sd')
    end_date = request.args.get('ed')
    area_name = request.args.get('aname')


    houses = House.query.filter_by(area_id=a_id)
    # 不能查询自己发布的房源，排除当前用户发布的房屋
    if 'user_id' in session:
        hlist = houses.filter(House.user_id != (session['user_id']))

    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
    order_list = Order.query.filter(Order.status != 'REJECTED')
    # 情况一：
    order_list1 = Order.query.filter(Order.begin_date >= begin_date, Order.end_date <= end_date)
    # 情况二：
    order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
    # 情况三：
    order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
    # 情况四：
    order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
    # 获取订单中的房屋编号
    house_ids = [order.house_id for order in order_list2]
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
    # 查询排除入住时间和离店时间在预约订单内的房屋信息
    hlist = hlist.filter(House.id.notin_(house_ids))

    # 排序规则,默认根据最新排列
    sort = House.id.desc()
    if sort_key == 'booking':
        sort = House.order_count.desc()
    elif sort_key == 'price-inc':
        sort = House.price.asc()
    elif sort_key == 'price-des':
        sort = House.price.desc()
    hlist = hlist.order_by(sort)
    hlist = [house.to_dict() for house in hlist]

    # 获取区域信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]

    return jsonify(code=status_code.OK, houses=hlist, areas=area_dict_list)


# 搜索接口
@user_blueprint.route('/index_search/', methods=['GET'])
def index_search():

    return jsonify()


@user_blueprint.route('/user_index/', methods=['GET'])
@is_login
def user_index():
    house_list = House.query.all()
    houses = [house.to_dict() for house in house_list]
    if session['user_id']:
        user = User.query.filter_by(id=session['user_id']).first()
    return jsonify({'code': '200', 'houses': houses, 'user': user.to_basic_dict()})


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



