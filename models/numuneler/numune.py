from marshmallow import fields,Schema

from models.yeniTeklifler import urun


class NumuneSchema(Schema):

    id = fields.Int()

    numuneNo = fields.String()

    giristarih = fields.String()
    yukleme_tarihi = fields.String()
    
    musteriAdi = fields.String()
    musteriId = fields.Int()

    ulkeAdi = fields.String()
    ulke = fields.Int()

    adres = fields.String()

    temsilci = fields.String()
    temsilci_id = fields.Int()
   
    takip_No  = fields.String()
    parite = fields.String()

    aciklama = fields.String()

    kuryeAlis = fields.Float()
    kuryeSatis = fields.Float()

    TL_Alis = fields.Float()
    TL_Satis = fields.Float()

    Euro_Alis = fields.Float()
    Euro_Satis = fields.Float()
    
    gonderiId = fields.Int()
    gonderiAdi = fields.String()
    
    bankaId = fields.Int()
    bankaAdi = fields.String()
    
    kategoriId = fields.Int()
    kategoriAdi = fields.String()

    urunBirimId = fields.Int()
    urunBirim = fields.String()
    
    Miktar = fields.Float()
    

    m2 = fields.Float()
    adet = fields.Int()
    mt = fields.Float()
    ton = fields.Float()
               
    numuneCloud = fields.Boolean()
    numuneCloudDosya = fields.String()

    numuneCloud2 = fields.Boolean()
    numuneCloudDosya2 = fields.String()
    aciklama = fields.String()
class NumuneModel:

    id = None
    numuneNo = ""

    giristarih = ""
    yukleme_tarihi = ""
    
    musteriAdi = ""
    musteriId = None

    ulkeAdi = ""
    ulke = None

    adres = ""

    temsilci = ""
    temsilci_id = None
   
    takip_No  = ""
    parite = ""

    kuryeAlis = 0
    kuryeSatis = 0

    TL_Alis = 0
    TL_Satis = 0

    Euro_Alis = 0
    Euro_Satis = 0
    
    gonderiId = None
    gonderiAdi = ""
    
    bankaId = None
    bankaAdi = ""
    
    kategoriId = None
    kategoriAdi = ""

    urunBirimId = None
    urunBirim = ""
    
    Miktar = 0

    m2 = 0
    adet = None
    mt = 0
    ton = 0

    numuneCloud = 0
    numuneCloudDosya = ""

    numuneCloud2 = 0
    numuneCloudDosya2 = ""
    aciklama = ""

class NumuneOdemelerSchema(Schema):
    id = fields.String()
    tarih = fields.String()
    musteri_id = fields.Int()
    numune_no = fields.String()
    aciklama = fields.String()
    tutar = fields.Float()
    masraf = fields.Float()
    banka = fields.String()
    
class NumuneOdemelerModel:
    id = 0
    tarih = ""
    musteri_id = 0
    numune_no = ""
    aciklama = ""
    tutar = 0
    masraf = 0
    banka = ""
    
