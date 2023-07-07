from marshmallow import Schema,fields


class MusteriAyrintiSchema(Schema):

    id = fields.Int()
    musteriadi = fields.String()
    musteri_id = fields.Int()
    siparisno = fields.String()
    yuklemetarihi = fields.String()
    tip = fields.String()
    toplam = fields.Float()
    kalan = fields.Float()
    vade = fields.String()
    pesinat = fields.Float()
    siparis_total = fields.Float()
    odenen_tutar = fields.Float()
    tahmini_eta = fields.String()
    kalan2 = fields.Float()
class MusteriAyrintiModel:
    id = None
    musteriadi = ""
    musteri_id = None
    siparisno = ""
    yuklemetarihi = ""
    tip = ""
    toplam = 0
    kalan = 0
    vade = ""
    pesinat = 0
    siparis_total = 0
    odenen_tutar = 0
    tahmini_eta = ""
    kalan2 = 0
    
class ByCustomersPoSchema(Schema):
    id = fields.Int()
    siparisNo = fields.String()

class ByCustomersPoModel:
    id = 0
    siparisNo = ""