from helpers import SqlConnect,TarihIslemler
from models.ozel_maliyet import OzelMaliyetListeModel,OzelMaliyetListeKarModel
from resource_api.maliyet_raporlar.urunler import UrunlerKar
from resource_api.maliyet_raporlar.odemeler import OdemelerKar
from resource_api.maliyet_raporlar.masraflar import MasraflarKar
from resource_api.finans.guncel_kur import DovizListem

class Siparisler:

    def __init__(self,yil,ay):

        self.data = SqlConnect().data
        self.yil = yil
        self.ay = ay

        self.siparis_listesi = list()
        self.alisFiyatiKontrolSql = self.data.getStoreList("""
                                                    select 


                                                        su.AlisFiyati,
                                                        s.SiparisNo

                                                    from SiparislerTB s , 
                                                         SiparisUrunTB su 
                                                    where 
                                                        s.SiparisNo = su.SiparisNo and 
                                                        Year(s.YuklemeTarihi)=? and 
                                                        Month(s.YuklemeTarihi)=? and 
                                                        su.AlisFiyati in (0,Null)
                                                                                                    
                                                                                                    
                                                   """,(yil,ay))
    
        self.__siparisOlustur()
        
        

    def __siparisOlustur(self):

        result = self.data.getStoreList(
            """
            select
            s.ID,
            s.SiparisNo,
            s.SiparisTarihi,
            s.YuklemeTarihi,
            m.FirmaAdi as MusteriAdi,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.DetayTutar_4,
            s.NavlunAlis,
            s.DetayAlis_1,
            s.DetayAlis_2,
            s.DetayAlis_3,
            u.UlkeAdi,
            m.Marketing,
            t.TeslimTur,
            s.Komisyon,
            s.EvrakGideri,
            s.depo_yukleme,
            s.sigorta_id,
            s.sigorta_Tutar,
            s.sigorta_tutar_satis,

			(select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.SiparisSahibi) as siparisci,
			(select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.Operasyon) as operasyon,
            (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as faturalama,


			(select sum(ozel.Tutar) from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo) as ozeliscilik,
   			(select TOP 1 TedarikciID from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo and ozel.TedarikciID=1) as isciliktedarikcimekmer,
			(select TOP 1 TedarikciID from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo and ozel.TedarikciID=123) as isciliktedarikcimekmoz,
            YEAR(s.YuklemeTarihi) as YuklemeYil,
			MONTH(s.YuklemeTarihi) as YuklemeAy,
            DAY(s.YuklemeTarihi) as YuklemeGun,
            s.alisFiyatiControl
            from
            SiparislerTB s,MusterilerTB m,YeniTeklif_UlkeTB u,SiparisTeslimTurTB t
            where
            s.SiparisDurumID=3
            and m.Marketing='Mekmar'
            and m.UlkeId=u.Id
            and s.TeslimTurID=t.ID
            and s.MusteriID=m.ID
			and Year(s.YuklemeTarihi)=?
            and Month(s.YuklemeTarihi)=?
            order by s.YuklemeTarihi asc
            """,(self.yil,self.ay)
        )
        
        tarihIslem = TarihIslemler()

        for item in result:

            model = OzelMaliyetListeModel()

            model.id = item.ID
            model.faturatur = item.faturalama
            model.siparis_no = item.SiparisNo
            model.operasyon = item.operasyon
            model.siparisci = item.siparisci
            if item.SiparisTarihi != None:
                model.siparis_tarihi = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y") 

            if item.YuklemeTarihi != None:
                model.yukleme_tarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")

            model.musteri_adi = item.MusteriAdi


            if item.ozeliscilik != None:
                model.ozel_iscilik = item.ozeliscilik

            navlun = 0
            detay_tutar_1 = 0
            detay_tutar_2 = 0
            detay_tutar_3 = 0
            detay_tutar_4 = 0
            model.sigorta_id = item.sigorta_id
            if item.NavlunSatis != None:
                navlun = item.NavlunSatis
                model.navlun_satis = item.NavlunSatis

            if item.DetayTutar_1 != None:
                detay_tutar_1 = item.DetayTutar_1

            if item.DetayTutar_2 != None:
                detay_tutar_2 = item.DetayTutar_2

            if item.DetayTutar_3 != None:
                detay_tutar_3 = item.DetayTutar_3

            if item.DetayTutar_4 != None:
                detay_tutar_4 = item.DetayTutar_4

            if item.depo_yukleme != None:
                 model.mekus_id  = item.depo_yukleme  
                   
            if item.sigorta_tutar_satis != None:
                model.sigorta_tutar_satis = item.sigorta_tutar_satis
                
            model.toplam_bedel = navlun + detay_tutar_1 + detay_tutar_2 + detay_tutar_3 + model.sigorta_tutar_satis
            model.mekus_masraf = detay_tutar_4
          
            navlun_alis = 0
            detay_alis_1 = 0
            detay_alis_2 = 0
            detay_alis_3 = 0

            if item.NavlunAlis != None:
                navlun_alis = item.NavlunAlis

            if item.DetayAlis_1 != None:
                detay_alis_1 = item.DetayAlis_1
                model.detay_1 = detay_alis_1

            if item.DetayAlis_2 != None:
                detay_alis_2 = item.DetayAlis_2
                model.detay_2 = detay_alis_2

            if item.DetayAlis_3 != None:
                detay_alis_3 = item.DetayAlis_3
                model.detay_3 = detay_alis_3
            if item.sigorta_Tutar != None:
                
                model.sigorta = item.sigorta_Tutar
              

            model.navlun = navlun_alis
            model.diger_masraflar = detay_alis_1 + detay_alis_2 + detay_alis_3  + detay_tutar_4
            model.ulke_adi = item.UlkeAdi
            model.marketing = item.Marketing
            model.teslim_sekli = item.TeslimTur
            model.kurye_masrafi = item.EvrakGideri
            if item.Komisyon != None:
                model.pazarlama = item.Komisyon
            model.yukleme_year = item.YuklemeYil
            model.yukleme_month = item.YuklemeAy
            model.yukleme_day = item.YuklemeGun
            if self.__getAlisControl(item.SiparisNo):
                if(item.alisFiyatiControl):
                    model.alisFiyatiKontrol = ""
                else:
                    
                    model.alisFiyatiKontrol = "#F1948A"
                
            if item.isciliktedarikcimekmer != None:
                model.isciliktedarikcimekmer = item.isciliktedarikcimekmer
            
            if item.isciliktedarikcimekmoz != None:
                model.isciliktedarikcimekmoz = item.isciliktedarikcimekmoz
        
            self.siparis_listesi.append(model)

    
    def __getAlisControl(self,siparisNo):
        if len(self.alisFiyatiKontrolSql)>0:
            for item in self.alisFiyatiKontrolSql:
                if item.SiparisNo != siparisNo:
                    continue
                else:
                    return True
        else:
            return False
    

