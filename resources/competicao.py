from flask import request
from flask_restx import Resource, fields

from models.competicao import CompeticaoModel
from schemas.competicao import CompeticaoSchema

from server.instance import server

competicao_ns = server.competicao_ns

ITEM_NOT_FOUND = "Competicao não encontrada."
ITEM_NOT_ADD = "Competicao já encerrada"

competicao_schema = CompeticaoSchema()
competicao_list_schema = CompeticaoSchema(many=True)

# Model required by flask_restplus for expect
item = competicao_ns.model('Competicao', {
    'competicao': fields.String('Nome da competicao'),
    'atleta': fields.String('Nome do atleta'),
    'value': fields.String('Pontos do atleta'),
    'unidade': fields.String('Unidade da competicao'),
    'enc': fields.String('0'),
})


class Competicao(Resource):

    def get(self, id):
        competicao_data = CompeticaoModel.find_by_id(id)
        if competicao_data:
            return competicao_schema.dump(competicao_data)
        return {'message': ITEM_NOT_FOUND}, 404

    def delete(self, id):
        competicao_data = CompeticaoModel.find_by_id(id)
        competicao_json = request.get_json()
        if competicao_data:
            competicao_data.atleta = competicao_json['atleta']
            competicao_data.competicao = competicao_json['competicao']
            competicao_data.unidade = competicao_json['unidade']
            competicao_data.value = competicao_json['value']
            competicao_data.enc = "1"
            competicao_data.save_to_db()
            return competicao_schema.dump(competicao_data),
        return {'message': ITEM_NOT_FOUND}, 404

    @competicao_ns.expect(item)
    def put(self, id):
        competicao_data = CompeticaoModel.find_by_id(id)
        competicao_json = request.get_json()

        if competicao_data:
            competicao_data.atleta = competicao_json['atleta']
            competicao_data.competicao = competicao_json['competicao']
            competicao_data.unidade = competicao_json['unidade']
            competicao_data.value = competicao_json['value']
            competicao_data.enc = "0"
        else:
            competicao_data = competicao_schema.load(competicao_json)

        competicao_data.save_to_db()
        return competicao_schema.dump(competicao_data), 200


class CompeticaoList(Resource):
    @competicao_ns.doc('Get all the Items')
    def get(self):
        return competicao_list_schema.dump(CompeticaoModel.find_all()), 200

    @competicao_ns.expect(item)
    @competicao_ns.doc('Create an Item')
    def post(self):
        competicao_data = CompeticaoModel.find_all()
        competicao_json = request.get_json()
        for i in competicao_data:
            if (i.competicao == competicao_json['competicao']):
                if(i.enc != competicao_json['enc']):
                    return {'message': ITEM_NOT_FOUND}, 404
        competicao_data = competicao_schema.load(competicao_json)
        competicao_data.save_to_db()

        return competicao_schema.dump(competicao_data), 201
