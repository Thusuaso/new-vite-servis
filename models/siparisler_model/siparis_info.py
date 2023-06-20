from marshmallow import Schema,fields

class SatisciInfoSchema(Schema):
    id = fields.Int()
    po = fields.String()
    satisci_id = fields.Int()
    satisci_adi = fields.String()
    operasyon_id = fields.Int()
    operasyon_adi = fields.String()
    
class SatisciInfoModel:
    id = 0
    po = ""
    satisci_id = ""
    satisci_adi = ""
    operasyon_id = 0
    operasyon_adi = ""
    
class SatisciInfoOzetSchema(Schema):
    ad = fields.String()
    adet = fields.Int()
    
class SatisciInfoOzetModel:
    ad = ""
    adet = 0