class SiparislerKar:
    def __init__(self,yil):
        self.data = SqlConnect().data
        self.yil = yil

        self.siparis_listesi = list()
        self.urunler = UrunlerKar(yil)
        self.odemeler = OdemelerKar(yil)
        self.masraflar = MasraflarKar(yil)
        self.__siparisOlustur()
        
    def __siparisOlustur(self):
        try:
            
            self.siparis_listesi_kar = self.data.getStoreList("""
                                                                select 
                                                                s.MusteriID,
                                                                s.SiparisNo,
                                                                s.NavlunSatis as NavlunSatis,
                                                                s.DetayTutar_1 as DetaySatis1,
                                                                s.DetayTutar_2 as DetaySatis2,
                                                                s.DetayTutar_3 as DetaySatis3,
                                                                s.DetayTutar_4 as DetaySatis4,
                                                                s.NavlunAlis as NavlunAlis,
                                                                s.DetayAlis_1 as DetayAlis1,
                                                                s.DetayAlis_2 as DetayAlis2,
                                                                s.DetayAlis_3 as DetayAlis3,
                                                                s.Komisyon as Komisyon,
                                                                s.EvrakGideri as EvrakGideri,
                                                                s.sigorta_tutar_satis as SigortaSatis,
                                                                s.sigorta_Tutar as SigortaAlis,
                                                                (select sum(se.Tutar) from SiparisEkstraGiderlerTB se where se.SiparisNo = s.SiparisNo) as OzelIscilik,
                                                                YEAR(s.YuklemeTarihi) as Yil,
                                                                MONTH(s.YuklemeTarihi) as Ay,
                                                                DAY(s.YuklemeTarihi) as Gun
                                                            from SiparislerTB s
                                                                inner join MusterilerTB m on m.ID = s.MusteriID

                                                            where 
                                                                YEAR(s.YuklemeTarihi) = ? and 
                                                                m.Marketing='Mekmar' and 
                                                                s.SiparisDurumID=3

                                                            
                                                            
                                                            """,(self.yil))

            for item in self.siparis_listesi_kar:
                model = OzelMaliyetListeKarModel()
                model.musteri_id = item.MusteriID
                model.siparis_no = item.SiparisNo
                model.navlun_satis = self.__noneControl(item.NavlunSatis)
                model.detay_1 = self.__noneControl(item.DetaySatis1)
                model.detay_2 = self.__noneControl(item.DetaySatis2)
                model.detay_3 = self.__noneControl(item.DetaySatis3)
                model.sigorta_tutar_satis = self.__noneControl(item.SigortaSatis)
                model.mekus_masraf = self.__noneControl(item.DetaySatis4)
                
                model.masraf_toplam = self.__noneControl(item.NavlunAlis) + self.__noneControl(item.DetayAlis1) +self.__noneControl(item.DetayAlis2) +self.__noneControl(item.DetayAlis3) +self.__noneControl(item.Komisyon) +self.__noneControl(item.EvrakGideri) +self.__noneControl(item.SigortaAlis) + model.mekus_masraf + self.__noneControl(item.OzelIscilik) + self.odemeler.getOdemelerModel(item.SiparisNo).banka_masrafi + self.masraflar.getMasraflarModel(item.SiparisNo).fatura_masraflari + self.urunler.getUrunModel(item.SiparisNo).alis_toplami
                model.navlun_alis = self.__noneControl(item.NavlunAlis)
                model.detay_alis_1 = self.__noneControl(item.DetayAlis1)
                model.detay_alis_2 = self.__noneControl(item.DetayAlis2)
                model.detay_alis_3 = self.__noneControl(item.DetayAlis3)
                model.komisyon = self.__noneControl(item.Komisyon)
                model.evrak_gideri = self.__noneControl(item.EvrakGideri)
                model.banka_masrafi = self.odemeler.getOdemelerModel(item.SiparisNo).banka_masrafi
                model.iscilik_masrafi = self.__noneControl(item.OzelIscilik)
                model.fatura_masraflari = self.masraflar.getMasraflarModel(item.SiparisNo).fatura_masraflari
                model.alis_toplami = self.urunler.getUrunModel(item.SiparisNo).alis_toplami
                model.satis_toplami = self.urunler.getUrunModel(item.SiparisNo).satis_toplami
                model.sigorta_alis = self.__noneControl(item.SigortaAlis)
                model.toplam_bedel = model.satis_toplami + model.navlun_satis + model.detay_1 + model.detay_2 + model.detay_3 + model.sigorta_tutar_satis
                model.odenen_usd_tutar = self.odemeler.getOdemelerModel(item.SiparisNo).odenen_usd_tutar
                model.odenen_try_tutar = self.odemeler.getOdemelerModel(item.SiparisNo).odenen_try_tutar
                model.ortalama_kur = self.odemeler.getOdemelerModel(item.SiparisNo).ortalama_kur
                model.kar_zarar = model.odenen_usd_tutar - model.masraf_toplam
                model.yukleme_tarihi = str(item.Yil) + '/' + str(item.Ay) + '/' + str(item.Gun)
                if(model.odenen_usd_tutar != 0):
                    model.kar_zarar_orani = round(model.kar_zarar / model.odenen_usd_tutar * 100,2)
                else:
                    model.kar_zarar_orani = 0
                    
                if(model.ortalama_kur != 0):
                    model.kar_zarar_tl = model.odenen_try_tutar - (model.masraf_toplam * model.ortalama_kur)
                else:
                    doviz = DovizListem()
                    dovizKur = doviz.getDovizKurListe(str(item.Yil),str(item.Ay),str(item.Gun))
                    model.kar_zarar_tl = self.__noneControl(model.odenen_try_tutar) - (self.__noneControl(model.masraf_toplam) * float(dovizKur))
                    
                
                
                
                
                
                
                
                self.siparis_listesi.append(model)
        except Exception as e:
            print('__siparisOlustur hata',str(e))
            return False
    def __noneControl(self,value):
        if(value == None):
            return 0
        else:
            return float(value)     
            






 
