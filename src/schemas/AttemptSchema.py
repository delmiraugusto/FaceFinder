from marshmallow import Schema, fields

class AttemptSchema(Schema):
    codigo_uuid = fields.String()
    status = fields.Boolean()
    create_at = fields.DateTime()
    dia = fields.Date()
    hospedes = fields.List(fields.Nested("HospedeSchema"))
    ## falta add documentData