from marshmallow import Schema,fields
from models import SiparisUrunSchema,SiparisUrunModel


class SiparisGirisUrunSchema(SiparisUrunSchema):
    urunAdi = fields.String()
    en = fields.String()
    boy = fields.String()
    kenar = fields.String()
    yuzeyIslem = fields.String()
    m2 = fields.Float()
    mt = fields.Float()
    ton = fields.Float()
    adet = fields.Float()
    miktar = fields.Float()
    newAmountm2 = fields.Float()
    newAmountmt = fields.Float()
    newAmountadet = fields.Float()
    newAmountmiktar = fields.Float()
    isChange = fields.Boolean()
    whatMultiplyM2 = fields.String()
    whatMultiplyAdet = fields.String()
    whatMultiplyMt = fields.String()
    alisFiyatiKontrol = fields.Boolean()
class SiparisGirisUrunModel(SiparisUrunModel):
    urunAdi = ""
    en = ""
    boy = ""
    kenar = ""
    yuzeyIslem = ""
    m2 = 0
    mt = 0
    adet = 0
    ton = 0
    miktar = 0
    newAmountm2 = 0
    newAmountmt = 0
    newAmountadet = 0
    newAmountmiktar = 0
    isChange = False
    whatMultiplyM2 = ""
    whatMultiplyAdet = ""
    whatMultiplyMt = ""
    alisFiyatiKontrol = False
    
    


