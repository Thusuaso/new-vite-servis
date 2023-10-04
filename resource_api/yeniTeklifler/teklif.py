from models import TakvimSchema,TakvimModel,TeklifUlkeSchema,TeklifUlkeModel
from models.yeniTeklifler import *
from helpers import SqlConnect,TarihIslemler
from flask_restful import Resource
from flask import jsonify 
import datetime
from models.shared import StyleSchema,StyleSchema
from resource_api.yeniTeklifler.raporlar.teklif_takip.teklifListe import TeklifListe


class TeklifAnaSayfaData(Resource):

    def get(self,userId):

        teklif = Teklif(userId)
        data = {
            'takvimList' : teklif.getTakvimList(),
            'temsilciOzetList' : teklif.getTemsilciListOzet(),
            'hatirlatmaList' : teklif.getHatirlatmaList(),
            'musteriOzetList' : teklif.getMusteriOzetList(),
            'ulkelerToplamTeklif':teklif.getTeklifUlkeler()
        }

        return jsonify(data)

class TeklifAyrintiListe(Resource):

    def get(self,kullaniciId):

        teklifList = TeklifListeler() 
        teklif = TeklifListe()

        alist = teklifList.getKullaniciListeAyrinti(kullaniciId)

        blist = teklifList.getKullaniciListeAyrinti_BList(kullaniciId)
        
        labels,datasets = teklif.getGrafikRaporHepsi()
        
        datasets_oncelik,labels_oncelik = teklif.getOncelikGrafikRapor()
        
        aListChart = {
            'labels' : labels,
            'datasets' : datasets, 
        }
        bListChart =  {
            'datasets' : datasets_oncelik,
            'labels' : labels_oncelik
        }
            
        data = {

            "alist" : alist,
            "blist" : blist,
            "aListChart":aListChart,
            "bListChart":bListChart,
            
        }

        return jsonify(data)



class TeklifAyrintiListeHepsi(Resource):

    def get(self):

        teklifList = TeklifListeler()

        teklif = TeklifListe()

        labels,datasets = teklif.getGrafikRaporHepsi()
        datasets_oncelik,labels_oncelik = teklif.getOncelikGrafikRapor()
        blist = teklifList.getKullaniciListeHepsi_BList()
        alist = teklifList.getKullaniciListeHepsi()
        
        

        aListChart = {
            'labels' : labels,
            'datasets' : datasets, 
        }
        bListChart =  {
            'datasets' : datasets_oncelik,
            'labels' : labels_oncelik
        }
            
        data = {

            "alist" : alist,
            "blist" : blist,
            "aListChart":aListChart,
            "bListChart":bListChart,
            
        }

        return jsonify(data)


