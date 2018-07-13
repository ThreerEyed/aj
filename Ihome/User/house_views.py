from flask import Blueprint, render_template

house = Blueprint('house', __name__)


# 展示我的房源
@house.route('/myhouse/', methods=['GET'])
def show_house():
    return render_template('myhouse.html')



