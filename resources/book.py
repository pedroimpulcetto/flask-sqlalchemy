from flask import request
from flask_restplus import Resource, fields

from models.book import BookModel
from schemas.book import BookSchema

from server.instance import server

book_ns = server.book_ns

ITEM_NOT_FOUND = "Book not found."


book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

# Model required by flask_restplus for expect
item = book_ns.model('Book', {
    'title': fields.String('Book title'),
    'pages': fields.Integer(0),
})


class Book(Resource):

    def get(self, id):
        book_data = BookModel.find_by_id(id)
        if book_data:
            return book_schema.dump(book_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        book_data = BookModel.find_by_id(id)
        if book_data:
            book_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}, 404

    @book_ns.expect(item)
    def put(self, id):
        book_data = BookModel.find_by_id(id)
        book_json = request.get_json()

        if book_data:
            book_data.pages = book_json['pages']
            book_data.title = book_json['title']
        else:
            book_data = book_schema.load(book_json)

        book_data.save_to_db()
        return book_schema.dump(book_data), 200


class BookList(Resource):
    @book_ns.doc('Get all the Items')
    def get(self):
        return book_list_schema.dump(BookModel.find_all()), 200

    @book_ns.expect(item)
    @book_ns.doc('Create an Item')
    def post(self):
        book_json = request.get_json()
        book_data = book_schema.load(book_json)

        book_data.save_to_db()

        return book_schema.dump(book_data), 201
