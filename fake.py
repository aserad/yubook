# -*- encoding: utf-8 -*-
from app import create_app
from app.models.user import User
from app.models.base import db

app = create_app()
with app.app_context():
    with db.auto_commit():
        user = User()
        user.nickname = 'admin'
        user.password = 'abcd1234'
        user.email = '999@qq.com'
        user.auth = 2
        db.session.add(user)
