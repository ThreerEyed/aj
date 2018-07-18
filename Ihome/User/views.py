import os
import random
import re

import redis as redis
from flask import render_template, Blueprint, request, jsonify, redirect, url_for, current_app, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash

from User.models import User, db
from utils import statucode
from utils.captcha import sms
from utils.captcha.captcha import captcha
from utils.decorator import is_login

user = Blueprint('user', __name__)
redis_store = redis.StrictRedis(host='127.0.0.1', port=6379)


# 注册显示页面
@user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user.route('/imagecode/<image_code_id>',methods=['GET'])
def generate_image_code(image_code_id):
    """
    生成图片验证码
    1. 调用captcha 扩展包生成图片验证码，name,text, image
    2. 在服务器保存图片验证码内容，在缓存redis数据库中存储
    3. 使用响应对象返回前端图片验证码
    :param image_code_id:
    :return:
    """
    # 生成图片验证码，调用captcha 扩展包
    name, text, image = captcha.generate_captcha()
    # 在服务器redis缓存中存储图片验证码的内容，指定过期时间
    try:
        redis_store.setex('ImageCode_'+ image_code_id, 300, text)
    except Exception as e:
        # 日志记录
        current_app.logger.error(e)
        # jsonify 序列化数据
        return jsonify(statucode.DATABASE_ERROR, errmsg='保存图片验证码失败')
        # 返回前图片验证码，需要使用响应对象
        # finally是无论是否有异常，都会被执行，else如未异常执行
    else:
        response = make_response(image)
        # 设置响应的数据类型
        response.headers['Content-Type'] = 'image/jpg'
        # 返回前端图片验证码
        return response


# 校验图片验证码并发送手机验证码
@user.route('/smscode/', methods=['GET'])
def send_sms_code():
    """
    发送短信：获取参数/校验参数/查询数据/返回结果
    1. 获取参数，查询字符串的参数获取，mobile, text, id, request.args.get('text')
    2. 校验参数，首先校验参数存在
    3. 校验手机号，正则表达式，re.match(r'^1[]$',mobile)
    4. 校验图片验证码：获取本地存储的真实图片验证码
    5. 判断获取结果，如果图片验证码过期结束程序
    6. 删除图片验证码
    7. 比较图片验证码：统一转成小写比较图片验证码内容是否一致
    8. 生成短信码： 使用random 模块随机数
    9. 在本地保存短信验证码内容，判断用户是否已注册
    10. 调用云通讯发送信息： 使用异常进行处理
    11. 保存云通讯的发送结果，判断是否发送成功
    12. 返回前端结果

    :param modile:
    :return:
    """
    phone = request.args.get('phone')
    text = request.args.get('text')
    uuid = request.args.get('id')

    # 校验参数完整性
    if not all([phone, text, uuid]):
        return jsonify(statucode.INFO_IS_NOT_COMPLETE)

    reg = re.match('((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[035-8])|(18[0-9])|166|198|199|(147))\\d{8}', phone)
    # 验证数据有效性
    if not reg:
        return jsonify(statucode.PHONE_NUMBER_IS_INVALID)

    # 验证本地图片验证码
    try:
        image_code = redis_store.get('ImageCode_' + uuid)
    except Exception as e:
        return jsonify(statucode.SELECT_IMAGE_ERROR)
    # 验证图片验证码是否过期或者是否存在
    if not image_code:
        return jsonify(statucode.IMAGE_SAVE_OUT)

    # 比较验证码是否一致
    if image_code.decode('utf-8').lower() != text.lower():
        return jsonify(statucode.IMAGE_CODE_ERROR)

    # 图片验证码只能获取一次，无论是否获取到，都必须删除图片验证码
    try:
        redis_store.delete('ImageCode_' + uuid)
    except Exception as e:
        current_app.logger.error(e)

    # 发送手机验证码
    sms_code = random.randint(100000, 999999)
    try:
        redis_store.setex('SMSCode_' + phone, 300, sms_code)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(statucode.MESAGE_SAVE_DEFATE)
        # 写注册的时候在使用
        # # 判断用户是否已注册
        # try:
        #     user = User.query.filter_by(mobile=mobile).first()
        # except Exception as e:
        #     current_app.logger.error(e)
        #     return jsonify(errno=RET.DBERR,errmsg='查询用户信息异常')
        # else:
        #     # 判断查询结果，用户是否注册
        #     if user is not None:
        #         return jsonify(errno=RET.DATAEXIST, errmsg='手机号已注册')

        # 发送短信，调用云通讯接口
    mesage = "您的验证码是：%s。请不要把验证码泄露给其他人。" % sms_code
    try:
        # 实例化对象
        a = sms.send_sms(mesage, phone)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(statucode.MESAGE_SEND_DEFATE)
        # 判断发送结果
        # if result ==0:
        # 表达式判断，变量写在后面

    return jsonify({'code': statucode.OK, 'msg': statucode.MESAGE_SEND_SUCCESS})


