from helpers import SqlConnect


class Odemeler:

    def __init__(self,yil):

        self.data = SqlConnect().data
        
        self.dtOdemeList = self.data.getStoreList(

            """
            select
            o.SiparisNo,
            o.MusteriID,
            o.Tutar 
            from OdemelerTB o
            where Year(o.Tarih)=?
            and o.SiparisNo in 
            (
                Select s.SiparisNo from SiparislerTB s where s.SiparisNo=o.SiparisNo
                and s.SiparisDurumID=3
            )
            """,(yil)
        )

        self.dtEskiOdemeList = self.data.getStoreList(

            """
            select
            o.SiparisNo,
            o.MusteriID,
            o.Tutar 
            from OdemelerTB o
            where Year(o.Tarih)<?
            and o.SiparisNo in 
            (
                Select s.SiparisNo from SiparislerTB s where s.SiparisNo=o.SiparisNo
                and s.SiparisDurumID=3
                
            )
            """,(yil)
        )

        self.dtPesinatList = self.data.getStoreList(
            """
            select
            o.Tutar,
            o.MusteriID
            from
            OdemelerTB o,SiparislerTB s
            where
            s.SiparisNo=o.SiparisNo
            and s.SiparisDurumID in (1,2)
            and Year(o.Tarih)=?
            """,(yil)
        )
       
        self.dtEskiPesinatList = self.data.getStoreList(
            """
            select
            o.SiparisNo,
            o.MusteriID,
            o.Tutar
            from
            OdemelerTB o
            where
            o.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s where
            s.SiparisNo=o.SiparisNo and s.SiparisDurumID in (1,2)
            )
            and Year(o.Tarih)<?
            """,(yil)
        )
        

    def getOdeme(self,musteriid):

        odeme_toplam = float(0)

        for item in self.dtOdemeList:

            if musteriid == item.MusteriID and item.Tutar != None:
                odeme_toplam += float(item.Tutar)

        return odeme_toplam

    def getOdeme_GecenYil(self,musteriid):

        odeme_toplam = float(0)

        for item in self.dtEskiOdemeList:

            if musteriid == item.MusteriID and item.Tutar != None:
                odeme_toplam += float(item.Tutar)

        return odeme_toplam

    def getPesinat(self,musteriid):

        odeme_toplam = float(0)

        for item in self.dtPesinatList:

            if musteriid == item.MusteriID and item.Tutar != None :
                odeme_toplam += float(item.Tutar)

        return odeme_toplam

    def getEskiPesinat(self,musteri_id):

        tutar = 0
       
        for item in self.dtEskiPesinatList:
            if item.MusteriID == musteri_id:
                tutar += item.Tutar

        
        return tutar

    def getKapanmayanSiparis(self,musteri_id):

        result = self.data.getStoreList(
            """
         select   
            sum(u.SatisToplam) as fob,  
         
            s.NavlunSatis,  
            s.DetayTutar_1,  
            s.DetayTutar_2,  
            s.DetayTutar_3,  
           (select sum(Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odemeler 
  
            
            from  
            SiparislerTB s , SiparisUrunTB u   
            where s.SiparisNo = u.SiparisNo  
            and s.MusteriID=?
            AND s.SiparisDurumID =3  
   
            group by s.SiparisNo,s.NavlunSatis, s.MusteriID ,  
            s.DetayTutar_1,  
            s.DetayTutar_2,  
            s.DetayTutar_3 

            """,(musteri_id)
        )
       
        masraf = 0
        top = 0
        kalan = 0
        for item in result : 
           
           top = item.fob + item.NavlunSatis + item.DetayTutar_1 +   item.DetayTutar_2 +   item.DetayTutar_3
           if item.Odemeler == None :
               item.Odemeler = 0
           if top - item.Odemeler > 10 : 
              masraf +=top
              kalan += top - item.Odemeler
           else :
               masraf = masraf   
       
        return masraf , kalan
    
