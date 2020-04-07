"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException


class TodoListNotFound(APIException):
    code = 404  # http状态码
    msg = '没有找到相关数据'  # 异常信息
    error_code = 80010  # 约定的异常码

    
class RefreshException(APIException):
    code = 401
    msg = "refresh token 获取失败"
    error_code = 10100
