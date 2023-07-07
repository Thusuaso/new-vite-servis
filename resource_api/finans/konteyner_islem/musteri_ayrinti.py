from helpers import SqlConnect,TarihIslemler
from models.finans import *
from models.finans import MusteriOdemeSchema,MusteriOdemeModel
from models.finans import MusteriOdemeSecimSchema,MusteriOdemeSecimModel
import datetime
class MusteriAyrinti:

    def __init__(self,musteriid):

        self.data = SqlConnect().data
        self.musteri_id = musteriid

    def getKonteynerAyrintiList(self): #2 ayrı tabloyu birleştirme

        yukleme_list = self.__uretilenler()
        
        for item in self.__yuklenenler():

            yukleme_list.append(item)

        schema = MusteriAyrintiSchema(many=True)

        return schema.dump(yukleme_list)
    
    def __yuklenenler(self):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select
            s.ID,
            s.SiparisNo,
            s.YuklemeTarihi,
            s.Vade,
            s.TahminiEtaTarihi,
            m.FirmaAdi,
            s.MusteriID,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            s.Pesinat,
            (
            select Sum(Tutar) from OdemelerTB o where o.SiparisNo=s.SiparisNo
            and s.MusteriID=m.ID
            ) as Odeme,
            (
              select Sum(SatisToplam) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo
            ) as UrunBedeli        
            from
            SiparislerTB s,MusterilerTB m
            where
            s.MusteriID=m.ID
            and m.ID=?
            and s.SiparisDurumID=3
            order by s.YuklemeTarihi desc
            """,(self.musteri_id)
        )

        liste = list()

        for item in result:
            
            model = MusteriAyrintiModel()
            model.id = item.ID 
            model.musteriadi = item.FirmaAdi
            model.musteri_id = item.MusteriID
            model.siparisno = item.SiparisNo 
            model.tip = "Yükleme"           
            if item.YuklemeTarihi != None:
                model.yuklemetarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")               
            if item.Vade != None:
                model.vade = tarihIslem.getDate(item.Vade).strftime("%d-%m-%Y")
            
            if item.TahminiEtaTarihi != None:
                model.tahmini_eta = tarihIslem.getDate(item.TahminiEtaTarihi).strftime("%d-%m-%Y")  
            model.pesinat = item.Pesinat
            navlun = 0 
            tutar_1 = 0
            tutar_2 = 0
            tutar_3 = 0
            
            urun_bedel = 0
            odeme = 0
            sigorta  = 0
            if item.NavlunSatis != None:
                navlun = item.NavlunSatis
            if item.DetayTutar_1 != None:
                tutar_1 = item.DetayTutar_1
            if item.DetayTutar_2 != None:
                tutar_2 = item.DetayTutar_2
            if item.DetayTutar_3 != None:
                tutar_3 = item.DetayTutar_3
              
            if item.UrunBedeli != None:
                urun_bedel = item.UrunBedeli
            if item.Odeme != None:
                odeme = item.Odeme
            if item.sigorta_tutar_satis != None:
                sigorta = item.sigorta_tutar_satis
            model.toplam = navlun + tutar_1 + tutar_2 + tutar_3  + urun_bedel + sigorta
            model.siparis_total = model.toplam
            
            model.kalan = model.toplam - odeme
            model.kalan2 = model.toplam - odeme
            model.odenen_tutar = odeme
            liste.append(model)

        return liste  

    def __uretilenler(self):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select
            s.ID,
            s.SiparisNo,
            s.YuklemeTarihi,
            s.Vade,
            s.TahminiEtaTarihi,
            m.FirmaAdi,
            s.MusteriID,
            s.Pesinat,
            s.NavlunSatis,
            s.DetayTutar_1,
            s.DetayTutar_2,
            s.DetayTutar_3,
            s.sigorta_tutar_satis,
            
            (
            select Sum(Tutar) from OdemelerTB o where o.SiparisNo=s.SiparisNo
            and s.MusteriID=m.ID
            ) as Odeme,
            (
            select Sum(SatisToplam) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo
            ) as UrunBedeli
            from
            SiparislerTB s,MusterilerTB m
            where
            s.MusteriID=m.ID
            and m.ID=?
            and s.Pesinat > 0
           
            and s.SiparisDurumID in (1,2)
            """,(self.musteri_id)
        )

        liste = list()

        for item in result:
            
            model = MusteriAyrintiModel()
            model.id = item.ID 
            model.musteriadi = item.FirmaAdi
            model.musteri_id = item.MusteriID
            model.siparisno = item.SiparisNo 
            model.tip = "Üretim"
            if item.YuklemeTarihi != None:
                model.yuklemetarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")
            if item.Vade != None:
                model.vade = tarihIslem.getDate(item.Vade).strftime("%d-%m-%Y")
            if item.TahminiEtaTarihi != None:
                model.tahmini_eta = tarihIslem.getDate(item.TahminiEtaTarihi).strftime("%d-%m-%Y")
           
            pesinat = 0
            navlun = 0 
            tutar_1 = 0
            tutar_2 = 0
            tutar_3 = 0
            sigorta = 0 
            urun_bedel = 0
            odeme = 0
            
            if item.NavlunSatis != None:
                navlun = item.NavlunSatis
            if item.DetayTutar_1 != None:
                tutar_1 = item.DetayTutar_1
            if item.DetayTutar_2 != None:
                tutar_2 = item.DetayTutar_2
            if item.DetayTutar_3 != None:
                tutar_3 = item.DetayTutar_3
            
            if item.UrunBedeli != None:
                urun_bedel = item.UrunBedeli
            if item.Pesinat != None:
                pesinat = item.Pesinat
            if item.sigorta_tutar_satis != None:
                sigorta = item.sigorta_tutar_satis
            if item.Odeme != None:
                odeme = item.Odeme
            model.pesinat = pesinat
            model.siparis_total = navlun + tutar_1 + tutar_2 + tutar_3 + urun_bedel + sigorta
            model.toplam = item.Pesinat
            model.kalan2 = model.siparis_total - item.Pesinat
            model.kalan =  -odeme
            model.odenen_tutar = odeme
            liste.append(model)

        return liste      

    def getOdemeListesi(self):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select
            o.Tarih,
            sum(o.Tutar) as Tutar
            from
            OdemelerTB o
            where o.MusteriID=?
            and o.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s
            where s.SiparisNo=o.SiparisNo
            and s.MusteriID=?
            )
            group by o.Tarih
            order by o.Tarih desc
                        """,(self.musteri_id,self.musteri_id)
        )

        liste = list()

        key = 1

        for item in result:

            model = MusteriOdemeModel()
            model.id = key
            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")

            model.tutar = item.Tutar          
            liste.append(model)

            key += 1

        schema = MusteriOdemeSchema(many=True)

        return schema.dump(liste)

    def getOdemeSecimPoList(self,tarih):
        
        tarih = tarih
        forMat = '%d-%m-%Y'
        tarih = datetime.datetime.strptime(tarih, forMat)
        tarih = tarih.date()
        result = self.data.getStoreList(
            """
            select
            o.ID,
            o.SiparisNo,
            o.Tutar,
            o.Aciklama,
            o.Masraf,
            o.Kur,
		    (select t.OdemeTur from OdemeTurTB t where t.ID=o.FinansOdemeTurID) as tur
            from
            OdemelerTB o
            where o.MusteriID=?
            and o.Tarih=?
            and o.SiparisNo in
            (
            Select s.SiparisNo from SiparislerTB s
            where s.SiparisNo=o.SiparisNo
            and s.MusteriID=o.MusteriID
            )
            """,(self.musteri_id,tarih)
        )

        liste = list()
        key = 0
        for item in result:

            model = MusteriOdemeSecimModel()
            model.id = item.ID
            model.siparisno = item.SiparisNo
            model.tutar = item.Tutar
            model.aciklama = item.Aciklama
            model.masraf = item.Masraf
            model.faturatur = item.tur
            model.kur = item.Kur
            key +=1
            model.sira = key 
            
          
            liste.append(model)

        schema = MusteriOdemeSecimSchema(many=True)

        return schema.dump(liste)

    def getByCustomersPo(self):
        try:
            result = self.data.getStoreList("""
                                   
                                    select ID,SiparisNo from SiparislerTB where MusteriID = ?
                                   """,(self.musteri_id))
            liste = list()
            for item in result:
                model = ByCustomersPoModel()
                model.id = item.ID
                model.siparisNo = item.SiparisNo
                liste.append(model)
            schema = ByCustomersPoSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print("getByCustomersPo hata",str(e))
            return False