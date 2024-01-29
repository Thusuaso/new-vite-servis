from marshmallow import Schema,fields


class EvrakSiparisListeSchema(Schema):
    id = fields.Int() 
    siparisno = fields.String()
    musteriid = fields.Int()
   
    mail = fields.String()
    musteriAdi = fields.String()
    odeme = fields.String()
    teslim = fields.String()
    ulke = fields.String()
    eta = fields.String()
    KonteynerNo = fields.String()
    line = fields.String()
    navlunAlis = fields.Float()
    navlunSatis = fields.Float()

class EvrakSiparisListeModel:

    id = None 
    siparisno = ""
    musteriid = None 
    mail = ""
    musteriAdi =""
    odeme = ""
    teslim = ""
    ulke = ""
    eta = ""
    KonteynerNo = ""
    line = ""
    navlunAlis = 0
    navlunSatis = 0

class EvrakListeSchema(Schema):
    Faturaid = fields.Int() 
    faturaadi = fields.String()
    renk = fields.String()
    

class EvrakListeModel:

    Faturaid = None 
    faturaadi = ""
    renk = ""

class FaturaListeSchema(Schema):
    id = fields.Int() 
    faturaId = fields.Int()
    yuklemeTarihi =fields.DateTime()
    adi = fields.String()
    Draft = fields.String()
    kullanici = fields.String()
    faturano = fields.String()
    yeniID = fields.String()
    yeniEvrakAdi = fields.String()
    durum = fields.Int()
    olmayan_durum = fields.String()
    evrakadi = fields.String()
    tedarikciId = fields.Int()
    siparisNo = fields.String()

class FaturaListeModel:

    id = None
    faturaId = 0
    yuklemeTarihi = ""  
    adi = ""  
    Draft =""
    kullanici = ""
    faturano = ""
    yeniID = ""
    yeniEvrakAdi = ""
    durum = 0
    olmayan_durum = ""
    tedarikciId =0
    evrakadi=""
    siparisNo = ""

class FaturaKayitSchema(Schema):
     id = fields.Int() 
     kullaniciAdi = fields.String()
     siparisno = fields.String()


class FaturaKayitModel:

    id = None 
    kullaniciAdi = ""
    siparisno = ""  

    
class TedarikciSchema(Schema):

     ID = fields.Int() 
     tedarikci = fields.String()
     siparisno = fields.String()


class TedarikciModel:

    ID = None
    tedarikci = ""
    siparisno = ""      
   

