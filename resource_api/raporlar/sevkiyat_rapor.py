from helpers import SqlConnect,TarihIslemler
from models.raporlar import SevkiyatSchema,SevkiyatModel



class SevkiyatRapor:

    def __init__(self):
        self.data = SqlConnect().data
        self.tarihIslem = TarihIslemler()


    def getSevkiyatListeHepsiMekmer(self):
        
        result = self.data.getList("""
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID
				

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where Year(s.Tarih) in ('2022','2021') and m.Marketing in ('Mekmer','İç Piyasa')
                order by s.Tarih desc

            
        
        
        
        """
        )
        """ İLK SORGU
            
            select  
            s.ID,  
            s.Tarih,  
            (  
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID  
            ) as Kime,  
            (  
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID  
            ) as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori, 
            s.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,  
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.KutuAdet,  
            u.Miktar,  
            (  
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID  
            ) as Birim,  
            s.CikisNo,  
            s.BirimFiyat,  
            s.Toplam  
            from  
            SevkiyatTB s,UretimTB u  
              
            s.KasaNo=u.KasaNo  
            order by s.Tarih desc  


        
        """



        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeAllMekmer(self):
        
        result = self.data.getList("""
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)
				where m.Marketing in ('Mekmer','İç Piyasa')
                order by s.Tarih desc

            
        
        
        
        """
        )
        """ İLK SORGU
            
            select  
            s.ID,  
            s.Tarih,  
            (  
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID  
            ) as Kime,  
            (  
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID  
            ) as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori, 
            s.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,  
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.KutuAdet,  
            u.Miktar,  
            (  
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID  
            ) as Birim,  
            s.CikisNo,  
            s.BirimFiyat,  
            s.Toplam  
            from  
            SevkiyatTB s,UretimTB u  
              
            s.KasaNo=u.KasaNo  
            order by s.Tarih desc  


        
        """



        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    
    def getSevkiyatListeHepsiMekmar(self):
        
        result = self.data.getList("""
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID
				

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where Year(s.Tarih) in ('2022','2021') and m.Marketing in ('Mekmar')
                order by s.Tarih desc

            
        
        
        
        """
        )
        """ İLK SORGU
            
            select  
            s.ID,  
            s.Tarih,  
            (  
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID  
            ) as Kime,  
            (  
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID  
            ) as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori, 
            s.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,  
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.KutuAdet,  
            u.Miktar,  
            (  
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID  
            ) as Birim,  
            s.CikisNo,  
            s.BirimFiyat,  
            s.Toplam  
            from  
            SevkiyatTB s,UretimTB u  
              
            s.KasaNo=u.KasaNo  
            order by s.Tarih desc  


        
        """



        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeAllMekmar(self):
        
        result = self.data.getList("""
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)
				where m.Marketing in ('Mekmar')
                order by s.Tarih desc

            
        
        
        
        """
        )
        """ İLK SORGU
            
            select  
            s.ID,  
            s.Tarih,  
            (  
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID  
            ) as Kime,  
            (  
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID  
            ) as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori, 
            s.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,  
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.KutuAdet,  
            u.Miktar,  
            (  
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID  
            ) as Birim,  
            s.CikisNo,  
            s.BirimFiyat,  
            s.Toplam  
            from  
            SevkiyatTB s,UretimTB u  
              
            s.KasaNo=u.KasaNo  
            order by s.Tarih desc  


        
        """



        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)


    
    
    
    
    
    def getSevkiyatListeTarihMekmar(self,tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE s.Tarih <= ? and m.Marketing in ('Mekmar')

                order by s.Tarih desc 
            """,(tarih)
        )
        """ TEK TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and s.Tarih<=?
            order by s.Tarih desc 
            """





        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeTekTarihMekmar(self,tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE YEAR(s.Tarih) = ? and m.Marketing in ('Mekmar')

                order by s.Tarih desc 
            """,(tarih)
        )
        """ TEK TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and YEAR(s.Tarih) =?
            order by s.Tarih desc 
            """





        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeIkiTarihMekmar(self,ilk_tarih,son_tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE s.Tarih between ? and ?  and m.Marketing in ('Mekmar')

                order by s.Tarih desc  
            """,(ilk_tarih,son_tarih)
        )

        """ İKİ TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and s.Tarih between ? and ?
            order by s.Tarih desc 
            """




        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    
    def getSevkiyatListeTarihMekmer(self,tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE s.Tarih <= ? and m.Marketing in ('Mekmer','İç Piyasa')

                order by s.Tarih desc 
            """,(tarih)
        )
        """ TEK TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and s.Tarih<=?
            order by s.Tarih desc 
            """





        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeTekTarihMekmer(self,tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE YEAR(s.Tarih) = ? and m.Marketing in ('Mekmer','İç Piyasa')

                order by s.Tarih desc 
            """,(tarih)
        )
        """ TEK TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and YEAR(s.Tarih) =?
            order by s.Tarih desc 
            """





        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeIkiTarihMekmer(self,ilk_tarih,son_tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE s.Tarih between ? and ?  and m.Marketing in ('Mekmer','İç Piyasa')

                order by s.Tarih desc  
            """,(ilk_tarih,son_tarih)
        )

        """ İKİ TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and s.Tarih between ? and ?
            order by s.Tarih desc 
            """




        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeHepsiAll(self):
        
        result = self.data.getList("""
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID,
                u.KutuIciAdet
				

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                where Year(s.Tarih) in ('2023','2022')
                order by s.Tarih desc

            
        
        
        
        """
        )
        """ İLK SORGU
            
            select  
            s.ID,  
            s.Tarih,  
            (  
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID  
            ) as Kime,  
            (  
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID  
            ) as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori, 
            s.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,  
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.KutuAdet,  
            u.Miktar,  
            (  
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID  
            ) as Birim,  
            s.CikisNo,  
            s.BirimFiyat,  
            s.Toplam  
            from  
            SevkiyatTB s,UretimTB u  
              
            s.KasaNo=u.KasaNo  
            order by s.Tarih desc  


        
        """



        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeAllAll(self):
        
        result = self.data.getList("""
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)
                order by s.Tarih desc

            
        
        
        
        """
        )
        """ İLK SORGU
            
            select  
            s.ID,  
            s.Tarih,  
            (  
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID  
            ) as Kime,  
            (  
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID  
            ) as Kimden,  
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori, 
            s.KasaNo,  
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,  
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,  
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,  
            dbo.Get_Olcu_En(u.UrunKartID) as En,  
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,  
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,  
            u.Adet,  
            u.KutuAdet,  
            u.Miktar,  
            (  
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID  
            ) as Birim,  
            s.CikisNo,  
            s.BirimFiyat,  
            s.Toplam  
            from  
            SevkiyatTB s,UretimTB u  
              
            s.KasaNo=u.KasaNo  
            order by s.Tarih desc  


        
        """



        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)
    
    def getSevkiyatListeTarihAll(self,tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE s.Tarih <= ? and m.Marketing

                order by s.Tarih desc 
            """,(tarih)
        )
        """ TEK TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and s.Tarih<=?
            order by s.Tarih desc 
            """





        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeTekTarihAll(self,tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE YEAR(s.Tarih) = ?
                order by s.Tarih desc 
            """,(tarih)
        )
        """ TEK TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and YEAR(s.Tarih) =?
            order by s.Tarih desc 
            """





        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    def getSevkiyatListeIkiTarihAll(self,ilk_tarih,son_tarih):

        result = self.data.getStoreList(
            """
            select 

                s.ID,
                s.Tarih,
                s.KasaNo,
                u.Adet,  
                u.KutuAdet,  
                u.Miktar,
                s.CikisNo,  
                s.BirimFiyat,  
                s.Toplam,
                m.FirmaAdi as Kime,
                t.FirmaAdi as Kimden,
                o.OcakAdi as Ocak,
                ub.BirimAdi as Birim,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as Islem,
                urun.UrunAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
				u.UrunKartID,
                u.KutuIciAdet

                from 

                SevkiyatTB s

                inner join UretimTB u on (s.KasaNo = u.KasaNo )
                inner join MusterilerTB m on (m.ID=s.MusteriID)
                inner join TedarikciTB t on (t.ID=u.TedarikciID)
                inner join UrunOcakTB o on (o.ID=u.UrunOcakID)
                inner join UrunBirimTB ub on (ub.ID=u.UrunBirimID)
                inner join UrunKartTB uk on (uk.ID = u.UrunKartID)
                inner join KategoriTB k on (k.ID = uk.KategoriID)
                inner join YuzeyKenarTB yk on (yk.ID = uk.YuzeyID) 
                inner join UrunlerTB urun on (urun.ID = uk.UrunID)
                inner join OlculerTB ol on (ol.ID = uk.OlcuID)

                
                WHERE s.Tarih between ? and ? 

                order by s.Tarih desc  
            """,(ilk_tarih,son_tarih)
        )

        """ İKİ TARİHLİ İLK SORGU
            select
            s.ID,
            s.Tarih,
            (
            Select m.FirmaAdi from MusterilerTB m where m.ID=s.MusteriID
            ) as Kime,
            (
            select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID
            ) as Kimden,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            s.KasaNo,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            (select o.OcakAdi from UrunOcakTB o where o.ID=u.UrunOcakID) as Ocak,
            dbo.Get_KenarIslem(u.UrunKartID) as Islem,
            dbo.Get_Olcu_En(u.UrunKartID) as En,
            dbo.Get_Olcu_Boy(u.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(u.UrunKartID) as Kenar,
            u.Adet,
            u.KutuAdet,
            u.Miktar,
            (
            select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID
            ) as Birim,
            s.CikisNo,
            s.BirimFiyat,
            s.Toplam
            from
            SevkiyatTB s,UretimTB u
            where
            s.KasaNo=u.KasaNo
            and s.Tarih between ? and ?
            order by s.Tarih desc 
            """




        liste = list()
        
        for item in result:

            model = self.__getModel(item)
            liste.append(model)
        
        schema = SevkiyatSchema(many=True)

        return schema.dump(liste)

    
    def __getModel(self,item):
        
        model = SevkiyatModel()
        model.id = item.ID
            
        if item.Tarih != None:
            model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")

        model.musteriadi = item.Kime 
        model.kimden = item.Kimden
        model.kasano = item.KasaNo
        model.urunadi = item.UrunAdi
        model.ocakadi = item.Ocak
        model.yuzeyadi = item.Islem
        model.en = item.En
        model.boy = item.Boy
        model.kenar = item.Kenar
        model.adet = item.Adet
        model.kutuadet = item.KutuAdet
        model.miktar = item.Miktar
        model.birimadi = item.Birim
        model.siparisno = item.CikisNo
        model.birimfiyat = item.BirimFiyat
        model.toplam = item.Toplam
        model.kategori = item.Kategori
        model.urunKartID = item.UrunKartID
        model.kutuiciadet = self.__noneControl(item.KutuIciAdet)
        model.kutuadet = self.__noneControl(item.KutuAdet)
        return model
    
    def __noneControl(self,value):
        if(value == None):
            return 0
        else:
            return value