from marshmallow import Schema,fields


class KonteynerSchema(Schema):

    id = fields.Float()
    fatura_no = fields.String()
    yukleme_tarihi = fields.String()
    firma_adi = fields.String()
    siparis_no = fields.String()
    tutar = fields.Float()
    faturaid = fields.Int()
    tur=fields.String()
    aciklama=fields.String()
    evrak_id=fields.Int()
    evrak_adi=fields.String()
    gumruk_evrak = fields.String()
    gumruk=fields.Int()
    liman= fields.Int()
    liman_evrak=fields.String()
    navlun_evrak=fields.String()
    ilaclama = fields.Int()
    ilaclama_evrak = fields.String()  
    nakliye = fields.Int()
    nakliye_evrak = fields.String()
    kur = fields.Float()
    genel_link = fields.String()
    aciklama = fields.String()
class KonteynerModel:
    id = 0
    fatura_no = ""
    yukleme_tarihi = ""
    firma_adi = ""
    siparis_no = ""
    tutar = 0 
    faturaid = 0
    tur = ""
    aciklama=""
    evrak_id = 0
    evrak_adi=""
    gumruk_evrak = ""
    gumruk= 0
    liman = 0 
    liman_evrak = ""
    navlun_evrak = ""
    ilaclama = 0 
    ilaclama_evrak = ""
    nakliye = 0 
    nakliye_evrak = ""
    kur = 0
    genel_link = ""
    aciklama = ""

class KonteynerListeSchema(Schema):
    
    id = fields.Int() 
    firma_adi = fields.String()
    Firma_id = fields.Int()
    faturaNo = fields.String()
    Tutar_tl = fields.Float()
    kur = fields.Float()
    Tutar_dolar = fields.Float()
    tarih = fields.Date()
    link = fields.String()
    
    
class KonteynerListeModel:
    id = None 
    firma_adi = ""
    Firma_id = 0
    faturaNo = ""
    Tutar_tl = 0
    kur = 0
    Tutar_dolar = 0
    tarih = None
    link = ""
    
class KonteynerIslemSchema(Schema):
    
    
    id = fields.Int() 
    dosya_id = fields.Int()
    firma_adi = fields.String()
    Firma_id = fields.Int()
    siparisno = fields.String()
    faturaNo = fields.String()
    Tutar_tl = fields.Float()
    kur = fields.Float()
    Tutar_dolar = fields.Float()
    tarih = fields.Date()
    fatura_tur = fields.Int()
    fatura_tur_list = fields.String()
    guncel_kur = fields.Int()
   
    
    
class KonteynerIslemModel:
    
    id = None 
    dosya_id = None
    firma_adi = ""
    Firma_id = 0
    siparisno = ""
    fatura_tur = 0
    fatura_tur_list = ""
    faturaNo = ""
    Tutar_tl = 0
    kur = 0
    Tutar_dolar = 0
    tarih = None
    guncel_kur = 0
  


   