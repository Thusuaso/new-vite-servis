from marshmallow import Schema,fields,validate
from models.ozel_maliyet.tedarikci_fatura import TedarikciFaturaSchema


class OzelMaliyetAyrintiSchema(Schema):

    id = fields.Int()
    siparis_no = fields.String()
    invoiced = fields.Float()
    mekmer_alim = fields.Float()
    mek_moz_alim = fields.Float()
    dis_alim  = fields.Float()
    
    nakliye = fields.Float()
    gumruk = fields.Float()
    ilaclama = fields.Float()
    liman = fields.Float()
    sigorta = fields.Float()
    navlun_alis = fields.Float()
    detay_1 = fields.Float()
    detay_2 = fields.Float()
    detay_3 = fields.Float()
    mekus_masraf = fields.Float()
    komisyon = fields.Float()
    ozel_iscilik = fields.Float()
    banka_masrafi = fields.Float()
    kurye = fields.Float()
    total_in = fields.Float()
    navlun = fields.Float()
    alisFiyatiControl = fields.Boolean()
    kur = fields.Float()
    
  

class OzelMaliyetAyrintiModel:

    id = None
    siparis_no = "" 
   
    invoiced = 0
    mekmer_alim = 0
    mek_moz_alim = 0
    dis_alim  = 0
    nakliye = 0
   
    gumruk = 0
    ilaclama = 0
    sigorta = 0
    liman = 0
    navlun_alis = 0
    detay_1 = 0
    detay_2 = 0
    detay_3 = 0
    mekus_masraf = 0
    komisyon = 0
    ozel_iscilik = 0
    banka_masrafi = 0
    kurye = 0
    total_in = 0
    alisFiyatiControl = False
    kur = 0
    
class BankaAyrintiSchema(Schema):

    id = fields.Int()
    siparis_no = fields.String()
    tutar = fields.Float() 
    tutartl = fields.Float()
    kur= fields.Float()
    masraf = fields.Float()
    tarih = fields.String()
   
    
  

class BankaAyrintiModel:

    id = None
    siparis_no = ""
    tutar = 0
    tutartl = 0
    kur = 0
    masraf = 0
    tarih = ""
    
   
