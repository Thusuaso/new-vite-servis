from models.siparis_liste import *
from helpers import SqlConnect,TarihIslemler
import helpers.metotSure as metotSure
from datetime import date



class SiparisListe:
    def __init__(self,siparisDurum):
        self.data = SqlConnect().data
        self.siparisDurum = siparisDurum
        self.tedarikciFormList = self.data.getList("Select * from SiparisUrunTedarikciFormTB")
        self.iscilikList = self.data.getList(
            """
            Select s.SiparisNo,s.UrunKartId,t.FirmaAdi from
            SiparisEkstraGiderlerTB s,TedarikciTB t
            where s.TedarikciID=t.ID  
            """
        )
        
    def getSiparisList(self):
        tarihIslem = TarihIslemler() 
        sorgu = None 
        if self.siparisDurum == 1 or self.siparisDurum == 2:
            sorgu = self.data.getStoreList(
                "{call PytService_SiparisUrunListesi_t3(?)}",(self.siparisDurum)
            )
        if self.siparisDurum == 3:
            sorgu = self.data.getList("{call PytService_SiparisUrunListesi_Sevk3_Tn3}")
            """PytService_SiparisUrunListesi_Sevk3"""
        siparisResult = self.data.getStoreList(
            """
            Select 
            s.ID,
             s.SiparisNo,
             m.FirmaAdi,
             s.SiparisTarihi,
             YuklemeTarihi
             ,m.Marketing ,
             (select  lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
               (select  lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
             (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
             (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16) evrakc,
              (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
              
             from SiparislerTB s,MusterilerTB m
            where s.MusteriID = m.ID and s.SiparisDurumID=?
            order by s.SiparisTarihi desc
            """,(self.siparisDurum)
        )
        siparisList = list()
        sira = 1
        for item in siparisResult:

            siparisModel = SiparisListeModel()
            siparisModel.id = item.ID
            siparisModel.siparisNo = item.SiparisNo
            siparisModel.musteriAdi = item.FirmaAdi
            siparisModel.faturaKesimTur = item.fatura
            #siparisModel.sure = 0
            siparisModel.tarih = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y")
            if self.siparisDurum == 2:
                bugun = date.today()
                gun,ay,yil =  siparisModel.tarih.split('-')
                siparisTarihi =  date(int(yil),int(ay),int(gun) )
                
                sonuc =  bugun - siparisTarihi
                siparisModel.sure = sonuc.days
                
            siparisModel.sira = sira
            siparisModel.marketing = item.Marketing
            if item.SiparisDurumID == 2 :
             siparisModel.link =  f"https://file-service.mekmar.com/file/download/2/{item.SiparisNo}"

            elif item.SiparisDurumID == 3: 
             siparisModel.link =  f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"

            elif self.siparisDurum == 1:       
              siparisModel.link =  ""
            if self.siparisDurum == 3:
                siparisModel.tarih = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")

            siparisModel.urunler = self.__getSiparisUrunListe(sorgu,siparisModel.siparisNo,sira,siparisModel.sure,item.Marketing,item.FirmaAdi,siparisModel.faturaKesimTur,siparisModel.temsilci,siparisModel.operasyon,siparisModel.link,siparisModel.evrak,siparisModel.evrakc)

            siparisList.append(siparisModel)

            sira = sira + 1
        
        schema = SiparisListeSchema(many=True)
     
       
        return schema.dump(siparisList)
        
    def getSiparisUrunList(self,yil):

        tarihIslem = TarihIslemler()
        sorgu = None
        if self.siparisDurum == 1 or self.siparisDurum == 2:
            sorgu = self.data.getStoreList(
                "{call PytService_SiparisUrunListesi_t4(?)}",(self.siparisDurum)
            )
        if self.siparisDurum == 3:
            sorgu = self.data.getList("{call PytService_SiparisUrunListesi_Sevk3_Tn4}")
        
        if self.siparisDurum == 2 or self.siparisDurum == 1:  
            if(yil == 'Hepsi'):
                
                siparisResult = self.data.getStoreList(
                """
                Select 
                s.ID,
                s.SiparisNo,
                m.FirmaAdi,
                s.SiparisTarihi,
                YuklemeTarihi,
                m.Marketing ,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.SiparisSahibi) as logo,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.Operasyon) as operasyonlogo,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16 ) as evrakc,
                (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
                from SiparislerTB s,MusterilerTB m
                where s.MusteriID = m.ID and s.SiparisDurumID=?  
                
                order by s.YuklemeTarihi desc ,s.SiparisTarihi desc
            
                """,(self.siparisDurum)
                )
            else:
                siparisResult = self.data.getStoreList(
                """
                Select 
                s.ID,
                s.SiparisNo,
                m.FirmaAdi,
                s.SiparisTarihi,
                YuklemeTarihi,
                m.Marketing ,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.SiparisSahibi) as logo,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.Operasyon) as operasyonlogo,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16 ) as evrakc,
                (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
                from SiparislerTB s,MusterilerTB m
                where s.MusteriID = m.ID and s.SiparisDurumID=?  and
                
                (Year(s.SiparisTarihi) =? or year(s.YuklemeTarihi)=?)
                order by s.YuklemeTarihi desc ,s.SiparisTarihi desc
            
                """,(self.siparisDurum,yil,yil)
                )
        elif self.siparisDurum == 3:
            if yil == '2023':
                siparisResult = self.data.getStoreList(
                """
                Select 
                s.ID,
                s.SiparisNo,
                m.FirmaAdi,
                s.SiparisTarihi,
                YuklemeTarihi,
                m.Marketing ,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.SiparisSahibi) as logo,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.Operasyon) as operasyonlogo,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16 ) as evrakc,
                (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
                from SiparislerTB s,MusterilerTB m
                where s.MusteriID = m.ID and s.SiparisDurumID=?  and
                
                (Year(s.SiparisTarihi) >= 2021 or year(s.YuklemeTarihi) >=2021)
                order by s.YuklemeTarihi desc ,s.SiparisTarihi desc
            
                """,(self.siparisDurum)
                )
            else:
                siparisResult = self.data.getStoreList(
                """
                Select 
                s.ID,
                s.SiparisNo,
                m.FirmaAdi,
                s.SiparisTarihi,
                YuklemeTarihi,
                m.Marketing ,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
                (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.SiparisSahibi) as logo,
                (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.Operasyon) as operasyonlogo,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16 ) as evrakc,
                (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
                from SiparislerTB s,MusterilerTB m
                where s.MusteriID = m.ID and s.SiparisDurumID=?  and
                
                (Year(s.SiparisTarihi) = ? or Year(s.YuklemeTarihi) = ?)
                order by s.YuklemeTarihi desc ,s.SiparisTarihi desc
            
                """,(self.siparisDurum,yil,yil)
                )
        
        urunListesi = list()
        sira = 1
        for item in siparisResult:
            sure = 0
            if self.siparisDurum == 2:
                tarih = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y")
                bugun = date.today()
                gun,ay,yil =  tarih.split('-')
                siparisTarihi =  date(int(yil),int(ay),int(gun) )
               
                link =  f"https://file-service.mekmar.com/file/download/2/{item.SiparisNo}"
                
                sonuc =  bugun - siparisTarihi
                sure = sonuc.days
            elif self.siparisDurum == 3:
              link =  f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"
            
            elif self.siparisDurum == 1:       
             link =  ""
            
            liste = self.__getSiparisUrunListe(sorgu,item.SiparisNo,sira,sure,item.Marketing,item.FirmaAdi,item.fatura,item.temsilci,item.operasyon,link,item.evrak,item.logo,item.operasyonlogo,item.evrakc)
            for urun in liste:
                urunListesi.append(urun)

            sira = sira + 1
        
        schema = SiparisUrunListeSchema(many=True)
       

        return schema.dump(urunListesi)

    def getSiparisUrunHepsiList(self):

        tarihIslem = TarihIslemler()
        sorgu = None
        if self.siparisDurum == 1 or self.siparisDurum == 2:
            sorgu = self.data.getStoreList(
                "{call PytService_SiparisUrunListesi_t3(?)}",(self.siparisDurum)
            )
            """PytService_SiparisUrunListesi3"""
        if self.siparisDurum == 3:
            sorgu = self.data.getList("{call PytService_SiparisUrunListesi_Sevk3_Tn3}")
       
        siparisResult = self.data.getStoreList(
            """
            Select 
            s.ID,
             s.SiparisNo,
             m.FirmaAdi,
             s.SiparisTarihi,
             YuklemeTarihi,
             m.Marketing ,
            (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
               (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
             (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.SiparisSahibi) as logo,
             (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.Operasyon) as operasyonlogo,
            (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
             (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16) as evrakc,
            (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
             from SiparislerTB s,MusterilerTB m
            where s.MusteriID = m.ID and s.SiparisDurumID=?  
             order by s.YuklemeTarihi desc ,s.SiparisTarihi desc
          
            """,(self.siparisDurum)
        )
        urunListesi = list()
        sira = 1
        for item in siparisResult:
            sure = 0
            if self.siparisDurum == 2:
                tarih = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y")
                bugun = date.today()
                gun,ay,yil =  tarih.split('-')
                siparisTarihi =  date(int(yil),int(ay),int(gun) )

                link =  f"https://file-service.mekmar.com/file/download/2/{item.SiparisNo}"
                sonuc =  bugun - siparisTarihi
                sure = sonuc.days
            elif self.siparisDurum == 3:    
             link =  f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}"

            elif self.siparisDurum == 1:       
              link =  ""
            liste = self.__getSiparisUrunListe(sorgu,item.SiparisNo,sira,sure,item.Marketing,item.FirmaAdi,item.fatura,item.temsilci,item.operasyon,link,item.evrak,item.logo,item.operasyonlogo,item.evrakc)
            for urun in liste:
                urunListesi.append(urun)

            sira = sira + 1
        
        schema = SiparisUrunListeSchema(many=True)
       

        return schema.dump(urunListesi)    

    def getSiparisUrun(self,siparisNo): 

        tarihIslem = TarihIslemler()
        
        
        sorgu = self.data.getStoreList(
             "{call PytService_SiparisUrunListesi_SiparisNo2_1(?)}",(siparisNo)
        )
       
         
        siparisResult = self.data.getStoreList(
            """
            Select
            s.ID, 
            s.SiparisNo,
            m.FirmaAdi,
            s.SiparisTarihi,
            YuklemeTarihi,
            m.Marketing,
            (select  lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.SiparisSahibi) as temsilci,
               (select lower(k.KullaniciAdi) from KullaniciTB k where k.ID=s.Operasyon) as operasyon,
            (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.SiparisSahibi) as logo,
            (select  'https://mekmar-image.fra1.digitaloceanspaces.com/personel/' + k.Image  from KullaniciTB k where k.ID=s.Operasyon) as operasyonlogo,
            (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as evrak,
            (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=16 ) as evrakc,
            (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as fatura
            from SiparislerTB s,MusterilerTB m
            where s.MusteriID = m.ID and s.SiparisNo=?
            order by s.YuklemeTarihi desc
            """,(siparisNo)
        )
        urunListesi = list()
        sira = 1
        item = siparisResult

       
       
        if self.siparisDurum == 2:
            tarih = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y")
            bugun = date.today()
            gun,ay,yil =  tarih.split('-')
            siparisTarihi =  date(int(yil),int(ay),int(gun) )

            link =  f"https://file-service.mekmar.com/file/download/2/${item.SiparisNo}"   
            sonuc =  bugun - siparisTarihi
            sure = sonuc.days
        elif self.siparisDurum == 3:  
            link =  f"https://file-service.mekmar.com/file/download/16/{item.SiparisNo}" 
        elif self.siparisDurum == 1:       
             link =  "" 

        liste = self.__getSiparisUrunListe(sorgu,item.SiparisNo,sira,sure,item.Marketing,item.FirmaAdi,item.fatura,item.temsilci,item.operasyon,link,item.evrak,item.logo,item.operasyonlogo,item.evrakc)
        for urun in liste:
            urunListesi.append(urun)

            
        
        schema = SiparisUrunListeSchema(many=True)
      
        return schema.dump(urunListesi)


    def __getSiparisUrunListe(self,sorgu,siparisNo,sira,sure,marketing,musteriAdi,fatura,temsilci,operasyon,link,evrak,logo,operasyonlogo,evrakc):
        tarihIslem = TarihIslemler()
        result = filter(lambda x :x.SiparisNo == siparisNo,sorgu)
        
        urunListe = list()
        
        index = 1
        
        for item in result:
            model = SiparisUrunListeModel()
            model.id = item.ID
            model.urunAdi = item.UrunAdi
            model.icerik = item.UretimAciklama
            model.musteriAciklama = item.MusteriAciklama
            model.kenar = item.Kenar
            model.en = item.En
            model.boy = item.Boy
            model.faturaKesimTur = fatura
            model.evrak = evrak
            model.evrakc = evrakc
            model.link = link
            model.logo = logo
            model.operasyonlogo = operasyonlogo
            model.iscilik = self.__getIscilik(siparisNo,item.UrunKartID)
            model.tedarikciAdi = item.TedarikciAdi
            model.siparisMiktari = item.SiparisMiktari
            model.birim = item.BirimAdi
            if(item.BirimAdi == 'Adet'):
                model.adet = item.SiparisMiktari
                model.siparisMiktari = item.SiparisMiktari
                
            else:
                model.siparisMiktari = item.SiparisMiktari
                model.adet = 0
                
            if(item.BirimAdi == 'M2'):
                model.mt2 = item.SiparisMiktari
                model.siparisMiktari = item.SiparisMiktari
                
            else:
                model.siparisMiktari = item.SiparisMiktari
                model.mt2 = 0
                
            model.sira = sira
            model.temsilci= temsilci
            model.operasyon = operasyon
            model.siparisNo = item.SiparisNo
            model.sure = sure
            model.kasa = 0
            model.faturaDurumRenk = self.__getFaturaDurumRenk(fatura)
            model.marketing = marketing
            model.ton = item.Ton
            if item.KasaAdet != None:
                model.kasa = int(item.KasaAdet)
            if self.siparisDurum != 3:
                model.uretimMiktari = item.UretimMiktari
                model.tedarikciForm = self.__getTedarikciFormDurum(model.siparisNo,item.TedarikciId)
                model.urunDurumRenk = self.__getUrunDurumRenk(model.tedarikciForm,model.uretimMiktari,model.siparisMiktari,sure,item.TedarikciId,model.marketing,item.disarda)
            
            
            model.birimFiyat = item.SatisFiyati
           
            model.satisToplam = item.SatisToplam
            model.tarih = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y")
            if self.siparisDurum == 3:
                model.tarih = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")
            if index != 1:
                model.isGroup = "ozel"
            model.musteriAdi = musteriAdi
            
            index = index + 1
            urunListe.append(model)
            
       
        return urunListe


    def __getTedarikciFormDurum(self,siparisNo,tedarikciId):

        durum = False
        for ted in self.tedarikciFormList:
            if ted.SiparisNo == siparisNo and ted.TedarikciID == tedarikciId:
                durum = True

        return durum

    def __getUrunDurumRenk(self,tedarikciFormDurum,uretimMiktari,siparisMiktari,sure,tedarikciId,marketing,disarda):
        renk = 'transparent'

        if tedarikciFormDurum == False or tedarikciId==32:
            renk = 'red'
        if  marketing !='Mekmar' and ( tedarikciId == 1 or tedarikciId  == 123 ):
            if uretimMiktari == siparisMiktari:
                renk = 'green'
            elif uretimMiktari >= siparisMiktari:
                renk = 'black'
            else:
                renk = 'transparent'
        else:
            if uretimMiktari > 0:
                if uretimMiktari == siparisMiktari:
                   
                        renk = 'green'
                if  disarda != None :
                     if disarda == 1 :
                         if(uretimMiktari == siparisMiktari):
                             
                            renk = 'blue'
                         else:
                             renk = 'transparent'
                if uretimMiktari > siparisMiktari:
                    renk = 'black'
                if siparisMiktari > uretimMiktari and sure > 30:
                    renk = 'orange'
             
        return renk

    def __getFaturaDurumRenk(self,faturaKesimTur):
        
        renk = 'transparent1'

        if faturaKesimTur == 'Efes':
            renk = '#a6dced'
        else:
            renk = 'light gray'
                
        
        return renk     

    def __getIscilik(self,siparisNo,urunKartId):
        iscilik = ''
        for item in filter(lambda x: x.SiparisNo == siparisNo and x.UrunKartId == urunKartId,self.iscilikList):
            iscilik = item.FirmaAdi
        return iscilik

        

