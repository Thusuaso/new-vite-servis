from marshmallow import Schema,fields

from models.urunKart import UrunKartSchema
from models.tedarikci import TedarikciSchema


class SiparisUrunSchema(Schema):
    id = fields.Int()
    siparisNo = fields.String()
    tedarikciId = fields.Int()
    urunKartId = fields.Int()
    urunBirimId = fields.Int()
    urunbirimAdi = fields.String()
    miktar = fields.Float()
    ozelMiktar = fields.Float()
    kasaAdet = fields.Int()
    satisFiyati = fields.Float()
    satisToplam = fields.Float()
    uretimAciklama = fields.String()
    pazarlama = fields.String()
    musteriAciklama = fields.String()
    notlar = fields.String()
    kullaniciId = fields.Int()
    alisFiyati = fields.Float()
    alisFiyati_Tl = fields.Float()
    siraNo = fields.Int()
    kullaniciAdi = fields.String()
    siparisSahibi = fields.String()
    siparisDurumID = fields.Int()
    operasyon = fields.String()
    finansman = fields.String()

    #custom alanlar
    tedarikciAdi = fields.String()
    #urun = fields.Nested(UrunKartSchema)
    uretimMiktari = fields.Float()
    tedarikci = fields.Nested(TedarikciSchema)
    iscilik = fields.String()
    alisFiyatiKontrol = fields.Boolean()
    


class SiparisUrunModel:
    id = None
    siparisNo = ""
    siparisDurumID = 0
    tedarikciId = None
    urunKartId = None
    siparisSahibi = ""
    urunBirimId = None
    urunbirimAdi = ""
    miktar = 0
    ozelMiktar = 0
    kasaAdet = None
    kullaniciAdi = ""
    operasyon = ""
    finansman = ""
    satisFiyati = 0
    satisToplam = 0
    uretimAciklama = ""
    pazarlama = ""
    musteriAciklama = ""
    notlar = ""
    kullaniciId = None
    alisFiyati = 0
    alisFiyati_Tl = 0
    siraNo = None
    #custom alanlar
    tedarikciAdi = ""
    #urun = None
    uretimMiktari = 0
    tedarikci = None
    iscilik = ""
    alisFiyatiKontrol = False
    
    
    