
from marshmallow import Schema,fields

class KasaOlcuDetaylariSchema(Schema):
    id = fields.Int()
    ebat = fields.String()
    tedarikci = fields.Int()
    tedarikci_adi = fields.String()
    kasa_olculeri = fields.String()
    adet = fields.Int()
    
class KasaOlcuDetaylariModel:
    id = 0
    ebat = ""
    tedarikci = 0
    tedarikci_adi = ""
    kasa_olculeri = ""
    adet = 0