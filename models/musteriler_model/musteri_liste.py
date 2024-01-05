from marshmallow import Schema,fields


class MusteriListeSchema(Schema):

    id = fields.Int()
    musteriadi = fields.String()
    unvan = fields.String()
    adres = fields.String()
    marketing = fields.String()
    ulkeadi = fields.String()
    logo = fields.String()
    temsilci = fields.String()
    devir = fields.Boolean()
    ozel = fields.Boolean()
    telefon = fields.String()
    sira = fields.Int()
    isim = fields.String()
    satisci = fields.String()
    notlar = fields.String()
    sonkullanici = fields.Boolean()
    kod = fields.String()

class MusteriListeModel:
    id = None
    musteriadi = ""
    unvan = ""
    adres = ""
    marketing = ""
    ulkeadi = ""
    logo = ""
    temsilci = ""
    devir = False
    ozel =  False
    telefon = ""
    sira = 0
    isim = ""
    satisci=""
    notlar =  ""
    sonkullanici=False
    kod = ""

class MusteriPoListeSchema(Schema):
    po = fields.String()
    id = fields.Int()
    customer_name = fields.String()
    
class MusteriPoListeModel:
    po = ""
    id = 0
    customer_name = ""

class MusteriSiparisListeSchema(Schema):

    firmaadi = fields.String()
    urunadi = fields.String()
    yuzeyadi = fields.String()
    satisFiyati = fields.Float()
    siparisno = fields.String()
    en = fields.String()
    boy = fields.String()
    kenar = fields.String()
    year = fields.DateTime()
    urunbirim = fields.String()

    

class MusteriSiparisListeModel:
    firmaadi = ""
    urunadi=""
    satisFiyati = None
    siparisno = ""
    yuzeyadi = ""
    en = ""
    boy = ""
    kenar = ""
    year = None
    urunbirim = ""
    
    
class MusteriSipAyrintiCardSchema(Schema):
    firmaAdi = fields.String()
    sumOrder = fields.Float()
    topOrder = fields.String()
    marketing = fields.String()
    
class MusteriSipAyrintiCardModel(Schema):
    firmaAdi = ""
    sumOrder = 0
    topOrder = ""
    marketing = ""
    
    
class CustomersSurfaceListSchema(Schema):
    id = fields.Int()
    surface= fields.String()
    firstName = fields.String()
    lastName = fields.String()
    adress = fields.String()
    city = fields.String()
    email = fields.String()
    phone = fields.String()
    surfaceId = fields.Int()
    user_id = fields.Int()
    
class CustomersSurfaceListModel:
    id = 0
    surface = ""
    firstName = ""
    lastName = ""
    adress = ""
    city = ""
    email = ""
    phone = ""
    surfaceId = 0
    user_id = 0
    
    


















class MusteriAyrintiSchema(Schema):

    sira = fields.Int()
    tarih = fields.Date()
    aciklama = fields.String()
    dosya = fields.String()
    

class MusteriAyrintiModel:
    sira = 0
    tarih =  None
    aciklama = ""
    dosya = ""