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

     
     musteri_id = fields.Int()
     musteri = fields.String()
     ulkeAdi = fields.String()
     
     sonSiparisTarihi = fields.String()
     logo = fields.String()
     BuYil = fields.Float()
     GecenYil = fields.Float()
     OncekiYil = fields.Float()
     OnDokuzYili = fields.Float()
     OnSekizYili = fields.Float()
     OnYediYili = fields.Float()
     OnAltiYili = fields.Float()
     OnBesYili = fields.Float()
     OnDortYili = fields.Float()
     OnUcYili = fields.Float()
     OnUcYiliOncesi = fields.Float()
     Toplam = fields.Float()
     marketing = fields.String()
     oncelik = fields.String()
     temsilci = fields.String()
     BuYilUretim = fields.Float()
     BuYilSevkiyat = fields.Float()
   

    
class KullaniciModel:

    
    musteri_id = 0
    musteri = ""
    ulkeAdi = ""
    logo = ""
    BuYil = 0
    GecenYil = 0
    OncekiYil = 0
    sonSiparisTarihi = ""
    OnDokuzYili = 0
    OnSekizYili = 0
    OnYediYili = 0
    OnAltiYili = 0
    OnBesYili = 0
    OnDortYili = 0
    OnUcYili = 0
    OnUcYiliOncesi=0
    Toplam = 0 
    marketing = ""
    oncelik = ""
    temsilci = ""
    BuYilUretim = 0
    BuYilSevkiyat = 0
   