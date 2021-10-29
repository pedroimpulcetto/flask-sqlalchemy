from flask import Flask, Blueprint, jsonify
from flask_restx import Api
from ma import ma
from db import db

from resources.competicao import Competicao, CompeticaoList, competicao_ns
from marshmallow import ValidationError

from server.instance import server

api = server.api
app = server.app


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


api.add_resource(Competicao, '/competicao/<int:id>')
api.add_resource(CompeticaoList, '/competicao')

if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    server.run()
