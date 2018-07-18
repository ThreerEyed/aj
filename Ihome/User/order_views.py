from flask import Blueprint, render_template, jsonify, session, request

from User.models import Order

order_blueprint = Blueprint('order', __name__)


# 预定页面
@order_blueprint.route('/booking/', methods=['GET'])
def show_booking():
    return render_template('booking.html')


# 展示订单
@order_blueprint.route('/show_lorders/', methods=['GET'])
def show_lorders():
    return render_template('lorders.html')


# 客户订单接口
@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    """
    需要返回的值
    1. data.orders
    :return:
    """
    orders = Order.query.filter(Order.user_id != session.get('user_id')).all()
    return jsonify

