from ma import ma
from models.competicao import CompeticaoModel


class CompeticaoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CompeticaoModel
        load_instance = True
