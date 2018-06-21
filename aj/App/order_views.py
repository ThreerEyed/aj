from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session

from App.models import House, Order, db
from utils import status_code

order_blueprint = Blueprint('order', __name__)


# 预定
@order_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


# 预定接口
@order_blueprint.route('/bookings/<int:id>/', methods=['GET'])
def bookings(id):
    house = House.query.filter_by(id=id).first()
    return jsonify({'code': '200', 'house': house.to_full_dict()})


@order_blueprint.route('/bookings/<int:id>/', methods=['POST'])
def bookings_post(id):
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    live_time = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    if live_time.days < 0:
        return jsonify(status_code.ORDER_DATE_IS_INVALID)
    house = House.query.filter_by(id=id).first()
    order = Order()
    order.user_id = session['user_id']
    order.house_id = id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = live_time.days
    order.house_price = house.price
    order.amount = live_time.days * house.price

    try:
        order.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify({'code': '200'})


# 我的订单
@order_blueprint.route('/orders/', methods=['GET'])
def orders():
    return render_template('orders.html')


# 租客的所有订单
@order_blueprint.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


# @order_blueprint.route('/lorders/', methods=['GET'])
# def lorders():
#     order = Order.query.filter_by(user_id=session['user_id']).first()
#     return jsonify({'code': '200', 'order': order.to_dict()})


# 房东的所有订单
@order_blueprint.route('/renter_lorders/', methods=['GET'])
def renter_lorders():
    return jsonify({'code': '200'})
