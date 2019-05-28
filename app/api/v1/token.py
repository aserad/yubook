# -*- encoding: utf-8 -*-
import json

from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    # 验证账户密码，获取用户id
    identity = promise[form.type.data](form.account.data, form.secret.data)
    # 生成token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t), 201
    # return json.dumps(t, ensure_ascii=False), 201


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """
    ac_type
    :param uid: 用户id
    :param ac_type: 客户端类型
    :param scope:
    :param expiration: 有效期 默认7200秒
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'ac_type': ac_type.value,
        'scope': scope,
    })
