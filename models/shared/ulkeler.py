from marshmallow import Schema,fields


class UlkelerSchema(Schema):
    id = fields.Int()
    ulkeAdi = fields.String()
    logo = fields.String()
    path = fields.String()
class UlkelerModel:
    id = None
    ulkeAdi = ""
    logo = ""
    path = '/assets/layout/images/country-logo/'