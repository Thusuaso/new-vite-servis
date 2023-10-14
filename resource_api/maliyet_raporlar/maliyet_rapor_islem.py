from resource_api.maliyet_raporlar.siparisler import Siparisler,Siparisler_Yil,SiparislerKar
from resource_api.maliyet_raporlar.urunler import Urunler,Urunler_Yil
from resource_api.maliyet_raporlar.odemeler import Odemeler
from resource_api.maliyet_raporlar.masraflar import Masraflar,Masraflar_Yil
from models.ozel_maliyet import OzelMaliyetListeSchema,OzelMaliyetListeKarModel,OzelMaliyetListeKarSchema,OzelMaliyetListeModel,TedarikciFaturaSchema,TedarikciFaturaModel
from helpers import SqlConnect
import datetime
class MaliyetRaporIslem:

    def __init__(self,yil,ay):

        self.siparisler = Siparisler(yil,ay).siparis_listesi
        self.urunler = Urunler(yil,ay)
        self.odemeler = Odemeler()
        self.masraflar = Masraflar(yil,ay)
        data = SqlConnect().data
        self.dtTedarikci_group_result = data.getStoreList(
            """
            select
            u.TedarikciID,
            u.SiparisNo
            from
            SiparisUrunTB u
            where
            u.TedarikciID not in (1,123) and 
            u.SiparisNo in (
            Select s.SiparisNo from SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID and s.SiparisNo=u.SiparisNo
            and m.Marketing='Mekmar'
            and s.SiparisDurumID=3
            and Year(s.YuklemeTarihi)=?
            and Month(s.YuklemeTarihi)=?
            )
            group by u.TedarikciID,u.SiparisNo
            """,(yil,ay)
        )

        self.dtDisFaturaList = data.getList(

            """
                select 
           
            u.TedarikciID ,
            s.SiparisNo
            from SiparisUrunTedarikciFormTB u , SiparisFaturaKayitTB s
             where s.SiparisNo=u.SiparisNo and U.TedarikciID not in (1,123) AND YuklemeEvrakID=3  
              group by u.TedarikciID ,s.SiparisNo
           
            """

        )
        self.dtOzeliscilikFaturaList = data.getList(

            """
            select * from SiparisFaturaKayitTB where YuklemeEvrakID=40
            """

        )
        self.dtMekmarFaturaList = data.getList(

            """
            select 
            s.EvrakAdi ,
            u.TedarikciID ,
            s.SiparisNo
            from SiparisUrunTedarikciFormTB u , SiparisFaturaKayitTB s
             where s.SiparisNo=u.SiparisNo and YuklemeEvrakID=3 and u.TedarikciID=1  
              group by u.TedarikciID , s.EvrakAdi,s.SiparisNo
            """

        )

        self.dtMekmozFaturaList = data.getList(

            """
             select 
            s.EvrakAdi ,
            u.TedarikciID ,
            s.SiparisNo
            from SiparisUrunTedarikciFormTB u , SiparisFaturaKayitTB s
             where s.SiparisNo=u.SiparisNo and YuklemeEvrakID=3 and u.TedarikciID=123  
              group by u.TedarikciID , s.EvrakAdi,s.SiparisNo
            """

        )
        self.dtDovizKur = data.getList(
            """
           select k.Kur , s.SiparisNo from SiparisFaturaKayitTB s ,KonteynerDigerFaturalarKayitTB k where k.ID = s.FaturaKayitID
            """
        )
        self.dtTedarikciForm = data.getList(
            """
             select * from SiparisUrunTedarikciFormTB

            """
        )
        self.dtTedarikciFatura = data.getList(
            """
             select * from Tedarikci_Siparis_FaturaTB

            """
        )
        self.dtTedarikciTum = data.getList(
            """
         
             select TedarikciID ,SiparisNo from SiparisUrunTB where  TedarikciID not in (1,123) group by SiparisNo, TedarikciID

            """
        )
    def getMaliyetListesi(self):
        try:
            liste = list()
            for item in self.siparisler:
                
                urun_model = self.urunler.getUrunModel(item.siparis_no)
            
                item.toplam_bedel += urun_model.toplam_bedel
                item.mekmar_alim = urun_model.mekmar_alim
                item.mekmoz_alim = urun_model.mekmoz_alim
                item.dis_alim = urun_model.dis_alim
                item.banka_masrafi = self.odemeler.getOdemeBankaMasrafi(item.siparis_no)
                item.odeme_tarihi = self.odemeler.getOdemeTarih(item.siparis_no) 
                item.odenen_try_tutar , item.odenen_usd_tutar =  self.odemeler.getOdemeBankaTRY(item.siparis_no)
                if item.odenen_try_tutar != 0 and item.odenen_usd_tutar != 0 : 
                    item.ortalama_kur =  item.odenen_try_tutar / item.odenen_usd_tutar
                    item.odenen_toplam_tutar = self.odemeler.getOdenenToplamMasrafi(item.siparis_no)   
                    item.ozel_iscilik_evrak = list() #urun_model.ozel_iscilik_evrak      
                    item.mekmar_alim_evrak = list() #urun_model.mekmar_alim_evrak
                    item.mekmoz_alim_evrak = list() #urun_model.mekmoz_alim_evrak
                    item.dis_alim_evrak = list() #urun_model.dis_alim_evrak
                    item.dis_alim_tedarikci = list()
                    item.tedarikci_sayisi_evrak = list()

                if item.toplam_bedel <= item.odenen_toplam_tutar : # eğer toplam gelen para sipariş bedelini eşit veya gelen para dah butukse bu dosya kapanmıstır deriz
                    item.dosya_kapanma_date = item.odeme_tarihi # ödeme_tarihi son gelen paranın tarihiydi . eğer yukardaki koşulu sağlarsa bu sipariş en son su tarıhte ödemeyi yaptı ve borcu bitti deriz son tarih ise bizim kapanma tarıhımız olur .
                else :
                    item.dosya_kapanma_date =  '-'    #eger hala alacaklıysak 21ACC01-2 de oldugu gibi dosyası kapanmamıstır ve tarıhı - ile göster deriz .
                
                """
                if item.siparis_no =='21AAC02-2' : #birde bu negatif mevzusu var toplamlarda mı sorun var
                    item.dosya_kapanma_date =  '11-11-2021'
                """
                fatura_sayisi = 0
                

                for fat in self.dtTedarikci_group_result:
                    if fat.SiparisNo == item.siparis_no:
                        fatura_sayisi += 1

                for ted_fatura in self.dtDisFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/3/{item.siparis_no}"
                        item.dis_alim_evrak.append(model)

                for ted_fatura in self.dtTedarikciFatura:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/40/{item.siparis_no}"

                        item.dis_alim_tedarikci.append(model)    
                
                for ted_fatura in self.dtTedarikciTum:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/40/{item.siparis_no}"

                        item.tedarikci_sayisi_evrak.append(model)            

                for ted_fatura in self.dtMekmarFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/3/{item.siparis_no}"

                        item.mekmar_alim_evrak.append(model)

                # for ted_fatura in self.dtOzeliscilikFaturaList:
                #     if ted_fatura.SiparisNo == item.siparis_no:
                #         model = TedarikciFaturaModel()
                #         model.id = ted_fatura.ID
                #         model.link = f"https://file-service.mekmar.com/file/download/40/{item.siparis_no}"
                #         model.evrak_adi = ted_fatura.SiparisNo

                #         item.ozel_iscilik_evrak.append(model)

                        
                
                for ted_fatura in self.dtMekmozFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/3/{item.siparis_no}"
                        
                        item.mekmoz_alim_evrak.append(model)

                item.mekmar_alim_evrak_sayisi = len(item.mekmar_alim_evrak)
                item.mekmoz_alim_evrak_sayisi = len(item.mekmoz_alim_evrak)
                item.dis_alim_evrak_sayisi = len(item.dis_alim_evrak)
                item.dis_alim_tedarikci_sayisi = len(item.dis_alim_tedarikci)
                item.tedarikci_sayisi  = len(item.tedarikci_sayisi_evrak)
                item.ozel_iscilik_sayisi = len(item.ozel_iscilik_evrak)

                item.dis_alim_fatura_sayisi = fatura_sayisi

                masraf_model = self.masraflar.getMasrafModel(item.siparis_no)

        

                item.gumruk = masraf_model.gumruk
                item.liman = masraf_model.liman
                x = datetime.datetime(item.yukleme_year,item.yukleme_month,item.yukleme_day)
                if item.yukleme_month ==1 and item.yukleme_day ==1:
                    if(x.strftime('%A') == 'Saturday'):
                        item.yukleme_year = item.yukleme_year - 1
                        item.yukleme_month = 12
                    elif(x.strftime('%A') == 'Sunday'):
                        item.yukleme_year = item.yukleme_year - 1
                        item.yukleme_month = 12
                        item.yukleme_day = 29
                else:
                    if(x.strftime('%A') == 'Saturday'):
                        item.yukleme_day = item.yukleme_day - 1
                    elif(x.strftime('%A') == 'Sunday'):
                        item.yukleme_day = item.yukleme_day - 2

                
                item.doviz_kur = self.odemeler.getOdenenKur(item.siparis_no,item.odenen_toplam_tutar,item.yukleme_year,item.yukleme_month,item.yukleme_day) 
                item.nakliye = masraf_model.nakliye
                item.ilaclama = masraf_model.ilaclama
                item.lashing = masraf_model.lashing
                item.booking = masraf_model.booking
                item.spazlet = masraf_model.spazlet
                
                if item.mekus_id == False:
                    
                    item.navlun_evrak = masraf_model.navlun_evrak
                else:
                    item.navlun_evrak = []
                item.gumruk_evrak = masraf_model.gumruk_evrak
                item.nakliye_evrak = masraf_model.nakliye_evrak
                item.ilaclama_evrak = masraf_model.ilaclama_evrak
                item.liman_evrak = masraf_model.liman_evrak
                item.lashing_evrak = masraf_model.lashing_evrak
                item.booking_evrak = masraf_model.booking_evrak
                item.spazlet_evrak = masraf_model.spazlet_evrak
                
                
                item.satis_faturasi = masraf_model.satis_faturasi
                item.masraf_toplam += (
                    item.mekmar_alim + item.mekmoz_alim + item.dis_alim + item.nakliye + item.gumruk + item.lashing + item.booking + item.spazlet + 
                    item.ilaclama + item.liman + item.navlun + item.pazarlama + item.banka_masrafi 
                    + item.diger_masraflar+item.ozel_iscilik+item.kurye_masrafi + item.sigorta
                )

                if(item.dosya_kapanma_date == '-'):
                    item.kar_zarar = 0
                else:
                    item.kar_zarar = item.toplam_bedel - item.masraf_toplam
                    if item.toplam_bedel != 0 and item.kar_zarar != 0:
                        
                        item.kar_zarar_tl_yuzdesi = round(((item.kar_zarar / item.toplam_bedel ) * 100),2)
                    else:
                        item.kar_zarar_tl_yuzdesi = 0 
                    
                if item.dosya_kapanma_date == '-':
                    item.kar_zarar_tl = 0
                    item.kar_zarar_tl_yuzdesi = 0
                else:
                    
                    if item.doviz_kur !=0 and item.doviz_kur != None:
                        
                        item.kar_zarar_tl =  float(item.kar_zarar) * float(item.doviz_kur)

                if len(item.navlun_evrak) > 0 and item.navlun_satis <= 0:
                    item.navlun_kontrol = False

                if item.toplam_bedel == 0 and item.odenen_toplam_tutar ==0:
                    item.dosya_kapanma_date = self.__getLoadDate(item.siparis_no)
                    
                if item.siparis_no == '22KET01 - 3':
                    item.dosya_kapanma_date = self.__getLoadDate(item.siparis_no)

                
                if item.isciliktedarikcimekmer == True and item.isciliktedarikcimekmoz:
                    item.dis_alim_evrak = list() #urun_model.dis_alim_evrak
                    item.dis_alim_tedarikci = list()
                    item.dis_alim_tedarikci_sayisi = 0
                    item.tedarikci_sayisi = 0
                    item.dis_alim_fatura_sayisi = 0
                if item.mekus_id   == True:
                    item.dis_alim_evrak = list() #urun_model.dis_alim_evrak
                    item.dis_alim_tedarikci = list()
                    item.dis_alim_tedarikci_sayisi = 0
                    item.tedarikci_sayisi = 0
                    item.dis_alim_fatura_sayisi = 0
                print("item",item)
                liste.append(item)


            schema = OzelMaliyetListeSchema(many=True)

            return schema.dump(liste)
        except Exception as e:
            print('getMaliyetListesi hata',str(e))
            return False
    
    def __getLoadDate(self,siparisNo):
        for item in  self.siparisler:
            if(item.siparis_no == siparisNo):
                return item.yukleme_tarihi
 