class OdemelerNew:
    def __init__(self,yil):

        self.data = SqlConnect().data
        
        self.dtOdemeList = self.data.getStoreList(

            """
            select
            o.SiparisNo,
            o.MusteriID,
            o.Tutar 
            from OdemelerTB o
            where Year(o.Tarih)=?
            and o.SiparisNo in 
            (
                Select s.SiparisNo from SiparislerTB s where s.SiparisNo=o.SiparisNo
                and s.SiparisDurumID=3
            )
            """,(yil)
        )

        self.dtEskiOdemeList = self.data.getStoreList(

            """
            select
            o.SiparisNo,
            o.MusteriID,
            o.Tutar 
            from OdemelerTB o
            where Year(o.Tarih)<?
            and o.SiparisNo in 
            (
                Select s.SiparisNo from SiparislerTB s where s.SiparisNo=o.SiparisNo
                and s.SiparisDurumID=3
                
            )
            """,(yil)
        )

        self.dtPesinatList = self.data.getStoreList(
            """
            select
            o.Tutar,
            o.MusteriID
            from
            OdemelerTB o,SiparislerTB s
            where
            s.SiparisNo=o.SiparisNo
            and s.SiparisDurumID in (1,2)
            and Year(o.Tarih)=?
            """,(yil)
        )
       
        self.dtEskiPesinatList = self.data.getStoreList(
            """
            select
            o.SiparisNo,
            o.MusteriID,
            o.Tutar
            from
            OdemelerTB o
            where
            o.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s where
            s.SiparisNo=o.SiparisNo and s.SiparisDurumID in (1,2)
            )
            and Year(o.Tarih)<?
            """,(yil)
        )
        

    def getOdeme(self,musteriid):

        odeme_toplam = float(0)

        for item in self.dtOdemeList:

            if musteriid == item.MusteriID and item.Tutar != None:
                odeme_toplam += float(item.Tutar)

        return odeme_toplam

    def getOdeme_GecenYil(self,musteriid):

        odeme_toplam = float(0)

        for item in self.dtEskiOdemeList:

            if musteriid == item.MusteriID and item.Tutar != None:
                odeme_toplam += float(item.Tutar)

        return odeme_toplam

    def getPesinat(self,musteriid):

        odeme_toplam = float(0)

        for item in self.dtPesinatList:

            if musteriid == item.MusteriID and item.Tutar != None :
                odeme_toplam += float(item.Tutar)

        return odeme_toplam

    def getEskiPesinat(self,musteri_id):

        tutar = 0
       
        for item in self.dtEskiPesinatList:
            if item.MusteriID == musteri_id:
                tutar += item.Tutar

        
        return tutar

    def getKapanmayanSiparis(self,musteri_id):

        result = self.data.getStoreList(
            """
         select   
            sum(u.SatisToplam) as fob,  
         
            s.NavlunSatis,  
            s.DetayTutar_1,  
            s.DetayTutar_2,  
            s.DetayTutar_3,  
           (select sum(Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odemeler 
  
            
            from  
            SiparislerTB s , SiparisUrunTB u   
            where s.SiparisNo = u.SiparisNo  
            and s.MusteriID=?
            AND s.SiparisDurumID =3  
   
            group by s.SiparisNo,s.NavlunSatis, s.MusteriID ,  
            s.DetayTutar_1,  
            s.DetayTutar_2,  
            s.DetayTutar_3 

            """,(musteri_id)
        )
       
        masraf = 0
        top = 0
        kalan = 0
        for item in result : 
           
           top = item.fob + item.NavlunSatis + item.DetayTutar_1 +   item.DetayTutar_2 +   item.DetayTutar_3
           if item.Odemeler == None :
               item.Odemeler = 0
           if top - item.Odemeler > 10 : 
              masraf +=top
              kalan += top - item.Odemeler
           else :
               masraf = masraf   
       
        return masraf , kalan
    