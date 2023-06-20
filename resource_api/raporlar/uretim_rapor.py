from models.raporlar import *
from helpers import SqlConnect,TarihIslemler
import datetime


class UretimRapor:

    def __init__(self):

        self.data = SqlConnect().data

    def getUretimListesiHepsi(self):

        result = self.data.getList(
           
           """
            select

                u.ID,  
                u.Tarih,
                u.KasaNo,  
                u.Adet,  
                u.Miktar,  
                u.SiparisAciklama,
                t.FirmaAdi as Kimden,
                ur.OcakAdi,
                ub.BirimAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as YuzeyAdi,
                urun.UrunAdi,
                u.UrunKartID,
				u.Aciklama
                from 


                UretimTB u

                inner join TedarikciTB t on (u.TedarikciID = t.ID)
                inner join UrunOcakTB ur on (ur.ID = u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID = u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where

                u.TedarikciID in (1,123)

                order by u.Tarih desc
           """

        )

        """ URETİM RAPOR HEPSİ İLK SORGU
            select  
            u.ID,  
            u.Tarih,  
            t.FirmaAdi as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,  
            u.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            o.OcakAdi,  
            dbo.Get_KenarIslem(u.UrunKartID) as YuzeyAdi,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.Miktar,  
            b.BirimAdi,  
            u.SiparisAciklama  
            from  
            UretimTB u,TedarikciTB t,UrunOcakTB o,UrunBirimTB b  
            where u.TedarikciID=t.ID  
            and o.ID=u.UrunOcakID  
            and b.ID=u.UrunBirimID  
            and u.TedarikciID in (1,123)  
            order by u.Tarih desc  
              
           """

        tarihIslem = TarihIslemler()
        liste = list()

        for item in result:

            model = UretimModel()
            model.id = item.ID

            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")

            model.kimden = item.Kimden
            model.kategori = item.Kategori
            model.kasano = item.KasaNo
            model.urunadi = item.UrunAdi
            model.ocakadi = item.OcakAdi
            model.yuzeyadi = item.YuzeyAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.adet = item.Adet
            model.miktar = item.Miktar
            model.birimadi = item.BirimAdi
            model.siparisno = item.SiparisAciklama
            model.urunKartID = item.UrunKartID
            model.aciklama = item.Aciklama
            liste.append(model)

        schema = UretimSchema(many=True)

        return schema.dump(liste)
    def getUretimListesiYil(self,yil):

        result = self.data.getStoreList(
           
           """
            select

                u.ID,  
                u.Tarih,
                u.KasaNo,  
                u.Adet,  
                u.Miktar,  
                u.SiparisAciklama,
                t.FirmaAdi as Kimden,
                ur.OcakAdi,
                ub.BirimAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as YuzeyAdi,
                urun.UrunAdi,
                u.UrunKartID,
				u.Aciklama
                from 


                UretimTB u

                inner join TedarikciTB t on (u.TedarikciID = t.ID)
                inner join UrunOcakTB ur on (ur.ID = u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID = u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where

                u.TedarikciID in (1,123) and YEAR(u.Tarih) = ?

                order by u.Tarih desc
           """,(yil)
           )

      

        tarihIslem = TarihIslemler()
        liste = list()

        for item in result:

            model = UretimModel()
            model.id = item.ID

            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")

            model.kimden = item.Kimden
            model.kategori = item.Kategori
            model.kasano = item.KasaNo
            model.urunadi = item.UrunAdi
            model.ocakadi = item.OcakAdi
            model.yuzeyadi = item.YuzeyAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.adet = item.Adet
            model.miktar = item.Miktar
            model.birimadi = item.BirimAdi
            model.siparisno = item.SiparisAciklama
            model.urunKartID = item.UrunKartID
            model.aciklama = item.Aciklama
            liste.append(model)

        schema = UretimSchema(many=True)

        return schema.dump(liste)


    def getUretimListesiSonTariheGore(self,tarih):

        result = self.data.getStoreList(
            """
            select

                u.ID,  
                u.Tarih,
                u.KasaNo,  
                u.Adet,  
                u.Miktar,  
                u.SiparisAciklama,
                t.FirmaAdi as Kimden,
                ur.OcakAdi,
                ub.BirimAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as YuzeyAdi,
                urun.UrunAdi,
                u.UrunKartID
                from 


                UretimTB u

                inner join TedarikciTB t on (u.TedarikciID = t.ID)
                inner join UrunOcakTB ur on (ur.ID = u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID = u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where

                u.TedarikciID in (1,123) and u.Tarih<=?

                order by u.Tarih desc

            """,(tarih)
        )
            

        """ ÜRETİM RAPOR SON TARİHE GORE İLK SORGU
            select
            u.ID,
            u.Tarih,
            t.FirmaAdi as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            u.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            o.OcakAdi,
            dbo.Get_KenarIslem(u.UrunKartID) as YuzeyAdi,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.Miktar,
            b.BirimAdi,
            u.SiparisAciklama
            from
            UretimTB u,TedarikciTB t,UrunOcakTB o,UrunBirimTB b
            where u.TedarikciID=t.ID
            and o.ID=u.UrunOcakID
            and b.ID=u.UrunBirimID
            and u.TedarikciID in (1,123)
            and u.Tarih<=?
            order by u.Tarih desc

            """

        tarihIslem = TarihIslemler()
        liste = list()

        for item in result:

            model = UretimModel()
            model.id = item.ID

            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")

            model.kimden = item.Kimden
            model.kategori = item.Kategori
            model.kasano = item.KasaNo
            model.urunadi = item.UrunAdi
            model.ocakadi = item.OcakAdi
            model.yuzeyadi = item.YuzeyAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.adet = item.Adet
            model.miktar = item.Miktar
            model.birimadi = item.BirimAdi
            model.siparisno = item.SiparisAciklama
            model.urunKartID = item.UrunKartID

            liste.append(model)

        schema = UretimSchema(many=True)

        return schema.dump(liste)

    def getUretimListesiIkiTarihArasi(self,ilk_tarih,son_tarih):

        result = self.data.getStoreList(
            """
            select

                u.ID,  
                u.Tarih,
                u.KasaNo,  
                u.Adet,  
                u.Miktar,  
                u.SiparisAciklama,
                t.FirmaAdi as Kimden,
                ur.OcakAdi,
                ub.BirimAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as YuzeyAdi,
                urun.UrunAdi,
                u.UrunKartID
                from 


                UretimTB u

                inner join TedarikciTB t on (u.TedarikciID = t.ID)
                inner join UrunOcakTB ur on (ur.ID = u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID = u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where

                u.TedarikciID in (1,123) and u.Tarih between ? and ?

                order by u.Tarih desc

            """,(ilk_tarih,son_tarih)
        )



        """ ÜRETİM RAPORU İKİ TARİH ARASI İLK SORGU
            select
            u.ID,
            u.Tarih,
            t.FirmaAdi as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            u.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            o.OcakAdi,
            dbo.Get_KenarIslem(u.UrunKartID) as YuzeyAdi,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.Miktar,
            b.BirimAdi,
            u.SiparisAciklama
            from
            UretimTB u,TedarikciTB t,UrunOcakTB o,UrunBirimTB b
            where u.TedarikciID=t.ID
            and o.ID=u.UrunOcakID
            and b.ID=u.UrunBirimID
            and u.TedarikciID in (1,123)
            and u.Tarih between ? and ?
            order by u.Tarih desc

            """








        tarihIslem = TarihIslemler()
        liste = list()

        for item in result:

            model = UretimModel()
            model.id = item.ID

            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")

            model.kimden = item.Kimden
            model.kategori = item.Kategori
            model.kasano = item.KasaNo
            model.urunadi = item.UrunAdi
            model.ocakadi = item.OcakAdi
            model.yuzeyadi = item.YuzeyAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.adet = item.Adet
            model.miktar = item.Miktar
            model.birimadi = item.BirimAdi
            model.siparisno = item.SiparisAciklama
            model.urunKartID = item.UrunKartID
            liste.append(model)

        schema = UretimSchema(many=True)

        return schema.dump(liste)


    def getSeleksiyonEtiketTariheGore(self,tarih):

        result = self.data.getStoreList(
            """
           select
            u.ID as Id,
            u.KasaNo as kasano,
            u.Tarih as tarih,
            (select k.KategoriAdi from KategoriTB k where k.ID=uk.KategoriID) as kategori,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as ocak,
            (select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID) as tedarikci,
            dbo.Get_UrunAdi(uk.ID) as urunadi,
            dbo.Get_KenarIslem(uk.ID) as kenarislem,
            dbo.Get_Olcu_Boy(uk.ID) as boy,
            dbo.Get_Olcu_En(uk.ID) as en,
            dbo.Get_Olcu_Kenar(uk.ID) as kenar,
            u.KutuAdet as kutuadet,
            dbo.GetUretim_Miktar(u.Miktar,u.OzelMiktar) as miktar,
            u.Miktar,
            u.Adet as kasa_adet,
            u.SiparisAciklama as siparisaciklama,
            u.TedarikciID as tedarikci_id,
            u.UrunBirimID as birim_id,
            u.Aciklama,
            u.UrunKartID
            from
            UretimTB u,UrunKartTB uk
            where
            u.UrunDurumID=1 and uk.ID=u.UrunKartID
            and u.TedarikciID is not null  and u.Tarih =? and u.UrunOcakID = 28
            order by u.KasaNo desc

            """,(tarih)
        )
        tarihIslem = TarihIslemler()
        liste = list()

        for item in result:

            model = UretimModel()
            model.id = item.Id

            if item.tarih != None:
                model.tarih = tarihIslem.getDate(item.tarih).strftime("%d-%m-%Y")

            model.kimden = item.tedarikci
            model.kategori = item.kategori
            model.kasano = item.kasano
            model.urunadi = item.urunadi
            model.ocakadi = item.ocak
            model.yuzeyadi = item.kenarislem
            model.en = item.en
            model.boy = item.boy
            model.kenar = item.kenar
            model.adet = item.kutuadet
            model.miktar = item.miktar
            model.birimadi = item.birim_id
            model.siparisno = item.siparisaciklama
            model.urunKartID = item.UrunKartID
            liste.append(model)

        schema = UretimSchema(many=True)
        
        return schema.dump(liste)     


    