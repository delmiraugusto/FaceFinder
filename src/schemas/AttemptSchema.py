from marshmallow import Schema, fields
from src.schemas.HospedeSchema import HospedeSchema

class AttemptSchema(Schema):
    codigo_uuid = fields.String()
    status = fields.Boolean()
    create_at = fields.DateTime()
    hospedes = fields.List(fields.Nested(HospedeSchema))
    ## falta add documentData