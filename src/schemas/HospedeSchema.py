from marshmallow import Schema, fields

class HospedeSchema(Schema):
    codigo_uuid = fields.String(dump_only=True)
    status = fields.Boolean()
    nome = fields.String()
    ag_uid = fields.String()
    reservas = fields.List(fields.Nested("ReservaSchema"))
    attempts = fields.List(fields.Nested("AttemptSchema"))