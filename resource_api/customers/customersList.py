from helpers import SqlConnect
from models.satisci import *
from openpyxl import *
import shutil

class MusteriListem:

    def __init__(self):

        self.data = SqlConnect().data

     
    def getMusteriListesi(self,users): #2 ayrı tabloyu birleştirme

        yukleme_list = self.__musteriListesi(users)
        
        for item in self.__musteriTeklifListesi(users):

            yukleme_list.append(item)

        schema = MusteriListeSchema(many=True)
       
        return schema.dump(yukleme_list)


    def getMusteriListesiSatisci(self,users):
        return self.__musteriListesi(users)
    
    def getMusteriListesiTeklifler(self,users):
        return self.__musteriTeklifListesi(users)

    def getMusteriListesiBGN(self,users):
        return self.__musteriTeklifListesiBGN(users)

    def getMusteriListesiAll(self):
        yukleme_list = self.__musteriListesiAll()
        
        for item in self.__musteriTeklifListesiAll():

            yukleme_list.append(item)

        schema = MusteriListeSchema(many=True)
       
        return schema.dump(yukleme_list)
    
    def getMusteriListesiAllSatisci(self):
        return self.__musteriListesiAll()
    
    def getMusteriListesiAllTeklifler(self):
        return self.__musteriTeklifListesiAll()
    
    def getMusteriListesiAllTekliflerBGN(self):
        return self.__musteriTeklifListesiBGNAll()
    
    
    def __musteriListesi(self,users):

        result = self.data.getStoreList(
            """
            select
            m.ID,
            m.FirmaAdi,
            m.MusteriOncelik,
           (select top 1  s.Baslik from SatisciAyrintiTB s where s.MusteriAdi = m.FirmaAdi  order by s.Tarih desc ) as baslik,
            k.KullaniciAdi as Temsilci,
			m.Takip as Takip,
            (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId) as UlkeAdi,
            u.Png_Flags as Flag,
            m.MailAdresi as Mail
           
            from
            MusterilerTB m,YeniTeklif_UlkeTB u,KullaniciTB k
            where u.Id=m.UlkeId and k.ID=m.MusteriTemsilciId  and   m.Marketing ='Mekmar' and ( m.MusteriOncelik  = 'A' or m.MusteriOncelik = 'B' or m.MusteriOncelik = 'C') and m.Takip = 1 and m.MusteriTemsilciId=?
			order by m.MusteriOncelik
			
           

            """,(users)
        )

        liste = list()

        for item in result:

            model = MusteriListeModel()
            model.id = item.ID
            model.musteriadi = item.FirmaAdi
            model.oncelik = item.MusteriOncelik
            if item.MusteriOncelik == 'A':
                model.newOncelik = "1"
            elif item.MusteriOncelik == 'B':
                model.newOncelik = "2"
            elif item.MusteriOncelik == 'C':
                model.newOncelik = "3"
            model.oncelikBackground = '#63b0f5'
            model.temsilci = item.Temsilci
            if item.baslik == None:
                item.baslik = ""
            model.aciklama =  item.baslik
            model.flag = item.Flag
            model.ulkeAdi = item.UlkeAdi
            model.mail = item.Mail
            model.satisciDurum = 'Musteri'
            model.takipEt = item.Takip
            liste.append(model)

        schema = MusteriListeSchema(many=True)

        return schema.dump(liste)

    def __musteriTeklifListesi(self,users):

        result = self.data.getStoreList(
            """
           select
            m.MusteriAdi,
            t.TeklifOncelik,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = t.KullaniciId) as temsilci,
			(select top 1  s.Baslik from SatisciAyrintiTB s where s.MusteriAdi = m.MusteriAdi   order by s.Tarih desc) as baslik,
            (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId) as UlkeAdi,
            u.Png_Flags as Flag,
            (select mt.MailAdresi from MusterilerTB mt where mt.FirmaAdi = m.MusteriAdi) as Mail,
            t.KaynakYeri as Kaynak,
            t.Id as ID,
			t.TakipEt
            from YeniTeklifTB t , YeniTeklif_MusterilerTB m,YeniTeklif_UlkeTB u
            where m.Id = t.MusteriId and ( t.TeklifOncelik='A' or  t.TeklifOncelik='B' or t.TeklifOncelik='C') and t.TakipEt=1 and u.Id = m.UlkeId and t.KullaniciId=?
            GROUP BY  m.MusteriAdi,t.TeklifOncelik, t.KullaniciId,m.UlkeId,u.Png_Flags,t.KaynakYeri,t.Id,t.TakipEt
			order by t.TeklifOncelik


            """,(users)
        )

        liste = list()

        for item in result:

            model = MusteriListeModel()
            model.id = 1
            model.musteriadi = item.MusteriAdi
            model.oncelik = item.TeklifOncelik
            model.newOncelik = item.TeklifOncelik
            if item.Kaynak == 'BGP Network':
                
                model.oncelikBackground = '#93c47d'
            else:
                model.oncelikBackground = '#c592ad'
            model.temsilci = item.temsilci
            if item.baslik == None:
                item.baslik = ""
            model.aciklama = item.baslik
            model.ulkeAdi = item.UlkeAdi
            model.flag = item.Flag
            model.mail = item.Mail
            model.satisciDurum = 'Teklif'
            model.teklifSira = item.ID
            model.takipEt = item.TakipEt
            liste.append(model)

        schema = MusteriListeSchema(many=True)

        return schema.dump(liste)
    
    
    def __musteriTeklifListesiBGN(self,users):

        result = self.data.getStoreList(
            """
           select
            m.MusteriAdi,
            t.TeklifOncelik,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = t.KullaniciId) as temsilci,
			(select top 1  s.Baslik from SatisciAyrintiTB s where s.MusteriAdi = m.MusteriAdi   order by s.Tarih desc) as baslik,
            (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId) as UlkeAdi,
            u.Png_Flags as Flag,
            (select mt.MailAdresi from MusterilerTB mt where mt.FirmaAdi = m.MusteriAdi) as Mail,
            t.KaynakYeri as Kaynak,
            t.Id as ID
            from YeniTeklifTB t , YeniTeklif_MusterilerTB m,YeniTeklif_UlkeTB u
            where m.Id = t.MusteriId and ( t.TeklifOncelik='A' or  t.TeklifOncelik='B' or t.TeklifOncelik='C') and t.TakipEt=1 and u.Id = m.UlkeId and t.KaynakYeri='BGP Network' and  t.KullaniciId=?
            GROUP BY  m.MusteriAdi,t.TeklifOncelik, t.KullaniciId,m.UlkeId,u.Png_Flags,t.KaynakYeri,t.Id
			order by t.TeklifOncelik


            """,(users)
        )

        liste = list()

        for item in result:

            model = MusteriListeModel()
            model.id = 1
            model.musteriadi = item.MusteriAdi
            model.oncelik = item.TeklifOncelik
            model.newOncelik = item.TeklifOncelik
            if item.Kaynak == 'BGP Network':
                
                model.oncelikBackground = '#93c47d'
            else:
                model.oncelikBackground = '#c592ad'
            model.temsilci = item.temsilci
            if item.baslik == None:
                item.baslik = ""
            model.aciklama = item.baslik
            model.ulkeAdi = item.UlkeAdi
            model.flag = item.Flag
            model.mail = item.Mail
            model.satisciDurum = 'Teklif'
            model.teklifSira = item.ID
            liste.append(model)

        schema = MusteriListeSchema(many=True)

        return schema.dump(liste)
    
    
    
    
    
    def __musteriListesiAll(self):

        result = self.data.getList(
            """
            select
            m.ID,
            m.FirmaAdi,
            m.MusteriOncelik,
           (select top 1  s.Baslik from SatisciAyrintiTB s where s.MusteriAdi = m.FirmaAdi  order by s.Tarih desc ) as baslik,
            k.KullaniciAdi as Temsilci,
			m.Takip as Takip,
            (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId) as UlkeAdi,
            u.Png_Flags as Flag,
            m.MailAdresi as Mail
           
            from
            MusterilerTB m,YeniTeklif_UlkeTB u,KullaniciTB k
            where u.Id=m.UlkeId and k.ID=m.MusteriTemsilciId  and   m.Marketing ='Mekmar' and ( m.MusteriOncelik  = 'A' or m.MusteriOncelik = 'B' or m.MusteriOncelik = 'C') and m.Takip = 1
			order by m.MusteriOncelik
			
           

            """
        )

        liste = list()

        for item in result:

            model = MusteriListeModel()
            model.id = item.ID
            model.musteriadi = item.FirmaAdi
            model.oncelik = item.MusteriOncelik
            if item.MusteriOncelik == 'A':
                model.newOncelik = "1"
                model.oncelikBackground = '#ec1802'
            elif item.MusteriOncelik == 'B':
                model.newOncelik = "2"
                model.oncelikBackground = '#0073e5'
                
            elif item.MusteriOncelik == 'C':
                model.newOncelik = "3"
                model.oncelikBackground = '#e9f204'
                
            model.oncelikBackground = '#63b0f5'
            model.temsilci = item.Temsilci
            if item.baslik == None:
                item.baslik = ""
            model.aciklama =  item.baslik
            model.flag = item.Flag
            model.ulkeAdi = item.UlkeAdi
            model.mail = item.Mail
            model.satisciDurum = 'Musteri'
            liste.append(model)

        schema = MusteriListeSchema(many=True)

        return schema.dump(liste)

    def __musteriTeklifListesiAll(self):

        result = self.data.getList(
            """
            select
            m.MusteriAdi,
            t.TeklifOncelik,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = t.KullaniciId) as temsilci,
			(select top 1  s.Baslik from SatisciAyrintiTB s where s.MusteriAdi = m.MusteriAdi   order by s.Tarih desc) as baslik,
            (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId) as UlkeAdi,
            u.Png_Flags as Flag,
            (select mt.MailAdresi from MusterilerTB mt where mt.FirmaAdi = m.MusteriAdi) as Mail,
            t.KaynakYeri as Kaynak,
			t.Id as ID,
			t.TakipEt
            from YeniTeklifTB t , YeniTeklif_MusterilerTB m,YeniTeklif_UlkeTB u
            where m.Id = t.MusteriId and ( t.TeklifOncelik='A' or  t.TeklifOncelik='B' or t.TeklifOncelik='C') and t.TakipEt=1 and u.Id = m.UlkeId
            GROUP BY  m.MusteriAdi,t.TeklifOncelik, t.KullaniciId,m.UlkeId,u.Png_Flags,t.KaynakYeri,t.Id,t.TakipEt
			order by t.TeklifOncelik


            """
        )

        liste = list()

        for item in result:

            model = MusteriListeModel()
            model.id = 1
            model.musteriadi = item.MusteriAdi
            model.oncelik = item.TeklifOncelik
            model.newOncelik = item.TeklifOncelik
            if item.TeklifOncelik == 'A':
                model.oncelikBackground = 'yellow'
            elif item.TeklifOncelik == 'B':
                model.oncelikBackground = 'blue'
            elif item.TeklifOncelik == 'C':
                model.oncelikBackground = 'green'
            model.temsilci = item.temsilci
            if item.baslik == None:
                item.baslik = ""
            if item.Kaynak == 'BGP Network':
                
                model.oncelikBackground = '#93c47d'
            else:
                model.oncelikBackground = '#c592ad'
            model.aciklama = item.baslik
            model.ulkeAdi = item.UlkeAdi
            model.flag = item.Flag
            model.mail = item.Mail
            model.satisciDurum = 'Teklif'
            model.teklifSira = item.ID
            liste.append(model)

        schema = MusteriListeSchema(many=True)

        return schema.dump(liste)
    
    
    
    def __musteriTeklifListesiBGNAll(self):

        result = self.data.getList(
            """
            select
            m.MusteriAdi,
            t.TeklifOncelik,
            (select k.KullaniciAdi from KullaniciTB k where k.ID = t.KullaniciId) as temsilci,
			(select top 1  s.Baslik from SatisciAyrintiTB s where s.MusteriAdi = m.MusteriAdi   order by s.Tarih desc) as baslik,
            (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId) as UlkeAdi,
            u.Png_Flags as Flag,
            (select mt.MailAdresi from MusterilerTB mt where mt.FirmaAdi = m.MusteriAdi) as Mail,
            t.KaynakYeri as Kaynak,
			t.Id as ID
            from YeniTeklifTB t , YeniTeklif_MusterilerTB m,YeniTeklif_UlkeTB u
            where m.Id = t.MusteriId and ( t.TeklifOncelik='A' or  t.TeklifOncelik='B' or t.TeklifOncelik='C') and t.TakipEt=1 and u.Id = m.UlkeId and t.KaynakYeri='BGP Network'
            GROUP BY  m.MusteriAdi,t.TeklifOncelik, t.KullaniciId,m.UlkeId,u.Png_Flags,t.KaynakYeri,t.Id
			order by t.TeklifOncelik


            """
        )

        liste = list()

        for item in result:

            model = MusteriListeModel()
            model.id = 1
            model.musteriadi = item.MusteriAdi
            model.oncelik = item.TeklifOncelik
            model.newOncelik = item.TeklifOncelik
            if item.TeklifOncelik == 'A':
                model.oncelikBackground = 'yellow'
            elif item.TeklifOncelik == 'B':
                model.oncelikBackground = 'blue'
            elif item.TeklifOncelik == 'C':
                model.oncelikBackground = 'green'
            model.temsilci = item.temsilci
            if item.baslik == None:
                item.baslik = ""
            if item.Kaynak == 'BGP Network':
                
                model.oncelikBackground = '#93c47d'
            else:
                model.oncelikBackground = '#63b0f5'
            model.aciklama = item.baslik
            model.ulkeAdi = item.UlkeAdi
            model.flag = item.Flag
            model.mail = item.Mail
            model.satisciDurum = 'Teklif'
            model.teklifSira = item.ID
            liste.append(model)

        schema = MusteriListeSchema(many=True)

        return schema.dump(liste)
    