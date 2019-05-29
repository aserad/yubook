# -*- encoding: utf-8 -*-
import uuid
from datetime import date, datetime

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from app.libs.err_code import ServerError


# 使用jsonify做序列化时用到的
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, uuid.UUID):
            return str(o)
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder  # 使用自己定义的 JSONEncoder 代替flask自带的 JSONEncoder









