from marshmallow import Schema,fields
from models import *
from models.siparisler_model.siparisGirisUrun import SiparisGirisUrunSchema,SiparisGirisUrunModel


class SiparisGirisSchema(Schema):    
    siparis = fields.Nested(SiparislerSchema())
    siparisUrunler = fields.Nested(SiparisGirisUrunSchema(many=True))   
    proformaBilgileri = fields.Nested(SiparislerSchema())
    urunModel = fields.Nested(SiparisGirisUrunSchema)
    urunlerYeni = fields.Nested(SiparisGirisUrunSchema(many=True))  
    urunlerDegisenler = fields.Nested(SiparisGirisUrunSchema(many=True))
    urunlerSilinenler = fields.Nested(SiparisGirisUrunSchema(many=True))
class SiparisGirisModel:   
    siparis = SiparislerModel()
    siparisUrunler = list()  
    proformaBilgileri = SiparislerModel()
    urunModel = SiparisGirisUrunModel()
    urunlerYeni = list()
    urunlerDegisenler = list()
    urunlerSilinenler = list()
class ContainerAmountSchema(Schema):
    container_amount = fields.Int()
    
class ContainerAmountModel:
    container_amount = 0
    
    
class SiparisNoListSchema(Schema):
    siparisNo = fields.String()
    
class SiparisNoListModel:
    siparisNo = ""