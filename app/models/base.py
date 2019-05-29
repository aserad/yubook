# -*- encoding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer, DateTime
from contextlib import contextmanager
from datetime import datetime

from app.libs.err_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    # 继承 SQLAlchemy 类， 添加一个上下文管理器，可以自动提交对数据库的修改
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    # 重写 filter_by 方法， 给每个 filter_by 都添加了 status=0 的条件
    def filter_by(self, **kwargs):
        if 'status' not in kwargs:
            kwargs['status'] = 0
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True  # 不要创建base表
    status = Column(SmallInteger, default=0)  # 表示记录删除的flag，1表示删除
    create_time = Column('create_time', DateTime, default=datetime.now)   # 需要测试如果使用 default=datetime.now 而不使用 __init__会怎样

    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)

    # @property
    # def create_datetime(self):
    #     if self.create_time:
    #         return datetime.fromtimestamp(self.create_time)
    #     else:
    #         return None

    def delete(self):
        self.status = 1

    def __getitem__(self, item):   # 为了能够通过 o['name']的方式访问对象的属性而添加的方法
        return getattr(self, item)

    def keys(self):
        return self.fields

    def hide(self, *args):
        for field in args:
            if field in self.fields:
                self.fields.remove(field)
        return self

    def append(self, *args):
        for field in args:
            if field not in self.fields:
                self.fields.append(field)
        return self
