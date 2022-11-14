from helpers import SqlConnect,TarihIslemler
from models.ozel_maliyet import OzelMaliyetListeModel


class Siparisler:

    def __init__(self,yil,ay):

        self.data = SqlConnect().data
        self.yil = yil
        self.ay = ay

        self.siparis_listesi = list()

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

			(select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.SiparisSahibi) as siparisci,
			(select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.Operasyon) as operasyon,
            (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as faturalama,


			(select sum(ozel.Tutar) from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo) as ozeliscilik,
            YEAR(s.YuklemeTarihi) as YuklemeYil,
			MONTH(s.YuklemeTarihi) as YuklemeAy
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

            model.toplam_bedel = navlun + detay_tutar_1 + detay_tutar_2 + detay_tutar_3 
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
            
            self.siparis_listesi.append(model)

class Siparisler_Yil:

    def __init__(self,yil):

        self.data = SqlConnect().data
        self.yil = yil        

        self.siparis_listesi = list()

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
            (select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.SiparisSahibi) as siparisci,
			(select k.KullaniciAdi from KullaniciTB k WHERE k.ID = s.Operasyon) as operasyon,
			(select sum(ozel.Tutar) from SiparisEkstraGiderlerTB ozel  where ozel.SiparisNo=s.SiparisNo) as ozeliscilik,
            (select f.FaturaAdi from FaturaKesilmeTB f where f.ID = s.FaturaKesimTurID) as faturalama,
			Month(s.YuklemeTarihi) as YuklemeMonth
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

            model.toplam_bedel = navlun + detay_tutar_1 + detay_tutar_2 + detay_tutar_3 
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

              

            model.navlun = navlun_alis
            model.diger_masraflar = detay_alis_1 + detay_alis_2 + detay_alis_3  + detay_tutar_4
            model.ulke_adi = item.UlkeAdi
            model.marketing = item.Marketing
            model.teslim_sekli = item.TeslimTur
            model.kurye_masrafi = item.EvrakGideri
            if item.Komisyon != None:
                model.pazarlama = item.Komisyon
            model.yukleme_month = item.YuklemeMonth
            self.siparis_listesi.append(model)
            

        
        