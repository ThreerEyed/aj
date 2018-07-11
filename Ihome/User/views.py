import re
from flask import render_template, Blueprint, request, jsonify, redirect, url_for

from utils import statucode

user = Blueprint('user', __name__)


# 注册显示页面
@user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 注册提交信息然后返回借口的页面
@user.route('/register/', methods=['POST'])
def register_count():
    # 提交的所有信息
    phone = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    phonecode = request.form.get('phonecode')
    pwd = request.form.get('password')
    pwd2 = request.form.get('password2')

    # 验证信息完整性
    if not all([phone, imagecode, phonecode, pwd, pwd2]):
        return jsonify({'code': 200, 'msg': '请输入完整信息'})

    reg = re.match('((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[035-8])|(18[0-9])|166|198|199|(147))\\d{8}', phone)
    # 验证数据有效性
    if not reg:
        return jsonify(statucode.PHONE_NUMBER_IS_INVALID)
    # 验证图片验证码
    # 验证手机验证码
    # 验证密码是否一致
    return redirect(url_for('user.login'))


@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')



