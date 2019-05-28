# -*- encoding: utf-8 -*-
import json

from app.libs.enums import ClientTypeEnum
from app.libs.err_code import ClientTypeError, Success
from app.libs.redprint import Redprint
from flask import request
from werkzeug.exceptions import HTTPException
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    # 如果初始化Form时传递的是json类型的数据，一定要用关键字参数data=
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)

