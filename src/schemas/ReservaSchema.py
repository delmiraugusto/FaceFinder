from marshmallow import Schema, fields

class ReservaSchema(Schema):
    codigo_uuid = fields.String()
    status = fields.Boolean()
    hospedes = fields.List(fields.Nested("HospedeSchema"))
