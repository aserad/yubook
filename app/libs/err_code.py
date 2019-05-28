# -*- encoding: utf-8 -*-
from app.libs.err import APIException


class Success(APIException):
    code = 201
    msg = 'OK'
    error_code = 0


class ServerError(APIException):
    code = 500
    msg = 'sorry. wo made a mistake (*^ ^*)'
    error_code = 9999


class ClientTypeError(APIException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParamException(APIException):
    code = 400
    msg = 'params is invalid'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 1002


class Forbidden(APIException):
    code = 403
    msg = 'request forbidden'
    error_code = 1003


class NotFound(APIException):
    code = 404
    msg = 'not found'
    error_code = 1004











