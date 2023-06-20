from marshmallow import Schema,fields

class SiparisUrunListeSchema(Schema):
    id = fields.Int()
    faturaKesimTur = fields.String()
    siparisNo = fields.String()
    urunAdi = fields.String()
    icerik = fields.String()
    musteriAciklama=fields.String()
    uretimAciklama = fields.String()
    kenar = fields.String()
    en = fields.String()
    boy = fields.String()
    iscilik = fields.String()
    tedarikciAdi = fields.String()
    siparisMiktari = fields.Float()
    birim = fields.String()
    uretimMiktari = fields.Float()
    birimFiyat = fields.Float()
    temsilci = fields.String()
    satisToplam = fields.Float()
    #custom alanlar
    musteriAdi = fields.String()
    tarih = fields.String()   
    sira = fields.Int()
    isGroup = fields.String()
    kasa = fields.Int()
    sure = fields.Int()
    tedarikciForm = fields.Boolean()
    urunDurumRenk = fields.String()
    faturaDurumRenk = fields.String()
    marketing = fields.String()
    link = fields.String()
    evrak = fields.Int()
    evrakc = fields.Int()
    path = fields.String()
    logo = fields.String()
    operasyonlogo = fields.String()
    operasyon = fields.String()
    finansman = fields.String()
    opChange = fields.Boolean()
    ton = fields.Float()
    newAmount = fields.Float()
    adet=fields.Float()
    mt2=fields.Float()

class SiparisListeSchema(Schema):
    id = fields.Int()
    faturaKesimTur =fields.String()
    sira = fields.Int()
    musteriAdi = fields.String()
    siparisNo = fields.String()
    sure = fields.Int()
    tarih = fields.String()
    marketing = fields.String()
    urunler = fields.Nested(SiparisUrunListeSchema,many=True)

class SiparisListeModel:
    id = None
    faturaKesimTur = ""
    sira = 1
    musteriAdi = ""
    siparisNo = ""
    sure = 0
    tarih = ""
    marketing = ""
    urunler = list()




class SiparisUrunListeModel:
    id = None
    faturaKesimTur = ""
    siparisNo = ""
    urunAdi = ""
    icerik = ""
    musteriAciklama=""
    uretimAciklama = ""
    kenar = ""
    en = ""
    boy = ""
    iscilik = ""
    tedarikciAdi = ""
    siparisMiktari = 0
    birim = ""
    uretimMiktari = 0
    birimFiyat = 0
    satisToplam = 0
    #custom alanlar
    musteriAdi = ""
    temsilci = ""
    operasyon = ""
    finansman = ""
    opChange = False
    tarih = ""   
    sira = 0
    isGroup = ""
    kasa = None
    sure = None
    tedarikciForm = False
    urunDurumRenk = 'white'
    faturaDurumRenk = 'white'
    marketing = ""
    link = ""
    evrak = 0
    evrakc = 0
    logo = ""
    operasyonlogo=""
    path = '/assets/layout/images/personel/' + logo
    ton = 0
    newAmount:0
    adet:0
    mt2:0
