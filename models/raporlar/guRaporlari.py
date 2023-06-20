from marshmallow import Schema,fields,validate
class OzelMaliyetListeKarSchema(Schema):
    musteri_id = fields.Int()
    musteri_adi = fields.String()
    siparis_no = fields.String()
    navlun_satis = fields.Float()
    detay_1 = fields.Float()
    detay_2 = fields.Float()
    detay_3 = fields.Float()
    navlun_alis = fields.Float()
    detay_alis_1 = fields.Float()
    detay_alis_2 = fields.Float()
    detay_alis_3 = fields.Float()
    sigorta_tutar_satis = fields.Float()
    mekus_masraf = fields.Float()
    toplam_bedel = fields.Float()
    satis_toplami = fields.Float()
    alis_toplami = fields.Float()
    banka_masrafi = fields.Float()
    odenen_usd_tutar = fields.Float()
    odenen_try_tutar = fields.Float()
    ortalama_kur = fields.Float()
    fatura_masraflari = fields.Float()
    masraf_toplam = fields.Float()
    kar_zarar = fields.Float()
    kar_zarar_tl = fields.Float()
    kar_zarar_orani = fields.Float()
    yukleme_yil = fields.String()
    yukleme_ay = fields.String()
    yukleme_gun = fields.String()
    masraf_toplam_tl = fields.Float()
    komisyon = fields.Float()
    evrak_gideri = fields.Float()
    iscilik_masrafi = fields.Float()
    banka_masrafi = fields.Float()
    sigorta_alis = fields.Float()
    kalan_bedel = fields.Float()
    yukleme_tarihi = fields.String()
class OzelMaliyetListeKarModel:
    musteri_id = 0
    musteri_adi = ""
    siparis_no = ""
    navlun_satis = 0
    detay_1 = 0
    detay_2 = 0
    detay_3 = 0
    sigorta_tutar_satis = 0
    mekus_masraf = 0
    toplam_bedel = 0
    satis_toplami = 0
    alis_toplami = 0
    banka_masrafi = 0
    odenen_usd_tutar = 0
    odenen_try_tutar = 0
    ortalama_kur = 0
    fatura_masraflari = 0
    masraf_toplam = 0
    masraf_toplam_tl = 0
    kar_zarar = 0
    kar_zarar_tl = 0
    kar_zarar_orani = 0
    yukleme_yil = ""
    yukleme_ay = ""
    yukleme_gun = ""
    navlun_alis = 0
    detay_alis_1 = 0
    detay_alis_2 = 0
    detay_alis_3 = 0
    komisyon = 0
    evrak_gideri = 0
    iscilik_masrafi = 0
    banka_masrafi = 0
    sigorta_alis = 0
    kalan_bedel = 0
    yukleme_tarihi = 0
    
class UlkeyeGoreSchema(Schema):
    sip_sayisi = fields.Int()
    ulke_adi = fields.String()
    ulke_id = fields.Int()
    konteynir_sayisi = fields.Int()

class UlkeyeGoreModel:
    sip_sayisi = 0
    ulke_adi = ""
    ulke_id = 0
    konteynir_sayisi = 0
    
class MekusMasraflarSchema(Schema):
    siparisNo = fields.String()
    mekusMasraf = fields.Float()
    
class MekusMasraflarModel:
    siparisNo = ""
    mekusMasraf = 0
    
class LogsMaliyetSchema(Schema):
    id = fields.Int()
    kayit_tarihi = fields.String()
    siparis_no = fields.String()
    yukleme_tarihi = fields.String()
    info = fields.String()
    kayit_kisi = fields.String()
    yil = fields.String()
    ay = fields.String()
    gun = fields.String()
    
class LogsMaliyetModel:
    id = 0
    kayit_tarihi = ""
    siparis_no = ""
    yukleme_tarihi = ""
    info = ""
    kayit_kisi = ""
    yil = ""
    ay = ""
    gun = ""
    
class MusteriyeGoreSchema(Schema):
    id = fields.Int()
    firma_adi = fields.String()
    yuk_mus_sayisi = fields.Int()
    ulke_adi = fields.String()
    konteynir_sayisi = fields.Int()
    
class MusteriyeGoreModel:
    id = 0
    firma_adi = ""
    yuk_mus_sayisi = 0
    ulke_adi = ""
    konteynir_sayisi = 0
    
class TedarikciyeGoreSchema(Schema):
    tedarikci_id = fields.Int()
    firma_adi = fields.String()
    total_alis = fields.Float()
    yuklenen_tedarikci_sayisi = fields.Int()
    
class TedarikciyeGoreModel:
    tedarikci_id = 0
    firma_adi = ""
    total_alis = 0
    yuklenen_tedarikci_sayisi = 0