# 注册提交信息然后返回接口的页面
@user.route('/user_register/', methods=['POST'])
def register_count():
    # 提交的所有信息
    # phone = request.form.get('mobile')
    # imagecode = request.form.get('imagecode')
    # phonecode = request.form.get('phonecode')
    # pwd = request.form.get('password')
    # pwd2 = request.form.get('password2')

    data = request.get_json()
    phone = data.get('mobile')
    pwd = data.get('password')
    phonecode = data.get('sms_code')

    # 验证信息完整性
    if not all([phone, phonecode, pwd]):
        msg = '请输入完整信息'
        return jsonify(statucode.INFO_IS_NOT_COMPLETE)

    reg = re.match('((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[035-8])|(18[0-9])|166|198|199|(147))\\d{8}', phone)
    # 验证数据有效性
    if not reg:
        return jsonify(statucode.PHONE_NUMBER_IS_INVALID)

    # 验证用户是否已存在
    if User.query.filter_by(phone=phone).first():
        return jsonify(statucode.USER_EXISTS)

    # 验证图片验证码
    # if not imagecode:
    #     return jsonify(statucode.IMAGE_CODE_ERROR)
    # 验证手机验证码
    phone_code = redis_store.get('SMSCode_' + phone)
    if phonecode != phone_code.decode('utf-8'):
        return jsonify(statucode)

    # 删除数据库中用户的短信信息
    redis_store.delete('SMSCode_' + phone)

    # 保存用户数据到数据库
    user_register = User()
    user_register.name = phone
    user_register.phone = phone
    # 密码加密
    user_register.pw_hash = generate_password_hash(pwd)

    try:
        db.session.add(user_register)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(statucode.DATABASE_ERROR)

    return jsonify(statucode.COUNT_REGISTER_SUCCESS)


# 登录页面展示
@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 登录接口
@user.route('/login/', methods=['POST'])
def user_login():
    data = request.get_json()
    phone = data.get('mobile')
    pwd = data.get('passwd')

    if User.query.filter_by(phone=phone).first():
        a_user = User.query.filter_by(phone=phone).first()
        if check_password_hash(a_user.pw_hash, pwd):
            session['user_id'] = a_user.id
            session['phone'] = phone
            return jsonify(statucode.LOGIN_SUCCESS)
        else:
            return jsonify(statucode.USER_PASSWORD_ERROR)
    else:
        return jsonify(statucode.USER_NOT_EXISTS)


# 退出接口
@user.route('/logout/', methods=['delete'])
def logout():
    session.clear()
    return jsonify({'code': statucode.OK})


# 首页展示
@user.route('/show_index/', methods=['GET'])
def show_index():
    return render_template('index.html')


@user.route('/index/', methods=['GET'])
def index():
    user_id = session.get('user_id')
    if user_id:
        a_user = User.query.filter(User.id == user_id).first()
        data = {
            'id': a_user.id,
            'phone': a_user.phone
        }
        return jsonify({'code': statucode.OK, 'data': data})
        # return render_template('index.html')
    return jsonify()


# 个人中心
@user.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 个人中心接口
@user.route('/my_info/', methods=['GET'])
@is_login
def my_info():
    a_user = User.query.filter_by(id=session['user_id']).first()
    user_image = a_user.avatar if a_user.avatar else 'landlord01.jpg'
    data = {
        'name': a_user.name,
        'mobile': a_user.phone,
        'avatar': '/static/upload/' + user_image
    }
    return jsonify({'code': statucode.OK, 'data': data})


# 修改个人信息
@user.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


# 修改个人信息
@user.route('/profile/', methods=['PUT'])
@is_login
def profile_info():
    data = request.get_json()
    name = data.get('name')

    if User.query.filter_by(name=name).first():
        return jsonify(statucode.USER_EXISTS)

    a_user = User.query.filter_by(id=session.get('user_id')).first()
    a_user.name = name

    try:
        db.session.add(a_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(statucode.DATABASE_ERROR)
    return jsonify({'code': statucode.OK})


# 展示个人信息
@user.route('/show_user_info/', methods=['GET'])
@is_login
def show_user_info():

    if not session['user_id']:
        return jsonify(statucode.USER_NO_LOGIN)
    a_user = User.query.filter_by(id=session['user_id']).first()
    data = {
        'avatar': '/static/upload/' + a_user.avatar,
        'name': a_user.name
    }
    return jsonify({'code': statucode.OK, 'data': data})


# 头像上传
@user.route('/avatar/', methods=['POST'])
@is_login
def avatar():
    file = request.files.get('avatar')
    # 先验证上传的是否是图片文件, 不是图片文件的返回
    if not re.match(r'image/*', file.mimetype):
        return jsonify(statucode.IMAGE_TYPE_ERROR)

    # 保存图片文件
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
    filename = file.filename
    filepath = os.path.join(BASEDIR, 'static/upload', filename)
    file.save(filepath)

    a_user = User.query.filter_by(id=session['user_id']).first()
    a_user.avatar = file.filename

    try:
        db.session.add(a_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(statucode.DATABASE_ERROR)
    data = '/static/upload/' + file.filename
    return jsonify({'code': statucode.OK, 'data': data})


# 实名认证
@user.route('/show_auth/', methods=['GET'])
@is_login
def show_auth():
    return render_template('auth.html')


# 实名认证接口
@user.route('/auth/', methods=['GET'])
@is_login
def auth_():
    a_user = User.query.filter_by(id=session['user_id']).first()
    real_name = a_user.id_name
    id_card = a_user.id_card

    data = {
        'real_name': real_name,
        'id_card': id_card
    }
    return jsonify({'code': statucode.OK, 'data': data})


@user.route('/auth/', methods=['POST'])
@is_login
def auth():
    data = request.get_json()
    real_name = data['real_name']
    id_card = data['id_card']

    a_user = User.query.filter_by(id=session['user_id']).first()
    a_user.id_name = real_name
    a_user.id_card = id_card

    try:
        db.session.add(a_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(statucode.DATABASE_ERROR)

    return jsonify({'code': statucode.OK})

