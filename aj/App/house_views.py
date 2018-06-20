
from flask import Blueprint, render_template, session, jsonify

from App.models import User, House, Area, Facility

house_blueprint = Blueprint('house', __name__)


# 我的房源页面
@house_blueprint.route('/myhouse/')
def myhouse():
    return render_template('myhouse.html')


# 我的房源接口
@house_blueprint.route('/myhouses/', methods=['GET'])
def my_house():
    user = User.query.filter_by(id=session['user_id']).first()
    return jsonify({'msg': user.to_auth_dict()})


# 新的房源
@house_blueprint.route('/newhouse/')
def newhouse():
    return render_template('newhouse.html')


# 新的房源接口
@house_blueprint.route('/newhouses/', methods=['GET'])
def newhouses():
    houses = House.query.filter_by(user_id=session['user_id'])
    facilitys = Facility.query.all()
    areas = Area.query.all()

    all_facility = [facility.to_dict() for facility in facilitys]
    all_house = [house.to_dict() for house in houses]
    all_area = [area.to_dict() for area in areas]
    return jsonify(all_house=all_house, all_area=all_area, all_facility=all_facility)