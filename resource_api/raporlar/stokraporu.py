from models.raporlar import StokSchema,StokModel,StokTopSchema,StokTopModel,StokTopAyrintiModel,StokTopAyrintiSchema,StokEbatModel,StokEbatSchema,StokAnaListeSchema,StokAnaListeModel
from helpers import SqlConnect
from openpyxl import *
from openpyxl.styles import Border, Side , Font ,Alignment,PatternFill
from openpyxl.cell import Cell
import shutil


class StokRapor:

    def __init__(self):

        self.data = SqlConnect().data
        self.resultMiktarList = self.data.getList("""
                                                select

                                                    sum(ur.Miktar) as Miktar,
                                                    ur.UrunKartID as UrunID

                                                from
                                                    UretimTB ur

                                                where
                                                    ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1
                                                group by 
                                                    ur.UrunKartID
                                             
                                             
                                             """)
        self.resultMiktarMekmer = self.data.getList("""
                                                       select

                                                            sum(ur.Miktar) as Miktar,
                                                            ur.UrunKartID as UrunID

                                                        from
                                                            UretimTB ur

                                                        where
                                                            ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID in (1)
                                                        group by 
                                                            ur.UrunKartID 
                                                    
                                                    
                                                    """)
        self.resultMiktarMekMoz = self.data.getList("""
                                                        select

                                                            sum(ur.Miktar) as Miktar,
                                                            ur.UrunKartID as UrunID

                                                        from
                                                            UretimTB ur

                                                        where
                                                            ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID in (123)
                                                        group by 
                                                            ur.UrunKartID
                                                    
                                                    
                                                    """)
        self.resultMiktarOnlyMekmer = self.data.getList("""
                                                            select

                                                            sum(ur.Miktar) as Miktar,
                                                            ur.UrunKartID as UrunID

                                                        from
                                                            UretimTB ur

                                                        where
                                                            ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID in (1,123) and ur.UretimTurID=1
                                                        group by 
                                                            ur.UrunKartID
                                                        
                                                        
                                                        
                                                        """)
        
        self.resultMiktarOnlyStocksMekmerMekmoz = self.data.getList("""
                                                            select

                                                            sum(ur.Miktar) as Miktar,
                                                            ur.UrunKartID as UrunID

                                                        from
                                                            UretimTB ur

                                                        where
                                                            ur.UrunDurumID in (1) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID in (1,123) and ur.SiparisAciklama = 'Stok'
                                                        group by 
                                                            ur.UrunKartID
                                                        """)
        self.resultMiktarOnlyStocksDis = self.data.getList("""
                                                            select

                                                            sum(ur.Miktar) as Miktar,
                                                            ur.UrunKartID as UrunID

                                                        from
                                                            UretimTB ur

                                                        where
                                                            ur.UrunDurumID in (1) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.Disarda = 1 and ur.TedarikciID not in (1,123)
                                                        group by 
                                                            ur.UrunKartID
                                                        """)
        self.resultMiktarOnlyStocksDisMekmerdeOlan = self.data.getList("""
                                                            select

                                                            sum(ur.Miktar) as Miktar,
                                                            ur.UrunKartID as UrunID

                                                        from
                                                            UretimTB ur

                                                        where
                                                            ur.UrunDurumID in (1) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.Disarda != 1 and ur.TedarikciID not in (1,123)
                                                        group by 
                                                            ur.UrunKartID
                                                        """)
    
    
    def getStokListesiHepsi(self):

        result = self.data.getList(
            """
                select  
                [dbo].[Get_Ebat](ur.UrunKartID) as Ebat,  
                [dbo].[Get_KategoriAdi](ur.UrunKartID) as Kategori,  
                [dbo].[Get_KenarIslem](ur.UrunKartID) as YuzeyIslem,  
                [dbo].[Get_UrunAdi](ur.UrunKartID) as UrunAdi,  
              
                ur.UrunKartID,  
                Count(*) as KasaAdet               
                from  
                UretimTB ur  
                where   
                 ur.UrunDurumID=1 and ur.Disarda=0
                group by   
                [dbo].[Get_Ebat](ur.UrunKartID),  
                [dbo].[Get_KategoriAdi](ur.UrunKartID),  
                
                [dbo].[Get_KenarIslem](ur.UrunKartID),  
              
                [dbo].[Get_UrunAdi](ur.UrunKartID),  
                ur.UrunKartID
               


            """
        )
        
        liste = list()
  
        for item in result:

            model = StokModel()

            model.ebat = item.Ebat
            model.kategori = item.Kategori
            model.yuzey_islem = item.YuzeyIslem
            model.urun_adi = item.UrunAdi
           
            model.urunkart_id = item.UrunKartID
            model.kasa_adet = item.KasaAdet
           

            liste.append(model)

        schema = StokSchema(many=True)

        return schema.dump(liste)
   
    def getStokTopListesi(self):

        result = self.data.getList(
            """
            select  
            top 10  
            [dbo].[Get_KategoriAdi](ur.UrunKartID) as Kategori,  
            [dbo].[Get_Ebat](ur.UrunKartID) as Ebat,  
            t.FirmaAdi as TedarikciAdi,  
            [dbo].[Get_KenarIslem](ur.UrunKartID) as YuzeyIslem,  
            [dbo].[Get_UrunAdi](ur.UrunKartID) as UrunAdi,  
         
            ur.UrunKartID,  
            Count(*) as KasaAdet,  
            t.ID as TedarikciID               
            from  
            UretimTB ur,TedarikciTB t  
            where   
            ur.TedarikciID=t.ID and ur.UrunDurumID=1  and ur.Disarda=0
            group by   
            [dbo].[Get_Ebat](ur.UrunKartID),  
            t.FirmaAdi,  
            [dbo].[Get_KenarIslem](ur.UrunKartID),  
            ur.Kutu,  
            [dbo].[Get_UrunAdi](ur.UrunKartID),  
            ur.UrunKartID,  
            t.ID ,  
            [dbo].[Get_KategoriAdi](ur.UrunKartID)  
            order by Count(*) desc  

            """
        )
        
        liste = list()

        for item in result:

            model = StokTopModel()

            model.ebattop = item.Ebat
            model.kategoritop = item.Kategori
            model.tedarikci_aditop = item.TedarikciAdi
            model.yuzey_islemtop = item.YuzeyIslem
            model.urun_aditop = item.UrunAdi
           
            model.urunkart_idtop = item.UrunKartID
            model.kasa_adettop = item.KasaAdet
            model.tedarikci_idtop = item.TedarikciID
           

            liste.append(model)

        schema = StokTopSchema(many=True)

        return schema.dump(liste)

    def getStokTopAyrintiListesi(self,en,boy,kenar,yuzeyIslem,urunAdi):
        result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 

            ur.UrunDurumID in (1,2) and 
            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
            urn.UrunAdi=? and 
            olc.En=? and 
            olc.Boy=? and 
            olc.Kenar=? and 
            yz.YuzeyIslemAdi=?
            


            

            """,(urunAdi,en,boy,kenar,yuzeyIslem)
        )
        """
            
            select  
            ur.ID,
            t.FirmaAdi as TedarikciAdi,  
            [dbo].[Get_KategoriAdi](ur.UrunKartID) as KategoriAdi,  
            ur.Tarih,  
            ur.KasaNo,  
            [dbo].[Get_UrunAdi](ur.UrunKartID) as UrunAdi,  
            ub.OcakAdi,  
            [dbo].[Get_KenarIslem](ur.UrunKartID) as YuzeyIslem,  
            [dbo].[Get_Olcu_En](ur.UrunKartID) as En,  
            [dbo].[Get_Olcu_Boy](ur.UrunKartID) as Boy,  
            [dbo].[Get_Olcu_Kenar](ur.UrunKartID) as Kenar,  
            ur.Adet,  
            ur.Miktar,  
            b.BirimAdi,  
            ur.Aciklama,  
            ur.KutuAdet  ,
            ur.SiparisAciklama
            from  
            UretimTB ur,TedarikciTB t,UrunOcakTB ub,UrunBirimTB b  
            where  
            ur.TedarikciID=t.ID  and ur.UrunDurumID=1  and ur.Disarda=0
            and ub.ID=ur.UrunOcakID and b.ID=ur.UrunBirimID  and
            (ur.UrunKartID)=?
            order by ur.SiparisAciklama desc
            

            """
        liste = list()
        sira = 1
        for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

        schema = StokTopAyrintiSchema(many=True)

        return schema.dump(liste)
    
    def getStokTopAyrintiListesiMekmer(self,en,boy,kenar,yuzeyIslem,urunAdi):
        result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 
            ur.TedarikciID = 1 and
            ur.UrunDurumID in (1,2) and 
            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
            urn.UrunAdi=? and 
            olc.En=? and 
            olc.Boy=? and 
            olc.Kenar=? and 
            yz.YuzeyIslemAdi=?
            


            

            """,(urunAdi,en,boy,kenar,yuzeyIslem)
        )
        """
            
            select  
            ur.ID,
            t.FirmaAdi as TedarikciAdi,  
            [dbo].[Get_KategoriAdi](ur.UrunKartID) as KategoriAdi,  
            ur.Tarih,  
            ur.KasaNo,  
            [dbo].[Get_UrunAdi](ur.UrunKartID) as UrunAdi,  
            ub.OcakAdi,  
            [dbo].[Get_KenarIslem](ur.UrunKartID) as YuzeyIslem,  
            [dbo].[Get_Olcu_En](ur.UrunKartID) as En,  
            [dbo].[Get_Olcu_Boy](ur.UrunKartID) as Boy,  
            [dbo].[Get_Olcu_Kenar](ur.UrunKartID) as Kenar,  
            ur.Adet,  
            ur.Miktar,  
            b.BirimAdi,  
            ur.Aciklama,  
            ur.KutuAdet  ,
            ur.SiparisAciklama
            from  
            UretimTB ur,TedarikciTB t,UrunOcakTB ub,UrunBirimTB b  
            where  
            ur.TedarikciID=t.ID  and ur.UrunDurumID=1  and ur.Disarda=0
            and ub.ID=ur.UrunOcakID and b.ID=ur.UrunBirimID  and
            (ur.UrunKartID)=?
            order by ur.SiparisAciklama desc
            

            """
        liste = list()
        sira = 1
        for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

        schema = StokTopAyrintiSchema(many=True)

        return schema.dump(liste)
    
    
    
    def getStokTopAyrintiListesiMekmoz(self,en,boy,kenar,yuzeyIslem,urunAdi):
        result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 
            ur.TedarikciID = 123 and
            ur.UrunDurumID in (1,2) and 
            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
            urn.UrunAdi=? and 
            olc.En=? and 
            olc.Boy=? and 
            olc.Kenar=? and 
            yz.YuzeyIslemAdi=?
            


            

            """,(urunAdi,en,boy,kenar,yuzeyIslem)
        )
        """
            
            select  
            ur.ID,
            t.FirmaAdi as TedarikciAdi,  
            [dbo].[Get_KategoriAdi](ur.UrunKartID) as KategoriAdi,  
            ur.Tarih,  
            ur.KasaNo,  
            [dbo].[Get_UrunAdi](ur.UrunKartID) as UrunAdi,  
            ub.OcakAdi,  
            [dbo].[Get_KenarIslem](ur.UrunKartID) as YuzeyIslem,  
            [dbo].[Get_Olcu_En](ur.UrunKartID) as En,  
            [dbo].[Get_Olcu_Boy](ur.UrunKartID) as Boy,  
            [dbo].[Get_Olcu_Kenar](ur.UrunKartID) as Kenar,  
            ur.Adet,  
            ur.Miktar,  
            b.BirimAdi,  
            ur.Aciklama,  
            ur.KutuAdet  ,
            ur.SiparisAciklama
            from  
            UretimTB ur,TedarikciTB t,UrunOcakTB ub,UrunBirimTB b  
            where  
            ur.TedarikciID=t.ID  and ur.UrunDurumID=1  and ur.Disarda=0
            and ub.ID=ur.UrunOcakID and b.ID=ur.UrunBirimID  and
            (ur.UrunKartID)=?
            order by ur.SiparisAciklama desc
            

            """
        liste = list()
        sira = 1
        for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

        schema = StokTopAyrintiSchema(many=True)

        return schema.dump(liste)
    
    
    def getStokTopAyrintiListesiOnlyStockMekmer(self,en,boy,kenar,yuzeyIslem,urunAdi):
        result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 
            ur.TedarikciID in (1,123) and
            ur.UretimTurID=1 and
            ur.UrunDurumID in (1,2) and 
            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
            urn.UrunAdi=? and 
            olc.En=? and 
            olc.Boy=? and 
            olc.Kenar=? and 
            yz.YuzeyIslemAdi=?
            


            

            """,(urunAdi,en,boy,kenar,yuzeyIslem)
        )
        """
            
            select  
            ur.ID,
            t.FirmaAdi as TedarikciAdi,  
            [dbo].[Get_KategoriAdi](ur.UrunKartID) as KategoriAdi,  
            ur.Tarih,  
            ur.KasaNo,  
            [dbo].[Get_UrunAdi](ur.UrunKartID) as UrunAdi,  
            ub.OcakAdi,  
            [dbo].[Get_KenarIslem](ur.UrunKartID) as YuzeyIslem,  
            [dbo].[Get_Olcu_En](ur.UrunKartID) as En,  
            [dbo].[Get_Olcu_Boy](ur.UrunKartID) as Boy,  
            [dbo].[Get_Olcu_Kenar](ur.UrunKartID) as Kenar,  
            ur.Adet,  
            ur.Miktar,  
            b.BirimAdi,  
            ur.Aciklama,  
            ur.KutuAdet  ,
            ur.SiparisAciklama
            from  
            UretimTB ur,TedarikciTB t,UrunOcakTB ub,UrunBirimTB b  
            where  
            ur.TedarikciID=t.ID  and ur.UrunDurumID=1  and ur.Disarda=0
            and ub.ID=ur.UrunOcakID and b.ID=ur.UrunBirimID  and
            (ur.UrunKartID)=?
            order by ur.SiparisAciklama desc
            

            """
        liste = list()
        sira = 1
        for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

        schema = StokTopAyrintiSchema(many=True)

        return schema.dump(liste)
    
    
    def getStokRaporMekmerMekmoz(self):
        try:
            
            result = self.data.getList("""
                                            select 

                                            count(urn.UrunAdi) as KasaSayisi,
                                            urn.UrunAdi,
                                            olc.En,
                                            olc.Boy,
                                            olc.Kenar,
                                            yz.YuzeyIslemAdi,
                                            ur.UrunKartID,
                                            (select ukt.Price from UrunKartTB ukt where ukt.ID = ur.UrunKartID) as Price
                                            



                                        from UretimTB ur
                                            inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                                            inner join UrunlerTB urn on urn.ID = uk.UrunID
                                            inner join OlculerTB olc on olc.ID=uk.OlcuID
                                            inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                                        where 

                                        ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID in (1,123) and ur.SiparisAciklama ='Stok'

                                        group by ur.UrunKartID,urn.UrunAdi,olc.En,olc.Boy,olc.Kenar,yz.YuzeyIslemAdi
                                        order by olc.En
                                       
                                       
                                       """)
            
            liste = list()
            for item in result:

                model = StokAnaListeModel()
                model.urunKartId = item.UrunKartID
                model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
                model.kasaSayisi = item.KasaSayisi
                model.yuzeyIslem = item.YuzeyIslemAdi
                model.urunAdi = item.UrunAdi
                model.en = item.En
                model.boy = item.Boy
                model.kenar = item.Kenar
                model.price = item.Price
                model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarOnlyStocksMekmerMekmoz)
                
                liste.append(model)

            schema = StokAnaListeSchema(many=True)

            return schema.dump(liste)
        except Exception as e:
            print('getStokRaporMekmerMekmoz hata',str(e))
            return False
    
    def getStokRaporDis(self):
        try:
            
            result = self.data.getList("""
                                            select 

                                            count(urn.UrunAdi) as KasaSayisi,
                                            urn.UrunAdi,
                                            olc.En,
                                            olc.Boy,
                                            olc.Kenar,
                                            yz.YuzeyIslemAdi,
                                            ur.UrunKartID,
                                            (select ukt.Price from UrunKartTB ukt where ukt.ID = ur.UrunKartID) as Price
                                            



                                        from UretimTB ur
                                            inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                                            inner join UrunlerTB urn on urn.ID = uk.UrunID
                                            inner join OlculerTB olc on olc.ID=uk.OlcuID
                                            inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                                        where 

                                        ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID not in (1,123) and ur.Disarda= 1

                                        group by ur.UrunKartID,urn.UrunAdi,olc.En,olc.Boy,olc.Kenar,yz.YuzeyIslemAdi
                                        order by olc.En
                                       
                                       
                                       """)
            
            liste = list()
            for item in result:

                model = StokAnaListeModel()
                model.urunKartId = item.UrunKartID
                model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
                model.kasaSayisi = item.KasaSayisi
                model.yuzeyIslem = item.YuzeyIslemAdi
                model.urunAdi = item.UrunAdi
                model.en = item.En
                model.boy = item.Boy
                model.kenar = item.Kenar
                model.price = item.Price
                model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarOnlyStocksDis)
                
                liste.append(model)

            schema = StokAnaListeSchema(many=True)

            return schema.dump(liste)
        except Exception as e:
            print('getStokRaporMekmerMekmoz hata',str(e))
            return False
    
    def getStokRaporDisMekmardaOlanlar(self):
        try:
            
            result = self.data.getList("""
                                            select 

                                            count(urn.UrunAdi) as KasaSayisi,
                                            urn.UrunAdi,
                                            olc.En,
                                            olc.Boy,
                                            olc.Kenar,
                                            yz.YuzeyIslemAdi,
                                            ur.UrunKartID,
                                            (select ukt.Price from UrunKartTB ukt where ukt.ID = ur.UrunKartID) as Price
                                            



                                        from UretimTB ur
                                            inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                                            inner join UrunlerTB urn on urn.ID = uk.UrunID
                                            inner join OlculerTB olc on olc.ID=uk.OlcuID
                                            inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                                        where 

                                        ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID not in (1,123) and ur.Disarda != 1

                                        group by ur.UrunKartID,urn.UrunAdi,olc.En,olc.Boy,olc.Kenar,yz.YuzeyIslemAdi
                                        order by olc.En
                                       
                                       
                                       """)
            
            liste = list()
            for item in result:

                model = StokAnaListeModel()
                model.urunKartId = item.UrunKartID
                model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
                model.kasaSayisi = item.KasaSayisi
                model.yuzeyIslem = item.YuzeyIslemAdi
                model.urunAdi = item.UrunAdi
                model.en = item.En
                model.boy = item.Boy
                model.kenar = item.Kenar
                model.price = item.Price
                model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarOnlyStocksDisMekmerdeOlan)
                
                liste.append(model)

            schema = StokAnaListeSchema(many=True)

            return schema.dump(liste)
        except Exception as e:
            print('getStokRaporMekmerMekmoz hata',str(e))
            return False
    
     
                   
    def getStokRaporMekmerMekmozAyrinti(self,urunId):
       result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 

            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
			ur.TedarikciID in (1,123) and
            ur.SiparisAciklama ='Stok' and
			ur.UrunKartID=?
            


            

            """,(urunId)
        )
       liste = list()
       sira = 1
       for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

       schema = StokTopAyrintiSchema(many=True)

       return schema.dump(liste)
            
    def getStokRaporDisAyrinti(self,urunId):
       result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 

            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
			ur.TedarikciID not in (1,123) and
			ur.Disarda = 1 and
			ur.UrunKartID=?
            


            

            """,(urunId)
        )
       liste = list()
       sira = 1
       for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

       schema = StokTopAyrintiSchema(many=True)

       return schema.dump(liste)
    
    def getStokRaporDisMekmardaOlanAyrinti(self,urunId):
       result = self.data.getStoreList(
            """
            
            select 
                ur.ID as ID,
                urn.UrunAdi as UrunAdi,
                olc.En as En,
                olc.Boy as Boy,
                olc.Kenar as Kenar,
                yz.YuzeyIslemAdi as YuzeyIslem,
                tb.FirmaAdi as TedarikciAdi,
                ur.KasaNo,
                ur.Tarih,
                ur.Adet,
                ur.Miktar,
                ur.Aciklama,
                ur.KutuAdet,
                ur.SiparisAciklama,
                urb.BirimAdi,
                ock.OcakAdi,
                ktg.KategoriAdi


            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
                inner join UrunBirimTB urb on urb.ID = ur.UrunBirimID
                inner join UrunOcakTB ock on ock.ID = ur.UrunOcakID
                inner join KategoriTB ktg on ktg.ID = uk.KategoriID
            where 

            ur.Aciklama != 'bulunamadı' and
            ur.UrunDurumID=1 and
			ur.TedarikciID not in (1,123) and
			ur.Disarda != 1 and
			ur.UrunKartID=?
            


            

            """,(urunId)
        )
       liste = list()
       sira = 1
       for item in result:

            model = StokTopAyrintiModel()
            model.id = item.ID
            model.kategoritop = item.KategoriAdi
            model.sira = sira
            sira = sira + 1
            model.tedarikci_aditop = item.TedarikciAdi
            model.tarihtop = item.Tarih
            model.kasanotop = item.KasaNo
            model.urunaditop = item.UrunAdi
            model.ocakaditop = item.OcakAdi
            model.yuzeyislemtop = item.YuzeyIslem
            model.entop = item.En
            model.boytop = item.Boy
            model.kenartop =  item.Kenar
            model.adettop = item.Adet
            model.miktartop =  item.Miktar
            model.birimaditop =  item.BirimAdi
            
            model.kutuadettop = item.KutuAdet
            model.durum = item.SiparisAciklama
            model.aciklama = item.Aciklama

            liste.append(model)

       schema = StokTopAyrintiSchema(many=True)

       return schema.dump(liste)
               
    def setStockExcellCikti(self,data_list):
        try:
            source_path = 'resource_api/raporlar/sablonlar/stock_list_fiyatli.xlsx'
            target_path = 'resource_api/raporlar/dosyalar/stock_list_fiyatli.xlsx'

            shutil.copy2(source_path, target_path)


            kitap = load_workbook(target_path)
            sayfa = kitap.get_sheet_by_name('Sayfa1')

            satir = 2
            
            for item in data_list:
               
                sayfa.cell(satir,column=1,value=item['urunAdi'])
                sayfa.cell(satir,column=2,value=item['yuzeyIslem']) 
                sayfa.cell(satir,column=3,value=item['en'])  
                sayfa.cell(satir,column=4,value=item['boy'])             
                sayfa.cell(satir,column=5,value=item['kenar'])
                sayfa.cell(satir,column=6,value=item['miktar'])
                if(item['price'] == None):
                    sayfa.cell(satir,column=7,value=0)
                else: 
                    sayfa.cell(satir,column=7,value=item['price'])
                
                
                satir += 1
           
            kitap.save(target_path)
            kitap.close()

            return True

        except Exception as e:
            print('setStockExcellCikti Hata : ',str(e))
            return False 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def getStokOlculerListesi(self):

        result = self.data.getList(
            """
                select 

                    ol.En as EN,ol.Boy as BOY,ol.Kenar as KENAR,count(ol.ID) as KASAADET

                from UretimTB ur
                    inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                    inner join OlculerTB ol on uk.OlcuID = ol.ID


                where ur.Bulunamadi=0 and ur.UrunDurumID=1

                group by ol.En,ol.Boy,ol.Kenar,ol.ID
            
            
            """
        )
        """
           select
                sum(ur.KasaNo),
                ur.UrunKartID,
                o.En as EN,
                o.Boy as BOY,
                o.Kenar as KENAR
                
            from
                UretimTB ur
                inner join UrunKartTB uk on ur.UrunKartID=uk.ID
                inner join OlculerTB o on uk.OlcuID = o.ID
                where ur.UrunDurumID=1

                group by ur.UrunKartID,o.En,o.Boy,o.Kenar
                order by UrunKartID desc

            """
        
        liste = list()
        for item in result:

            model = StokEbatModel()

            model.ebat = item.EN +'x'+ item.BOY +'x'+ item.KENAR
            model.kasaadet = item.KASAADET

            liste.append(model)

        schema = StokEbatSchema(many=True)

        return schema.dump(liste)

    def getStokAnaList(self):

        resultStockList = self.data.getList(
            """
            select 

                count(urn.UrunAdi) as KasaSayisi,
                urn.UrunAdi,
                olc.En,
                olc.Boy,
                olc.Kenar,
                yz.YuzeyIslemAdi,
                ur.UrunKartID,
                (select ukt.Price from UrunKartTB ukt where ukt.ID = ur.UrunKartID) as Price
                



            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
            where 

            ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.Bulunamadi != 1

            group by ur.UrunKartID,urn.UrunAdi,olc.En,olc.Boy,olc.Kenar,yz.YuzeyIslemAdi
            order by olc.En
            
            """
        )
        
        liste = list()
        for item in resultStockList:

            model = StokAnaListeModel()
            model.urunKartId = item.UrunKartID
            model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
            model.kasaSayisi = item.KasaSayisi
            model.yuzeyIslem = item.YuzeyIslemAdi
            model.urunAdi = item.UrunAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.price = item.Price
            model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarList)
            
            liste.append(model)

        schema = StokAnaListeSchema(many=True)

        return schema.dump(liste)

    def getStokAnaListMiktarKontrol(self,urunKartId,result):
        for item in result:
            if item.UrunID == urunKartId:
                
                return item.Miktar
    
    
    def getStokFilterList(self,tedarikci):
        result = self.data.getStoreList(
            """
           select 

            count(urn.UrunAdi) as KasaSayisi,
            urn.UrunAdi,
            olc.En,
            olc.Boy,
            olc.Kenar,
            yz.YuzeyIslemAdi,
            ur.UrunKartID


        from UretimTB ur
            inner join UrunKartTB uk on uk.ID=ur.UrunKartID
            inner join UrunlerTB urn on urn.ID = uk.UrunID
            inner join OlculerTB olc on olc.ID=uk.OlcuID
            inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
        where 

        ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID=? and ur.Bulunamadi != 1

        group by urn.UrunAdi,olc.En,olc.Boy,olc.Kenar,yz.YuzeyIslemAdi,ur.UrunKartID
        order by olc.En

            """,(tedarikci)
        )
        
        liste = list()
        for item in result:

            model = StokAnaListeModel()

            model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
            model.kasaSayisi = item.KasaSayisi
            model.yuzeyIslem = item.YuzeyIslemAdi
            model.urunAdi = item.UrunAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            if tedarikci == 1:
                model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarMekmer)
            elif tedarikci == 123:
                model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarMekMoz)
            liste.append(model)

        schema = StokAnaListeSchema(many=True)

        return schema.dump(liste)
    
    def getStokAyrintiList(self):
        result = self.data.getList(
            """
           select 

                urn.UrunAdi,
                olc.En,
                olc.Boy,
                olc.Kenar,
                yz.YuzeyIslemAdi,
                tb.FirmaAdi



            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
                inner join TedarikciTB tb on tb.ID = ur.TedarikciID
            where 

            ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and urn.UrunAdi=? and olc.En=? and olc.Boy=? and olc.Kenar=?

            """
        )
        
        liste = list()
        for item in result:

            model = StokAnaListeModel()

            model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
            model.kasaSayisi = item.KasaSayisi
            model.yuzeyIslem = item.YuzeyIslemAdi
            model.urunAdi = item.UrunAdi
            model.tedarikciAdi = item.FirmaAdi
            liste.append(model)

        schema = StokAnaListeSchema(many=True)

        return schema.dump(liste)

    def getStokOnlyMekmer(self):

        resultStockList = self.data.getList(
            """
            select 

                count(urn.UrunAdi) as KasaSayisi,
                urn.UrunAdi,
                olc.En,
                olc.Boy,
                olc.Kenar,
                yz.YuzeyIslemAdi,
                ur.UrunKartID
                
                



            from UretimTB ur
                inner join UrunKartTB uk on uk.ID=ur.UrunKartID
                inner join UrunlerTB urn on urn.ID = uk.UrunID
                inner join OlculerTB olc on olc.ID=uk.OlcuID
                inner join YuzeyKenarTB yz on yz.ID= uk.YuzeyID
            where 

            ur.UrunDurumID in (1,2) and ur.Aciklama != 'bulunamadı' and ur.UrunDurumID=1 and ur.TedarikciID in (1,123) and ur.UretimTurID=1 and ur.Bulunamadi != 1

            group by ur.UrunKartID,urn.UrunAdi,olc.En,olc.Boy,olc.Kenar,yz.YuzeyIslemAdi
            order by olc.En
            
            """
        )
        
        liste = list()
        for item in resultStockList:

            model = StokAnaListeModel()

            model.ebat = item.En +'x'+ item.Boy +'x'+ item.Kenar
            model.kasaSayisi = item.KasaSayisi
            model.yuzeyIslem = item.YuzeyIslemAdi
            model.urunAdi = item.UrunAdi
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar
            model.miktar = self.getStokAnaListMiktarKontrol(item.UrunKartID,self.resultMiktarOnlyMekmer)
            
            liste.append(model)

        schema = StokAnaListeSchema(many=True)

        return schema.dump(liste)


