from marshmallow import Schema,fields

class SiparisCekiSchema(Schema):
    id = fields.Int()
    sira = fields.Int()
    tedarikciAdi = fields.String()
    kategoriAdi = fields.String()
    kasaNo = fields.Int()
    yuzeyIslem = fields.String()
    urunAdi = fields.String()
    kenar = fields.String()
    en = fields.String()
    boy = fields.String()
    adet = fields.Float()
    miktar = fields.Float()
    birimAdi = fields.String()
    kutuAdet = fields.Int()
    urunKart = fields.Int()
    tonaj = fields.Float()

class SiparisCekiModel:
    id = None
    sira = 0
    tedarikciAdi = ""
    kategoriAdi = ""
    kasaNo = 0
    yuzeyIslem = ""
    urunAdi = ""
    kenar = ""
    en = ""
    boy = ""
    adet = 0
    miktar = 0
    birimAdi = ""
    kutuAdet = 0
    urunKart = 0
    tonaj = 0