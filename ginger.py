# -*- encoding: utf-8 -*-
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.err import APIException
from app.libs.err_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    # APIException
    # HTTPException
    # Exception
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # log 自己添加
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    print(app.url_map)
    app.run()
