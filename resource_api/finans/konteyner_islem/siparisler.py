from helpers import SqlConnect
from resource_api.finans.konteyner_islem.siparis_urunler import SiparisUrunler,SiparisUrunlerNew


class SiparisModel:
    siparisNo = ""
    musteriadi = ""
    musteriid = None 
    toplam_tutar = float(0) 

class Siparisler:

    def __init__(self,yil):
        self.data = SqlConnect().data
        self.dtSiparisler = self.data.getStoreList(
            """
            Select
            s.SiparisNo,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            m.FirmaAdi,
            s.MusteriID,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId) as temsilci,
             (select sum(Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odemeler 
            from SiparislerTB s,MusterilerTB m
            where m.ID=s.MusteriID and s.SiparisDurumID=3
            and Year(YuklemeTarihi)=?
            and m.Mt_No=2
            and m.ID not in (6,34)
            """,(yil)
        )



        self.dtEskiSiparisler = self.data.getStoreList(
            """
            Select
            s.SiparisNo,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            m.FirmaAdi,
            s.MusteriID,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId) as temsilci,
             (select sum(Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odemeler 
            from SiparislerTB s,MusterilerTB m
            where m.ID=s.MusteriID and s.SiparisDurumID=3
            and Year(YuklemeTarihi)<?
            and m.Mt_No=2 
            and m.ID not in (6,34)
            """,(yil)
        )

        self.dtPesinatList = self.data.getStoreList(

            """
            select
            s.MusteriID,
            m.FirmaAdi,
            Sum(o.Tutar) as Pesinat,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId) as temsilci
            from
            SiparislerTB s,MusterilerTB m,OdemelerTB o
            where
            s.SiparisDurumID in (1,2) and s.MusteriID=m.ID
            and s.SiparisNo=o.SiparisNo
            and o.MusteriID=m.ID 
            and Year(o.Tarih)=?
            and s.SiparisNo not in
            (
            Select es.SiparisNo from SiparislerTB es
            where es.SiparisNo=s.SiparisNo
            and es.SiparisDurumID=3
            and YEAR(es.YuklemeTarihi)=?
            )
            group by s.MusteriID,m.FirmaAdi,m.Marketing,m.MusteriTemsilciId
            """,(yil,yil)
        )

        self.dtBekleyenList = self.data.getStoreList(
            """
            Select
            m.FirmaAdi,
            s.MusteriID,
			Sum(s.Pesinat) as Pesinat,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId)  as temsilci
            from SiparislerTB s,MusterilerTB m
            where m.ID=s.MusteriID and s.SiparisDurumID in (1,2)
            and m.Mt_No=2
            and m.ID not in (6,34)
			and s.Pesinat >0
			and s.SiparisNo not in
			(
			 select es.SiparisNo from SiparislerTB es
			 where es.SiparisNo=s.SiparisNo
			 and es.SiparisDurumID=3
			 and Year(es.YuklemeTarihi)=?
			)
            and s.SiparisNo in
			(
			Select o.SiparisNo from OdemelerTB o where o.SiparisNo=s.SiparisNo
			)
			group by m.FirmaAdi,s.MusteriID,m.Marketing, m.MusteriTemsilciId
            """,(yil)
        )

        self.siparis_list = list()
        self.eski_siparis_list = list()
        self.pesinat_listesi = list()
        self.bekleyen_listesi = list()

        
        
        self.urun = SiparisUrunler(yil)
        self.__getSiparis_yeni()
        self.__getSiparis_eski()
        self.__pesinatList()
        self.__getSiparis_bekleyen()

        

    def __getSiparis_yeni(self):

        for item in self.dtSiparisler:
           

            data = {
                "musteriid" : item.MusteriID,
                "musteriadi" : item.FirmaAdi,
                "siparisNo" : item.SiparisNo,
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "sigorta_tutar_satis":float(0),
                 "Odemeler" : float(0),
                "urunbedel"  : float(self.__getUrunToplam(item.SiparisNo)),
                "toplam_tutar" : float(self.__getUrunToplam(item.SiparisNo)),
                "temsilci" : item.temsilci,
                "marketing" : item.Marketing
            }
           
            toplam = float(0)
            
            if item.NavlunSatis != None:
                data['navlunsatis'] = float(item.NavlunSatis)
                toplam += float(item.NavlunSatis)
                

            if item.DetayTutar_1 != None:
                data['detaytutar_1'] = float(item.DetayTutar_1)
                toplam += float(item.DetayTutar_1)
                

            if item.DetayTutar_2 != None:
                data['detaytutar_2'] = float(item.DetayTutar_2)
                toplam += float(item.DetayTutar_2)
                

            if item.DetayTutar_3 != None:
                data['detaytutar_3'] = float(item.DetayTutar_3)
                toplam += float(item.DetayTutar_3)

            if item.Odemeler != None:
                data['Odemeler'] = float(item.Odemeler)
            
            if item.sigorta_tutar_satis != None:
                data['sigorta_tutar_satis'] = float(item.sigorta_tutar_satis)
            
            data['toplam_tutar'] += toplam  
            
            self.siparis_list.append(data)

    def __getSiparis_eski(self):



        for item in self.dtEskiSiparisler:

            data = {
                "musteriid" : item.MusteriID,
                "musteriadi" : item.FirmaAdi,
                "siparisNo" : item.SiparisNo,
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "sigorta_tutar_satis":float(0),
                "Odemeler" : float(0),
                "urunbedel"  : float(self.__getUrunToplam_Eski(item.SiparisNo)),
                "temsilci" : item.temsilci,
                "marketing" : item.Marketing
                
            }

            if item.NavlunSatis != None:
                data['navlunsatis'] = float(item.NavlunSatis)

            if item.DetayTutar_1 != None:
                data['detaytutar_1'] = float(item.DetayTutar_1)

            if item.DetayTutar_2 != None:
                data['detaytutar_2'] = float(item.DetayTutar_2)

            if item.DetayTutar_3 != None:
                data['detaytutar_3'] = float(item.DetayTutar_3)

            if item.Odemeler != None:
                data['Odemeler'] = float(item.Odemeler)    

            if item.sigorta_tutar_satis != None:
                data['sigorta_tutar_satis'] = float(item.sigorta_tutar_satis)
           
            
            self.eski_siparis_list.append(data)

    def __pesinatList(self):

        for item in self.dtPesinatList:

            data = {

                'musteriadi' : item.FirmaAdi,
                'musteriid' :  item.MusteriID,
                'pesinat' : float(item.Pesinat),
                "siparisNo" :"",
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "sigorta_tutar_satis":float(0),
                "Odemeler" : float(0),
                "urunbedel"  : float(0),
                "toplam_tutar" : float(0),
                "marketing" : item.Marketing,
                "temsilci" : item.temsilci
            }
          
            self.pesinat_listesi.append(data)


    def __getUrunToplam(self,siparisNo):

        urun_bedel = 0

        urunlist = list(filter(lambda x:x['siparisNo'] == siparisNo,self.urun.urunlist))
       
        for item in urunlist:
            
               
            urun_bedel += item['satisToplam']
        
        return urun_bedel

    def __getUrunToplam_Eski(self,siparisNo):

        urun_bedel = 0

        urunlist = list(filter(lambda x:x['siparisNo'] == siparisNo,self.urun.eski_urunlist))
       
        for item in urunlist:
            
               
            urun_bedel += item['satisToplam']

        
        return urun_bedel

    def __getSiparis_bekleyen(self):

        for item in self.dtBekleyenList:

            data = {
                "musteriid" : item.MusteriID,
                "musteriadi" : item.FirmaAdi,
                "pesinat"      : float(item.Pesinat),
                "siparisNo" : "",
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "Odemeler" : float(0),
                "urunbedel"  : float(0),
                "toplam_tutar" : float(0),
                "marketing" : item.Marketing,
                "temsilci" : item.temsilci
            }
            odeme = self.__pesinatOdemeKontrol(item.MusteriID)
            if item.Pesinat > odeme:
                self.bekleyen_listesi.append(data)

    def __pesinatOdemeKontrol(self,musteri_id):

        odeme = 0

        result = self.data.getStoreList(

            """
            Select Sum(Tutar) as Tutar from OdemelerTB o
            where o.MusteriID=?
            and o.SiparisNo in
            (
                Select s.SiparisNo from SiparislerTB s where 
                s.SiparisNo=o.SiparisNo
                and s.SiparisDurumID=1
            )
            """,(musteri_id)
        )

        for item in result:
            if item.Tutar != None:
                odeme += item.Tutar

        return float(odeme)