class Teklif:

    def __init__(self,userId):
        self.data = SqlConnect().data
        self.tarihIslem = TarihIslemler()
        self.kullaniciId = userId

    
    def getTakvimList(self):

        liste = list()
        if self.__getTakvimDataList() != None:
            
            takvim_list = self.__getTakvimDataList()
        
        """
        
        for item in self.__getTakvimDataSatisciList():

            takvim_list.append(item)
        """
        #hatırlatma tarih kontrolu geride kalan tarihlerin güncellenmesi
        

        for item in takvim_list:

            model = TakvimModel()
            model.id = item.TeklifId 
            model.title = item.MusteriAdi
           # model.goruldu = item.Goruldu
            #model.url = 'http://localhost:8080/#/siparisler/uretim'
            if item.KullaniciAdi == 'Fadime':
                model.color = 'orange'
            if item.KullaniciAdi == 'Gizem':
                model.color = 'yellow'
            if item.KullaniciAdi == 'Ozlem':
                model.color = '#CF4FD5'
            if item.KullaniciAdi == 'Ozgul':
                model.color = '#F39C27'
            if item.KullaniciAdi == 'Fatmanur':
                model.color = 'green'    
            if item.KullaniciAdi == 'Fatih':
                model.color = 'blue' 
            if item.KullaniciAdi == 'Sema':
                model.color = '#641537'
            if item.KullaniciAdi == 'Hakan':
                model.color = '#a2c4c9' 
            
            
            if item.HatirlatmaTarihi != None:
                model.start = self.tarihIslem.getDate(item.HatirlatmaTarihi).strftime("%Y-%m-%d")
                model.end = self.tarihIslem.getDate(item.HatirlatmaSonTarih).strftime("%Y-%m-%d")
                model.hatirlatmaAciklama = item.HatirlatmaAciklama
                model.hatirlatmaDurum = item.HatirlatilmaDurumu
                
                
                
            liste.append(model)

        
        schema = TakvimSchema(many=True)

        return schema.dump(liste)

    def getTemsilciListOzet(self):

        result = self.data.getList(
            #10 Gizem
            #16 Fadime
            #19 Özlem
            """
          	select * from KullaniciTB where Teklif=1
            """
        )

        liste = list()
        id = 1
        for item in result:

            model = TemsilciOzetModel()
            model.id = id
            model.adi = item.KullaniciAdi
            model.temsilci_id = item.ID
            model.teklifSayisi = int(self.__getTakipTeklifSayisi(item.ID))
            model.proformaSayisi = int(self.__getTeklifProformaSayisi(item.ID))
            liste.append(model)
            id += 1

        schema = TemsilciOzetSchema(many=True)

        return schema.dump(liste)

    def getMusteriOzetList(self):
        liste = list()

        result = self.data.getStoreList(
            """
            select
            
            m.MusteriAdi,
            k.KullaniciAdi,
            u.UlkeAdi,
            count(*) as TeklifSayisi
            from
            YeniTeklifTB yt, YeniTeklif_MusterilerTB m,YeniTeklif_UlkeTB u,KullaniciTB k
            where
            yt.MusteriId=m.Id and m.UlkeId=u.Id and yt.TakipEt=1
            and yt.KullaniciId=? and k.ID=yt.KullaniciId
            group by m.MusteriAdi,u.UlkeAdi,k.KullaniciAdi
            order by count(*) desc
            """,(self.kullaniciId)
        )

        for item in result:
            model = MusteriOzetModel()
            
            model.musteriAdi = item.MusteriAdi
            model.kullaniciAdi = item.KullaniciAdi 
            model.ulkeAdi = item.UlkeAdi 
            model.teklifSayisi = item.TeklifSayisi 

            liste.append(model)

        schema = MusteriOzetSchema(many=True)

        return schema.dump(liste)

    def getHatirlatmaList(self):
        
        liste = list()

        result = self.data.getStoreList(
            """
            select
            yt.Id as TeklifId,
            yt.HatirlatmaTarihi,
            m.MusteriAdi,
            u.UlkeAdi
            from
            YeniTeklifTB yt,YeniTeklif_UlkeTB u,YeniTeklif_MusterilerTB m
            where
            yt.MusteriId=m.Id and m.UlkeId=u.Id and yt.TakipEt=1
            and yt.HatirlatmaTarihi is not null 
            and yt.KullaniciId=?
			and YEAR(yt.HatirlatmaTarihi) = YEAR(GETDATE())
			and MONTH(yt.HatirlatmaTarihi) > MONTH(GETDATE())
            """,(self.kullaniciId)
        )

        for item in result:
            model = HatirlatmaModel()
            model.id = item.TeklifId
            model.tarih = self.tarihIslem.getDate(item.HatirlatmaTarihi).strftime("%d-%m-%Y")
            model.musteriAdi = item.MusteriAdi 
            model.ulkeAdi = item.UlkeAdi 

            liste.append(model)

        schema = HatirlatmaSchema(many=True)

        return schema.dump(liste)

    def getTeklifUlkeler(self):
        try:
            result = self.data.getList("""
                                            select 
                                                count(yu.Id) UlkeTop,
                                                yu.Id as UlkeId,
                                                yu.UlkeAdi
                                            from YeniTeklifTB yt

                                            inner join YeniTeklif_MusterilerTB ym on ym.Id = yt.MusteriId
                                            inner join YeniTeklif_UlkeTB yu on yu.Id = ym.UlkeId

                                            where 
                                                YEAR(yt.Tarih) = 2023

                                            group by
                                                yu.Id,yu.UlkeAdi
                                       
                                       """)
            liste = list()
            for item in result:
                model = TeklifUlkeModel()
                model.id = item.UlkeId
                model.country = item.UlkeAdi
                model.countryTop = item.UlkeTop
                liste.append(model)
            schema = TeklifUlkeSchema(many=True)
            return schema.dump(liste)
            
        
        except Exception as e:
            print('e',str(e))
            return False

    def __getTakipTeklifSayisi(self,kullaniciId):

        item = self.data.getStoreList(
            """
            Select count(*) as durum from YeniTeklifTB where 
            KullaniciId=? and TakipEt=1
            """,(kullaniciId)
        )[0]

        return item.durum

    def __getTeklifProformaSayisi(self,kullaniciId):

        item = self.data.getStoreList(
            """
             Select count(*) as durum from YeniTeklifTB where
             KullaniciId=? and TakipEt=1 and Proforma_Cloud=1
            """,(kullaniciId)
        )[0]

        return item.durum

    def __getTakvimDataList(self):
        result = self.data.getStoreList(
            """
            select
            yt.Id as TeklifId,
            yt.HatirlatmaTarihi,
            m.MusteriAdi,
            u.UlkeAdi,
            k.KullaniciAdi,
            yt.HatirlatmaSonTarih,
            yt.Goruldu,
			yt.HatirlatmaAciklama,
			yt.HatirlatilmaDurumu
            from
            YeniTeklifTB yt,YeniTeklif_UlkeTB u,
            YeniTeklif_MusterilerTB m,KullaniciTB k
            where
            yt.MusteriId=m.Id and m.UlkeId=u.Id and yt.TakipEt=1
            and yt.HatirlatmaTarihi is not null  
            and k.ID=yt.KullaniciId and yt.KullaniciId=? and YEAR(yt.HatirlatmaTarihi) = YEAR(GETDATE()) and MONTH(yt.HatirlatmaTarihi) > MONTH(GETDATE())
            """,(self.kullaniciId)
        )

        return result

    def __getTakvimDataSatisciList(self):
        result = self.data.getStoreList(
            """
          select 0 as TeklifId,
            Hatirlatma_Tarih as HatirlatmaTarihi,
            Hatirlatma_Notu,
            MusteriAdi,
            (select k.KullaniciAdi from KullaniciTB k where k.ID=Temsilci) as KullaniciAdi
            from SatisciAyrintiTB where Temsilci=?
            """,(self.kullaniciId)
        )

        return result
    
    def __hatirlatmaTarihKontrol(self,hatirlatmaTarihi,id):

        _tarih = str(hatirlatmaTarihi).split('-')

        yil = int(_tarih[0])
        ay = int(_tarih[1])
        gun = int(_tarih[2])

        tarih = datetime.datetime(yil,ay,gun)

        bugun = datetime.datetime.today()

        kontrol = bugun - tarih
    
        if kontrol.days > 0:
            self.data.update_insert(
                """
                update YeniTeklifTB set HatirlatmaTarihi=DateAdd(day,1,HatirlatmaTarihi),
                HatirlatmaSonTarih=DateAdd(day,1,HatirlatmaSonTarih)
                where Id=?
                """,(id)
            )
            print('Güncelleme Yapıldı')

   


