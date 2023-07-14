from helpers import SqlConnect,TarihIslemler
from models.operasyon.konteyner_listesi import *



class KonteynerHepsiListesi:

    def __init__(self):

        self.data = SqlConnect().data
        self.firmalar = self.data.getList("Select * from FirmalarTB")
        self.digerFaturalar = self.data.getList("Select * from KonteynerDigerFaturalarKayitTB")
        self.nakliyeFaturalar = self.data.getList("Select * from NakliyeFaturaKayitTB")
        self.evrakListesi = self.data.getList("Select * from YuklemeEvraklarTB")

  
    def getHepsi(self):

        result = self.data.getList(
            """      
            
        select (select a.FirmaAdi from FirmalarTB a where a.ID=k.FirmaID)  as firma,
        f.EvrakYuklemeTarihi ,
        f.SiparisFaturaTurID, 
        f.SiparisNo ,
        k.FaturaNo , 
        f.EvrakAdi, 
        k.FirmaID,
        f.YuklemeEvrakID,
        k.Kur,
        k.ID,
        f.Tutar,
		k.Aciklama
        from SiparisFaturaKayitTB f , KonteynerDigerFaturalarKayitTB k 
        where k.ID=f.FaturaKayitID and f.SiparisFaturaTurID !=0 and f.SiparisNo !=''
        order by f.EvrakYuklemeTarihi desc
      
            """
        ) 
        self.digerFaturalar = self.data.getList("Select * from KonteynerDigerFaturalarKayitTB")
        
        liste = list()

        for item in result:
            model = KonteynerModel()
            model.id = item.ID
            model.yukleme_tarihi = item.EvrakYuklemeTarihi
            model.firma_adi = item.firma
            model.fatura_no=item.FaturaNo
            model.tutar=item.Tutar
            model.siparis_no=item.SiparisNo
            model.evrak_id=item.SiparisFaturaTurID
            model.evrak_adi=item.EvrakAdi
            model.kur = item.Kur
            model.aciklama = item.Aciklama

            if  item.SiparisFaturaTurID == 73:
                model.tur = "İlaçlama"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"
            if item.SiparisFaturaTurID == 7 or item.SiparisFaturaTurID == 8:
               model.tur = "Gümrük"
               if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"
            if item.SiparisFaturaTurID == 13 and item.YuklemeEvrakID == 50:
                model.tur = "Navlun"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"
            
            if item.SiparisFaturaTurID == 100 and item.YuklemeEvrakID == 50:
                model.tur = "Lashing"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"
            
            if item.SiparisFaturaTurID == 101 and item.YuklemeEvrakID == 50:
                model.tur = "Booking"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"
            if item.SiparisFaturaTurID == 102 and item.YuklemeEvrakID == 50:
                model.tur = "Spanzet"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"
            
            if item.SiparisFaturaTurID == 15:
                model.tur = "Sigorta"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"

            if (item.SiparisFaturaTurID == 9 or item.SiparisFaturaTurID == 10  ) and item.YuklemeEvrakID == 50:
                model.tur = "Liman"
                if item.FirmaID != None:
                        model.genel_link = f"https://file-service.mekmar.com/file/download/customer/{item.FirmaID}/{item.EvrakAdi}"

            

            
            liste.append(model)

        schema = KonteynerSchema(many=True)

        return schema.dump(liste)  

        
   
        
    def __set(self):
        pass