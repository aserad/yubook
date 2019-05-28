# -*- encoding: utf-8 -*-
from flask import Blueprint, jsonify
from sqlalchemy import or_, and_

from app.libs.redprint import Redprint
from app.models.book import Book
from app.validators.forms import BookSearchForm

api = Redprint('book')


@api.route('')
def search_book():
    # url   http://localhost:5000/v1/book?q={}
    form = BookSearchForm().validate_for_api()
    q = '%' + form.q.data + '%'
    books = Book.query.filter(and_(
        or_(Book.title.like(q), Book.author.like(q), Book.publisher.like(q)),
        Book.status == 0
    )).all()
    return jsonify(books)


@api.route('/<int:isbn>', methods=['GET'])
def book_detail(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return jsonify(book)


