import random
import re

import redis as redis
from flask import render_template, Blueprint, request, jsonify, redirect, url_for, current_app, make_response
from werkzeug.security import generate_password_hash

from User.models import User, db
from utils import statucode
from utils.captcha import sms
from utils.captcha.captcha import captcha

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
    phone = request.args.get('mobile')
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

    # 图片验证码只能获取一次，无论是否获取到，都必须删除图片验证码
    try:
        redis_store.delete('ImageCode_' + uuid)
    except Exception as e:
        current_app.logger.error(e)

    # 比较验证码是否一致
    if image_code.lower() != text.lower():
        return jsonify({'code': 200, 'msg': statucode.IMAGE_CODE_ERROR})

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
        result = sms.send_sms(phone, mesage)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(statucode.MESAGE_SEND_DEFATE)
        # 判断发送结果
        # if result ==0:
        # 表达式判断，变量写在后面
    if 0 == result:
        return jsonify({'code': 200, 'msg': statucode.MESAGE_SEND_SUCCESS})


# 注册提交信息然后返回接口的页面
@user.route('/registers/', methods=['POST'])
def register_count():
    # 提交的所有信息
    phone = request.form.get('mobile')
    # imagecode = request.form.get('imagecode')
    # phonecode = request.form.get('phonecode')
    pwd = request.form.get('password')
    pwd2 = request.form.get('password2')

    # 验证信息完整性
    if not all([phone, pwd, pwd2]):
        msg = '请输入完整信息'
        return jsonify(statucode.INFO_IS_NOT_COMPLETE)

    reg = re.match('((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[035-8])|(18[0-9])|166|198|199|(147))\\d{8}', phone)
    # 验证数据有效性
    if not reg:
        msg = '请输入正确的手机号码'
        return jsonify(statucode.PHONE_NUMBER_IS_INVALID)
    # 验证图片验证码
    # 验证手机验证码
    # 验证密码是否一致
    if pwd != pwd2:
        msg = '两次密码输入不一致'
        return jsonify(statucode.PASSWORD_ERROR)

    # 保存数据到数据库
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

    return redirect(url_for('user.login', user=user_register))


@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')