class MaliyetRaporIslem_Yil: # hepsi butonna basıldıgında bu alan çalışır . 

    def __init__(self,yil):

        self.siparisler = Siparisler_Yil(yil).siparis_listesi
        self.urunler = Urunler_Yil(yil)
        self.odemeler = Odemeler()
        self.masraflar = Masraflar_Yil(yil)
        
      
    
     
        data = SqlConnect().data
        self.dtTedarikci_group_result = data.getStoreList(
            """
            select
            u.TedarikciID,
            u.SiparisNo
            from
            SiparisUrunTB u
            where
            u.TedarikciID not in (1,123) and 
            u.SiparisNo in (
            Select s.SiparisNo from SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID and s.SiparisNo=u.SiparisNo
            and m.Marketing='Mekmar'
            and s.SiparisDurumID=3
            and Year(s.YuklemeTarihi)=?
          
            )
            group by u.TedarikciID,u.SiparisNo
            """,(yil)
        )

        self.dtDisFaturaList = data.getList(

            """
                select 
           
            u.TedarikciID ,
            s.SiparisNo
            from SiparisUrunTedarikciFormTB u , SiparisFaturaKayitTB s
             where s.SiparisNo=u.SiparisNo and U.TedarikciID not in (1,123) AND YuklemeEvrakID=3  
              group by u.TedarikciID ,s.SiparisNo
           
            """

        )
        self.dtOzeliscilikFaturaList = data.getList(

            """
            select * from SiparisFaturaKayitTB where YuklemeEvrakID=40
            """

        )
        self.dtMekmarFaturaList = data.getList(

            """
            select 
            s.EvrakAdi ,
            u.TedarikciID ,
            s.SiparisNo
            from SiparisUrunTedarikciFormTB u , SiparisFaturaKayitTB s
             where s.SiparisNo=u.SiparisNo and YuklemeEvrakID=3 and u.TedarikciID=1  
              group by u.TedarikciID , s.EvrakAdi,s.SiparisNo
            """

        )

        self.dtMekmozFaturaList = data.getList(

            """
             select 
            s.EvrakAdi ,
            u.TedarikciID ,
            s.SiparisNo
            from SiparisUrunTedarikciFormTB u , SiparisFaturaKayitTB s
             where s.SiparisNo=u.SiparisNo and YuklemeEvrakID=3 and u.TedarikciID=123  
              group by u.TedarikciID , s.EvrakAdi,s.SiparisNo
            """

        )
        self.dtDovizKur = data.getList(
            """
           select k.Kur , s.SiparisNo from SiparisFaturaKayitTB s ,KonteynerDigerFaturalarKayitTB k where k.ID = s.FaturaKayitID
            """
        )
        self.dtTedarikciForm = data.getList(
            """
             select * from SiparisUrunTedarikciFormTB

            """
        )
        self.dtTedarikciFatura = data.getList(
            """
             select * from Tedarikci_Siparis_FaturaTB

            """
        )
        self.dtTedarikciTum = data.getList(
            """
         
             select TedarikciID ,SiparisNo from SiparisUrunTB where  TedarikciID not in (1,123) group by SiparisNo, TedarikciID

            """
        )
    def getMaliyetListesi(self):
        try:
            
            liste = list()

            for item in self.siparisler:
            
                urun_model = self.urunler.getUrunModel(item.siparis_no)
            
                item.toplam_bedel += urun_model.toplam_bedel
                item.mekmar_alim = urun_model.mekmar_alim
                item.mekmoz_alim = urun_model.mekmoz_alim
                item.dis_alim = urun_model.dis_alim
                item.banka_masrafi = self.odemeler.getOdemeBankaMasrafi(item.siparis_no)
                item.odeme_tarihi = self.odemeler.getOdemeTarih(item.siparis_no)
                item.odenen_try_tutar , item.odenen_usd_tutar =  self.odemeler.getOdemeBankaTRY(item.siparis_no)
                if item.odenen_try_tutar != 0 and item.odenen_usd_tutar != 0 : 
                    item.ortalama_kur =  item.odenen_try_tutar / item.odenen_usd_tutar
                    item.odenen_toplam_tutar = self.odemeler.getOdenenToplamMasrafi(item.siparis_no)   
                    item.ozel_iscilik_evrak = list() #urun_model.ozel_iscilik_evrak      
                    item.mekmar_alim_evrak = list() #urun_model.mekmar_alim_evrak
                    item.mekmoz_alim_evrak = list() #urun_model.mekmoz_alim_evrak
                    item.dis_alim_evrak = list() #urun_model.dis_alim_evrak
                    item.dis_alim_tedarikci = list()
                    item.tedarikci_sayisi_evrak = list()
                
                    
                if item.toplam_bedel <= item.odenen_toplam_tutar :
                    item.dosya_kapanma_date = item.odeme_tarihi
                else :
                    item.dosya_kapanma_date =  '-'   
                fatura_sayisi = 0


                for fat in self.dtTedarikci_group_result:
                    if fat.SiparisNo == item.siparis_no:
                        fatura_sayisi += 1

                for ted_fatura in self.dtDisFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/3/{item.siparis_no}"
                    
                        item.dis_alim_evrak.append(model)

                for ted_fatura in self.dtTedarikciFatura:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/40/{item.siparis_no}"
                    
                        item.dis_alim_tedarikci.append(model)    
                
                for ted_fatura in self.dtTedarikciTum:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/40/{item.siparis_no}"
                    
                        item.tedarikci_sayisi_evrak.append(model)            

                for ted_fatura in self.dtMekmarFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/3/{item.siparis_no}"
                    
                        item.mekmar_alim_evrak.append(model)

                for ted_fatura in self.dtOzeliscilikFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                        model.id = ted_fatura.ID
                        model.link = f"https://file-service.mekmar.com/file/download/40/{item.siparis_no}"
                        model.evrak_adi = ted_fatura.SiparisNo
                        item.ozel_iscilik_evrak.append(model) 

                        
                
                for ted_fatura in self.dtMekmozFaturaList:
                    if ted_fatura.SiparisNo == item.siparis_no:
                        model = TedarikciFaturaModel()
                        model = TedarikciFaturaModel()
                    
                        model.link =  f"https://file-service.mekmar.com/file/download/3/{item.siparis_no}"
                        
                        item.mekmoz_alim_evrak.append(model)

                item.mekmar_alim_evrak_sayisi = len(item.mekmar_alim_evrak)
                item.mekmoz_alim_evrak_sayisi = len(item.mekmoz_alim_evrak)
                item.dis_alim_evrak_sayisi = len(item.dis_alim_evrak)
                item.dis_alim_tedarikci_sayisi = len(item.dis_alim_tedarikci)
                item.tedarikci_sayisi  = len(item.tedarikci_sayisi_evrak)
                item.ozel_iscilik_sayisi = len(item.ozel_iscilik_evrak)

                item.dis_alim_fatura_sayisi = fatura_sayisi

                masraf_model = self.masraflar.getMasrafModel(item.siparis_no)



                item.gumruk = masraf_model.gumruk
                item.liman = masraf_model.liman
                item.lashing = masraf_model.lashing
                item.booking = masraf_model.booking
                item.spazlet = masraf_model.spazlet

                
                x = datetime.datetime(item.yukleme_year,item.yukleme_month,item.yukleme_day)
                if item.yukleme_month ==1 and item.yukleme_day ==1:
                    if(x.strftime('%A') == 'Saturday'):
                        item.yukleme_year = item.yukleme_year - 1
                        item.yukleme_month = 12
                    elif(x.strftime('%A') == 'Sunday'):
                        item.yukleme_year = item.yukleme_year - 1
                        item.yukleme_month = 12
                        item.yukleme_day = 29
                        
                    else:
                        item.yukleme_day = item.yukleme_day
                        item.yukleme_year = item.yukleme_year
                        item.yukleme_month = item.yukleme_month
                else:
                    if(x.strftime('%A') == 'Saturday'):
                        item.yukleme_day = item.yukleme_day - 1
                    elif(x.strftime('%A') == 'Sunday'):
                        item.yukleme_day = item.yukleme_day - 2
                    else:
                        item.yukleme_day = item.yukleme_day
                        item.yukleme_year = item.yukleme_year
                        item.yukleme_month = item.yukleme_month
                

                
                    
                        
                
                item.doviz_kur = self.odemeler.getOdenenKur(item.siparis_no,item.odenen_toplam_tutar,item.yukleme_year,item.yukleme_month,item.yukleme_day)
                
                item.nakliye = masraf_model.nakliye
                item.ilaclama = masraf_model.ilaclama
                if item.mekus_id == False:
                    
                    item.navlun_evrak = masraf_model.navlun_evrak
                else:
                    item.navlun_evrak = []
                
                
                item.gumruk_evrak = masraf_model.gumruk_evrak
                item.nakliye_evrak = masraf_model.nakliye_evrak
                item.ilaclama_evrak = masraf_model.ilaclama_evrak
                item.liman_evrak = masraf_model.liman_evrak
                item.lashing_evrak = masraf_model.lashing_evrak
                item.booking_evrak = masraf_model.booking_evrak
                item.spazlet_evrak = masraf_model.spazlet_evrak
                
                
                
                item.satis_faturasi = masraf_model.satis_faturasi
                item.masraf_toplam += (
                    item.mekmar_alim + item.mekmoz_alim + item.dis_alim + item.nakliye + item.gumruk + item.lashing + 
                    item.booking +item.spazlet +
                    item.ilaclama + item.liman + item.navlun + item.pazarlama + item.banka_masrafi 
                    + item.diger_masraflar+item.ozel_iscilik+item.kurye_masrafi
                )
                
                if(item.dosya_kapanma_date == '-'):
                    item.kar_zarar = 0
                else:
                    item.kar_zarar = item.toplam_bedel - item.masraf_toplam
                    if item.toplam_bedel !=0 and item.kar_zarar != 0:
                        
                        item.kar_zarar_tl_yuzdesi = round(((item.kar_zarar / item.toplam_bedel ) * 100),2)
                    else:
                        item.kar_zarar_tl_yuzdesi = 0
                
    
                if(item.dosya_kapanma_date == '-'):
                    item.kar_zarar_tl = 0
                else:
                    
                    if item.doviz_kur !=0 and item.doviz_kur != None:
                        item.kar_zarar_tl =  float(item.kar_zarar) * float(item.doviz_kur)

                if len(item.navlun_evrak) > 0 and item.navlun_satis <= 0:
                    item.navlun_kontrol = False
                


                
                if item.toplam_bedel == 0 and item.odenen_toplam_tutar ==0:
                    item.dosya_kapanma_date = self.__getLoadDate(item.siparis_no)

                if item.siparis_no == '22KET01 - 3':
                    item.dosya_kapanma_date = self.__getLoadDate(item.siparis_no)
                    
                if item.isciliktedarikcimekmer == True and item.isciliktedarikcimekmoz:
                    item.dis_alim_evrak = list() #urun_model.dis_alim_evrak
                    item.dis_alim_tedarikci = list()
                    item.dis_alim_tedarikci_sayisi = 0
                    item.tedarikci_sayisi = 0
                    item.dis_alim_fatura_sayisi = 0
                if item.mekus_id   == True:
                    item.dis_alim_evrak = list() #urun_model.dis_alim_evrak
                    item.dis_alim_tedarikci = list()
                    item.dis_alim_tedarikci_sayisi = 0
                    item.tedarikci_sayisi = 0
                    item.dis_alim_fatura_sayisi = 0
                liste.append(item)

            
            schema = OzelMaliyetListeSchema(many=True)

            return schema.dump(liste)
        except Exception as e:
            print('getMaliyetListesi hata hepsi',str(e))
            return False

    
    def __getLoadDate(self,siparisNo):
        for item in  self.siparisler:
            if(item.siparis_no == siparisNo):
                return item.yukleme_tarihi
            

