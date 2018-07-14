import os

from flask import Blueprint, render_template, session, request, current_app
from flask.json import jsonify

from User.models import User, Area, Facility, House, db, HouseImage
from utils import statucode

house = Blueprint('house', __name__)


# 展示我的房源
@house.route('/myhouse/', methods=['GET'])
def show_house():
    return render_template('myhouse.html')


# 验证是否实名
@house.route('/check_auth/', methods=['GET'])
def check_auth():
    a_user = User.query.filter_by(id=session.get('user_id')).first()

    data = {
        'real_name': a_user.id_name,
        'id_card': a_user.id_card
    }
    return jsonify({'code': statucode.OK, 'data': data})


# 发布新房源展示页面
@house.route('/show_newhouse/', methods=['GET'])
def show_newhouse():
    return render_template('newhouse.html')


# 返回我的房源的接口
@house.route('/houses/', methods=['GET'])
def show_houses():
    houses = House.query.filter(House.user_id == session.get('user_id')).all()
    house_info = [house.to_full_dict() for house in houses] if houses else ''

    data = {
        'houses': house_info
    }
    return jsonify({'code': statucode.OK, 'data': data})


# 返回房屋区域和房源设施的信息
@house.route('/house_area_facilities/', methods=['GET'])
def areas():
    areas = Area.query.all()
    facilities = Facility.query.all()

    data = {
        'areas': [area.to_dict() for area in areas],
        'facilities': [facility.to_dict() for facility in facilities]
    }
    return jsonify({'code': statucode.OK, 'data': data})


# 发布新房源借口
@house.route('/release_house/', methods=['POST'])
def release_house():
    """
        发布新房屋:获取参数、校验参数、查询数据、返回结果
        1. 获取参数，user_id = g.user_id, 获取post请求的房屋数据
        2. 验证参数的存在
        3. 获取详细的参数信息，主要包括房屋的基本字段
        4. 对参数的校验，对价格进行单位转换，由元转成分
        5. 保存房屋数据，构造模型类对象，存储房屋的基本信息，db.session.add(house)
        6. 尝试获取配套设施信息，如果有数据，对设施进行过滤操作
        7. 存储配套设施信息，house.facilities = facilities
        8. 提交数据到数据库
        9. 返回结果，需要返回房屋id
        :return:
        """
    # 获取参数user_id, 房屋基本数据
    user_id = session.get('user_id')
    # 存储房屋数据post请求的参数
    house_data = request.get_json()
    # 检验参数的存在
    if not house_data:
        return jsonify(statucode.PARAMERR)
    # 获取详细的房屋参数信息
    # 房屋标题
    title = house_data.get('title')
    # 房屋价格
    price = house_data.get('price')
    # 房屋区域
    area_id = house_data.get('area_id')
    # 房屋地址
    address = house_data.get('address')
    # 房间数目
    room_count = house_data.get('room_count')
    # 房屋面积
    acreage = house_data.get('acreage')
    # 房屋户型
    unit = house_data.get('unit')
    # 房屋适住人数
    capacity = house_data.get('capacity')
    # 房屋卧床配置
    beds = house_data.get('beds')
    # 房屋押金
    deposit = house_data.get('deposit')
    # 最小入住天数
    min_days = house_data.get('min_days')
    # 最大入住天数
    max_days = house_data.get('max_days')
    # 校验参数的完整性
    if not all(
            [title, price, area_id, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(statucode.PARAMERR_MISS)
    # 对参数处理，转换价格单位，前端使用元为单位，后端数据库中存储的是分为单位，所以需要转换单位
    try:
        price = int(float(price) * 100)
        deposit = int(float(deposit) * 100)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(statucode.PRICE_ERROR)
    # 先保存房屋基本信息
    house = House()
    house.title = title
    house.user_id = user_id
    house.area_id = area_id
    house.price = price
    house.address = address
    house.room_count = room_count
    house.deposit = deposit
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.acreage = acreage
    house.min_days = min_days
    house.max_days = max_days
    # 处理房屋配套设施，尝试获取配套设施的参数信息
    facility = house_data.get('facility')
    # 判断配置设施存在
    if facility:
        # 过滤配套设施标号，in_判断用户传入的设施编号在模型类中存在
        try:
            facilities = Facility.query.filter(Facility.id.in_(facility)).all()
            # 保存房屋设施信息
            house.facilities = facilities
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(statucode.SELECT_FACILITY_ERROR)

    # 提交数据到数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        # 提交数据发生异常需要进行回滚
        db.session.rollback()
        return jsonify(statucode.DATABASE_ERROR)
    # 返回结果
    return jsonify(code=statucode.OK, errmsg='OK', data={'house_id': house.id})


# 接收房屋图片接口
@house.route('/house_images/', methods=['POST'])
def house_images():
    """
    保存房屋图片
    1. 获取参数，获取用户上传的房屋图片request.files.get('house_image')
    2. 通过house_id,保存房屋图片，查询数据库确定房屋存在
    3. 校验查询结果
    4. 读取图片数据
    5. 调用七牛云接口，上传房屋图片
    6. 保存房屋图片，house_image = HouseImage()
    7. 保存房屋图片到房屋表，主图片设置判断
    8. 提交数据到数据库，如果发生异常需要进行回滚
    9. 拼接路径，返回前端图片url
    :return:
    """
    house_id = request.form.get('house_id')
    file = request.files.get('house_image')
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
    filename = file.filename
    filepath = os.path.join(BASEDIR, 'static/images', filename)
    file.save(filepath)
    # 判断该房源是否存在
    if HouseImage.query.filter(HouseImage.house_id == house_id).first():
        return jsonify(statucode.HOUSE_EXISTS)

    # 实例化对象并保存图片
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = filepath

    a_house = House.query.filter(House.id == house_id).first()

    # 给房屋设置首图用于展示
    if not a_house.index_image_url:
        a_house.index_image_url = '/static/images/' + file.filename

    # 将上传的房屋相关的图片上传到数据库
    db.session.add(a_house)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # 返回数据库出错的原因
        return jsonify(statucode.DATABASE_ERROR)

    return jsonify({'code': 200, 'url': '/static/images/' + filename})


