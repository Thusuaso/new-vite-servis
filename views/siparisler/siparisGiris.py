
from models.raporlar import yukleme
from models.siparisler_model import SiparisGirisSchema,SiparisGirisModel,ContainerAmountSchema,ContainerAmountModel
from models.siparisler_model.siparisGirisUrun import SiparisGirisUrunModel
from models import SiparislerModel
from helpers import SqlConnect,TarihIslemler
from helpers import MailService,DegisiklikMain
import datetime
from resource_api.finans.caprazkur import DovizListem
from views.shared.degisiklikTahmin import DegisiklikTahmin
class SiparisGiris:
    
    def __init__(self):
        self.data = SqlConnect().data
        
        self.iscilikList = self.data.getList(
            """
            Select s.SiparisNo,s.UrunKartId,t.FirmaAdi,s.Tutar from
            SiparisEkstraGiderlerTB s,TedarikciTB t
            where s.TedarikciID=t.ID
            """
        )
        self.firstOrdersList = self.data.getList("""
                                                    select 
                                                    s.SiparisNo,
                                                    s.NavlunSatis,
                                                    s.NavlunAlis,
                                                    s.DetayTutar_1,
                                                    s.DetayTutar_2,
                                                    s.DetayTutar_3,
                                                    s.DetayTutar_4 as Mekus,
                                                    s.DetayAlis_1,
                                                    s.DetayAlis_2,
                                                    s.DetayAlis_3,
                                                    s.Komisyon,
                                                    s.EvrakGideri,
                                                    s.sigorta_tutar_satis as SigortaSatis,
                                                    s.sigorta_Tutar as SigortaTutar



                                                from SiparislerTB s
                                                 
                                                 """)

    def getSiparisModel(self):
        model = SiparisGirisModel()
        schema = SiparisGirisSchema()

        return schema.dump(model)
    
    def getSiparis(self,siparisNo):
        model = SiparisGirisModel()

        model.siparis = self.__getSiparis(siparisNo)
        
        model.siparisUrunler = self.__getSiparisUrunler(siparisNo)
        model.proformaBilgileri = model.siparis

        schema = SiparisGirisSchema()

        return schema.dump(model)

    def __getMarketing(self,musteriId):
        result = self.data.getStoreList(
            """
             select * from MusterilerTB where ID=?
            """,(musteriId)
        )[0]
        return result.Marketing

    def __getSiparis(self,siparisNo):
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(
            """
            Select
            *,
            (Select Sum(u.SatisToplam) from SiparisUrunTB u 
            where u.SiparisNo=s.SiparisNo) as MalBedeli
            from
            SiparislerTB s
            where s.SiparisNo=?
            """,(siparisNo)
        )[0]

        model = SiparislerModel()

        model.id = result.ID
        model.siparisNo = result.SiparisNo
        model.siparisTarihi = tarihIslem.getDate(result.SiparisTarihi).strftime("%d-%m-%Y")
        if result.TahminiYuklemeTarihi != None:
         model.TahminiyuklemeTarihi = tarihIslem.getDate(result.TahminiYuklemeTarihi).strftime("%d-%m-%Y")
        model.odemeTurId = result.OdemeTurID
        model.faturaKesimTurId = result.FaturaKesimTurID
        model.liman = result.AktarmaLimanAdi
        model.teslimTurId = result.TeslimTurID 
        model.musteriId = result.MusteriID
        model.pesinat = result.Pesinat 
        model.navlunFirma = result.NavlunFirma 
        model.navlunMekmarNot = result.NavlunMekmarNot
        model.ulkeId = result.UlkeId
        model.depo = result.depo_yukleme
        model.sigorta_id = result.sigorta_id
        if result.NavlunAlis != None: 
            model.navlunAlis = result.NavlunAlis
        if result.NavlunSatis != None: 
            model.navlunSatis = result.NavlunSatis 
        model.kullaniciId = result.KullaniciID 
        model.siparisDurumId = result.SiparisDurumID 
        model.uretimAciklama = result.UretimAciklama 
        model.sevkiyatAciklama = result.SevkiyatAciklama
        model.finansAciklama  = result.FinansAciklama 
        model.odemeAciklama = result.OdemeAciklama
        model.siparisSahibi = result.SiparisSahibi
        model.operasyon = result.Operasyon
        model.finansman = result.Finansman
        model.iade = result.Iade
        model.maya = self.__noneBooleanControl(result.MayaControl)
        if model.siparisDurumId == 3:
            model.yuklemeTarihi = tarihIslem.getDate(result.YuklemeTarihi).strftime("%d-%m-%Y")
        model.faturaNo = result.FaturaNo 
        model.siparisFaturaNo = result.SiparisFaturaNo       
        if result.Vade != None:
            model.vade = tarihIslem.getDate(result.Vade).strftime("%d-%m-%Y")
            
        if result.TahminiEtaTarihi != None:
            model.tahmini_eta = tarihIslem.getDate(result.TahminiEtaTarihi).strftime("%d-%m-%Y")    
        
        model.ulke = result.Ulke 
        if result.Komisyon != None:
            model.komisyon = result.Komisyon
        model.detayAciklama_1 = result.DetayAciklama_1
        model.detayAciklama_2 = result.DetayAciklama_2
        model.detayAciklama_3 = result.DetayAciklama_3
        model.detayAciklama_4 = result.DetayAciklama_4
        model.detayMekmarNot_1 = result.DetayMekmarNot_1
        model.detayMekmarNot_2 = result.DetayMekmarNot_2
        model.detayMekmarNot_3 = result.DetayMekmarNot_3
        model.iscilikTutar = self.__getIscilikTutar(result.SiparisNo)
        if result.MalBedeli != None:
            model.malBedeli = result.MalBedeli
        model.odemeAciklama =  result.OdemeAciklama
        if result.DetayTutar_1 != None:
            model.detayTutar_1 = result.DetayTutar_1
        if result.DetayTutar_2 != None:
            model.detayTutar_2 = result.DetayTutar_2
        if result.DetayTutar_3 != None:
            model.detayTutar_3 = result.DetayTutar_3
        if result.DetayTutar_4 != None:
            model.detayTutar_4 = result.DetayTutar_4    
        if result.DetayAlis_1 != None:
            model.detayAlis_1 = result.DetayAlis_1
        if result.DetayAlis_2 != None:
            model.detayAlis_2 = result.DetayAlis_2
        if result.DetayAlis_3 != None:
            model.detayAlis_3 = result.DetayAlis_3
        if result.EvrakGideri != None:
            model.evrakGideri = result.EvrakGideri 
        if result.sigorta_Tutar != None:
            model.sigorta_tutar = result.sigorta_Tutar     
        if result.sigorta_tutar_satis !=None:
            model.sigorta_tutar_satis = result.sigorta_tutar_satis
        model.konteynerAyrinti = result.KonteynerAyrinti
        model.konteynerNo = result.KonteynerNo
        if result.İlaclamaGideri != None:
            model.ilaclamaGideri = result.İlaclamaGideri
       
        if result.Eta != None:
            model.eta = tarihIslem.getDate(result.Eta).strftime("%d-%m-%Y")
        model.digerTutarToplam = model.detayTutar_1 + model.detayTutar_2 + model.detayTutar_3 
        model.mekus_masraf = model.detayTutar_4
        model.genelToplam = model.navlunSatis + model.malBedeli + model.digerTutarToplam

       
        return model

    def __noneBooleanControl(self,value):
        if(value == None):
            return False
        else:
            return value
    
    def __getSiparisUrunler(self,siparisNo):

        result = self.data.getStoreList(
            """
            select
            *,
            (Select t.FirmaAdi from TedarikciTB t where t.ID=s.TedarikciID) as TedarikciAdi,
            (Select u.BirimAdi from UrunBirimTB u where u.ID=s.UrunBirimID) as urunbirimadi,
            dbo.Get_UrunAdi(s.UrunKartID) as UrunAdi,
            dbo.Get_Olcu_En(s.UrunKartID) as En,
            dbo.Get_Olcu_Boy(s.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(s.UrunKartID) as Kenar,
            dbo.Get_KenarIslem(s.UrunKartID) as YuzeyIslem,
             (select m.Marketing from SiparislerTB a , MusterilerTB m  where a.SiparisNo=s.SiparisNo and m.ID=a.MusteriID ) as musteri,
            s.UrunKartID
            from
            SiparisUrunTB s
            where s.SiparisNo=?
            order by s.SiraNo asc
            """,(siparisNo)
        )

        siparisList = list()

        for item in result:

            model = SiparisGirisUrunModel()

            model.id = item.ID 
            model.iscilik = self.__getIscilik(siparisNo,item.UrunKartID)
            model.siparisNo = item.SiparisNo 
            model.tedarikciId = item.TedarikciID 
            model.urunKartId = item.UrunKartID 
            model.urunBirimId = item.UrunBirimID 
            model.urunbirimAdi = item.urunbirimadi 
            model.miktar = item.Miktar 
            model.ozelMiktar = item.OzelMiktar 
            model.kasaAdet = item.KasaAdet 
            model.satisFiyati = item.SatisFiyati 
            model.satisToplam = item.SatisToplam 
            model.uretimAciklama = item.UretimAciklama 
            model.musteriAciklama = item.MusteriAciklama 
            model.pazarlama = item.musteri
            model.notlar = item.Notlar 
            model.kullaniciId = item.KullaniciID 
            model.alisFiyati = item.AlisFiyati 
            model.alisFiyati_Tl = item.AlisFiyati_TL
            model.siraNo = item.SiraNo 
            model.tedarikciAdi = item.TedarikciAdi
            m2,mt,ton,adet = self.__getMiktar(model.urunBirimId,model.miktar)
            
            if(model.urunBirimId == 1):
                model.m2 = m2
                model.adet = item.Adet
                model.mt = mt
                model.whatMultiplyM2 = '#fcaca7'
                model.whatMultiplyAdet = ""
                model.whatMultiplyMt = ""
                
            elif(model.urunBirimId == 2):
                model.m2 = self.__getM2Hesaplama(item.En,item.Boy,item.Miktar)
                model.adet = item.Miktar
                model.mt = mt
                model.whatMultiplyM2 = ''
                model.whatMultiplyAdet = "#fcaca7"
                model.whatMultiplyMt = ""
                
            else:
                getAdet,getM2 = self.__getMtHesaplama(item.En,item.Boy,item.Miktar)
                model.m2 = getM2
                model.mt = mt 
                model.adet = getAdet
                model.whatMultiplyM2 = ''
                model.whatMultiplyAdet = ""
                model.whatMultiplyMt = "#fcaca7"
            model.ton = item.Ton
            model.urunAdi = item.UrunAdi
            model.en = item.En 
            model.boy = item.Boy 
            model.kenar = item.Kenar 
            model.yuzeyIslem = item.YuzeyIslem
            siparisList.append(model)

        return siparisList

    def __getMiktar(self,urunBirim,miktar):

        m2 = 0
        mt = 0
        ton = 0
        adet = 0

        if urunBirim == 1:
            m2 = miktar 
        if urunBirim == 2:
            adet = miktar 
        if urunBirim == 3:
            mt = miktar
        if urunBirim == 4:
            ton = miktar

        return m2,mt,ton,adet
    
    def __getAdetHesaplama(self,en,boy,miktar):
        if(en == 'FR' or
           en == 'FRENCH' or
           en == 'VAR' or 
           en =='Various' or 
           en =='ANT' or 
           en == 'SLAB' or 
           en == '1 LT' or 
           en == 'Crazy' or 
           boy=='Free' or 
           boy == 'FREE' or
           en == 'Other' or 
           boy=='Other' or
           en == 'SET' or
           boy == 'MINI' or 
           boy =='SET' or
           en =='MINI'
           ):
            return 0
        else:
            
            return int((float(str(miktar).replace(',','.')) / (float(str(en).replace(',','.'))/100) / (float(str(boy).replace(',','.'))/100)))
    
    def __getM2Hesaplama(self,en,boy,miktar):
        if(en == 'FR' or
           en == 'FRENCH' or
           en == 'VAR' or 
           en =='Various' or 
           en =='ANT' or 
           en == 'SLAB' or 
           en == '1 LT' or 
           en == 'Crazy' or 
           boy=='Free' or 
           boy == 'FREE' or
           en == 'Other' or 
           boy=='Other' or
           en == 'SET' or
           boy == 'MINI' or 
           boy =='SET' or
           en =='MINI' or
           boy == 'VAR'
           ):
            return 0
        else:
            
            return (float(str(miktar).replace(',','.')) * (float(str(en).replace(',','.'))/100) * (float(str(boy).replace(',','.'))/100))
    
    def __getMtHesaplama(self,en,boy,miktar):
        if(en == 'FR' or
           en == 'FRENCH' or
           en == 'VAR' or 
           en =='Various' or 
           en =='ANT' or 
           en == 'SLAB' or 
           en == '1 LT' or 
           en == 'Crazy' or 
           en == 'Other' or 
           boy=='Other' or
           en == 'SET' or
           boy == 'MINI' or 
           boy =='SET' or
           en =='MINI' or 
           boy == 'VAR' 
           ):
            return 0,0
        elif (boy == 'Free' or boy == 'FREE'):
            adet = 0
            m2 = float(str(miktar).replace(',','.')) * (float(str(en).replace(',','.'))/100)
            return adet, m2
        else:
            m2 = float(str(miktar).replace(',','.')) * (float(str(en).replace(',','.'))/100)
            adet = int(m2 / (float(str(en).replace(',','.'))/100) / (float(str(boy).replace(',','.'))/100))
            return adet, m2
    
    
    
    def siparisKaydet(self,urunler,siparis):
       
      siparisKayitDurum = self.__siparisDataKayit(siparis)
      if siparisKayitDurum == True:
          
          marketing = self.__getMarketing(siparis['musteriId'])
          
          urunKayitDurum = self.__siparisUrunDataKayit(urunler,siparis['siparisNo'],marketing,siparis['musteriId'])
          if urunKayitDurum == True:
              self.mailGonderInsert(siparis,siparis['siparisNo']) #yeni sipariş için
              if siparis['faturaKesimTurId'] == 1:
                info2 = siparis['kayit_kisi']  + ' ' + siparis['siparisNo'] + ' siparişini girdi.'
                yukleme_tarihi=""
                renk = '#ffec31'
                DegisiklikMain().setMaliyetDegisiklik(info2,siparis['kayit_kisi'],siparis['siparisNo'],yukleme_tarihi,renk)
              
              return True
          else:
              self.__siparisDataSil(siparis['siparisNo'])
              self.__siparisUrunDataSilHepsi(siparis['siparisNo'])
              return False
      else:
          self.__siparisDataSil(siparis['siparisNo'])
          return False
    def __birim(self,id):
        if id == 1:
            return 'M2'
        elif id == 2:
            return 'Adet'
        elif id ==3:
            return 'MT'
        elif id == 4:
            return 'Ton'
        elif id == 5:
            return 'Sqft'
    def siparisGuncelle(self,siparis,urunlerYeni,urunlerDegisenler,urunlerSilinenler,degisenMasraflar):

        
        try:
            if(len(degisenMasraflar)>0):
                  
                mailListesi = []
                for item in degisenMasraflar:
                    if(item['isChange'] == 1):
                        mailListesi.append(self.__maliyetDegisimSendMail(item,siparis['siparisNo']))

                if siparis['faturaKesimTurId'] == 1:
                    for item in mailListesi:
                        info = item['degisenAdi'] + ' $' + str(item['eskiDeger']) + ' dan $' + str(item['yeniDeger']) + ' e değişti.'
                        renk = '#ffec31'
                        DegisiklikMain().setMaliyetDegisiklik(info,siparis['kayit_kisi'],siparis['siparisNo'],siparis['yuklemeTarihi'],renk)

            if(siparis['siparisDurumId']==1 and (siparis['odemeTurId']==1 or siparis['odemeTurId'] ==2) ):
                MailService(siparis['siparisNo'] + " nolu Sipariş Tahsil Edilmeli", "huseyin@mekmarmarble.com", siparis['siparisNo'] + ' nolu yeni sipariş bekleyende, tahsilatını gerçekleştirip üretime alınız!') 

            for item in urunlerDegisenler:
                item['miktar'] = float(item['miktar'])
            self.__siparisDataGuncelle(siparis)
            
            marketing = self.__getMarketing(siparis['musteriId'])
            
            self.__siparisUrunDataKayit(urunlerYeni,siparis['siparisNo'],marketing,siparis['musteriId'])
            if len(urunlerDegisenler) >= 1 : # ürün değiştirme 
              self.mailGonderUpdate(siparis,urunlerDegisenler,siparis['siparisNo'])
            

              
            self.__siparisUrunDataGuncelle(urunlerDegisenler)
            self.__siparisUrunDataSil(urunlerSilinenler)
            
        
            

            if len(urunlerYeni) >= 1 : #yeni ürün ekleme
              info = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' ' +  'Yeni Ürün Ekledi.'
              DegisiklikMain().setYapilanDegisiklikBilgisi(siparis['kayit_kisi'],info)
              self.mailGonderNew(siparis,urunlerYeni,siparis['siparisNo'])
              if(siparis['faturaKesimTurId'] == 1):
                for item in urunlerYeni:
                    info2 = siparis['kayit_kisi']  + ' ' + item['urunAdi'] +' '+ item['yuzeyIslem'] +' '+ item['en']+'x'+item['boy'] + 'x' + item['kenar'] + ' (' + item['miktar'] + ' ' + item['urunbirimAdi'] + ') $' + item['satisFiyati'] + ' ' + siparis['siparisNo'] + ' Siparişine Yeni Kalem Olarak Ekledi.'
                    yukleme_tarihi=""
                    result = self.data.getStoreList("""
                                                            select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                    """,(siparis['siparisNo']))
                    renk = '#ffec31'
                    if(result[0][0] == None or result[0][0] == ""):
                        yukleme_tarihi=""
                        DegisiklikMain().setMaliyetDegisiklik(info2,siparis['kayit_kisi'],siparis['siparisNo'],yukleme_tarihi,renk)
                    else:
                        DegisiklikMain().setMaliyetDegisiklik(info2,siparis['kayit_kisi'],siparis['siparisNo'],result[0][0],renk)
                    
            
              if(len(urunlerYeni) == 1):
                degisiklik = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' siparişine ' + urunlerYeni[0]['uretimAciklama'] + ', ' + str(urunlerYeni[0]['miktar']) +' ' + self.__birim(urunlerYeni[0]['urunBirimId']) + ' $'+str(urunlerYeni[0]['satisFiyati']) +' dan eklemiştir.'
                degisiklikAlani = 'Siparişler'
                islem2 = DegisiklikTahmin()
                pazarlama = ""
                if(siparis['faturaKesimTurId']==1):
                    pazarlama = 'Mekmar'
                if(siparis['faturaKesimTurId']==2):
                    pazarlama = 'Efes'
                if(siparis['faturaKesimTurId']==3):
                    pazarlama = 'Mekmer'
                now = datetime.datetime.now()
                year = now.strftime("%Y")
                month = now.strftime("%m")
                day = now.strftime("%d")
                hour = now.strftime("%H")
                minute = now.strftime("%M")
                second = now.strftime("%S")
                watch = str(hour) + ' : ' + str(minute) + ' : ' +  str(second)
                islem2.kaydet(degisiklik,degisiklikAlani,pazarlama,year,month,day,watch)     
              else:
                  for item in urunlerYeni:
                      degisiklik = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' siparişine ' + item['uretimAciklama'] + ', ' + str(item['miktar']) +' ' + self.__birim(item['urunBirimId']) + ' $'+str(item['satisFiyati']) +' dan eklemiştir.'
                      degisiklikAlani = 'Siparişler'
                      islem2 = DegisiklikTahmin()
                      pazarlama = ""
                      if(siparis['faturaKesimTurId']==1):
                         pazarlama = 'Mekmar'
                      if(siparis['faturaKesimTurId']==2):
                        pazarlama = 'Efes'
                      if(siparis['faturaKesimTurId']==3):
                          pazarlama = 'Mekmer'
                      now = datetime.datetime.now()
                      year = now.strftime("%Y")
                      month = now.strftime("%m")
                      day = now.strftime("%d")
                      hour = now.strftime("%H")
                      minute = now.strftime("%M")
                      second = now.strftime("%S")
                      watch = str(hour) + ' : ' + str(minute) + ' : ' +  str(second)
                      islem2.kaydet(degisiklik,degisiklikAlani,pazarlama,year,month,day,watch) 
            
            
            elif len(urunlerSilinenler) >= 1 : # ürün silindi ise
              info = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' ' +  'Bir Ürün Kalemi Silindi.'
              DegisiklikMain().setYapilanDegisiklikBilgisi(siparis['kayit_kisi'],info)
              self.mailGonderDelete(siparis,urunlerSilinenler,siparis['siparisNo'])
              if(siparis['faturaKesimTurId'] == 1):
                for item in urunlerSilinenler:
                    
                    info2 = siparis['kayit_kisi']  + ' ' + urunlerSilinenler[0]['uretimAciklama'] + ' (' + str(urunlerSilinenler[0]['miktar']) +' ' + self.__birim(urunlerSilinenler[0]['urunBirimId']) + ') $'+str(urunlerSilinenler[0]['satisFiyati']) +' ' +siparis['siparisNo'] + ' siparişinden bir kalemi sildi.'
                    
                    result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis['siparisNo']))
                    renk = '#ffec31'
                    if(result[0][0] == None or result[0][0] == ""):
                        yukleme_tarihi = ""
                        DegisiklikMain().setMaliyetDegisiklik(info2,siparis['kayit_kisi'],siparis['siparisNo'],yukleme_tarihi,renk)
                    else:
                        DegisiklikMain().setMaliyetDegisiklik(info2,siparis['kayit_kisi'],siparis['siparisNo'],result[0][0],renk)
                    
                
              if(len(urunlerSilinenler) == 1):
                degisiklik = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' siparişine ' + urunlerSilinenler[0]['uretimAciklama'] + ', ' + str(urunlerSilinenler[0]['miktar']) +' ' + self.__birim(urunlerSilinenler[0]['urunBirimId']) + ' $'+str(urunlerSilinenler[0]['satisFiyati']) +' dan silinmiştir.'
                degisiklikAlani = 'Siparişler'
                islem2 = DegisiklikTahmin()
                pazarlama = ""
                if(siparis['faturaKesimTurId']==1):
                    pazarlama = 'Mekmar'
                if(siparis['faturaKesimTurId']==2):
                    pazarlama = 'Efes'
                if(siparis['faturaKesimTurId']==3):
                    pazarlama = 'Mekmer'
                now = datetime.datetime.now()
                year = now.strftime("%Y")
                month = now.strftime("%m")
                day = now.strftime("%d")
                hour = now.strftime("%H")
                minute = now.strftime("%M")
                second = now.strftime("%S")
                watch = str(hour) + ' : ' + str(minute) + ' : ' +  str(second)
                islem2.kaydet(degisiklik,degisiklikAlani,pazarlama,year,month,day,watch)     
              else:
                  for item in urunlerSilinenler:
                      degisiklik = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' siparişine ' + item['uretimAciklama'] + ', ' + str(item['miktar']) +' ' + self.__birim(item['urunBirimId']) + ' $'+str(item['satisFiyati']) +' dan silinmiştir.'
                      degisiklikAlani = 'Siparişler'
                      islem2 = DegisiklikTahmin()
                      pazarlama = ""
                      if(siparis['faturaKesimTurId']==1):
                         pazarlama = 'Mekmar'
                      if(siparis['faturaKesimTurId']==2):
                        pazarlama = 'Efes'
                      if(siparis['faturaKesimTurId']==3):
                          pazarlama = 'Mekmer'
                      now = datetime.datetime.now()
                      year = now.strftime("%Y")
                      month = now.strftime("%m")
                      day = now.strftime("%d")
                      hour = now.strftime("%H")
                      minute = now.strftime("%M")
                      second = now.strftime("%S")
                      watch = str(hour) + ' : ' + str(minute) + ' : ' +  str(second)
                      islem2.kaydet(degisiklik,degisiklikAlani,pazarlama,year,month,day,watch)
            info = siparis['kayit_kisi'].capitalize() + ', ' + siparis['siparisNo'] + ' ' +  'Sipariş Bilgileri Değiştirildi.'
            DegisiklikMain().setYapilanDegisiklikBilgisi(siparis['kayit_kisi'],info)
            data = {
                'status':True,
            }
          
            
              
            return data
        except Exception as e:
            print('siparisGuncelle Hata 2 : ',str(e))
            return False
    
    def __maliyetDegisimSendMail(self,yeniItem,siparisno):
        
        for item in self.firstOrdersList:
            if item.SiparisNo == siparisno:
                if(yeniItem['label'] == 'Navlun Satış'):
                    eskiDeger = self.__noneControl(item.NavlunSatis)
                    yeniDeger = self.__noneControl(yeniItem['navlun_satis_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Navlun Alış'):
                    eskiDeger = self.__noneControl(item.NavlunAlis)
                    yeniDeger = self.__noneControl(yeniItem['navlun_alis_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Detay Satış 1'):
                    eskiDeger = self.__noneControl(item.DetayTutar_1)
                    yeniDeger = self.__noneControl(yeniItem['detay_tutar1_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Detay Satış 2'):
                    eskiDeger = self.__noneControl(item.DetayTutar_2)
                    yeniDeger = self.__noneControl(yeniItem['detay_tutar2_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Detay Satış 3'):
                    eskiDeger = self.__noneControl(item.DetayTutar_3)
                    yeniDeger = self.__noneControl(yeniItem['detay_tutar3_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Mekus Masrafı'):
                    eskiDeger = self.__noneControl(item.Mekus)
                    yeniDeger = self.__noneControl(yeniItem['mekus_masrafi_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Detay Alış 1'):
                    eskiDeger = self.__noneControl(item.DetayAlis_1)
                    yeniDeger = self.__noneControl(yeniItem['detay_alis1_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Detay Alış 2'):
                    eskiDeger = self.__noneControl(item.DetayAlis_2)
                    yeniDeger = self.__noneControl(yeniItem['detay_alis2_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Detay Alış 3'):
                    eskiDeger = self.__noneControl(item.DetayAlis_3)
                    yeniDeger = self.__noneControl(yeniItem['detay_alis3_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Komisyon'):
                    eskiDeger = self.__noneControl(item.Komisyon)
                    yeniDeger = self.__noneControl(yeniItem['komisyon_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Evrak Gideri'):
                    eskiDeger = self.__noneControl(item.EvrakGideri)
                    yeniDeger = self.__noneControl(yeniItem['evrak_gideritutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Sigorta Satış'):
                    eskiDeger = self.__noneControl(item.SigortaSatis)
                    yeniDeger = self.__noneControl(yeniItem['sigorta_satis_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
                elif (yeniItem['label'] == 'Sigorta Alış'):
                    eskiDeger = self.__noneControl(item.SigortaTutar)
                    yeniDeger = self.__noneControl(yeniItem['sigorta_alis_tutar'])
                    degisenAdi = yeniItem['label']
                    return {'eskiDeger':eskiDeger,'yeniDeger':yeniDeger,'degisenAdi':degisenAdi}
            else:
                continue         
    
    
    def __noneControl(self,value):
        if(value != None):
            return float(value)
        else:
            return 0
    
    
    def dateConvert(self,date_v):
        if (date_v) : 
            forMat = '%d-%m-%Y'
            date_v = datetime.datetime.strptime(date_v, forMat)
            return date_v.date()
        else:
            return None

    def __siparisDataKayit(self,siparis):
        
        try:
            
                
                s_tarihi = self.dateConvert(siparis['siparisTarihi'])
                t_yukleme_tarihi = self.dateConvert(siparis['TahminiyuklemeTarihi'])
                vade = None 
                if siparis['vade'] != None:
                    vade = self.dateConvert(siparis['vade'])
                    
                if siparis['tahmini_eta'] != None:
                    tahmini_eta = self.dateConvert(siparis['tahmini_eta'])



                self.data.update_insert(
                    """
                    insert into SiparislerTB (
                        SiparisNo,SiparisTarihi,OdemeTurID,TeslimTurID,MusteriID,Pesinat,NavlunFirma,NavlunMekmarNot,NavlunAlis,
                        NavlunSatis,KullaniciID,SiparisDurumID,UretimAciklama,SevkiyatAciklama,FinansAciklama,OdemeAciklama,TahminiYuklemeTarihi,
                        Vade,Ulke,UlkeId,Komisyon,DetayAciklama_1,DetayMekmarNot_1,DetayTutar_1,DetayAlis_1,DetayAciklama_2,DetayMekmarNot_2,
                        DetayTutar_2,DetayAlis_2,DetayAciklama_3,DetayMekmarNot_3,DetayTutar_3,DetayTutar_4,DetayAciklama_4,DetayAlis_3,SiparisSahibi,EvrakGideri,Eta,
                        KonteynerAyrinti,KonteynerNo,TeslimYeri,FaturaKesimTurID,AktarmaLimanAdi,depo_yukleme,sigorta_id,sigorta_Tutar,Operasyon ,Finansman,Iade,sigorta_tutar_satis,TahminiEtaTarihi,MayaControl
                    )
                    values
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,(
                        siparis['siparisNo'],s_tarihi,siparis['odemeTurId'],siparis['teslimTurId'],siparis['musteriId'],
                        siparis['pesinat'],siparis['navlunFirma'],siparis['navlunMekmarNot'],float(siparis['navlunAlis']),float(siparis['navlunSatis']),
                        siparis['kullaniciId'],siparis['siparisDurumId'],siparis['uretimAciklama'],siparis['sevkiyatAciklama'],
                        siparis['finansAciklama'],siparis['odemeAciklama'],t_yukleme_tarihi,vade,siparis['ulke'],siparis['ulkeId'],siparis['komisyon'],
                        siparis['detayAciklama_1'],siparis['detayMekmarNot_1'],float(siparis['detayTutar_1']),float(siparis['detayAlis_1']),
                        siparis['detayAciklama_2'],siparis['detayMekmarNot_2'],siparis['detayTutar_2'],float(siparis['detayAlis_2']),
                        siparis['detayAciklama_3'],siparis['detayMekmarNot_3'],float(siparis['detayTutar_3']),float(siparis['detayTutar_4']),siparis['detayAciklama_4'],float(siparis['detayAlis_3']),siparis['siparisSahibi'],
                        siparis['evrakGideri'],siparis['eta'],siparis['konteynerAyrinti'],siparis['konteynerNo'],siparis['teslimYeri'],siparis['faturaKesimTurId'],siparis['liman'],siparis['depo'], 
                        siparis['sigorta_id'],float(siparis['sigorta_tutar']),siparis['operasyon'],siparis['finansman'],siparis['iade'],float(siparis['sigorta_tutar_satis']),tahmini_eta,siparis['maya']
                    )
                )
                
                return True
        except Exception as e :
            print('Sipariş Data Kayıt Hata : ', str(e))
            return False

    def siparisDataKayitControl(self,siparisNo):
        result = self.data.getStoreList("""
                                            select * from SiparislerTB where SiparisNo=?
                                       """,(siparisNo))
        if len(result) > 0:
            return False
        else:
            return True
    
    def __siparisUrunDataKayit(self,urunler,siparisNo,marketing,musteriid):
            
            for item in urunler:
                
                ozelMiktar = self.decimalDegerKontrol(item['ozelMiktar'])
                ton = self.decimalDegerKontrol(item['ton'])
                if(marketing != 'Mekmar'):
                        if (item['tedarikciAdi'] == 'Mekmer' or  item['tedarikciAdi'] == 'Mek-Moz'):
                          item['alisFiyati']  = float(item['satisFiyati'] )* 0.85  
                self.data.update_insert(
                    """
                    insert into SiparisUrunTB (
                        SiparisNo,TedarikciID,UrunKartID,UrunBirimID,Miktar,OzelMiktar,KasaAdet,
                        SatisFiyati,SatisToplam,UretimAciklama,MusteriAciklama,
                        AlisFiyati,AlisFiyati_TL,SiraNo,Ton,musteriID,Adet
                    )
                    values
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,(
                        siparisNo,item['tedarikciId'],item['urunKartId'],item['urunBirimId'],
                        item['miktar'],ozelMiktar,item['kasaAdet'],item['satisFiyati'],
                        item['satisToplam'],item['uretimAciklama'],item['musteriAciklama'],
                        item['alisFiyati'],item['alisFiyati_Tl'],item['siraNo'],ton,musteriid,item['adet']
                    )
                )
           
            print('def __siparisUrunDataKayit')
            return True

    def decimalDegerKontrol(self,value):
        try:
            deger = float(value)
            return deger
        except:
            return 0

    def __siparisDataSil(self,siparisNo):

        self.data.update_insert(
            """
            delete from SiparislerTB where SiparisNo=?
            """,(siparisNo)
        )
    
    def __siparisUrunDataSilHepsi(self,siparisNo):

        self.data.update_insert(
            """
            delete from SiparisUrunTB where SiparisNo=?
            """,(siparisNo)
        )
        
    def __siparisUrunDataSil(self,urunler):

        try :
           
            for item in urunler:

                self.data.update_insert(
                    """
                    delete from SiparisUrunTB where ID=?
                    """,(item['id'])
                )
        
              
            return True
        except Exception as e:
            print('__siparisUrunDataSil : Hata : ', str(e))
            return False

    def __siparisDataGuncelle(self,siparis):
        try: 
            vade = None 
            siparis['TahminiyuklemeTarihi'] = self.dateConvert(siparis['TahminiyuklemeTarihi'])
            if siparis['vade'] != None:
                vade = self.dateConvert(siparis['vade']) 
            if siparis['tahmini_eta'] != None:
                tahmini_eta = self.dateConvert(siparis['tahmini_eta'])
            result = self.data.getStoreList("""
                select dhl from YeniTeklif_UlkeTB WHERE Id = ?

            """,(siparis['ulkeId']))
            cprz_kur_dhl = self.data.getStoreList("""
                    select DhlFiyat from DhlFiyatlari where ID = ?
            """,(result[0]))


            
            if siparis['yuklemeTarihi'] and siparis['teslimTurId'] != 5 and siparis['teslimTurId'] != 6 and siparis['teslimTurId'] !=12 and siparis['musteriId'] != 3444:
                
                yuklemeTarihi = self.dateConvert(siparis['yuklemeTarihi'])
                d = DovizListem()
                gun = yuklemeTarihi.day
                ay = yuklemeTarihi.month
                yil = yuklemeTarihi.year
                capraz_kur = d.getDovizKurListe(yil,ay,gun)
                evrak_gider = float(cprz_kur_dhl[0][0]) *  1.25 * float(capraz_kur) 
                evrak_gider = round(evrak_gider,2)

                

            else:
                evrak_gider = 0
            result=self.data.update_insert(
                """
                update SiparislerTB set OdemeTurID=?,TeslimTurID=?,Pesinat=?,NavlunFirma=?,NavlunMekmarNot=?,
                NavlunAlis=?,NavlunSatis=?,KullaniciID=?,UretimAciklama=?,SevkiyatAciklama=?,FinansAciklama=?,
                OdemeAciklama=?,TahminiYuklemeTarihi=?, SiparisFaturaNo=?,Vade=?,Ulke=?,UlkeId=?,Komisyon=?,
                DetayAciklama_1=?,DetayMekmarNot_1=?,DetayTutar_1=?,DetayAlis_1=?,
                DetayAciklama_2=?,DetayMekmarNot_2=?,DetayTutar_2=?,DetayAlis_2=?,
                DetayAciklama_3=?,DetayMekmarNot_3=?,DetayTutar_3=?,DetayTutar_4=?,DetayAciklama_4=?,DetayAlis_3=?,SiparisSahibi=?,EvrakGideri=?,
                KonteynerAyrinti=?,KonteynerNo=?,FaturaKesimTurID =? ,AktarmaLimanAdi =? , depo_yukleme=? ,sigorta_id=?,sigorta_Tutar=?, Operasyon =? , 
                Finansman =?, Iade=?,sigorta_tutar_satis=?, MalBedeli=? , TahminiEtaTarihi=?,MayaControl = ? where SiparisNo=?
                """,(
                    siparis['odemeTurId'],siparis['teslimTurId'],siparis['pesinat'],siparis['navlunFirma'],siparis['navlunMekmarNot'],
                    float(siparis['navlunAlis']),float(siparis['navlunSatis']),siparis['kullaniciId'],siparis['uretimAciklama'],siparis['sevkiyatAciklama'],siparis['finansAciklama'],
                    siparis['odemeAciklama'], siparis['TahminiyuklemeTarihi'],siparis['siparisFaturaNo'],vade,siparis['ulke'],siparis['ulkeId'],siparis['komisyon'],
                    siparis['detayAciklama_1'],siparis['detayMekmarNot_1'],float(siparis['detayTutar_1']),float(siparis['detayAlis_1']),
                    siparis['detayAciklama_2'],siparis['detayMekmarNot_2'],float(siparis['detayTutar_2']),float(siparis['detayAlis_2']),
                    siparis['detayAciklama_3'],siparis['detayMekmarNot_3'],float(siparis['detayTutar_3']),float(siparis['detayTutar_4']),siparis['detayAciklama_4'],float(siparis['detayAlis_3']),
                    siparis['siparisSahibi'],evrak_gider,siparis['konteynerAyrinti'],siparis['konteynerNo'], siparis['faturaKesimTurId'],siparis['liman'],siparis['depo'], siparis['sigorta_id'],
                    float(siparis['sigorta_tutar']), siparis['operasyon'], siparis['finansman'],siparis['iade'],float(siparis['sigorta_tutar_satis']),siparis['malBedeli'],tahmini_eta,siparis['maya'],siparis['siparisNo']
                )
            )
            
            
            
            if siparis['siparisDurumId'] == 1 and siparis['odemeTurId']  == 3 :
                self.__siparisDurumGuncelle1(siparis['siparisNo']) 
            return True
        except Exception as e:
            print('__siparisDataGuncelle Hata  a : ',str(e))
            return False

    
    def __siparisDurumGuncelle1(self,siparis_no):
       

        try:

            self.data.update_insert(

                """
                update SiparislerTB set SiparisDurumID=2 where SiparisNo=?
                """,(siparis_no)
            )
            
           
            print("beklyen uretime gecti")
          
            return True 
        except Exception as e:
            print('__siparisDurumGuncelle1 Hata : ',str(e))             

    def __siparisUrunDataGuncelle(self,urunler):
        try:
            for item in urunler:
                    ton = self.decimalDegerKontrol(item['ton'])
                    if(item['pazarlama'] != 'Mekmar'):
                        if (item['tedarikciAdi'] == 'Mekmer' or  item['tedarikciAdi'] == 'Mek-Moz'):

                             item['AlisFiyati']  =  float(item['satisFiyati'] )* 0.85 
                    
                    self.data.update_insert(
                        """
                        update SiparisUrunTB set TedarikciID=?,UrunKartID=?,UrunBirimID=?,Miktar=?,
                        OzelMiktar=?,KasaAdet=?,SatisFiyati=?,SatisToplam=?,UretimAciklama=?,
                        MusteriAciklama=?,Notlar=?,KullaniciID=?,AlisFiyati=?,AlisFiyati_TL=?,
                        SiraNo=?,Ton=?,Adet=? where ID=?
                        """,(
                            item['tedarikciId'],item['urunKartId'],item['urunBirimId'],item['miktar'],
                            item['ozelMiktar'],item['kasaAdet'],item['satisFiyati'],item['satisToplam'],
                            item['uretimAciklama'],item['musteriAciklama'],item['notlar'],
                            item['kullaniciId'],item['alisFiyati'],item['alisFiyati_Tl'],item['siraNo'],ton,item['adet'],
                            item['id']
                        )
                    )
            
           
            return True
        except Exception as e:
            print('__siparisUrunDataGuncelle Hata : ',str(e))

    def __getIscilik(self,siparisNo,urunKartId):
        iscilik = ''
        for item in filter(lambda x: x.SiparisNo == siparisNo and x.UrunKartId == urunKartId,self.iscilikList):
            iscilik = item.FirmaAdi
        return iscilik

    def __getIscilikTutar(self,siparisNo):

        tutar = 0

        for item in filter(lambda x: x.SiparisNo == siparisNo,self.iscilikList):

            tutar += item.Tutar 
        
        return tutar

    
      
    def mailGonderInsert(self,siparis,siparis_no):
       
        
        result = self.data.getStoreList(
            """
            select 
            s.SiparisTarihi ,
		    s.SiparisDurumID,
            s.ID,
            s.SiparisNo,
            u.Miktar, 
            
            (select BirimAdi from UrunBirimTB t  where t.ID=u.UrunBirimID) as UrunBirimi,
            (select k.FirmaAdi from TedarikciTB k where k.ID=u.TedarikciID) as Tedarikci,
             u.UretimAciklama ,
            (select m.UrunAdi from UrunlerTB m where m.ID = n.UrunID) as urunadi,
            (select y.YuzeyIslemAdi from YuzeyKenarTB y where y.ID=n.YuzeyID) as yuzeyadi ,
            (select o.En  from OlculerTB o where o.ID=n.OlcuID) as En,
            (select o.Boy from OlculerTB o where o.ID=n.OlcuID) as Boy,
            (select o.Kenar  from OlculerTB o where o.ID=n.OlcuID) as Kenar,
		    (select p.KullaniciAdi  from KullaniciTB p where p.ID=s.SiparisSahibi) as SiparisSahibi,
            (select p.MailAdres  from KullaniciTB p where p.ID=s.Operasyon) as SiparisMail
           
            from
            SiparisUrunTB u ,SiparislerTB s ,UrunKartTB n 
            
            where 
            s.SiparisNo= u.SiparisNo 
            and u.UrunKartID = n.ID
		    and (s.SiparisDurumID=2)
            and s.SiparisNo=?
            order by s.SiparisTarihi desc
            """,(siparis_no)
        )
        baslik =  siparis['kayit_kisi'] + " tarafından işlendi ."
        body = """
        <table >
       
            <tr style ="background-color: #f2f2f2;">
                <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Sipariş Numarası
                </th>
                <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tedarikçi
                </th>
                <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Ürün Bilgisi 
                </th>
                 <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Üretim Açıklama 
                </th>
                 <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Miktarı
                </th>
                <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Sipariş Temsilcisi
                </th>
            </tr>
        """
         
      
        if siparis['siparisDurumId'] == 2:
            for item in result:
            
                body += f"""
            
                <tr style ="background-color: #ddd;">
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item.SiparisNo}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item.Tedarikci}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item.urunadi} {item.yuzeyadi} {item.En}x{item.Boy}x{item.Kenar}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                    {item.UretimAciklama}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item.Miktar} {item.UrunBirimi} 
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item.SiparisSahibi} 
                    </td>
                    
                </tr>
            
            
                """
            
            body = body + "</table>"
            mekmer = 0
            mekmoz = 0
            diger = 0
        
    
       
        
            for item in result:
                if item.Tedarikci == "Mekmer":
                    
                 mekmer +=1
                    
                if item.Tedarikci == "Mek-Moz":
                    
                    mekmoz +=1

                if item.Tedarikci != "Mek-Moz" and item.Tedarikci != "Mekmer":
                    
                    diger +=1    

            
            
            if  (mekmer >=1 ) and item.SiparisDurumID ==2:

                MailService(siparis_no + " Yeni Sipariş ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
            elif (mekmoz>=1) and item.SiparisDurumID == 2:
                MailService(siparis_no + " Yeni Sipariş ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
                
            
      
                
            if  (mekmoz + mekmer >=1) and item.SiparisDurumID ==2:
                    MailService(siparis_no + " Yeni Sipariş ", "mehmet@mekmer.com",  " "+ baslik + body) #Mehmet 
                  
                    
                    
            if  (diger >=1 ) and item.SiparisDurumID ==2:
                    MailService(siparis_no + " Yeni Sipariş ", "info@mekmar.com",  " " +baslik + body) #gizem
                    
                    
            if item.SiparisSahibi != 'Mehmet'  or item.SiparisSahibi != 'Gizem' : 
                  MailService(siparis_no + " Yeni Sipariş ",item.SiparisMail , " "+ baslik + body) #satıs temsilcisi
              

    def mailGonderNew(self,siparis,yeni,siparis_no):
       
        baslik =  siparis['kayit_kisi'] + " tarafından işlendi ."
       
        body = """
        <table >
       
            <tr style ="background-color: green;">
                <th style ="color: white;background-color: green;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Sipariş Numarası
                </th>
                <th style ="color: white;background-color:green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tedarikçi
                </th>
                <th  style ="color: white;background-color: green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Ürün Bilgisi 
                </th>
                 <th  style ="color: white;background-color: green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Üretim Açıklama 
                </th>
                 <th  style ="color: white;background-color: green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Miktarı
                </th>
               
            </tr>
        """
         
      
        if siparis['siparisDurumId'] == 2:
            for item in yeni:
                
                body += f"""
               
                <tr style ="background-color: #ddd;">
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {siparis_no}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                   { item['tedarikciAdi'] }
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                   {item['urunAdi']} {item['yuzeyIslem']} {item['en']}x{item['boy']}x{item['kenar']}
                    </td>
                     <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                    {item['uretimAciklama']}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item['miktar']} {item['urunbirimAdi']} 
                    </td>
                   
                    
                </tr>
            
            
                """
            
            body = body + "</table>"
            mekmer = 0
            mekmoz = 0
            diger = 0
        
    
       
        
            for item in yeni:
                if item['tedarikciAdi'] == "Mekmer":
                    
                 mekmer +=1
                    
                if item['tedarikciAdi'] == "Mek-Moz":
                    
                    mekmoz +=1

                if item['tedarikciAdi'] != "Mek-Moz" and item['tedarikciAdi'] != "Mekmer":
                    
                    diger +=1    

            
            
            if  (mekmer >=1 ) and siparis['siparisDurumId'] ==2 :

              MailService(siparis_no + " Yeni Eklenen Kalemler ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
            
                
            
      
                
            if  (mekmoz + mekmer >=1) and siparis['siparisDurumId'] ==2 :
                MailService(siparis_no + " Yeni Eklenen Kalemler ", "mehmet@mekmer.com",  " "+ baslik + body) #Mehmet 
            
                    
                    
            if  (diger >=1 ) and siparis['siparisDurumId'] ==2 :
                 MailService(siparis_no + " Yeni Eklenen Kalemler ", "info@mekmar.com",  " " +baslik + body) #gizem
                    
            sahibi , maili = self.__siparisDetayi(siparis_no)        
            if sahibi != 'Mehmet'  or sahibi != 'Gizem': 
                  MailService(siparis_no + " Yeni Eklenen Kalemler ", maili , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):  
       
  
       
    def mailGonderUpdate(self,siparis,degisen,siparis_no):
        
        degismeyen = list()
        if len(degisen)==1:
            
            degismeyen = self.data.getStoreList("""
                                                select 

                                                    s.ID,
                                                    s.SiparisNo,
                                                    s.AlisFiyati,
                                                    s.SatisFiyati,
                                                    s.Miktar,
                                                    s.UretimAciklama,
                                                    s.MusteriAciklama,
                                                    ur.BirimAdi,
                                                    t.FirmaAdi,
                                                    s.musteriID


                                                from 
                                                    SiparisUrunTB s,
                                                    UrunBirimTB ur,
                                                    TedarikciTB t 
                                                where 
                                                    s.ID=? and 
                                                    s.UrunBirimID = ur.ID and 
                                                    s.TedarikciID = t.ID
                                            
                                            """,(degisen[0]['id']) )
        else:
            for i in range(0,len(degisen)):
                degismeyen.append( self.data.getStoreList("""
                                                select 

                                                    s.ID,
                                                    s.SiparisNo,
                                                    s.AlisFiyati,
                                                    s.SatisFiyati,
                                                    s.Miktar,
                                                    s.UretimAciklama,
                                                    s.MusteriAciklama,
                                                    ur.BirimAdi,
                                                    t.FirmaAdi,
                                                    s.musteriID


                                                from 
                                                    SiparisUrunTB s,
                                                    UrunBirimTB ur,
                                                    TedarikciTB t 
                                                where 
                                                    s.ID=? and 
                                                    s.UrunBirimID = ur.ID and 
                                                    s.TedarikciID = t.ID
                                            
                                """,(degisen[i]['id']) ))
        
        
        baslik =  siparis['kayit_kisi'] + " tarafından işlendi ."
        
        body = """
        <table >
            <tr style ="background-color: orange;">
                <th style ="color: white;background-color: orange;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Durum
                </th>
                <th style ="color: white;background-color: orange;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Sipariş Numarası
                </th>
                <th style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tedarikçi
                </th>
                <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Ürün Bilgisi 
                </th>
                 <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Üretim Açıklama 
                </th>
                 <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Miktarı
                </th>
                </th>
                 <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Birim
                </th>
                <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Alış Fiyatı
                </th>
                <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Satış Fiyatı
                </th>
            </tr>
        """
        
                
            
        

        
        
        if siparis['siparisDurumId'] == 2:
            if len(degisen)==1:
                
                body += f"""
                        <tr style ="background-color: #ddd;">
                            <td style ="border: 1px solid #ddd;background-color:red;color:white;padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞTİRİLEN ↓↓↓
                                    
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][1]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][8]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][6]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                                {degismeyen[0][5]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][4]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][7]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {float(degismeyen[0][2])}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {float(degismeyen[0][3])}
                            </td>
                        </tr>
                
                
                        """
            
            
            else:
                for i in range(0,len(degisen)):
                    body += f"""
                        <tr style ="background-color: #ddd;">
                            <td style ="border: 1px solid #ddd;background-color:red;color:white;padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞTİRİLEN ↓↓↓
                                    
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][1]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][8]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][6]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                            {degismeyen[i][0][5]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {str(float(degismeyen[i][0][4]))}  
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][7]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {str(float(degismeyen[i][0][2]))}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {str(float(degismeyen[i][0][3]))}
                            </td>
                        </tr>
                
                
                        """

            sayac = 0
            for item in degisen:
                body += f"""
                    <tr style ="background-color: #ddd;">
                        <td style ="border: 1px solid #ddd;background-color:#2fc289;color:white; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞEN
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:#ddd;">
                            {siparis_no}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['tedarikciAdi'],sayac,degismeyen,1,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {item['tedarikciAdi']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['musteriAciklama'],sayac,degismeyen,7,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])};">
                            {item['musteriAciklama']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;background-color:{self.__kontrol(item['uretimAciklama'],sayac,degismeyen,2,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {item['uretimAciklama']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['miktar'],sayac,degismeyen,3,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {str(float(item['miktar']))}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['urunbirimAdi'],sayac,degismeyen,8,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {item['urunbirimAdi']} 
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['alisFiyati'],sayac,degismeyen,5,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {str(float(item['alisFiyati']))}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['satisFiyati'],sayac,degismeyen,6,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {str(float(item['satisFiyati']))}
                        </td>
                    </tr>
            
            
                """
                sayac += 1

            body = body + "</table>"
            mekmer = 0
            mekmoz = 0
            diger = 0
        
    
       
        
            for item in degisen:
               
                if item['tedarikciAdi'] == "Mekmer":
                    
                 mekmer +=1
                    
                if item['tedarikciAdi'] == "Mek-Moz":
                    
                    mekmoz +=1

                if item['tedarikciAdi'] != "Mek-Moz" and item['tedarikciAdi'] != "Mekmer":
                    
                    diger +=1    

            if  (mekmer >=1 ) and siparis['siparisDurumId'] == 2 :
              
              MailService(siparis_no +" Düzenlenen Kalemler ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
            elif (mekmoz>1) and siparis['siparisDurumId'] == 2:
                MailService(siparis_no +" Düzenlenen Kalemler ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
                
            if  (mekmoz + mekmer >=1) and siparis['siparisDurumId'] ==2 :
                 MailService(siparis_no +" Düzenlenen Kalemler ", "mehmet@mekmer.com",  " "+ baslik + body) #Mehmet
                 
                 

            if  (diger >=1 ) and  siparis['siparisDurumId'] ==2:
                   MailService(siparis_no +" Düzenlenen Kalemler ", "info@mekmar.com",  " " +baslik + body) #gizem
                   
                   
            sahibi , maili = self.__siparisDetayi(siparis_no)     
            if sahibi != 'Mehmet'  or sahibi != 'Gizem' or sahibi != 'İP': 
                  MailService(siparis_no +" Düzenlenen Kalemler ",  maili , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):
            # MailService(siparis_no +" Düzenlenen Kalemler ",  'bilgiislem@mekmar.com' , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):
                  
                  
        elif siparis['siparisDurumId'] == 3:
 
            if len(degisen)==1:
                
                body += f"""
                        <tr style ="background-color: #ddd;">
                            <td style ="border: 1px solid #ddd;background-color:red;color:white;padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞTİRİLEN ↓↓↓
                                    
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][1]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][8]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][6]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                                {degismeyen[0][5]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][4]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][7]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {float(degismeyen[0][2])}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {float(degismeyen[0][3])}
                            </td>
                        </tr>
                
                
                        """
            else:
                for i in range(0,len(degisen)):
                    body += f"""
                        <tr style ="background-color: #ddd;">
                            <td style ="border: 1px solid #ddd;background-color:red;color:white;padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞTİRİLEN ↓↓↓
                                    
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][1]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[i][0][8]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][6]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                            {degismeyen[i][0][5]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {float(degismeyen[i][0][4])} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][7]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {float(degismeyen[i][0][2])}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {float(degismeyen[i][0][3])}
                            </td>
                        </tr>
                
                
                        """
            
            baslik =  siparis['kayit_kisi'] + " tarafından işlendi ."
            sayac = 0
            for item in degisen:
                body += f"""
                    <tr style ="background-color: #ddd;">
                        <td style ="border: 1px solid #ddd;background-color:#2fc289;color:white; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞEN
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:#ddd;">
                            {siparis_no}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['tedarikciAdi'],sayac,degismeyen,1,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {item['tedarikciAdi']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['musteriAciklama'],sayac,degismeyen,7,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])};">
                            {item['musteriAciklama']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;background-color:{self.__kontrol(item['uretimAciklama'],sayac,degismeyen,2,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {item['uretimAciklama']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['miktar'],sayac,degismeyen,3,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {float(item['miktar'])} 
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['urunbirimAdi'],sayac,degismeyen,8,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {item['urunbirimAdi']} 
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['alisFiyati'],sayac,degismeyen,5,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {float(item['alisFiyati'])}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['satisFiyati'],sayac,degismeyen,6,siparis_no,siparis['kayit_kisi'],siparis['faturaKesimTurId'])}">
                            {float(item['satisFiyati'])}
                        </td>
                    </tr>
            
            
                """
                sayac += 1
                
                
            sahibi , maili = self.__siparisDetayi(siparis_no)
            MailService(siparis_no +" Düzenlenen Kalemler ", maili  , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):
            MailService(siparis_no +" Düzenlenen Kalemler ", 'info@mekmar.com'  , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):
            # MailService(siparis_no +" Düzenlenen Kalemler ", 'bilgiislem@mekmar.com'  , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):
            
            
            
    def degisimKontrol(self,degisen,degismeyen,itemName):

        for i in degisen:
            if itemName=='tedarikciAdi':
                if i[itemName] == self.degismeyenKontrol(degisen,degismeyen,8,i[itemName]):
                    return False
                else:
                    
                    return True
            elif itemName=='uretimAciklama':
                if i[itemName] == self.degismeyenKontrol(degisen,degismeyen,5,i[itemName]):
                    return False
                else:
                    return True
            elif itemName=='miktar':
                if i[itemName] == self.degismeyenKontrol(degisen,degismeyen,4,i[itemName]):
                    return False
                else:
                    
                    return True
            elif itemName=='alisFiyati':
                if i[itemName] == self.degismeyenKontrol(degisen,degismeyen,2,i[itemName]):
                    return False
                else:
                    return True
            elif itemName=='satisFiyati':
                if i[itemName] == self.degismeyenKontrol(degisen,degismeyen,3,i[itemName]):
                    return False
                else:
                    return True
           
    def degismeyenKontrol(self,degisen,degismeyen,value,itemValue):
        if len(degisen)==1:
            if degismeyen[0][value] == itemValue:
                return degismeyen[0][value]
            else:
                return degismeyen[0][value]
        else:
            for i in range(0,len(degisen)):
                if degismeyen[i][0][value] == itemValue:
                    return degismeyen[i][0][value]
                else:
                    return degismeyen[i][0][value]
               
                  
                   
    
    def mailGonderDelete(self,siparis,silinen,siparis_no):
       
        
       
        baslik =  siparis['kayit_kisi'] + " tarafından işlendi ."
      
        body = """
        <table >
       
            <tr>
                <th style ="color: white;background-color: red;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Sipariş Numarası
                </th>
                <th style ="color: white;background-color: red;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tedarikçi
                </th>
                <th  style ="color: white;background-color: red;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Ürün Bilgisi 
                </th>
                 <th  style ="color: white;background-color: red;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Üretim Açıklama 
                </th>
                 <th  style ="color: white;background-color: red;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Miktarı
                </th>
              
            </tr>
        """
         
        
        if siparis['siparisDurumId'] == 2:
            for item in silinen:
                
                body += f"""
               
                <tr style ="background-color: #ddd;">
                    <td style ="border: 1px solid #ddd;  padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {siparis_no}
                    </td>
                    <td style ="border: 1px solid #ddd;   padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                   { item['tedarikciAdi'] }
                    </td>
                    <td style ="border: 1px solid #ddd;   padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                   {item['urunAdi']} {item['yuzeyIslem']} {item['en']}x{item['boy']}x{item['kenar']}
                    </td>
                     <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                    {item['uretimAciklama']}
                    </td>
                    <td style ="border: 1px solid #ddd; padding: 8px;  color:Red ; font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                    {item['miktar']} {item['urunbirimAdi']} 
                    </td>
                   
                    
                </tr>
            
            
                """
            
            body = body + "</table>"
            mekmer = 0
            mekmoz = 0
            diger = 0
        
    
       
        
            for item in silinen:
                if item['tedarikciAdi'] == "Mekmer":
                    
                 mekmer +=1
                    
                if item['tedarikciAdi'] == "Mek-Moz":
                    
                    mekmoz +=1

                if item['tedarikciAdi'] != "Mek-Moz" and item['tedarikciAdi'] != "Mekmer":
                    
                    diger +=1    

            
            
            if  (mekmer >=1 ) and siparis['siparisDurumId'] ==2 :

                 MailService(siparis_no +" Silinen Kalemler " , "muhsin@mekmer.com"," "+ baslik + body) #muhsin
            
            if  (mekmoz + mekmer >=1) and siparis['siparisDurumId'] ==2 :
                    MailService(siparis_no +" Silinen Kalemler " , "mehmet@mekmer.com",  " "+ baslik + body) #Mehmet 
          
                    
                    
            if  (diger >=1 ) and siparis['siparisDurumId'] ==2 :
                    MailService(siparis_no +" Silinen Kalemler " , "info@mekmar.com",  " " +baslik + body) #gizem
                    
            sahibi , maili = self.__siparisDetayi(siparis_no)          
            if sahibi != 'Mehmet'  or sahibi != 'Gizem': 
                  MailService(siparis_no +" Silinen Kalemler " , maili  , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):  
        
    def __siparisDetayi(self,siparis_no):     
       
       result = self.data.getStoreList(
            """
        select 
            (select p.KullaniciAdi  from KullaniciTB p where p.ID=s.SiparisSahibi) as SiparisSahibi,
            (select p.MailAdres  from KullaniciTB p where p.ID=s.Operasyon) as SiparisMail
           
        from
            SiparislerTB s 
            
        where 
           
            s.SiparisNo=?
         """,(siparis_no)
        )
       
       for item in result:
        
          return item.SiparisSahibi , item.SiparisMail


    def mailGonderOp(self,username,orderNo,then,now,info):
        baslik =  username + " tarafından " + orderNo + " siparişinin " + info +  " değiştirildi ."
        thenKullanici,nowKullanici = self.__getKullaniciAdi(then,now)
        body = f"""
        <table >
       
            <tr style ="background-color: green;">
                <th  style ="color: white;background-color: green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Sipariş
                </th>
                <th  style ="color: white;background-color: green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 {info} Sahibi Eski
                </th>
                <th  style ="color: white;background-color: green ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 {info} Sahibi Yeni
                </th>
            </tr>
        """
        body += f"""
            
            <tr style ="background-color: #ddd;">
                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                {orderNo}
                </td>
                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                {thenKullanici}
                </td>
                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                {nowKullanici}
                </td>
                
            </tr>
        
        
            """
            
        body = body + "</table>"
           
        thenMail,nowMail = self.__getMailAdress(then,now)
            
        MailService(orderNo + " " + info + " sahibi değişti ", thenMail , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no): 
        MailService(orderNo + " " + info + " sahibi değişti ", nowMail , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no): 
 
             
	
    def __kontrol(self,item,sayac,degismeyen,durum,siparis_no,kayit_kisi,fatura_kesim_tur_id):

        
        
        
        
        if len(degismeyen)== 1:
            
            if durum == 1:
                
                if item != degismeyen[sayac][8]:
                    return "red"
                else:
                    return "#ddd"
            elif durum == 2:
                
                if item != degismeyen[sayac][5]:
                    return "red"
                else:
                    return "#ddd"
            elif durum == 3:
                
                if float(item) != float(degismeyen[sayac][4]):
                    degisiklik = str(degismeyen[sayac][1]) + ' siparişinin ' + str(degismeyen[sayac][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][4],2)) + ' ' + str(degismeyen[sayac][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][7]) +  ' e değiştirildi'
                    degisiklikAlani = 'Siparişler'
                    fatura = str(self.__getMarketing(degismeyen[sayac][9]))
                    islem2 = DegisiklikTahmin()
                    now = datetime.datetime.now()
                    year = now.strftime("%Y")
                    month = now.strftime("%m")
                    day = now.strftime("%d")
                    hour = now.strftime("%H")
                    minute = now.strftime("%M")
                    second = now.strftime("%S")
                    watch = str(hour) + ' : ' + str(minute) + ' : ' + str(second)
                    islem2.kaydet(degisiklik,degisiklikAlani,fatura,year,month,day,watch)
                    
                    if fatura_kesim_tur_id == 1:
                        degisiklik = str(degismeyen[sayac][1]) + ' siparişinin ' + str(degismeyen[sayac][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][4],2)) + ' ' + str(degismeyen[sayac][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][7]) +  ' e değiştirildi'
                        
                        result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis_no))
                        renk = '#ffec31'
                        if(result[0][0] == None or result[0][0] == ""):
                            
                            yukleme_tarihi=""
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,yukleme_tarihi,renk)
                        else:
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,result[0][0],renk)
                    
                    
                    return "red"
                else:
                    return "#ddd"
            elif durum == 4:
                if item != degismeyen[sayac][7]:
                    return "red"
                else:
                    return "yellow"
            elif durum == 5:
                if float(item) != float(degismeyen[sayac][2]):
                    degisiklik = str(degismeyen[sayac][1]) + ' siparişinin ' + str(degismeyen[sayac][5]) + ' kaleminin alış fiyatı ' +  '$' + str(round(degismeyen[sayac][2],2))+ ' ==> ' + '$' + str(item) +  ' e değiştirildi'
                    degisiklikAlani = 'Siparişler'
                    fatura = str(self.__getMarketing(degismeyen[sayac][9]))
                    islem2 = DegisiklikTahmin()
                    now = datetime.datetime.now()
                    year = now.strftime("%Y")
                    month = now.strftime("%m")
                    day = now.strftime("%d")
                    hour = now.strftime("%H")
                    minute = now.strftime("%M")
                    second = now.strftime("%S")
                    watch = str(hour) + ' : ' + str(minute) + ' : ' + str(second)
                    islem2.kaydet(degisiklik,degisiklikAlani,fatura,year,month,day,watch)
                    if fatura_kesim_tur_id == 1:
                        degisiklik = str(degismeyen[sayac][1]) + ' siparişinin ' + str(degismeyen[sayac][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][4],2)) + ' ' + str(degismeyen[sayac][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][7]) +  ' e değiştirildi'
                        
                        result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis_no))
                        renk = '#ffec31'
                        if(result[0][0] == None or result[0][0] == ""):
                            
                            yukleme_tarihi=""
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,yukleme_tarihi,renk)
                        else:
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,result[0][0],renk)
                    return "red"
                else:
                    return "#ddd"
            elif durum == 6:
                
                if float(item) != float(degismeyen[sayac][3]):
                    degisiklik = str(degismeyen[sayac][1]) + ' siparişinin ' + str(degismeyen[sayac][5]) + ' kaleminin satış fiyatı ' + '$' +  str(round(degismeyen[sayac][3],2))+ ' ==> '  + '$' + str(item) +  ' e değiştirildi'
                    degisiklikAlani = 'Siparişler'
                    fatura = str(self.__getMarketing(degismeyen[sayac][9]))
                    islem2 = DegisiklikTahmin()
                    now = datetime.datetime.now()
                    year = now.strftime("%Y")
                    month = now.strftime("%m")
                    day = now.strftime("%d")
                    hour = now.strftime("%H")
                    minute = now.strftime("%M")
                    second = now.strftime("%S")
                    watch = str(hour) + ' : ' + str(minute) + ' : ' + str(second)
                    islem2.kaydet(degisiklik,degisiklikAlani,fatura,year,month,day,watch)
                    if(fatura_kesim_tur_id == 1):
                        degisiklik = str(degismeyen[sayac][1]) + ' siparişinin ' + str(degismeyen[sayac][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][4],2)) + ' ' + str(degismeyen[sayac][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][7]) +  ' e değiştirildi'
                        
                        result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis_no))
                        renk = '#ffec31'
                        if(result[0][0] == None or result[0][0] == ""):
                            
                            yukleme_tarihi=""
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,yukleme_tarihi,renk)
                        else:
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,result[0][0],renk)
                    return "red"
                else:
                    return "#ddd"
            elif durum == 7:
                if item != degismeyen[sayac][6]:
                    
                    return "red"
                else:
                    return "#ddd"
            elif durum == 8:
                if item != degismeyen[sayac][7]:
                    
                    return "red"
                else:
                    return "#ddd"
        else:
            if durum == 1:
                
                if item != degismeyen[sayac][0][8]:
                    return "red"
                else:
                    return "#ddd"
            elif durum == 2:
                
                if item != degismeyen[sayac][0][5]:
                    return "red"
                else:
                    return "#ddd"
            elif durum == 3:
                
                if float(item) != float(degismeyen[sayac][0][4]):
                    degisiklik = str(degismeyen[sayac][0][1]) + ' siparişinin ' + str(degismeyen[sayac][0][5]) + ' kaleminin miktarı ' +  str(round(degismeyen[sayac][0][4],2)) + ' ' + str(degismeyen[sayac][0][7]) + ' ==> ' +  str(item) + ' ' +str(degismeyen[sayac][0][7]) + ' e değiştirildi'
                    degisiklikAlani = 'Siparişler'
                    fatura = str(self.__getMarketing(degismeyen[sayac][0][9]))
                    islem2 = DegisiklikTahmin()
                    now = datetime.datetime.now()
                    year = now.strftime("%Y")
                    month = now.strftime("%m")
                    day = now.strftime("%d")
                    hour = now.strftime("%H")
                    minute = now.strftime("%M")
                    second = now.strftime("%S")
                    watch = str(hour) + ' : ' + str(minute) + ' : ' + str(second)
                    islem2.kaydet(degisiklik,degisiklikAlani,fatura,year,month,day,watch)
                    if fatura_kesim_tur_id == 1:
                        degisiklik = str(degismeyen[sayac][0][1]) + ' siparişinin ' + str(degismeyen[sayac][0][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][0][4],2)) + ' ' + str(degismeyen[sayac][0][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][0][7]) +  ' e değiştirildi'
                        
                        result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis_no))
                        renk = '#ffec31'
                        if(result[0][0] == None or result[0][0] == ""):
                            
                            yukleme_tarihi=""
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,yukleme_tarihi,renk)
                        else:
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,result[0][0],renk)
                    return "red"
                else:
                    return "#ddd"
            elif durum == 4:
                if item != degismeyen[sayac][0][7]:
                    return "red"
                else:
                    return "#ddd"
            elif durum == 5:
                if float(item) != float(degismeyen[sayac][0][2]):
                    degisiklik = str(degismeyen[sayac][0][1]) + ' siparişinin ' + str(degismeyen[sayac][0][5]) + ' kaleminin alış fiyatı ' + '$' + str(round(degismeyen[sayac][0][2],2))+ ' ==> ' + '$' + str(item) +   ' e değiştirildi'
                    degisiklikAlani = 'Siparişler'
                    fatura = str(self.__getMarketing(degismeyen[sayac][0][9]))
                    
                    islem2 = DegisiklikTahmin()
                    now = datetime.datetime.now()
                    year = now.strftime("%Y")
                    month = now.strftime("%m")
                    day = now.strftime("%d")
                    hour = now.strftime("%H")
                    minute = now.strftime("%M")
                    second = now.strftime("%S")
                    watch = str(hour) + ' : ' + str(minute) + ' : ' + str(second)
                    islem2.kaydet(degisiklik,degisiklikAlani,fatura,year,month,day,watch)
                    if fatura_kesim_tur_id == 1:
                        degisiklik = str(degismeyen[sayac][0][1]) + ' siparişinin ' + str(degismeyen[sayac][0][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][0][4],2)) + ' ' + str(degismeyen[sayac][0][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][0][7]) +  ' e değiştirildi'
                        
                        result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis_no))
                        renk = '#ffec31'
                        if(result[0][0] == None or result[0][0] == ""):
                            
                            yukleme_tarihi=""
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,yukleme_tarihi,renk)
                        else:
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,result[0][0],renk)
                    return "red"
                else:
                    return "#ddd"
            elif durum == 6:
                if float(item) != float(degismeyen[sayac][0][3]):
                    degisiklik = str(degismeyen[sayac][0][1]) + ' siparişinin ' + str(degismeyen[sayac][0][5]) + ' kaleminin satış fiyatı ' + '$' + str(round(degismeyen[sayac][0][3]))+ ' ==> '  + '$' + str(item) +  ' e değiştirildi'
                    degisiklikAlani = 'Siparişler'
                    fatura = str(self.__getMarketing(degismeyen[sayac][0][9]))
                    
                    islem2 = DegisiklikTahmin()
                    now = datetime.datetime.now()
                    year = now.strftime("%Y")
                    month = now.strftime("%m")
                    day = now.strftime("%d")
                    hour = now.strftime("%H")
                    minute = now.strftime("%M")
                    second = now.strftime("%S")
                    watch = str(hour) + ' : ' + str(minute) + ' : ' + str(second)
                    islem2.kaydet(degisiklik,degisiklikAlani,fatura,year,month,day,watch)
                    if fatura_kesim_tur_id == 1:
                        degisiklik = str(degismeyen[sayac][0][1]) + ' siparişinin ' + str(degismeyen[sayac][0][5]) + ' kaleminin miktarı ' + str(round(degismeyen[sayac][0][4],2)) + ' ' + str(degismeyen[sayac][0][7]) +  ' ==> ' + str(item)  + ' ' + str(degismeyen[sayac][0][7]) +  ' e değiştirildi'
                        
                        result = self.data.getStoreList("""
                                                        select YuklemeTarihi from SiparislerTB where SiparisNo=?
                                                """,(siparis_no))
                        renk = '#ffec31'
                        if(result[0][0] == None or result[0][0] == ""):
                            
                            yukleme_tarihi=""
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,yukleme_tarihi,renk)
                        else:
                            DegisiklikMain().setMaliyetDegisiklik(degisiklik,kayit_kisi,siparis_no,result[0][0],renk)
                    return "red"
                else:
                    return "#ddd"
            elif durum == 7:
                    if item != degismeyen[sayac][0][6]:
                        return "red"
                    else:
                        return "#ddd"
            elif durum == 8:
                    if item != degismeyen[sayac][0][7]:
                        return "red"
                    else:
                        return "#ddd"
            
       
    def opChange(self,datas):
        info = datas['username'].capitalize() + ', ' + datas['orderNo'] + ' ' + datas['info']  + '  Degiştirdi.'
        DegisiklikMain().setYapilanDegisiklikBilgisi(datas['username'],info)
        self.mailGonderOp(datas['username'],datas['orderNo'],datas['then'],datas['now'],datas['info'])
        

    def __getMailAdress(self,then,now):
        thenMail = self.data.getStoreList("""
                                             select MailAdres from KullaniciTB where ID=?
                                          """,(then))
        nowMail = self.data.getStoreList("""
                                            select MailAdres from KullaniciTB where ID=?
                                         """,(now))
        
        return thenMail[0].MailAdres,nowMail[0].MailAdres
    
    def __getKullaniciAdi(self,then,now):
        thenKullaniciAdi = self.data.getStoreList("""
                                                   select KullaniciAdi from KullaniciTB where ID=?
                                                  
                                                  """,(then))
        nowKullaniciAdi = self.data.getStoreList("""
                                                   select KullaniciAdi from KullaniciTB where ID=?
                                                  
                                                  """,(now))
        return thenKullaniciAdi[0].KullaniciAdi,nowKullaniciAdi[0].KullaniciAdi
    
    
    def getchangeOdemeBilgisi(self,siparisNo,odemeTur):
        try:
            
            self.data.update_insert("""
                                        update SiparislerTB SET SiparisDurumID=1 where SiparisNo=?
                                    
                                    """,(siparisNo))
            self.data.update_insert("""
                                        update SiparislerTB SET OdemeTurID=? where SiparisNo=?
                                    
                                    """,(odemeTur,siparisNo))
            return True
        except Exception as e:
            print('getchangeOdemeBilgisi hata',str(e))
            return False
        
    def getchangeOdemeBilgisiEx(self,siparisNo,odemeTur):
        try:
            
            self.data.update_insert("""
                                        update SiparislerTB SET SiparisDurumID=2 where SiparisNo=?
                                    
                                    """,(siparisNo))
            self.data.update_insert("""
                                        update SiparislerTB SET OdemeTurID=? where SiparisNo=?
                                    
                                    """,(odemeTur,siparisNo))
            return True
        except Exception as e:
            print('getchangeOdemeBilgisi hata',str(e))
            return False
        
        
    def setContainerAdd(self,data):
        try:
            self.data.update_insert("""
                                        update SiparislerTB set KonteynirSayisi=? where SiparisNo=?

                                
                                
                                """,(data['amount'],data['siparisNo']))
            return True
        except Exception as e:
            print('setContainerAdd hata',str(e))
            return False
        
    def getContainerAmount(self,sipNo):
        try:
            result = self.data.getStoreList("""
                                    select KonteynirSayisi from SiparislerTB where SiparisNo=?
                                   
                                   """,(sipNo))
            liste = list()
            for item in result:
                
                model = ContainerAmountModel()
                model.container_amount = item.KonteynirSayisi
                liste.append(model)
            
            schema = ContainerAmountSchema(many = True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getContainerAmount hata',str(e))
            return False
        
    def deleteProforma(self,po):
        try:
            id = self.data.getStoreList("""
                                        select ID from SiparisFaturaKayitTB where SiparisNo=? and YuklemeEvrakID=2                                    
                                    
                                    """,(po))[0].ID
            self.data.update_insert("""
                                        delete SiparisFaturaKayitTB where ID=?

                                    """,(id))
            return True
        except Exception as e:
            print('deleteProforma hata',str(e))
            return False