class Siparisler_Yil:

    def __init__(self,yil):

        self.data = SqlConnect().data
        self.yil = yil        

        self.siparis_listesi = list()
        self.alisFiyatiKontrolSql = self.data.getStoreList("""
                                                    select 


                                                        su.AlisFiyati,
                                                        s.SiparisNo

                                                    from SiparislerTB s , 
                                                         SiparisUrunTB su 
                                                    where 
                                                        s.SiparisNo = su.SiparisNo and 
                                                        Year(s.YuklemeTarihi)=? and 
                                                        su.AlisFiyati in (0,Null)
                                                                                                    
                                                                                                    
                                                   """,(yil))
    
        self.__siparisOlustur()

        

    def __siparisOlustur(self):

        result = self.data.getStoreList(
            """
           select
            s.ID,
            s.SiparisNo,
            s.SiparisTarihi,
            s.YuklemeTarihi,
            m.FirmaAdi as MusteriAdi,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.DetayTutar_4,
            s.NavlunAlis,
            s.DetayAlis_1,
            s.DetayAlis_2,
            s.DetayAlis_3,
            u.UlkeAdi,
            m.Marketing,
            t.TeslimTur,
            s.Komisyon,
            s.EvrakGideri,
            s.depo_yukleme,
            s.sigorta_Tutar,
            s.sigorta_id,
            s.sigorta_tutar_satis,
            (select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.SiparisSahibi) as siparisci,
			(select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.Operasyon) as operasyon,
			(select sum(ozel.Tutar) from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo) as ozeliscilik,
            (select TOP 1 TedarikciID from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo and ozel.TedarikciID=1) as isciliktedarikcimekmer,
			(select TOP 1 TedarikciID from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo and ozel.TedarikciID=123) as isciliktedarikcimekmoz,
            (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as faturalama,
			Month(s.YuklemeTarihi) as YuklemeMonth,
            YEAR(s.YuklemeTarihi) as YuklemeYil,
			MONTH(s.YuklemeTarihi) as YuklemeAy,
            DAY(s.YuklemeTarihi) as YuklemeGun,
            s.alisFiyatiControl
            from
            SiparislerTB s,MusterilerTB m,YeniTeklif_UlkeTB u,SiparisTeslimTurTB t
            where
            s.SiparisDurumID=3
            and m.Marketing='Mekmar'
            and m.UlkeId=u.Id
            and s.TeslimTurID=t.ID
            and s.MusteriID=m.ID
            and Year(s.YuklemeTarihi)=?
            order by s.YuklemeTarihi asc          
            """,(self.yil)
        )

        tarihIslem = TarihIslemler()

        for item in result:

            model = OzelMaliyetListeModel()

            model.id = item.ID
            model.faturatur = item.faturalama
            model.siparis_no = item.SiparisNo
            model.operasyon = item.operasyon
            model.siparisci = item.siparisci
            if item.SiparisTarihi != None:
                model.siparis_tarihi = tarihIslem.getDate(item.SiparisTarihi).strftime("%d-%m-%Y") 

            if item.YuklemeTarihi != None:
                model.yukleme_tarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")

            model.musteri_adi = item.MusteriAdi

            if item.ozeliscilik != None:
                model.ozel_iscilik = item.ozeliscilik
            
           

            navlun = 0
            detay_tutar_1 = 0
            detay_tutar_2 = 0
            detay_tutar_3 = 0
            detay_tutar_4 = 0

            if item.NavlunSatis != None:
                navlun = item.NavlunSatis
                model.navlun_satis = item.NavlunSatis

            if item.DetayTutar_1 != None:
                detay_tutar_1 = item.DetayTutar_1

            if item.DetayTutar_2 != None:
                detay_tutar_2 = item.DetayTutar_2

            if item.DetayTutar_3 != None:
                detay_tutar_3 = item.DetayTutar_3

            if item.DetayTutar_4 != None:
                detay_tutar_4 = item.DetayTutar_4

            if item.depo_yukleme != None:
                 model.mekus_id  = item.depo_yukleme    

            if item.sigorta_Tutar != None:
                 model.sigorta  = item.sigorta_Tutar
            else:
                model.sigorta = 0
                
            if item.sigorta_tutar_satis != None:
                 model.sigorta_tutar_satis  = item.sigorta_tutar_satis
            else:
                model.sigorta_tutar_satis = 0

            model.sigorta_id = item.sigorta_id
            model.toplam_bedel = navlun + detay_tutar_1 + detay_tutar_2 + detay_tutar_3 + model.sigorta_tutar_satis
            model.mekus_masraf = detay_tutar_4
           
            navlun_alis = 0
            detay_alis_1 = 0
            detay_alis_2 = 0
            detay_alis_3 = 0

            if item.NavlunAlis != None:
                navlun_alis = item.NavlunAlis

            if item.DetayAlis_1 != None:
                detay_alis_1 = item.DetayAlis_1
                model.detay_1 = detay_alis_1

            if item.DetayAlis_2 != None:
                detay_alis_2 = item.DetayAlis_2
                model.detay_2 = detay_alis_2

            if item.DetayAlis_3 != None:
                detay_alis_3 = item.DetayAlis_3
                model.detay_3 = detay_alis_3

              
            model.yukleme_year = item.YuklemeYil
            model.yukleme_month = item.YuklemeAy
            model.yukleme_day = item.YuklemeGun
            
            model.navlun = navlun_alis
            model.diger_masraflar = detay_alis_1 + detay_alis_2 + detay_alis_3  + detay_tutar_4 + model.sigorta
            model.ulke_adi = item.UlkeAdi
            model.marketing = item.Marketing
            model.teslim_sekli = item.TeslimTur
            model.kurye_masrafi = item.EvrakGideri
            if item.Komisyon != None:
                model.pazarlama = item.Komisyon
            model.yukleme_month = item.YuklemeMonth
            if self.__getAlisControl(item.SiparisNo):
                if(item.alisFiyatiControl):
                    
                    model.alisFiyatiKontrol = ""
                else:
                    model.alisFiyatiKontrol = "#F1948A"
                    
            if item.isciliktedarikcimekmer != None:
                model.isciliktedarikcimekmer = item.isciliktedarikcimekmer
            
            if item.isciliktedarikcimekmoz != None:
                model.isciliktedarikcimekmoz = item.isciliktedarikcimekmoz
                
            self.siparis_listesi.append(model)
            
            
    def __getAlisControl(self,siparisNo):
        if len(self.alisFiyatiKontrolSql)>0:
            for item in self.alisFiyatiKontrolSql:
                if item.SiparisNo != siparisNo:
                    continue
                else:
                    return True
        else:
            return False

        
        