from marshmallow import Schema,fields

class MaliyetHatalarModel:
    id = 0
    hata = ""
    maliyet = 0
    kullanici_id = 0
    kullanici_adi = ""
    tarih = ""

class MaliyetHatalarSchema(Schema):
    id = fields.Int()
    hata = fields.String()
    maliyet = fields.Float()
    kullanici_id = fields.Int()
    kullanici_adi = fields.String()
    tarih = fields.String()
    
class KullaniciSchema(Schema):
    id = fields.Int()
    name = fields.String()
    
class KullaniciModel:
    id = 0
    name = ""