from flask import Blueprint, render_template

order_blueprint = Blueprint('order', __name__)


# 展示订单
@order_blueprint.route('/show_lorders/', methods=['GET'])
def show_lorders():
    return render_template('lorders.html')

