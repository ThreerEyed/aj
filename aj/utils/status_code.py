
OK = {'code': '200', 'msg': '请求成功'}

# 数据库错误
DATABASE_ERROR = {'code': '0', 'msg': '数据库错误'}

# 用户模块1000 <= code <= 1100
# 注册
USER_REGISTER_DATA_NOT_NONE = {'code': '1001', 'msg': '请填写完所有参数'}
USER_REGISTER_MOBILE_ERROR = {'code': '1002', 'msg': '手机号码格式不正确'}
USER_REGISTER_PASSWORD_IS_NOT_VALID = {'code': '1003', 'msg': '两次密码输入不一致'}
USER_EXISTS = {'code': '1004', 'msg': '该用户已存在请登录'}
USER_PASSWORD_ERROR = {'code': '1005', 'msg': '用户名或密码错误'}
USER_NO_USER = {'code': '1006', 'msg': '没有此用户'}
USER_IMAGE_ERROR = {'code': '1007', 'msg': '上传图片格式不正确'}
USER_NAME_EXISTS = {'code': '1008', 'msg': '该用户名已存在'}

USER_AUTH_DATA_IS_NULL = {'code': '1009', 'msg': '实名认证不能为空'}
USER_AUTH_ID_CARD_IS_INVALID = {'code': '1010', 'msg': '身份证号码无效'}

USER_NOT_LOGIN_ERROR = {'code': '1011', 'msg': '没有找到该用户或未登陆'}


# 订单
ORDER_DATE_IS_INVALID = {'code': '1201', 'msg': '无效的日期'}