class TeklifListeler:

    def __init__(self):
        self.data = SqlConnect().data
        self.tarihIslem = TarihIslemler()

    def getKullaniciListeAyrinti(self,kullaniciId):
        liste = list()

        result = self.data.getStoreList(
                """
                    select
                    t.Tarih,
                    t.Id,
                    m.MusteriAdi,
                    u.UlkeAdi,
                    t.TeklifOncelik,
                    k.KullaniciAdi,
                    t.Goruldu,
                    t.Sira
                    from
                    YeniTeklifTB t,YeniTeklif_MusterilerTB m,
                    YeniTeklif_UlkeTB u,KullaniciTB k
                    where
                    t.MusteriId=m.Id and u.Id=m.UlkeId
                    and k.ID=t.KullaniciId and t.TakipEt=1
                    and k.ID=? and t.BList=0  order by t.TeklifOncelik , t.Tarih,t.Sira asc
                """,(kullaniciId)
                )
        
        for item in result:
            model = KullaniciListeAyrintiModel()
            model.id = item.Id
            model.musteriAdi = item.MusteriAdi 
            model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%Y-%m-%d")
            model.ulkeAdi = item.UlkeAdi
            model.teklifOncelik = item.TeklifOncelik
            model.goruldu = item.Goruldu 
            model.sira = item.Sira
            kullaniciAdi = ""
            if item.KullaniciAdi == 'Gizem':
                kullaniciAdi = "GU"
            if item.KullaniciAdi == 'Ozlem':
                kullaniciAdi = "OO"
            if item.KullaniciAdi == 'Hakan':
                kullaniciAdi = "HK"        

            model.temsilciAdi = kullaniciAdi

            liste.append(model)

        schema = KullaniciListeAyrintiSchema(many=True)

        return schema.dump(liste)

    def getKullaniciListeAyrinti_BList(self,kullaniciId):
        liste = list()

      
        result = self.data.getStoreList(
                """
                select
                t.Tarih,
                t.Id,
                m.MusteriAdi,
                u.UlkeAdi,
                t.TeklifOncelik,
                k.KullaniciAdi,
                t.Goruldu,
                t.Sira
                from
                YeniTeklifTB t,YeniTeklif_MusterilerTB m,
                YeniTeklif_UlkeTB u,KullaniciTB k
                where
                t.MusteriId=m.Id and u.Id=m.UlkeId
                and k.ID=t.KullaniciId and t.TakipEt=1
                and k.ID=? and t.BList=1 order by t.TeklifOncelik , t.Tarih,t.Sira asc
                """,(kullaniciId)
            )

        
        for item in result:
            model = KullaniciListeAyrintiModel()
            model.id = item.Id
            model.musteriAdi = item.MusteriAdi 
            model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%Y-%m-%d")
            model.ulkeAdi = item.UlkeAdi
            model.teklifOncelik = item.TeklifOncelik
            model.goruldu = item.Goruldu 
            model.sira = item.Sira
            kullaniciAdi = ""
            if item.KullaniciAdi == "Gizem":
                kullaniciAdi = "GU"

            if item.KullaniciAdi == "Ozlem":
                kullaniciAdi = "OO"

            if item.KullaniciAdi == "Hakan":
                kullaniciAdi = "HK"  
            model.temsilciAdi = kullaniciAdi

            liste.append(model)

        schema = KullaniciListeAyrintiSchema(many=True)

        return schema.dump(liste)



    def getKullaniciListeHepsi(self):
        liste = list()

        result = self.data.getList(
            """
          select
            t.Tarih,
            t.Id,
            m.MusteriAdi,
            u.UlkeAdi,
            t.TeklifOncelik,
            k.KullaniciAdi,
            t.Goruldu,
            t.Sira
            from
            YeniTeklifTB t,YeniTeklif_MusterilerTB m,
            YeniTeklif_UlkeTB u,KullaniciTB k
            where
            t.MusteriId=m.Id and u.Id=m.UlkeId
            and k.ID=t.KullaniciId and t.TakipEt=1
            and t.BList=0  order by t.TeklifOncelik , t.Tarih,t.Sira asc
            """
        )

        
        for item in result:
            model = KullaniciListeAyrintiModel()
            model.id = item.Id
            model.musteriAdi = item.MusteriAdi 
            model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%Y-%m-%d")
            model.ulkeAdi = item.UlkeAdi
            model.teklifOncelik = item.TeklifOncelik
            kullaniciAdi = ""
            model.sira = item.Sira
            model.goruldu = item.Goruldu
            if item.KullaniciAdi == "Gizem":
                kullaniciAdi = "GU"
            if item.KullaniciAdi == "Fadime":
                kullaniciAdi = "FY"
            if item.KullaniciAdi == "Ozlem":
                kullaniciAdi = "OO"
            if item.KullaniciAdi == "Fatih":
                kullaniciAdi = "FS"
            if item.KullaniciAdi == "Ozgul":
                kullaniciAdi = "OA"
            if item.KullaniciAdi == "Fatmanur":
                kullaniciAdi = "FNY"
            if item.KullaniciAdi == "Sema":
                kullaniciAdi = "Sİ"        
            if item.KullaniciAdi == "Hakan":
                kullaniciAdi = "HK" 
            model.temsilciAdi = kullaniciAdi

            liste.append(model)

        schema = KullaniciListeAyrintiSchema(many=True)

        return schema.dump(liste)

    
    def getKullaniciListeHepsi_BList(self):
        liste = list()

        result = self.data.getList(
            """
            select
            t.Tarih,
            t.Id,
            m.MusteriAdi,
            u.UlkeAdi,
            t.TeklifOncelik,
            k.KullaniciAdi,
            t.Goruldu,
            t.Sira
            from
            YeniTeklifTB t,YeniTeklif_MusterilerTB m,
            YeniTeklif_UlkeTB u,KullaniciTB k
            where
            t.MusteriId=m.Id and u.Id=m.UlkeId
            and k.ID=t.KullaniciId and t.TakipEt=1
            and t.BList=1 order by t.TeklifOncelik , t.Tarih,t.Sira asc
            """
        )

        
        for item in result:
            model = KullaniciListeAyrintiModel()
            model.id = item.Id
            model.musteriAdi = item.MusteriAdi 
            model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%Y-%m-%d")
            model.ulkeAdi = item.UlkeAdi
            model.teklifOncelik = item.TeklifOncelik
            kullaniciAdi = ""
            model.sira = item.Sira
            model.goruldu = item.Goruldu
            if item.KullaniciAdi == "Gizem":
                kullaniciAdi = "GU"
            if item.KullaniciAdi == "Fadime":
                kullaniciAdi = "FY"
            if item.KullaniciAdi == "Ozlem":
                kullaniciAdi = "OO"
            if item.KullaniciAdi == "Fatih":
                kullaniciAdi = "FS"
            if item.KullaniciAdi == "Ozgul":
                kullaniciAdi = "OA"
            if item.KullaniciAdi == "Fatmanur":
                kullaniciAdi = "FNY" 
            if item.KullaniciAdi == "Sema":
                kullaniciAdi = "Sİ"       
            if item.KullaniciAdi == "Hakan":
                kullaniciAdi = "HK"
            model.temsilciAdi = kullaniciAdi

            liste.append(model)

        schema = KullaniciListeAyrintiSchema(many=True)

        return schema.dump(liste)
