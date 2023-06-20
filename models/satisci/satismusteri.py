from marshmallow import Schema,fields


class MusteriListeSchema(Schema):

    id = fields.Int()
    musteriadi = fields.String()
    oncelik = fields.String()
    temsilci = fields.String()
    aciklama = fields.String()
    ulkeAdi = fields.String()
    flag = fields.String()
    mail = fields.String()
    oncelikBackground = fields.String()
    newOncelik = fields.String()
    satisciDurum = fields.String()
    teklifSira = fields.Int()
    takipEt = fields.Boolean()
class MusteriListeModel:
    id = None
    musteriadi = ""
    oncelik = ""
    temsilci = ""
    aciklama = ""
    ulkeAdi = ""
    flag = ""
    mail = ""
    oncelikBackground = ""
    newOncelik=""
    satisciDurum = ""
    teklifSira = 0
    takipEt = False

class MusteriAyrintiSchema(Schema):

    sira = fields.Int()
    id = fields.Int()
    musteriadi = fields.String()
    aciklama = fields.String()
    baslik = fields.String()
    satisci_cloud = fields.Int()
    satisci_cloud_dosya = fields.String()
    hatirlatmaTarihi = fields.String()
    hatirlatma_notu = fields.String()
    temsilci = fields.String()
    tarih_giris =fields.String()
    
    

class MusteriAyrintiModel:
    sira = 0
    id = None
    musteriadi = ""
    aciklama = ""
    baslik = ""
    satisci_cloud = 0
    hatirlatmaTarihi = ""
    hatirlatma_notu = ""
    temsilci = ""
    tarih_giris = ""
    satisci_cloud_dosya = ""



class MusteriIslemSchema(Schema):
    id = fields.Int()
    sira = fields.Int()
    musteriadi = fields.String()
    aciklama = fields.String()
    baslik = fields.String()
    satisci_cloud = fields.Boolean()
    satisci_cloud_dosya = fields.String()
    hatirlatmaTarihi = fields.String()
    hatirlatma_notu = fields.String()
    temsilci = fields.String()
    tarih_giris = fields.String()
    

class MusteriIslemModel:
    id = 0
    sira = 0
    musteriadi = ""
    aciklama = ""
    baslik = ""
    satisci_cloud = 0
    hatirlatmaTarihi = ""
    hatirlatma_notu = ""
    temsilci = ""
    tarih_giris = ""
    satisci_cloud_dosya = ""
    
    
class TeklifMusteriSchema(Schema):
    aciklama = fields.String()
    
class TeklifMusteriModel:
    aciklama = ""