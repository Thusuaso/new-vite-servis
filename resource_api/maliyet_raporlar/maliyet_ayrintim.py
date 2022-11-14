from helpers import SqlConnect,TarihIslemler
from models.ozel_maliyet.ozel_ayrinti import *

class MaliyetRaporuAyrinti:

    def __init__(self):

        self.data = SqlConnect().data
        

    def getBankaAyrintiList(self,siparisno):
        
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
             select * from OdemelerTB where SiparisNo=? order by Tarih desc
            """,(siparisno)
        )

        liste = list()
        
        for item in result:
            
            model = BankaAyrintiModel()
            model.id = item.ID 
            model.siparis_no = item.SiparisNo
            model.tutar = item.Tutar
            model.kur = item.Kur
            model.tutartl =   model.tutar *  model.kur
            model.masraf = item.Masraf
            model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            liste.append(model)
            
        schema = BankaAyrintiSchema(many=True)
        
        return schema.dump(liste)
    
    def getMaliyetAyrintiList(self,siparisno):
        
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
              select
            s.ID,
            s.SiparisNo,
            s.YuklemeTarihi,
            s.Vade,
            m.FirmaAdi,
            s.MusteriID,
            s.NavlunSatis,
			s.NavlunAlis,
            s.DetayTutar_1,
			s.DetayAlis_1,
            s.DetayTutar_2,
			s.DetayAlis_2,
            s.DetayTutar_3,
			s.DetayAlis_3,
           s.DetayTutar_4,
		   s.EvrakGideri,
		   s.Komisyon,
            s.Pesinat,
            (
            select Sum(Tutar) from OdemelerTB o where o.SiparisNo=s.SiparisNo
            and s.MusteriID=m.ID
            ) as Odeme,
			    (
            select Sum(Masraf) from OdemelerTB o where o.SiparisNo=s.SiparisNo
            and s.MusteriID=m.ID
            ) as BankaMasraf,
            (
              select Sum(SatisToplam) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo
            ) as UrunBedeli        
            from
            SiparislerTB s,MusterilerTB m
            where
            s.MusteriID=m.ID
            and s.SiparisNo=?
            and s.SiparisDurumID=3
            order by s.YuklemeTarihi desc
            """,(siparisno)
        )

        liste = list()

        for item in result:
            
            model = OzelMaliyetAyrintiModel()
            model.id = item.ID 
           
             
            model.siparis_no = item.SiparisNo
            model.invoiced = item.UrunBedeli + item.DetayTutar_1 + item.DetayTutar_2 + item.DetayTutar_3 + item.NavlunSatis
            if item.NavlunAlis != None:
             model.navlun_alis = item.NavlunAlis
            else : model.navlun_alis = 0

            

            if item.DetayAlis_1 != None:
             model.detay_1 = item.DetayAlis_1
            else : model.detay_1 = 0

            if item.DetayAlis_2 != None:
             model.detay_2 = item.DetayAlis_2
            else : model.detay_2 = 0
             
            if item.DetayAlis_3 != None:
             model.detay_3 = item.DetayAlis_3
            else : model.detay_3 = 0
            
            if item.DetayTutar_4 != None:
             model.mekus_masraf = item.DetayTutar_4
            else : model.mekus_masraf = 0
            
            if item.Komisyon != None:
             model.komisyon = item.Komisyon
            else : model.komisyon = 0
           
            if item.BankaMasraf != None:
             model.banka_masrafi = item.BankaMasraf
            else : model.banka_masrafi = 0
            
            if item.EvrakGideri != None:
             model.kurye = item.EvrakGideri
            else : model.kurye = 0
            
           
            
            model.mekmer_alim , model.mek_moz_alim , model.dis_alim = self.__tedarikciMaliyet(siparisno)
            model.nakliye , model.gumruk , model.ilaclama , model.liman  , model.sigorta = self.__digerMaliyet(siparisno)
            model.ozel_iscilik = self.__ozelIscilik(siparisno)
            model.total_in = model.sigorta + model.liman + model.ilaclama +  model.gumruk + model.nakliye + model.mekmer_alim + model.mek_moz_alim + model.dis_alim + model.banka_masrafi + model.ozel_iscilik + model.navlun_alis + model.detay_1 + model.detay_2 + model.detay_3 + model.mekus_masraf + model.komisyon + model.kurye
           
     
               
              
            liste.append(model)
            
        schema = OzelMaliyetAyrintiSchema(many=True)
        
        return schema.dump(liste)  

    def __tedarikciMaliyet(self,siparisno):

        result = self.data.getStoreList(

            """
            select * from SiparisUrunTB where SiparisNo=?
          
            """,(siparisno)
        )
       
        liste = list()
        mekmer = 0
        mek_moz = 0
        dis = 0
        for item in result:

            if item.AlisFiyati != None:
                if item.TedarikciID == 1 or item.TedarikciID == 123:
                    if item.TedarikciID == 1:
                        mekmer += item.AlisFiyati * item.Miktar
                        
                    if item.TedarikciID == 123:
                         mek_moz += item.AlisFiyati * item.Miktar
                        
                else:
                      dis += item.AlisFiyati *  item.Miktar


           
        return mekmer , mek_moz, dis

    def __digerMaliyet(self,siparisno):

        result = self.data.getStoreList(

            """
            select * from SiparisFaturaKayitTB where SiparisNo=?
          
            """,(siparisno)
        )
        nakliye = 0
        gumruk = 0
        ilaclama = 0
        liman = 0
        sigorta = 0
        liste = list()

        for item in result:

            if item.YuklemeEvrakID == 13:
                 nakliye += item.Tutar
            elif item.YuklemeEvrakID == 70:       
                 gumruk += item.Tutar
            elif item.SiparisFaturaTurID == 73:   
                  ilaclama += item.Tutar
            elif item.SiparisFaturaTurID == 15:   
                  sigorta += item.Tutar      
            elif item.SiparisFaturaTurID == 9 and item.YuklemeEvrakID == 50:  
                  liman += item.Tutar
  
        return nakliye,  gumruk  ,ilaclama ,liman,sigorta

    def __ozelIscilik(self,siparisno):

        result = self.data.getStoreList(

            """
          select * from SiparisEkstraGiderlerTB where SiparisNo=?
          
            """,(siparisno)
        )
        ozel_iscilik = 0
      
        liste = list()

        for item in result:

            ozel_iscilik += item.Tutar
  
        return ozel_iscilik  

  