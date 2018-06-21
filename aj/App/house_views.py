import re
import os

from flask import Blueprint, render_template, session, jsonify, request
from werkzeug.utils import secure_filename

from App.models import User, House, Area, Facility, db, HouseImage
from utils import status_code

house_blueprint = Blueprint('house', __name__)


# 我的房源页面
@house_blueprint.route('/myhouse/')
def myhouse():
    return render_template('myhouse.html')


# 我的房源接口
@house_blueprint.route('/myhouses/', methods=['GET'])
def my_house():
    user = User.query.filter_by(id=session['user_id']).first()
    houses = House.query.filter_by(user_id=session['user_id']).all()
    all_house = [house.to_dict() for house in houses]
    return jsonify({'code': '200', 'user': user.to_auth_dict(), 'houses': all_house})


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


# 房源接收借口
@house_blueprint.route('/newhouses/', methods=['POST'])
def newhouses_post():
    params = request.form.to_dict()
    facility_ids = request.form.getlist('facility')
    # 用户id
    user_id = session['user_id']
    # 房间标题
    house_title = params.get('title')
    # 房间价格
    house_price = params.get('price')
    # 所在城区
    area_id = params.get('area_id')
    # 房间地址
    house_address = params.get('address')
    # 房间数量
    house_room_count = params.get('room_count')
    # 房屋面积
    house_acreage = params.get('acreage')
    # 户型描述
    house_unit = params.get('unit')
    # 适宜人数
    house_capacity = params.get('capacity')
    # 卧床配置
    house_beds = params.get('beds')
    # 押金数额
    house_deposit = params.get('deposit')
    # 最少入住天数
    house_min_days = params.get('min_days')
    # 最多入住天数
    house_max_days = params.get('max_days')
    # 配套设施
    facility = params.get('facility')

    houses = House()
    houses.user_id = user_id
    houses.area_id = area_id
    houses.title = house_title
    houses.price = house_price
    houses.address = house_address
    houses.room_count = house_room_count
    houses.acreage = house_acreage
    houses.unit = house_unit
    houses.capacity = house_capacity
    houses.beds = house_beds
    houses.deposit = house_deposit
    houses.min_days = house_min_days
    houses.max_days = house_max_days
    houses.max_days = house_max_days

    if facility_ids:
        facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        houses.facilities = facility_list

    try:
        houses.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify({'code': '200', 'msg': houses.id})


@house_blueprint.route('/house_img/', methods=['POST'])
def house_img():
    # 图片上传
    house_id = request.form.get('house_id')
    file = request.files.get('house_image')
    # 校验图片的正确性
    reg = re.match(r'image/.*', file.mimetype)
    if not reg:
        return jsonify(status_code.USER_IMAGE_ERROR)

    # 保存图片
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(BASE_DIR, 'static/house_image', secure_filename(file.filename))
    file.save(file_path)

    house_image = HouseImage()
    house_image.url = '/static/house_image/' + file.filename
    image_path = '/static/house_image/' + file.filename
    house_image.house_id = house_id
    try:
        house_image.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    house = House.query.filter_by(id=house_id).first()
    if not house.index_image_url:
        index_image_url = image_path
        house.index_image_url = index_image_url
        db.session.add(house)
        db.session.commit()

    return jsonify({'code': '200', 'image_url': image_path})


# 房屋详情
@house_blueprint.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


# 房屋详情接口
@house_blueprint.route('/details/<int:id>/', methods=['GET'])
def detailes(id):
    house = House.query.filter_by(id=id).first()
    user = User.query.filter_by(id=session['user_id']).first()
    return jsonify({'code': '200', 'house': house.to_full_dict(), 'user': user.to_basic_dict()})


