from marshmallow import Schema,fields
import helpers.dateConvert as dateConvert
from models.siparisUrun import SiparisUrunSchema

class SiparislerSchema(Schema):
    id = fields.Int()
    siparisNo = fields.String()
    gidenSiparisNo = fields.String()
    kalanSiparisNo = fields.String()
    siparisTarihi = fields.String()
    TahminiyuklemeTarihi = fields.String()
    odemeTurId = fields.Int()
    faturaKesimTurId = fields.Int()
    teslimTurId = fields.Int()
    musteriId = fields.Int()
    pesinat = fields.Float()
    newPesinat = fields.Float()
    navlunFirma = fields.String()
    navlunMekmarNot = fields.String()
    navlunAlis = fields.Float()
    navlunSatis = fields.Float()
    kullaniciId = fields.Int()
    siparisDurumId = fields.Int()
    uretimAciklama = fields.String()
    sevkiyatAciklama = fields.String()
    finansAciklama = fields.String()
    raporDurum = fields.Boolean()
    tahminiYuklemeTarihi = fields.DateTime()
    tahminiAgirlik = fields.Float()
    yuklemeTarihi = fields.String()
    faturaNo = fields.Int()
    siparisFaturaNo = fields.String()
    vade = fields.String()
    tahmini_eta = fields.String()
    ulke = fields.String()
    komisyon = fields.Float()
    toplamPalet = fields.Int()

    detayAciklama_1 = fields.String()
    detayMekmarNot_1 = fields.String()
    detayTutar_1 = fields.Float()
    detayAlis_1 = fields.Float()

    detayAciklama_2 = fields.String()
    detayMekmarNot_2 = fields.String()
    detayTutar_2 = fields.Float()
    detayAlis_2 = fields.Float()

    detayAciklama_3 = fields.String()
    detayMekmarNot_3 = fields.String()
    detayTutar_3 = fields.Float()
    detayAlis_3 = fields.Float()

    detayTutar_4 = fields.Float()
    detayAciklama_4 = fields.String()

    
    detayTutar_4_sipBolme = fields.Float()
    
    
    
    siparisSahibi = fields.Int()
    operasyon = fields.Int()
    finansman = fields.Int()

    kayitKapali = fields.Boolean()

    sigorta_id = fields.Boolean()
    sigorta_tutar = fields.Float()
    sigorta_tutar_satis = fields.Float()
    evrakGideri = fields.Float()
    iade = fields.Float()
    ilaclamaGideri = fields.Float()
    eta = fields.String()
    konteynerAyrinti = fields.String()
    konteynerDurum = fields.Boolean()
    forwarder = fields.String()
    konteynerNo = fields.String()
    transitSuresi = fields.Int()
    ayrintiliCekiListesi = fields.Boolean()
    teslimYeri = fields.String()
    line = fields.String()
    evrakYuklemeTarihi = fields.DateTime()
    ertelemeTekrar = fields.Int()
    evrakMailGonderildi = fields.Boolean()
    draftMailGonderildi = fields.Boolean()
    geciciEta = fields.DateTime()
    geciciTransitSuresi = fields.Int()
    gemiKalkisTarihi = fields.DateTime()
    hizliYukleme = fields.Boolean()
    odemeAciklama = fields.String()

    #özel alanlar
    musteriAdi = fields.String()
    siparisUrunler = fields.Nested(SiparisUrunSchema,many=True)
    marketing = fields.String()
    sira = fields.Int()
    malBedeli = fields.Float()
    digerTutarToplam = fields.Float()
    genelToplam = fields.Float()
    ulkeId = fields.Int()
    iscilikTutar = fields.Float()
    liman = fields.String()
    depo = fields.Boolean()
    mekus_masraf = fields.Float()
    profit_usd = fields.Float()
    kayit_kisi =fields.String()
    mail = fields.String()
    opChange = fields.Boolean()
    maya = fields.Boolean()

class SiparislerModel:
    id = None
    siparisNo = ""
    gidenSiparisNo=""
    kalanSiparisNo=""
    mail = ""
    siparisTarihi = ""
    TahminiyuklemeTarihi = ""
    liman = ""
    depo = False
    odemeTurId = None
    faturaKesimTurId = None
    teslimTurId = None
    musteriId = None
    pesinat = 0
    newPesinat=0
    navlunFirma = ""
    navlunMekmarNot = ""
    navlunAlis = 0
    navlunSatis = 0
    kullaniciId = None
    siparisDurumId = None
    uretimAciklama = ""
    sevkiyatAciklama = ""
    finansAciklama = ""
    raporDurum = True
    operasyon = 0
    finansman = 0
    tahminiYuklemeTarihi = None
    tahminiAgirlik = 0
    yuklemeTarihi = ""
    faturaNo = None
    siparisFaturaNo = ""
    vade = ""
    tahmini_eta=""
    ulke = ""
    komisyon = 0
    toplamPalet = None
    iade = 0

    detayAciklama_1 = ""
    detayMekmarNot_1 = ""
    detayTutar_1 = 0
    detayAlis_1 = 0

    detayAciklama_2 = ""
    detayMekmarNot_2 = ""
    detayTutar_2 = 0
    detayAlis_2 = 0

    detayAciklama_3 = ""
    detayMekmarNot_3 = ""
    detayTutar_3 = 0
    detayAlis_3 = 0

    detayTutar_4 = 0
    detayAciklama_4 = ""
    detayTutar_4_sipBolme = 0
    siparisSahibi = None
    kayitKapali = False

    sigorta_id = False
    sigorta_tutar = 0
    sigorta_tutar_satis=0
    evrakGideri = 0
    ilaclamaGideri = 0
    eta = ""
    konteynerAyrinti = ""
    konteynerDurum = False
    forwarder = ""
    konteynerNo = ""
    transitSuresi = None
    ayrintiliCekiListesi = False
    teslimYeri = ""
    line = ""
    evrakYuklemeTarihi = None
    ertelemeTekrar = None
    evrakMailGonderildi = False
    draftMailGonderildi = False
    geciciEta = None
    geciciTransitSuresi = None
    gemiKalkisTarihi = None
    hizliYukleme = False
    odemeAciklama = ""
    opChange = False
    #özel alanlar
    musteriAdi = ""
    siparisUrunler = list()
    sira = 1
    marketing = ""
    malBedeli = 0
    digerTutarToplam = 0

    genelToplam = 0
    ulkeId = None
    iscilikTutar = 0
    profit_usd = 0
    mekus_masraf = 0
    kayit_kisi = ""
    maya = False


    








    




