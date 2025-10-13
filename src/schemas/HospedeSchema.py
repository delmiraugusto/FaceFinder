from marshmallow import Schema, fields
from src.schemas.ReservaSchema import ReservaSchema

class HospedeSchema(Schema):
    codigo_uuid = fields.String()
    status = fields.Boolean()
    nome = fields.String()
    ag_uid = fields.String()
    reservas = fields.List(fields.Nested(ReservaSchema))
    attempts = fields.List(fields.Nested(AttemptSchema))