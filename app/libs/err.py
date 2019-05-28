# -*- encoding: utf-8 -*-
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, there is something wrong.'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        """ Get json body """
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=f'{request.method} {self.get_url_no_param()}'
        )
        return json.dumps(body, ensure_ascii=False)

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')[0]
        return main_path

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]
