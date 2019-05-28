# -*- encoding: utf-8 -*-
from flask import current_app, g, request
from flask_httpauth import HTTPDigestAuth, HTTPBasicAuth, HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from collections import namedtuple

from app.libs.err_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

token_auth = HTTPTokenAuth()
digest_auth = HTTPDigestAuth()
auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


# @token_auth.verify_token
# def verify_token(token):
#     user_info = verify_auth_token(token)
#     if not user_info:
#         return False
#     else:
#         g.user = user_info
#         return True


@auth.verify_password
def verify_password(token, password):
    # token
    # HTTP 账号密码
    # header  key:value
    # key=Authorization
    # value=basic base64(account:password)
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid')
    except SignatureExpired:
        raise AuthFailed(msg='token is expired')
    uid = data['uid']
    ac_type = data['ac_type']
    scope = data['scope']
    # request 视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)

