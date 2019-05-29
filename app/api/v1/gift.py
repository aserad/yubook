# -*- encoding: utf-8 -*-
from flask import g, jsonify
from sqlalchemy import desc

from app.libs.err_code import Success, DuplicateGift
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.book import Book
from app.models.gift import Gift
from app.models.wish import Wish

api = Redprint('gift')


@api.route('/book/<int:isbn>', methods=['POST'])
@auth.login_required
def create_gift(isbn):
    uid = g.user.uid
    with db.auto_commit():
        Book.query.filter_by(isbn=isbn).first_or_404()
        gift = Gift.query.filter_by(isbn=isbn, uid=uid, launched=False).first()
        wish = Wish.query.filter_by(isbn=isbn, uid=uid, launched=False).first()
        if gift or wish:
            raise DuplicateGift()
        gift = Gift()
        gift.isbn = isbn
        gift.uid = uid
        db.session.add(gift)
    return Success(code=201)


@api.route('/user', methods=['GET'])
@auth.login_required
def my_gifts():
    uid = g.user.uid
    gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
    return jsonify(gifts)


@api.route('/book/<int:isbn>', methods=['DELETE'])
@auth.login_required
def delete_gifts(isbn):
    uid = g.user.uid
    gift = Gift.query.filter_by(isbn=isbn, uid=uid, launched=False).first()
    with db.auto_commit():
        gift.delete()
    return Success(error_code=204)

