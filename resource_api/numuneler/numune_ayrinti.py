from helpers import SqlConnect,TarihIslemler
from models.numuneler import *

class NumuneAyrinti:

    def __init__(self,po):

        self.data = SqlConnect().data
        self.numune_no = po
       

    def getNumuneAyrintiList(self):
        
         result = self.data.getStoreList(
            """
              select

                *,
                (select m.MusteriAdi from YeniTeklif_MusterilerTB m where n.MusteriID=m.Id ) as  MusteriAdi,
                (select k.Urun from NumuneKategoriTB k where k.ID=n.KategoriID) as KategoriAdi,
                (select u.BirimAdi from UrunBirimTB u where u.ID= n.UrunBirimi) as BirimAdi,
                (select g.GonderiAdi from NumuneGonderiTipi g where g.ID=n.GonderiTipi) as GonnderiAdi,
                (select b.BankaAdi from NumuneBankaSecim b where b.ID=N.BankaSecim) as BankaAdi
                from NumunelerTB n 
                where n.NumuneNo=? 
            """,(self.numune_no)
         )
         
         liste = list()
         tarihIslem = TarihIslemler() 
         for item in result:

            model = NumuneModel()
            model.id = item.ID
            model.numuneNo = item.NumuneNo
            model.giristarih = tarihIslem.getDate(item.NumuneTarihi).strftime("%d-%m-%Y")
            model.yukleme_tarihi = tarihIslem.getDate(item.NumuneTarihi).strftime("%d-%m-%Y")
            model.takip_No = item.TrackingNo
            model.parite = item.Parite
            model.temsilci = item.NumuneTemsilci
            model.adres = item.Adres
            model.aciklama = item.Aciklama
            model.musteriAdi = item.MusteriAdi
            model.musteriId = item.MusteriID
            model.ulke = item.Ulke
            model.kategoriAdi = item.KategoriAdi 
            model.kategoriId = item.KategoriID
            model.gonderiId = item.GonderiTipi
            model.bankaId = item.BankaSecim
            model.kuryeAlis = item.KuryeAlis
            model.kuryeSatis = item.KuryeSatis
            model.TL_Alis = item.TL_Alis
            model.TL_Satis = item.TL_Satis  

            model.Euro_Alis = item.Euro_Alis
            model.Euro_Satis = item.Euro_Satis 
            
            model.urunBirim = item.BirimAdi
            model.Miktar = item.Miktar
            model.urunBirimId = item.UrunBirimi
            if(item.Numune_Cloud_Dosya == None): 
                model.numuneCloudDosya = ""
            else:
                model.numuneCloudDosya = 'https://file-service.mekmar.com/file/download/numune/numuneDosya/' + str(item.ID) + '/' + item.Numune_Cloud_Dosya
                
            if(item.Numune_Cloud_Dosya2 == None): 
                model.numuneCloudDosya2 = ""
            else:
                model.numuneCloudDosya2 = 'https://file-service.mekmar.com/file/download/numune/numuneDosya/' + str(item.ID) + '/' + item.Numune_Cloud_Dosya2
                
            
            if item.BirimAdi != None:
                if item.BirimAdi == 'M2' :
                    
                    model.m2 = item.Miktar
                if item.BirimAdi == 'Adet' :
                    model.adet = item.Miktar 
                if item.BirimAdi == 'Mt' :
                    model.mt = item.Miktar  
                if item.BirimAdi == 'Ton' :
                    model.ton = item.Miktar              

           


            liste.append(model)
        
         schema = NumuneSchema(many=True)
        
         return schema.dump(liste)
    
    def getNumuneOdemelerList(self):
        try:
            result = self.data.getStoreList("""
                                                select * from NumuneOdemelerTB where NumuneNo=?

                                            """,(self.numune_no))
            liste = list()
            for item in result:
                model = NumuneOdemelerModel()
                model.id = item.ID
                model.tarih = item.Tarih
                model.musteri_id = item.MusteriID
                model.numune_no = item.NumuneNo
                model.aciklama = item.Aciklama
                model.tutar = self.__getNone(item.Tutar)
                model.masraf = self.__getNone(item.Masraf)
                model.banka = item.Banka
                liste.append(model)
            schema = NumuneOdemelerSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getNumuneOdemelerList hata ',str(e))
            return False
        
    def __getNone(self,value):
        if(value == None):
            return 0
        else:
            return float(value)