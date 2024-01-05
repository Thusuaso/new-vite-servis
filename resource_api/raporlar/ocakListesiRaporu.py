from models.raporlar import OcakModel,OcakSchema,OcakDetaySchema,OcakDetayModel
from helpers import SqlConnect
import datetime


class OcakListesiRapor:

    def __init__(self):

        self.data = SqlConnect().data


    def getOcakListesi(self):

        result = self.data.getList(
            """
                select 
                    o.OcakAdi,
                    (select sum(u.Miktar) from UretimTB u where u.UrunBirimID=1 and u.UrunDurumID=1 and u.UrunOcakID=o.ID) as m2,
                    (select sum(u.Miktar) from UretimTB u where u.UrunBirimID=2 and u.UrunDurumID=1 and u.UrunOcakID=o.ID) as adet,
                    (select sum(u.Miktar) from UretimTB u where u.UrunBirimID=3 and u.UrunDurumID=1 and u.UrunOcakID=o.ID) as mlt,
                    (select count(*) from UretimTB u where  u.UrunDurumID=1 and u.UrunOcakID=o.ID) as kasa


                    FROM UrunOcakTB as o 

                    where o.ID!=28

            """
        )
        
        liste = list()
  
        for item in result:
            model = OcakModel()
            if item.kasa != 0 :
                

            
                



                if item.m2 == None:
                    model.mt2 = 0

                else:
                    model.mt2 = item.m2

                if item.mlt ==None:
                    model.mt =0

                else:
                    model.mt = item.mlt
            
                if item.kasa == None:
                    model.kasaSayisi = 0
                else:
                    model.kasaSayisi = item.kasa

                if item.adet == None:
                    model.adet = 0
                else:
                    model.adet = item.adet
                
                model.ocakAdi = item.OcakAdi
           

                liste.append(model)

        schema = OcakSchema(many=True)

        return schema.dump(liste)
   
    def getOcakListesiDetaylı(self,ocak_adi):
        ocak_id = self.data.getStoreList("""
        
            select ID from UrunOcakTB WHERE OcakAdi = ?
        
        
        """,(ocak_adi))
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        result = self.data.getStoreList("""
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
                ol.Kenar

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

                where Year(s.Tarih) in (2024,2023,2022) and MONTH(s.Tarih)=? and o.ID=?
                order by s.Tarih desc
        
        """,((month),ocak_id[0][0]))

        liste = list()

        for item in result:

            model = OcakDetayModel()
            model.tarih = item.Tarih
            model.kasano =item.KasaNo
            model.adet = item.Adet
            model.mt2 = item.Miktar
            model.cikisno = item.CikisNo
            model.ocakAdi = item.Ocak
            model.kategori = item.Kategori
            model.urunadi = item.UrunAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.yuzeyislem = item.Islem
            liste.append(model)

        schema = OcakDetaySchema(many=True)
        return schema.dump(liste)
        
    def getOcakListesiDetaylUretim(self,ocak_adi):
        ocak_id = self.data.getStoreList("""
        
            select ID from UrunOcakTB WHERE OcakAdi = ?
        
        
        """,(ocak_adi))
        print(ocak_id)
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        result = self.data.getStoreList("""
            select

                u.Tarih,
                u.KasaNo,  
                u.Adet,  
                u.Miktar,  
                u.SiparisAciklama,
                ur.OcakAdi,
                ol.En,
                ol.Boy,
                ol.Kenar,
                k.KategoriAdi as Kategori,
                yk.YuzeyIslemAdi as YuzeyAdi,
                urun.UrunAdi
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

                u.TedarikciID in (1,123) and UrunOcakID=? and Year(Tarih) = 2022 and MONTH(Tarih) = ?

                order by u.Tarih desc
        
        """,(ocak_id[0][0],month))

        liste2 = list()

        for item in result:

            model = OcakDetayModel()
            model.tarih = item.Tarih
            model.kasano =item.KasaNo
            model.adet = item.Adet
            model.mt2 = item.Miktar
            model.cikisno = item.SiparisAciklama
            model.ocakAdi = item.OcakAdi
            model.kategori = item.Kategori
            model.yuzeyislem = item.YuzeyAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.urunadi = item.UrunAdi
            
            liste2.append(model)

        schema = OcakDetaySchema(many=True)
        return schema.dump(liste2)
        

