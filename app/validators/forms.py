# -*- encoding: utf-8 -*-

from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='账户名不能为空'), Length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
            self.type.data = client
        except ValueError as e:
            print(e)
            raise e


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='not a valid email')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_!@#$%^&*?]{6,18}$', message='密码不符合要求')])
    nickname = StringField(validators=[DataRequired(), Length(min=2, max=22)])    # DataRequired 不加括号会报错

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('该邮箱已经被注册')


class BookSearchForm(BaseForm):
    q = StringField()
