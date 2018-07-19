from flask import Blueprint, render_template, jsonify, session, request

from User.models import Order, db
from utils import statucode

order_blueprint = Blueprint('order', __name__)


# 预定页面
@order_blueprint.route('/booking/', methods=['GET'])
def show_booking():
    return render_template('booking.html')


# 展示客户订单
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
    data = {
        'orders': [order.to_dict() for order in orders]
    }
    return jsonify({'code': 200, 'data': data})


# 客户订单处理接口(接受订单)
@order_blueprint.route('/deal_order/<int:orderId>/status', methods=['PUT'])
def deal_order(orderId):
    order = Order.query.filter(Order.id == orderId).first()
    status = request.get_json()
    upgrade_status = status.get('action')
    reject_comment = status.get('reason')
    order.status = upgrade_status
    order.comment = reject_comment
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(statucode.DATABASE_ERROR)

    return jsonify({'code': statucode.OK})


# 展示我的订单 展示user订单
@order_blueprint.route('/show_order/', methods=['GET'])
def show_order():
    return render_template('orders.html')



