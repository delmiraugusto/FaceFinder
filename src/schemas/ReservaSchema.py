from marshmallow import Schema, fields
from src.schemas.HospedeSchema import HospedeSchema

class ReservaSchema(Schema):
    codigo_uuid = fields.String()
    status = fields.Boolean()
    hospedes = fields.List(fields.Nested(HospedeSchema))
