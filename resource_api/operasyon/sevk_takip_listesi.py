from models.operasyon import SevkTakipModel,SevkTakipSchema,SevkTakipSchema,SevkTakipModel
from helpers import SqlConnect,TarihIslemler
import datetime


class SevkTakip:

    def __init__(self):

        self.data = SqlConnect().data 

    def getSevkListesi(self):
        
        tarihIslem = TarihIslemler()
        result = self.data.getList(
            """
            select
            s.ID,
            s.SiparisNo,
            m.FirmaAdi as MusteriAdi,
            s.Pesinat,
            NavlunSatis + DetayTutar_1 + DetayTutar_2 + DetayTutar_3  as Navlun,
            ( Select Sum(o.Tutar) from OdemelerTB o where o.SiparisNo=s.SiparisNo ) as Odemeler,
            (Select Sum(u.SatisToplam) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo) as MalBedeli,
            (select k.KullaniciAdi from KullaniciTB k where k.ID=s.SiparisSahibi ) as Sorumlu,
            s.Eta,
            s.KonteynerNo,
            s.YuklemeTarihi,
            s.KonsimentoDurum,
            s.AktarmaLimanAdi,
            s.Line,
            s.Takip
            from
            SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID
            and s.SiparisDurumID=3 and s.Takip=1
            order by s.ID desc
            """
        )

        liste = list()
        sira =1
        for item in result:

            navlun = 0
            odemeler = 0
            mal_bedeli = 0
            sevk_tarihi = ""
            eta = ""
            model = SevkTakipModel()

            if item.Navlun != None:
                navlun = item.Navlun 
            
            if item.Odemeler != None:
                odemeler = item.Odemeler 
            
            if item.MalBedeli != None:
                mal_bedeli = item.MalBedeli
            model.sira = sira
            sira += 1
            if item.Eta != None: 
                try:
                    eta = tarihIslem.getDate(item.Eta).strftime("%d-%m-%Y")
                    bugun = datetime.date.today()
                    sontarih_str = eta.split('-')
                   
                    sontarih = datetime.date(int(sontarih_str[2]),int(sontarih_str[1]),int(sontarih_str[0]))
                    model.kalan_sure = (sontarih - bugun).days
                except Exception as e :
                    print('eta hatası : ', str(e))

            if item.YuklemeTarihi != None:
                sevk_tarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")

            
            model.id = item.ID 
            model.siparisno = item.SiparisNo 
            model.pesinat = item.Pesinat 
            model.kalan_alacak = (navlun + mal_bedeli) - odemeler
            model.sevk_tarihi = sevk_tarihi
            model.konteynerno = item.KonteynerNo 
            model.eta = eta
            model.sorumlusu = item.Sorumlu
            model.musteriadi = item.MusteriAdi
            model.takip = item.Takip
            if(item.KonsimentoDurum == None):
                model.konsimento = False
            else:
                model.konsimento = item.KonsimentoDurum
            model.line = item.Line
            model.liman = item.AktarmaLimanAdi

            liste.append(model)

        schema = SevkTakipSchema(many=True)

        return schema.dump(liste)

    def getTakiptenDusenler(self):
        
        tarihIslem = TarihIslemler()
        result = self.data.getList(
            """
            select
            s.ID,
            s.SiparisNo,
            m.FirmaAdi as MusteriAdi,
            s.Pesinat,
            NavlunSatis + DetayTutar_1 + DetayTutar_2 + DetayTutar_3 as Navlun,
            ( Select Sum(o.Tutar) from OdemelerTB o where o.SiparisNo=s.SiparisNo ) as Odemeler,
            (Select Sum(u.SatisToplam) from SiparisUrunTB u where u.SiparisNo=s.SiparisNo) as MalBedeli,
            (select k.KullaniciAdi from KullaniciTB k where k.ID=s.SiparisSahibi ) as Sorumlu,
            s.Eta,
            s.KonteynerNo,
            s.YuklemeTarihi,
            s.KonsimentoDurum,
            s.Line,
            s.AktarmaLimanAdi
            from
            SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID
            and s.SiparisDurumID=3 
			and Year(s.YuklemeTarihi)>=2020
			and m.Marketing in
			(
			'BD','Depo','Ghana','Mekmar','SM'
			)
			and s.KonteynerNo is not null
            and s.KonteynerNo != ''
            and s.Takip=0
            order by s.ID desc
            """
        )

        liste = list()
        sira = 1
        for item in result:

            navlun = 0
            odemeler = 0
            mal_bedeli = 0
            sevk_tarihi = ""
            eta = ""
            model = SevkTakipModel()
            model.sira = sira
            sira += 1
            if item.Navlun != None:
                navlun = item.Navlun 
            
            if item.Odemeler != None:
                odemeler = item.Odemeler 
            
            if item.MalBedeli != None:
                mal_bedeli = item.MalBedeli
            
            if item.Eta != None: 
                try:
                    eta = tarihIslem.getDate(item.Eta).strftime("%d-%m-%Y")
                    bugun = datetime.date.today()
                    sontarih_str = eta.split('-')
                    
                    sontarih = datetime.date(int(sontarih_str[2]),int(sontarih_str[1]),int(sontarih_str[0]))
                    if (sontarih - bugun).days < 0:
                        model.kalan_sure = 0
                    
                    else:
                        model.kalan_sure =  (sontarih - bugun).days
                except Exception as e :
                    print('eta hatası : ', str(e))

            if item.YuklemeTarihi != None:
                sevk_tarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")

            
            model.id = item.ID 
            model.siparisno = item.SiparisNo 
            model.pesinat = item.Pesinat 
            model.kalan_alacak = (navlun + mal_bedeli) - odemeler
            model.sevk_tarihi = sevk_tarihi
            model.konteynerno = item.KonteynerNo 
            model.eta = eta
            model.sorumlusu = item.Sorumlu
            model.musteriadi = item.MusteriAdi
            model.konsimento = item.KonsimentoDurum
            model.line = item.Line
            model.liman = item.AktarmaLimanAdi

            liste.append(model)

        schema = SevkTakipSchema(many=True)

        return schema.dump(liste)

    def getSevkDetay(self,id):
       
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(
            """
            select
            s.ID,
            s.Eta,
            s.KonteynerNo,
            s.KonsimentoDurum,
            s.Takip,
            s.Line
            from
            SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID
            and s.SiparisDurumID=3 
            and s.ID=?
            """,(id)
        )
      
        liste = list()
        sira = 1
        for item in result:
           
            model = SevkTakipModel()

            model.id = item.ID
                
            if item.Eta != None:
                    model.eta = tarihIslem.getDate(item.Eta).strftime("%d-%m-%Y")

            model.konteynerno = item.KonteynerNo
            model.konsimento = item.KonsimentoDurum
            model.takip = item.Takip
            model.line = item.Line
            model.sira = sira
            sira += 1
            liste.append(model)

        schema = SevkTakipSchema(many=True)

      

        return schema.dump(liste)

    def sevkDetayGuncelle(self,item):
        
        print(item)
        try:
            self.data.update_insert(
                """
                update SiparislerTB set KonsimentoDurum=?,
                Eta=?,KonteynerNo=?,Takip=?,Line=? where ID=?
                """,(
                    item['konsimento'],item['eta'],item['konteynerno'],
                    item['takip'],item['line'], item['id']
                )
            )

            return True 

        except Exception as e:
            print('Sevk Takip Güncelle Hata : ',str(e))
            return False    

