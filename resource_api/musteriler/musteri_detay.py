from flask_cors.core import try_match
from models.musteriler_model import *
from helpers import SqlConnect



class MusteriDetayIslem:

    def __init__(self):

        self.data = SqlConnect().data

    def getYeniMusteriModel(self):

        model = MusteriModel()

        schema = MusteriSchema()

        return schema.dump(model)

    def getMusteriDetay(self,id):

        item = self.data.getStoreList(

            """
            Select
            *           
            from
            MusterilerTB m,YeniTeklif_UlkeTB u
            where
            m.UlkeId=u.Id
            and m.ID=?
            """,(id)
        )[0]

        model = MusteriModel()

        model.id = item.ID
        model.musteri_adi = item.FirmaAdi
        model.unvan = item.Unvan
        model.adres = item.Adres
        model.ulke_adi = item.UlkeAdi
        model.ulke_id = item.Id
        model.logo = item.Png_Flags
        model.marketing = item.Marketing
        model.sira = item.Sira
        model.musteri_temsilci_id = item.MusteriTemsilciId
        model.satisci = item.Satisci
        model.kullanici_id = item.KullaniciID
        model.mail_adresi = item.MailAdresi
        model.telefon = item.Telefon
        model.devir = item.Devir
        model.ozel = item.Ozel
        model.selectOncelik = item.MusteriOncelik
        model.takip = item.Takip
        model.notlar = item.Notlar
        model.sonkullanici = item.SonKullanici

        


        schema = MusteriSchema()

        return schema.dump(model)


    def getSiparisBedeliDetay(self,id):

        result = self.data.getStoreList(

            """
           select    
            (Select Sum(NavlunSatis+DetayTutar_1+DetayTutar_2+DetayTutar_3) from SiparislerTB sb where sb.MusteriID=m.ID and Year(YuklemeTarihi)=Year(s.YuklemeTarihi) ) as Navlun,  
            Sum(u.SatisToplam) as UrunBedeli,   

            s.MusteriID,  
            YEAR(YuklemeTarihi) as Yil,  
            dbo.GetProfit(s.MusteriID,Year(YuklemeTarihi)) as Kar  
            from   
            SiparislerTB s,SiparisUrunTB u  , MusterilerTB m 
            where s.MusteriID=m.ID and s.SiparisDurumID=3  
            and u.SiparisNo=s.SiparisNo  and m.ID=?
            group by YEAR(YuklemeTarihi),s.MusteriID  ,m.ID
            order by YEAR(YuklemeTarihi) desc  
            """,(id)
        )
        liste = list()
        for item in result:
            model = MusteriSiparisModel()

            model.id = item.MusteriID
        
            model.Yil = item.Yil
            if item.Navlun != None and item.UrunBedeli != None :
              model.Total = item.UrunBedeli + item.Navlun
            liste.append(model)

        schema = MusteriSiparisSchema(many=True)

        return schema.dump(liste)  

    def getSiparisAyrintiDetay(self,yil,id):

        result = self.data.getStoreList(

            """
            SELECT s.SiparisNo ,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = s.SiparisSahibi) as Satisci, 
            (select k.KullaniciAdi from KullaniciTB k where k.ID = s.Operasyon) as Operasyon
            FROM SiparislerTB s , MusterilerTB m where m.ID = s.MusteriID and year(s.YuklemeTarihi)=? and s.MusteriID=?
            """,(yil,id)
        )
        liste = list()
        
        for item in result:
            model = MusteriSiparisAyrintiModel()

            model.SiparisNo = item.SiparisNo
            model.Satisci = item.Satisci
            model.Operasyon = item.Operasyon
            liste.append(model)
            
        schema = MusteriSiparisAyrintiSchema(many=True)

        return schema.dump(liste)   

    def getUlkeList(self):

        result = self.data.getList(
            """
            select * from YeniTeklif_UlkeTB
            """
        )

        liste = list()

        for item in result:

            model = MusteriUlkeModel()
            model.id = item.Id
            model.ulke_adi = item.UlkeAdi
            model.logo = item.Png_Flags

            liste.append(model)

        schema = MusteriUlkeSchema(many=True)

        return schema.dump(liste)

    def getTemsilciList(self):

        result = self.data.getList(

            """
            select * from KullaniciTB
            """
        )
        
        liste = list()

        for item in result:

            model = MusteriTemsilciModel()
            model.id = item.ID
            model.kullanici_adi = item.KullaniciAdi

            liste.append(model)

        schema = MusteriTemsilciSchema(many=True)

        return schema.dump(liste)

    



    def musteriKaydet(self,item):
        
        try:
            self.data.update_insert(

                """
                        insert into MusterilerTB (
                        FirmaAdi,Unvan,UlkeId,Marketing,Aktif,
                        Sira,Mt_No,MusteriTemsilciId,
                        KullaniciID,MailAdresi,Telefon,
                        Devir,Ozel,Adres,MusteriOncelik,Satisci,Notlar,SonKullanici,
						KayitTarihi
                    )
                    values
                    (
                        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                    )
                """,
                (
                    item['musteri_adi'],item['unvan'],item['ulke_id'],
                    item['marketing'],item['aktif'],item['sira'],
                    item['mt_no'],item['musteri_temsilci_id'],
                    item['kullanici_id'],item['mail_adresi'],
                    item['telefon'],item['devir'],item['ozel'],
                    item['adres'],item['selectOncelik'],item['satisci'],item['notlar'],item['sonkullanici'],item['kayit_tarihi']
                )
            )

            return True

        except Exception as e:
            print('MusteriDetayIslem musteriKaydet Hata : ',str(e))
            return False

    def musteriGuncelle(self,item):
        try:
            self.data.update_insert(
                """
                update MusterilerTB set FirmaAdi=?,Unvan=?,Adres=?,UlkeId=?,
                Marketing=?,Sira=?,MusteriTemsilciId=?,MailAdresi=?,
                Telefon=?,Devir=?,Ozel=? , MusteriOncelik=?,Satisci=?,Notlar=?,SonKullanici=? where ID=?
                """,(
                    item['musteri_adi'],item['unvan'],item['adres'],item['ulke_id'],
                    item['marketing'],item['sira'],item['musteri_temsilci_id'],
                    item['mail_adresi'],item['telefon'],item['devir'],item['ozel'], item['selectOncelik'],item['satisci'],item['notlar'],item['sonkullanici'],
                    item['id']
                )
            )

            return True

        except Exception as e:
            print('MusteriDetayIslem musteriGuncelle Hata : ',str(e))
            return False

    def musteriSilme(self,id):

        try:
           if self.__musteriKontrol(id) == True:
               self.data.update_insert(
                   """
                   delete from MusterilerTB where ID=?
                   """,(id)
               )
               return True
           return False
        except Exception as e:
            print('MusteriDetayIslem musteriSilme Hata : ',str(e))
            return False

    def __musteriKontrol(self,id):

        kontrol = False

        siparis_durum = self.data.getStoreList(

            """
            select count(*) as durum from SiparislerTB where MusteriID=?
            """,(id)
        )[0].durum

        odeme_durum = self.data.getStoreList(

            """
            select count(*) as durum from OdemelerTB where MusteriID=?
            """,(id)
        )[0].durum

        if siparis_durum <= 0 and odeme_durum <= 0:
            kontrol = True

        return kontrol