class MaliyetRaporIslemKar:
    def __init__(self,yil):

        self.siparisler = SiparislerKar(yil).siparis_listesi
        self.data = SqlConnect().data
        self.yil = yil
    def getMaliyetListesiKar(self):
        try:
            liste = []
            
            siparisler_musteri = self.data.getStoreList("""
                                                            select 
                                                                s.MusteriID,
                                                                m.FirmaAdi
                                                            from SiparislerTB s
                                                                inner join MusterilerTB m on m.ID = s.MusteriID

                                                            where
                                                                YEAR(s.YuklemeTarihi) = ? and
                                                                s.SiparisDurumID=3 and
                                                                m.Marketing = 'Mekmar'
                                                            group by
                                                                s.MusteriID,
                                                                m.FirmaAdi
                                                        
                                                        """,(self.yil))
            
            liste = list()
            for item in siparisler_musteri:
                model = OzelMaliyetListeKarModel()
                model.musteri_id = item.MusteriID
                model.musteri_adi = item.FirmaAdi
                toplam_bedel,masraf_toplam,odenen_usd_tutar,odenen_try_tutar,kar_zarar,kar_zarar_tl = self.__getSiparisler(item.MusteriID)
                model.toplam_bedel = toplam_bedel
                model.masraf_toplam = masraf_toplam
                model.odenen_usd_tutar = odenen_usd_tutar
                model.odenen_try_tutar = odenen_try_tutar
                model.kar_zarar =kar_zarar
                model.kar_zarar_tl = kar_zarar_tl
                model.kalan_bedel = model.toplam_bedel - model.odenen_usd_tutar
                if(odenen_usd_tutar != 0):
                    model.kar_zarar_orani = round((kar_zarar / odenen_usd_tutar * 100),2)
                else:
                    model.kar_zarar_orani = 0
                liste.append(model)
                
            schema = OzelMaliyetListeKarSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getMaliyetListesiKar',str(e))
            return False

    def __getSiparisler(self,musteri_id):
        toplam_bedel = 0
        masraf_toplam= 0
        odenen_usd_tutar= 0
        odenen_try_tutar= 0
        kar_zarar= 0
        kar_zarar_tl= 0

        for item in self.siparisler:
            if(item.musteri_id == musteri_id):
                toplam_bedel += self.__noneControl(item.toplam_bedel)
                masraf_toplam+= self.__noneControl(item.masraf_toplam)
                odenen_usd_tutar += self.__noneControl(item.odenen_usd_tutar)
                odenen_try_tutar += self.__noneControl(item.odenen_try_tutar)
                kar_zarar += self.__noneControl(item.kar_zarar)
                kar_zarar_tl += self.__noneControl(item.kar_zarar_tl)
                
        return toplam_bedel,masraf_toplam,odenen_usd_tutar,odenen_try_tutar,kar_zarar,kar_zarar_tl
                
                
            
    
    
    def __noneControl(self,value):
        if value == None:
            return 0
        else:
            return float(value)