class SiparislerNew:
    def __init__(self,yil):
        self.data = SqlConnect().data
        self.dtSiparisler = self.data.getStoreList(
            """
            Select
            s.SiparisNo,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            m.FirmaAdi,
            s.MusteriID,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId) as temsilci,
             (select sum(Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odemeler 
            from SiparislerTB s,MusterilerTB m
            where m.ID=s.MusteriID and s.SiparisDurumID in (1,2,3)
            and Year(SiparisTarihi)=?
            and m.Mt_No=2
            and m.ID not in (6,34)
            """,(yil)
        )



        self.dtEskiSiparisler = self.data.getStoreList(
            """
            Select
            s.SiparisNo,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            m.FirmaAdi,
            s.MusteriID,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId) as temsilci,
             (select sum(Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odemeler 
            from SiparislerTB s,MusterilerTB m
            where m.ID=s.MusteriID and s.SiparisDurumID in (1,2,3)
            and Year(SiparisTarihi)<?
            and m.Mt_No=2 
            and m.ID not in (6,34)
            """,(yil)
        )

        self.dtPesinatList = self.data.getStoreList(

            """
            select
            s.MusteriID,
            m.FirmaAdi,
            Sum(o.Tutar) as Pesinat,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId) as temsilci
            from
            SiparislerTB s,MusterilerTB m,OdemelerTB o
            where
            s.SiparisDurumID in (1,2) and s.MusteriID=m.ID
            and s.SiparisNo=o.SiparisNo
            and o.MusteriID=m.ID 
            and Year(o.Tarih)=?
            and s.SiparisNo not in
            (
            Select es.SiparisNo from SiparislerTB es
            where es.SiparisNo=s.SiparisNo
            and es.SiparisDurumID in (1,2,3)
            and YEAR(es.SiparisTarihi)=?
            )
            group by s.MusteriID,m.FirmaAdi,m.Marketing,m.MusteriTemsilciId
            """,(yil,yil)
        )

        self.dtBekleyenList = self.data.getStoreList(
            """
            Select
            m.FirmaAdi,
            s.MusteriID,
			Sum(s.Pesinat) as Pesinat,
            m.Marketing,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = m.MusteriTemsilciId)  as temsilci
            from SiparislerTB s,MusterilerTB m
            where m.ID=s.MusteriID and s.SiparisDurumID in (1,2)
            and m.Mt_No=2
            and m.ID not in (6,34)
			and s.Pesinat >0
			and s.SiparisNo not in
			(
			 select es.SiparisNo from SiparislerTB es
			 where es.SiparisNo=s.SiparisNo
			 and es.SiparisDurumID in (1,2)
			 and Year(es.SiparisTarihi)=?
			)
            and s.SiparisNo in
			(
			Select o.SiparisNo from OdemelerTB o where o.SiparisNo=s.SiparisNo
			)
			group by m.FirmaAdi,s.MusteriID,m.Marketing, m.MusteriTemsilciId
            """,(yil)
        )

        self.siparis_list = list()
        self.eski_siparis_list = list()
        self.pesinat_listesi = list()
        self.bekleyen_listesi = list()

        
        
        self.urun = SiparisUrunlerNew(yil)
        self.__getSiparis_yeni()
        self.__getSiparis_eski()
        self.__pesinatList()
        self.__getSiparis_bekleyen()

        

    def __getSiparis_yeni(self):

        for item in self.dtSiparisler:
           

            data = {
                "musteriid" : item.MusteriID,
                "musteriadi" : item.FirmaAdi,
                "siparisNo" : item.SiparisNo,
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "sigorta_tutar_satis":float(0),
                 "Odemeler" : float(0),
                "urunbedel"  : float(self.__getUrunToplam(item.SiparisNo)),
                "toplam_tutar" : float(self.__getUrunToplam(item.SiparisNo)),
                "temsilci" : item.temsilci,
                "marketing" : item.Marketing
            }
           
            toplam = float(0)
            
            if item.NavlunSatis != None:
                data['navlunsatis'] = float(item.NavlunSatis)
                toplam += float(item.NavlunSatis)
                

            if item.DetayTutar_1 != None:
                data['detaytutar_1'] = float(item.DetayTutar_1)
                toplam += float(item.DetayTutar_1)
                

            if item.DetayTutar_2 != None:
                data['detaytutar_2'] = float(item.DetayTutar_2)
                toplam += float(item.DetayTutar_2)
                

            if item.DetayTutar_3 != None:
                data['detaytutar_3'] = float(item.DetayTutar_3)
                toplam += float(item.DetayTutar_3)

            if item.Odemeler != None:
                data['Odemeler'] = float(item.Odemeler)
            
            if item.sigorta_tutar_satis != None:
                data['sigorta_tutar_satis'] = float(item.sigorta_tutar_satis)
            
            data['toplam_tutar'] += toplam  
            
            self.siparis_list.append(data)

    def __getSiparis_eski(self):



        for item in self.dtEskiSiparisler:

            data = {
                "musteriid" : item.MusteriID,
                "musteriadi" : item.FirmaAdi,
                "siparisNo" : item.SiparisNo,
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "sigorta_tutar_satis":float(0),
                "Odemeler" : float(0),
                "urunbedel"  : float(self.__getUrunToplam_Eski(item.SiparisNo)),
                "temsilci" : item.temsilci,
                "marketing" : item.Marketing
                
            }

            if item.NavlunSatis != None:
                data['navlunsatis'] = float(item.NavlunSatis)

            if item.DetayTutar_1 != None:
                data['detaytutar_1'] = float(item.DetayTutar_1)

            if item.DetayTutar_2 != None:
                data['detaytutar_2'] = float(item.DetayTutar_2)

            if item.DetayTutar_3 != None:
                data['detaytutar_3'] = float(item.DetayTutar_3)

            if item.Odemeler != None:
                data['Odemeler'] = float(item.Odemeler)    

            if item.sigorta_tutar_satis != None:
                data['sigorta_tutar_satis'] = float(item.sigorta_tutar_satis)
           
            
            self.eski_siparis_list.append(data)

    def __pesinatList(self):

        for item in self.dtPesinatList:

            data = {

                'musteriadi' : item.FirmaAdi,
                'musteriid' :  item.MusteriID,
                'pesinat' : float(item.Pesinat),
                "siparisNo" :"",
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "sigorta_tutar_satis":float(0),
                "Odemeler" : float(0),
                "urunbedel"  : float(0),
                "toplam_tutar" : float(0),
                "marketing" : item.Marketing,
                "temsilci" : item.temsilci
            }
          
            self.pesinat_listesi.append(data)


    def __getUrunToplam(self,siparisNo):

        urun_bedel = 0

        urunlist = list(filter(lambda x:x['siparisNo'] == siparisNo,self.urun.urunlist))
       
        for item in urunlist:
            
               
            urun_bedel += item['satisToplam']
        
        return urun_bedel

    def __getUrunToplam_Eski(self,siparisNo):

        urun_bedel = 0

        urunlist = list(filter(lambda x:x['siparisNo'] == siparisNo,self.urun.eski_urunlist))
       
        for item in urunlist:
            
               
            urun_bedel += item['satisToplam']

        
        return urun_bedel

    def __getSiparis_bekleyen(self):

        for item in self.dtBekleyenList:

            data = {
                "musteriid" : item.MusteriID,
                "musteriadi" : item.FirmaAdi,
                "pesinat"      : float(item.Pesinat),
                "siparisNo" : "",
                "navlunsatis" : float(0),
                "detaytutar_1" : float(0),
                "detaytutar_2" : float(0),
                "detaytutar_3" : float(0),
                "Odemeler" : float(0),
                "urunbedel"  : float(0),
                "toplam_tutar" : float(0),
                "marketing" : item.Marketing,
                "temsilci" : item.temsilci
            }
            odeme = self.__pesinatOdemeKontrol(item.MusteriID)
            if item.Pesinat > odeme:
                self.bekleyen_listesi.append(data)

    def __pesinatOdemeKontrol(self,musteri_id):

        odeme = 0

        result = self.data.getStoreList(

            """
            Select Sum(Tutar) as Tutar from OdemelerTB o
            where o.MusteriID=?
            and o.SiparisNo in
            (
                Select s.SiparisNo from SiparislerTB s where 
                s.SiparisNo=o.SiparisNo
                and s.SiparisDurumID=1
            )
            """,(musteri_id)
        )

        for item in result:
            if item.Tutar != None:
                odeme += item.Tutar

        return float(odeme)

        
