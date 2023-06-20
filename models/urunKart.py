from marshmallow import Schema,fields
from models.kategori import KategoriModel,KategoriSchema
from models.olculer import OlculerModel,OlculerSchema
from models.urunler import UrunlerSchema,UrunlerModel
from models.yuzeyKenar import YuzeyKenarModel,YuzeyKenarSchema

class UrunKartSchema(Schema):
    id = fields.Int()
    urunId = fields.Int()
    yuzeyId = fields.Int() 
    olcuId = fields.Int()
    kategoriId = fields.Int() 
    kullaniciId = fields.Int()
    kg = fields.Float()
    m2 = fields.Float()
    #custom alanlar
    urunAdi = fields.String()
    kategoriAdi = fields.String()
    en = fields.String()
    boy = fields.String()
    kenar = fields.String()
    yuzeyIslem = fields.String()
    yuzey_1 = fields.String()
    yuzey_2 = fields.String()
    yuzey_3 = fields.String()
    ebat = fields.String()
    username = fields.String()
    sira = fields.Int()
    

class UrunKartModel:

    id = None
    urunId = None
    yuzeyId = None
    olcuId = None
    kategoriId = None
    kullaniciId = None
    kg = 0
    m2 = 0
    #custom alanlar
    urunAdi = ""
    kategoriAdi = ""
    en = ""
    boy = ""
    kenar = ""
    yuzeyIslem = ""
    yuzey_1 = ""
    yuzey_2 = ""
    yuzey_3 = ""
    username = ""
    sira = 0
    
class UrunKartMusteriSatisSchema(Schema):
    id = fields.Int() 
    musteriAdi = fields.String()
    siparisNo = fields.String() 
    satisFiyati = fields.Float() 
    miktar = fields.Float() 
    tarih = fields.String() 

class UrunKartMusteriSatisModel:
    id = None 
    musteriAdi = ""
    siparisNo = ""
    satisFiyati = 0 
    miktar = 0 
    tarih = ""



class UrunKartListeSchema(UrunKartSchema):
    kategoriList = fields.Nested(KategoriSchema(many=True))
    urunList = fields.Nested(UrunlerSchema(many=True))
    olcuList = fields.Nested(OlculerSchema(many=True))
    yuzeyList = fields.Nested(YuzeyKenarSchema(many=True))
    musteriSatisList = fields.Nested(UrunKartMusteriSatisSchema(many=True))
    


class UrunKartListeModel(UrunKartModel):
    kategoriList = list()
    urunList = list()
    olcuList = list()
    yuzeyList = list()
    musteriSatisList = list()