class MaliyetRaporIslemKarAyrinti:
    def __init__(self,yil):
        self.yil = yil
        self.siparisler = SiparislerKar(yil).siparis_listesi
        self.data = SqlConnect().data
        
    def getMaliyetListesiKarAyrinti(self):
        try:
            
            liste = list()
            for item in self.siparisler:
                model = OzelMaliyetListeKarModel()
                model.musteri_id = item.musteri_id
                model.siparis_no = item.siparis_no
                model.toplam_bedel = item.toplam_bedel
                model.masraf_toplam = item.masraf_toplam
                model.odenen_usd_tutar = item.odenen_usd_tutar
                model.odenen_try_tutar = item.odenen_try_tutar
                model.kar_zarar = item.kar_zarar
                model.kar_zarar_tl = item.kar_zarar_tl
                model.navlun_satis = item.navlun_satis
                model.detay_1 = item.detay_1
                model.detay_2 = item.detay_2
                model.detay_3 = item.detay_3
                model.sigorta_tutar_satis = item.sigorta_tutar_satis
                model.mekus_masraf = item.mekus_masraf
                model.navlun_alis = item.navlun_alis
                model.detay_alis_1  = item.detay_alis_1
                model.detay_alis_2 = item.detay_alis_2
                model.detay_alis_3 = item.detay_alis_3
                model.komisyon = item.komisyon
                model.evrak_gideri = item.evrak_gideri
                model.banka_masrafi = item.banka_masrafi
                model.iscilik_masrafi = item.iscilik_masrafi
                model.fatura_masraflari = item.fatura_masraflari
                model.alis_toplami = item.alis_toplami
                model.satis_toplami = item.satis_toplami
                model.sigorta_alis = item.sigorta_alis
                model.yukleme_tarihi = item.yukleme_tarihi
                model.kalan_bedel = model.toplam_bedel - model.odenen_usd_tutar
                if(model.odenen_usd_tutar != 0):
                    model.kar_zarar_orani = round((model.kar_zarar / model.odenen_usd_tutar * 100),2)
                else:
                    model.kar_zarar_orani = 0
                liste.append(model)
            schema = OzelMaliyetListeKarSchema(many=True)
            return schema.dump(liste) 
        except Exception as e:
            print('getMaliyetListesiKarAyrinti hata',str(e))
            return False
    





