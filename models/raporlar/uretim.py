from marshmallow import Schema,fields



class UretimSchema(Schema): 

    id = fields.Int()
    tarih = fields.String()
    kimden = fields.String()
    kategori = fields.String()
    kasano = fields.Int()
    urunadi = fields.String()
    ocakadi = fields.String()
    yuzeyadi = fields.String()
    en = fields.String()
    boy = fields.String()
    kenar = fields.String()
    adet = fields.Float()
    miktar = fields.Float()
    birimadi = fields.String()
    siparisno = fields.String()
    urunKartID = fields.String()
    aciklama = fields.String()
    kutuiciadet = fields.Int()

class UretimModel:

    id = None
    tarih = ""
    kimden = ""
    kategori = ""
    kasano = 0
    urunadi = ""
    ocakadi = ""
    yuzeyadi = ""
    en = ""
    boy = ""
    kenar = ""
    adet = 0
    miktar = 0
    birimadi = ""
    siparisno = ""
    urunKartID=0
    aciklama=""
    kutuiciadet = 0