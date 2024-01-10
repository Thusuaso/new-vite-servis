from marshmallow import Schema,fields


class AtlantaStokSchema(Schema):
    id = fields.Int()
    sku = fields.String()
    tanim = fields.String()
    stok_kutu = fields.Int()
   
    stok_sqft =fields.Float()
    stok_m2 =fields.Float()
    mekmar_fiyat =fields.Float()
    maya_fiyat =fields.Float()
    bd_fiyat =fields.Float()
    villo_fiyat =fields.Float()
    su_kutu = fields.Int()
    kasa_adet = fields.Int()
    kutu_adet = fields.Int()
    su_sqft =fields.Float()
    su_m2 =fields.Float()
    kasa_Sqft = fields.Float()
    kasa_m2 = fields.Float()
    kasa_kutu = fields.Int()
    po = fields.String()
    kod = fields.String()
    keys = fields.String()
    kategori = fields.String()
    ebat = fields.String()
    toplam_mekus = fields.Float()
    kutu_sqft = fields.Float()

class AtlantaStokModel:
    id = None
    sku = ""
    tanim = ""
    stok_kutu = 0
   
    stok_sqft = 0
    stok_m2 =0
    mekmar_fiyat = 0
    maya_fiyat = 0
    bd_fiyat = 0
    villo_fiyat = 0
    su_kutu = 0
    kasa_adet = 0
    kutu_adet = 0
    su_sqft = 0
    su_m2 = 0
    kasa_Sqft = 0
    kasa_m2 = 0
    kasa_kutu = 0
    po = ""
    kod = ""
    keys = ""
    kategori =  ""
    ebat = ""
    toplam_mekus = 0
    kutu_sqft = 0

class Stok_SuSchema(Schema):

    id = fields.Int()
    yukleme_tarihi = fields.String()
    order_no = fields.String()
    box = fields.Int()
    sqft =fields.Float()
    m2 =fields.Float()
    eta =fields.String()
    konteyner_no =fields.String()
    inbound_date= fields.String()
    masraf =fields.Float()
   
class Stok_SuModel:
    id = None
    yukleme_tarihi = ""
    order_no = ""
    box = 0
    sqft = 0
    m2 =0
    eta = ""
    konteyner_no = ""
    inbound_date = ""
    masraf = 0

class DepoUrunSatisSchema(Schema):
    id = fields.Int()
    musteriAdi = fields.String()
    orderNo = fields.String()
    satisTarihi = fields.String() 
    sevkTarihi = fields.String() 
    odemeTarihi = fields.String()
    kutu = fields.Int()
    sqft = fields.Float()
    m2 = fields.Float()
    birimFiyat = fields.Float()
    toplamFiyat = fields.Float()
    rof =fields.String()
   
class DepoUrunSatisModel:
    id = None
    musteriAdi = ""
    orderNo = ""
    satisTarihi = ""
    sevkTarihi = ""
    odemeTarihi = ""
    kutu = 0
    sqft = 0
    m2 = 0
    birimFiyat = 0
    toplamFiyat = 0   
    rof = ""
    

class DepoMaliyetSchema(Schema):

    id = fields.Int()
    uretici = fields.String()
    uretici_fiyat = fields.Float()
    transport = fields.Float() 
    max_payload = fields.Int() 
    mekus_kira = fields.Float()
   
   
class DepoMaliyetModel:

    id = 0
    uretici = ""
    uretici_fiyat = 0
    transport = 0
    max_payload = 0
    mekus_kira = 0