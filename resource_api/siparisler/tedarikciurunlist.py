from helpers import SqlConnect

from models.siparisler_model.siparisGirisUrun import SiparisGirisUrunModel,SiparisGirisUrunSchema
from models.tedarikci_model.tedariki_liste import TedarikciListeSchema,TedarikciListeModel
class TedarikciSiparisUrunListe:

    def __init__(self,siparisno):
        self.data = SqlConnect().data
        self.siparisno = siparisno
       
    def getTedarikciSiparisAyrintiList(self): #2 ayrı tabloyu birleştirme

        siparis_urun_list = self.__getOzelIscilikUrunler()
       
        for item in self.__getSiparisUrunler():

            siparis_urun_list.append(item)

        schema = SiparisGirisUrunSchema(many=True)
       
        return schema.dump(siparis_urun_list)

    def getTedarikciSiparisTedarikciAyrintiList(self): #2 ayrı tabloyu birleştirme

        siparis_tedarikci_list = self.__getSiparisOzelTedarikciler()
        for item in self.__getSiparisTedarikciler():
            if(self.__tedarikciKontrol(item.tedarikciadi)):
                continue
            else:
                    
                siparis_tedarikci_list.append(item)

        schema = TedarikciListeSchema(many=True)
       
        return schema.dump(siparis_tedarikci_list)   
   

    def __tedarikciKontrol(self,tedarikciAdi):
        for item in self.__getSiparisOzelTedarikciler():
            if item.tedarikciadi == tedarikciAdi:
                return True
            else:
                return False

    def __getSiparisUrunler(self):

        result = self.data.getStoreList(
            """
            select
            *,
            (Select t.FirmaAdi from TedarikciTB t where t.ID=s.TedarikciID) as TedarikciAdi,
            (Select u.BirimAdi from UrunBirimTB u where u.ID=s.UrunBirimID) as urunbirimadi,
            dbo.Get_UrunAdi(s.UrunKartID) as UrunAdi,
            dbo.Get_Olcu_En(s.UrunKartID) as En,
            dbo.Get_Olcu_Boy(s.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(s.UrunKartID) as Kenar,
            dbo.Get_KenarIslem(s.UrunKartID) as YuzeyIslem,
            (select m.Marketing from SiparislerTB a , MusterilerTB m  where a.SiparisNo=s.SiparisNo and m.ID=a.MusteriID ) as musteri,
            s.UrunKartID
            from
            SiparisUrunTB s
            where s.SiparisNo=?
            order by s.SiraNo asc
            """,(self.siparisno)
        )

        siparisList = list()

        for item in result:

            model = SiparisGirisUrunModel()

            model.id = item.ID 
         
            model.siparisNo = item.SiparisNo 
            model.tedarikciId = item.TedarikciID 
            model.urunKartId = item.UrunKartID 
            model.urunBirimId = item.UrunBirimID 
            model.urunbirimAdi = item.urunbirimadi 
            model.miktar = item.Miktar 
            model.pazarlama = item.musteri
            model.ozelMiktar = item.OzelMiktar 
            model.kasaAdet = item.KasaAdet 
            model.satisFiyati = item.SatisFiyati 
            model.satisToplam = item.SatisToplam 
            model.uretimAciklama = item.UretimAciklama 
            model.musteriAciklama = item.MusteriAciklama 
            model.notlar = item.Notlar 
            model.kullaniciId = item.KullaniciID 
            model.alisFiyati = item.AlisFiyati 
            model.alisFiyati_Tl = item.AlisFiyati_TL
            model.siraNo = item.SiraNo 
            model.tedarikciAdi = item.TedarikciAdi
            if item.urunbirimadi == 'M2' : 
                model.m2 = item.Miktar
            elif  item.urunbirimadi == 'Adet': 
                 model.adet = item.Miktar
            elif  item.urunbirimadi == 'Mt': 
                 model.mt = item.Miktar
            elif  item.urunbirimadi == 'Ton': 
                 model.ton = item.Miktar 
            model.urunAdi = item.UrunAdi
            model.en = item.En 
            model.boy = item.Boy 
            model.kenar = item.Kenar 
            model.yuzeyIslem = item.YuzeyIslem

            siparisList.append(model)

        return siparisList


    def __getOzelIscilikUrunler(self):

        result = self.data.getStoreList(
            """
             select
           *,
            (Select t.FirmaAdi from TedarikciTB t where t.ID=e.TedarikciID) as TedarikciAdi,
            (Select u.BirimAdi from UrunBirimTB u where u.ID=s.UrunBirimID) as urunbirimadi,
            dbo.Get_UrunAdi(s.UrunKartID) as UrunAdi,
            dbo.Get_Olcu_En(s.UrunKartID) as En,
            dbo.Get_Olcu_Boy(s.UrunKartID) as Boy,
            dbo.Get_Olcu_Kenar(s.UrunKartID) as Kenar,
            dbo.Get_KenarIslem(s.UrunKartID) as YuzeyIslem,
			e.Tutar,
            s.UrunKartID
            from
            SiparisUrunTB s , SiparisEkstraGiderlerTB e 
            where s.SiparisNo=? and e.SiparisNo=s.SiparisNo and e.UrunKartId=s.UrunKartID
            order by s.SiraNo asc
            """,(self.siparisno)
        )

        siparisList = list()

        for item in result:

            model = SiparisGirisUrunModel()

            model.id = item.ID 
          
            model.siparisNo = item.SiparisNo 
            model.tedarikciId = item.TedarikciID 
            model.urunKartId = item.UrunKartID 
            model.urunBirimId = item.UrunBirimID 
            model.urunbirimAdi = item.urunbirimadi 
            model.miktar = item.Miktar 
            model.ozelMiktar = item.OzelMiktar 
            model.kasaAdet = item.KasaAdet 
            model.satisFiyati = item.SatisFiyati 
            model.satisToplam = item.Tutar  
            model.uretimAciklama = item.UretimAciklama 
            model.musteriAciklama = item.MusteriAciklama 
            model.notlar = item.Notlar 
            model.kullaniciId = item.KullaniciID 
            if(item.Tutar != 0 and item.Miktar != 0):
                
                model.alisFiyati = item.Tutar / item.Miktar
            else:
                model.alisFiyati = 0
            model.alisFiyati_Tl = item.AlisFiyati_TL
            model.siraNo = item.SiraNo 
            model.tedarikciAdi = item.TedarikciAdi
            if item.urunbirimadi == 'M2' : 
                model.m2 = item.Miktar
            elif  item.urunbirimadi == 'Adet': 
                 model.adet = item.Miktar
            elif  item.urunbirimadi == 'Mt': 
                 model.mt = item.Miktar
            elif  item.urunbirimadi == 'Ton': 
                 model.ton = item.Miktar 

            model.urunAdi = item.UrunAdi
            model.en = item.En 
            model.boy = item.Boy 
            model.kenar = item.Kenar 
            model.yuzeyIslem = item.YuzeyIslem

            siparisList.append(model)

        return siparisList
 
    def __getSiparisTedarikciler(self):

        result = self.data.getStoreList(
            """
            select
            t.FirmaAdi,
			t.ID
         
            from
            SiparisUrunTB s , TedarikciTB t , SiparisEkstraGiderlerTB e 
            where s.SiparisNo=? and t.ID=s.TedarikciID 
			group by   t.FirmaAdi,t.ID
      
            """,(self.siparisno)
        )

        tedarikciList = list()

        for item in result:

            model = TedarikciListeModel()
            model.id = item.ID
            model.tedarikciadi = item.FirmaAdi 
            tedarikciList.append(model)

        return tedarikciList

    def __getSiparisOzelTedarikciler(self):

        result = self.data.getStoreList(
            """
           select  
            t.FirmaAdi 
            from SiparisEkstraGiderlerTB s ,TedarikciTB t 
            where SiparisNo=? and t.ID=s.TedarikciID 
            group by   t.FirmaAdi
      
            """,(self.siparisno)
        )

        tedarikciList = list()

        for item in result:

            model = TedarikciListeModel()

            model.tedarikciadi = item.FirmaAdi 
            tedarikciList.append(model)

        return tedarikciList