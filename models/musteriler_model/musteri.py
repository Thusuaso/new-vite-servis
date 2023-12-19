from marshmallow import Schema,fields



class MusteriSchema(Schema):

    id = fields.Int()
    musteri_adi = fields.String()
    unvan = fields.String()
    adres = fields.String()
    ulke_adi = fields.String()
    ulke_id = fields.Int()
    logo = fields.String()
    marketing = fields.String()
    aktif = fields.Boolean()
    sira = fields.Int()
    mt_no = fields.Int()
    musteri_temsilci_id = fields.Int()
    satisci = fields.Int()
    kullanici_id = fields.Int()
    mail_adresi = fields.String()
    telefon = fields.String()
    devir = fields.Boolean()
    ozel = fields.Boolean()
    selectOncelik = fields.String()
    satisci=fields.String()
    takip = fields.Boolean()
    notlar = fields.String()
    sonkullanici = fields.Boolean()
    musteri_yeri = fields.String()
class MusteriModel:
    id = None
    musteri_adi = ""
    unvan = ""
    adres = ""
    ulke_adi = ""
    ulke_id = None
    logo = ""
    marketing = ""
    aktif = True
    sira = 0
    mt_no = 2
    musteri_temsilci_id = None
    satisci = None
    kullanici_id = None
    mail_adresi = ""
    telefon = ""
    devir = False
    ozel = False
    selectOncelik = ""
    satisci=""
    takip=False
    notlar = ""
    sonkullanici = False
    musteri_yeri = ""

class MusteriSiparisSchema(Schema):

    id = fields.Int()
    Yil = fields.String()
    Total = fields.Float()
    

class MusteriSiparisModel:
    id = None
    Yil = ""
    Total = 0
   
class MusteriSiparisAyrintiSchema(Schema):

    SiparisNo = fields.String()
    Satisci = fields.String()
    Operasyon = fields.String()
    

class MusteriSiparisAyrintiModel:

    SiparisNo = ""
    Satisci = ""
    Operasyon = ""

class TeklifMusterilerSchema(Schema):
    id = fields.Int()
    customer = fields.String()
    company = fields.String()
    email = fields.String()
    phone = fields.String()
    country = fields.Int()
    user = fields.Int()
    adress = fields.String()
    countryName = fields.String()
    username = fields.String()
    description = fields.String()
    
class TeklifMusterilerModel:
    id = 0
    customer = ""
    company = ""
    email = ""
    phone = ""
    country = 0
    user = 0
    adress = ""
    countryName=""
    username = ""
    description = ""
    
class FuarMusterilerSchema(Schema):
    id = fields.Int()
    customer = fields.String()
    company = fields.String()
    email = fields.String()
    phone = fields.String()
    country = fields.String()
    user = fields.Int()
    adress = fields.String()
    kullanici = fields.Int()
    satisci = fields.String()
    linkOn = fields.String()
    linkArka = fields.String()
    fairstatus = fields.Boolean()
    visitstatus = fields.Boolean()
    
    
    
class FuarMusterilerModel:
    id = 0
    customer = ""
    company = ""
    email = ""
    phone = ""
    country = ""
    user = 0
    adress = ""
    satisci = ""
    kullanici = 0
    linkOn = ""
    linkArka=""
    fairstatus = False
    visitstatus = False
    
class BgpMusterilerSchema(Schema):
    id = fields.Int()
    customer = fields.String()
    company = fields.String()
    email = fields.String()
    phone = fields.String()
    country = fields.String()
    user = fields.Int()
    adress = fields.String()
    kullanici = fields.Int()
    satisci = fields.String()
    linkOn = fields.String()
    linkArka = fields.String()
    
    
class BgpMusterilerModel:
    id = 0
    customer = ""
    company = ""
    email = ""
    phone = ""
    country = ""
    user = 0
    adress = ""
    satisci = ""
    kullanici = 0
    linkOn = ""
    linkArka=""