from marshmallow import Schema,fields
from models.shared import StyleModel,StyleSchema


class KullaniciListeAyrintiSchema(Schema):
    id = fields.Int()
    tarih = fields.String()  
    musteriAdi = fields.String()
    ulkeAdi = fields.String()
    temsilciAdi = fields.String()
    teklifOncelik = fields.String()
    goruldu = fields.Boolean()
    style = fields.Nested(StyleSchema)
    sira = fields.Int()
    acil = fields.Boolean()
    

class KullaniciListeAyrintiModel:
    id = None 
    tarih = "" 
    musteriAdi = ""
    ulkeAdi = ""
    temsilciAdi = ""
    teklifOncelik = ""
    goruldu = False
    style = StyleModel
    sira = 0
    acil = False
