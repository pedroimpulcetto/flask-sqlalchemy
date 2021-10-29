from db import db
from typing import List
from flask_sqlalchemy import desc


class CompeticaoModel(db.Model):
    __tablename__ = "competicoes"

    id = db.Column(db.Integer, primary_key=True)
    competicao = db.Column(db.String(80), nullable=False)
    atleta = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=False)
    unidade = db.Column(db.String(80), nullable=False)
    enc = db.Column(db.String(80), nullable=False)

    def __init__(self, competicao, atleta,value,unidade,enc):
        self.competicao = competicao
        self.atleta = atleta
        self.value = value
        self.unidade = unidade
        self.enc = enc

    def __repr__(self):
        return f'CompeticaoModel(competicao={self.competicao}, atleta={self.atleta},value={self.value}, unidade={self.unidade}, enc={self.enc})'

    def json(self):
        return {'competicao': self.competicao, 'atleta': self.atleta ,'value': self.value, 'unidade': self.unidade, 'enc': self.enc}

    @classmethod
    def filter_by_ranking(cls, value) -> "CompeticaoModel":
        return cls.query.order_by(desc(value)).all()

    @classmethod
    def find_by_competicao(cls, competicao) -> "CompeticaoModel":
        return cls.query.filter_by(competicao=competicao).first()

    @classmethod
    def find_by_id(cls, _id) -> "CompeticaoModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["CompeticaoModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
