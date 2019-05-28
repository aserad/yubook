# -*- encoding: utf-8 -*-
from flask import request
from wtforms import Form

from app.libs.err_code import ParamException


class BaseForm(Form):

    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super().__init__(data=data, **args)

    def validate_for_api(self):
        valid = super().validate()
        if not valid:
            # form errors
            raise ParamException(msg=self.errors)
        return self
