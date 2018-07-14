
# 注册状态码
OK = 200
INFO_IS_NOT_COMPLETE = {'code': 1001, 'msg': '信息不完整'}
PHONE_NUMBER_IS_INVALID = {'code': 1002, 'msg': '手机号格式不正确'}
PASSWORD_ERROR = {'code': 1003, 'msg': '密码不一致'}
SELECT_IMAGE_ERROR = {'code': 1004, 'msg': '查询图片异常'}
IMAGE_SAVE_OUT = {'code': 1005, 'msg': '验证码已过期'}
IMAGE_CODE_ERROR = {'code': 1006, 'msg': '图片验证码输入错误'}
MESAGE_SAVE_DEFATE = {'code': 1007, 'msg': '短信保存失败'}
MESAGE_SEND_DEFATE = {'code': 1008, 'msg': '短信发送失败'}
MESAGE_SEND_SUCCESS = {'code': 1009, 'msg': '短信发送成功'}
PHONE_CODE_ERROR = {'code': 1010, 'msg': '短信验证码错误'}
USER_EXISTS = {'code': 1011, 'msg': '该用户已存在'}

USER_NOT_EXISTS = {'code': 1012, 'msg': '该用户不存在'}
USER_PASSWORD_ERROR = {'code': 1013, 'msg': '用户账号或密码错误'}
LOGIN_SUCCESS = {'code': 1014, 'msg': '登录成功'}

USER_NO_LOGIN = {'code': 1015, 'msg': '用户未登录'}

COUNT_REGISTER_SUCCESS = {'code': 200, 'msg': '账号注册成功，即将自动跳转登录页面'}


# 数据库错误
DATABASE_ERROR = {'code': 0, 'msg': '数据库错误'}

# 修改个人信息
IMAGE_TYPE_ERROR = {'code': 1101, 'msg': '图片格式错误'}


# 房屋相关状态码
PARAMERR = {'code': 1201, 'msg': '参数错误'}
PARAMERR_MISS = {'code': 1202, 'msg': '参数丢失'}
PRICE_ERROR = {'code': 1203, 'msg': '价格不正常'}
SELECT_FACILITY_ERROR = {'code': 1204, 'msg': '查询设施错误'}

HOUSE_EXISTS = {'code': 1205, 'msg': '房源已经存在'}


