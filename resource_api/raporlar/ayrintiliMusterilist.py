from helpers import SqlConnect,TarihIslemler
from models.raporlar import *
from models.operasyon import *
import datetime


class GenelMusteriListesi:

    def __init__(self):

        self.data = SqlConnect().data

    
    def getGenelMusteriSiparis(self):
        liste = list()
        
        result = self.data.getList(
            "{call musteri_bazinda_tum_genel_ciro_son_7 }"
          )

        liste = list()
        
        for item in result:
            model = KullaniciModel()
            """
            if item.MusteriId == 3446:
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci

                model.BuYilUretim = self.bdToplam()[0]
                model.BuYilSevkiyat = self.bdToplam()[1]
                model.GecenYil = self.bdToplam()[2]
                model.OncekiYil = self.bdToplam()[3]
                model.OnDokuzYili = self.bdToplam()[4]
                model.OnSekizYili = self.bdToplam()[5]
                model.OnYediYili = self.bdToplam()[6]
                model.OnAltiYili = self.bdToplam()[7]
                model.OnBesYili = self.bdToplam()[8]
                model.OnDortYili = self.bdToplam()[9]
                model.OnUcYili = self.bdToplam()[10]
                model.OnUcYiliOncesi = self.getonuconcesi(3446)
                model.Toplam = self.bdToplam()[11] - self.bdToplam()[1] + self.getisNoneType(self.getonuconcesi(3446))
                
                
                
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
           
           

                liste.append(model)
            elif item.MusteriId==169:
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci

                model.BuYilUretim = self.tamerToplam()[0]
                model.BuYilSevkiyat = self.tamerToplam()[1]
                model.GecenYil = self.tamerToplam()[2]
                model.OncekiYil = self.tamerToplam()[3]
                model.OnDokuzYili = self.tamerToplam()[4]
                model.OnSekizYili = self.tamerToplam()[5]
                model.OnYediYili = self.tamerToplam()[6]
                model.OnAltiYili = self.tamerToplam()[7]
                model.OnBesYili = self.tamerToplam()[8]
                model.OnDortYili = self.tamerToplam()[9]
                model.OnUcYili = self.tamerToplam()[10]
                model.OnUcYiliOncesi = self.getonuconcesi(169)
                model.Toplam = self.tamerToplam()[11] - self.tamerToplam()[1] + self.getisNoneType(self.getonuconcesi(169))
                
                
                
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
           
           

                liste.append(model)
            elif item.MusteriId == 269:
                
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci

                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat

                model.BuYil = item.BuYilCiro
                model.GecenYil = item.GecenYilCiro
                model.OncekiYil = item.OncekiYilCiro
                model.OnDokuzYili = item.OndokuzYilCiro
                model.OnSekizYili = item.OnSekizYilCiro
                model.OnYediYili = self.mekusToplam()[0]
                model.OnAltiYili = self.mekusToplam()[1]
                model.OnBesYili = self.mekusToplam()[2]
                model.OnDortYili = item.OnDortYilCiro
                model.OnUcYili = item.OnUcYilCiro
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.mekusToplam()[0] + self.mekusToplam()[1] + self.mekusToplam()[2] + self.getisNoneType(self.getonuconcesi(269))
                model.OnUcYiliOncesi = self.getonuconcesi(269)
                
                
                
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
           
           

                liste.append(model)
            elif item.MusteriId == 260:
                pass
            elif item.MusteriId ==  255:
                pass
            elif item.MusteriId == 236:
                pass
            elif item.MusteriId == 217:
                pass
            elif item.MusteriId ==198:
                pass
            elif item.MusteriId ==191:
                pass
                
                """
            if item.MusteriId == 6:
                continue
            if item.MusteriId == 34:
                continue
            if item.MusteriId ==32:
                continue
            if item.MusteriId ==260:
                continue
            if item.MusteriId ==255:
                continue
            if item.MusteriId ==236:
                continue
            if item.MusteriId ==120:
                continue
            if item.MusteriId ==67:
                continue
            if item.MusteriId ==15:
                continue
            if item.MusteriId ==205:
                continue
            if item.MusteriId ==61:
                continue
            if item.MusteriId ==12:
                continue
            if item.MusteriId == self.isIcSiparis(item.MusteriId):
                continue
            
            if item.MusteriId ==217:
                continue
            if item.MusteriId ==198:
                continue
            if item.MusteriId ==191:
                continue
            if item.MusteriId ==3446:
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci
                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat
                model.BuYil = item.BuYilCiro
                model.GecenYil = self.getisNoneType(item.GecenYilCiro)
                model.OncekiYil = self.getisNoneType(item.OncekiYilCiro)
                model.OnDokuzYili = self.getisNoneType(item.OndokuzYilCiro)
                model.OnSekizYili = self.getisNoneType(item.OnSekizYilCiro)
                model.OnYediYili = self.getisNoneType(item.OnYediYilCiro)
                model.OnAltiYili = self.getisNoneType(item.OnAltiYilCiro)
                model.OnBesYili = self.getisNoneType(item.OnBesYilCiro)
                model.OnDortYili = self.getisNoneType(item.OnDortYilCiro)
                model.OnUcYili = self.getisNoneType(item.OnUcYilCiro)
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                for i in result:
                    if i.MusteriId == 6:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                        
                    if i.MusteriId ==34:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
                liste.append(model)
            elif item.MusteriId ==169:
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci
                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat
                model.BuYil = item.BuYilCiro
                model.GecenYil = self.getisNoneType(item.GecenYilCiro)
                model.OncekiYil = self.getisNoneType(item.OncekiYilCiro)
                model.OnDokuzYili = self.getisNoneType(item.OndokuzYilCiro)
                model.OnSekizYili = self.getisNoneType(item.OnSekizYilCiro)
                model.OnYediYili = self.getisNoneType(item.OnYediYilCiro)
                model.OnAltiYili = self.getisNoneType(item.OnAltiYilCiro)
                model.OnBesYili = self.getisNoneType(item.OnBesYilCiro)
                model.OnDortYili = self.getisNoneType(item.OnDortYilCiro)
                model.OnUcYili = self.getisNoneType(item.OnUcYilCiro)
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                
                for i in result:
                    if i.MusteriId == 32:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
                liste.append(model)          
            elif item.MusteriId == 269:
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci
                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat
                model.BuYil = item.BuYilCiro
                model.GecenYil = self.getisNoneType(item.GecenYilCiro)
                model.OncekiYil = self.getisNoneType(item.OncekiYilCiro)
                model.OnDokuzYili = self.getisNoneType(item.OndokuzYilCiro)
                model.OnSekizYili = self.getisNoneType(item.OnSekizYilCiro)
                model.OnYediYili = self.getisNoneType(item.OnYediYilCiro)
                model.OnAltiYili = self.getisNoneType(item.OnAltiYilCiro)
                model.OnBesYili = self.getisNoneType(item.OnBesYilCiro)
                model.OnDortYili = self.getisNoneType(item.OnDortYilCiro)
                model.OnUcYili = self.getisNoneType(item.OnUcYilCiro)
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                
                for i in result:
                    if i.MusteriId == 260:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                    if i.MusteriId ==217:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                    if i.MusteriId ==198:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                    if i.MusteriId ==191:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
                liste.append(model)
            elif item.MusteriId == 63:
                model.musteri_id = item.MusteriId
                model.musteri = 'Diğer Ghana'
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci
                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat
                model.BuYil = item.BuYilCiro
                model.GecenYil = self.getisNoneType(item.GecenYilCiro)
                model.OncekiYil = self.getisNoneType(item.OncekiYilCiro)
                model.OnDokuzYili = self.getisNoneType(item.OndokuzYilCiro)
                model.OnSekizYili = self.getisNoneType(item.OnSekizYilCiro)
                model.OnYediYili = self.getisNoneType(item.OnYediYilCiro)
                model.OnAltiYili = self.getisNoneType(item.OnAltiYilCiro)
                model.OnBesYili = self.getisNoneType(item.OnBesYilCiro)
                model.OnDortYili = self.getisNoneType(item.OnDortYilCiro)
                model.OnUcYili = self.getisNoneType(item.OnUcYilCiro)
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                
                for i in result:
                    if i.MusteriId == 120:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                    if i.MusteriId == 67:
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)    
                    
                        
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
                liste.append(model)
            
            elif item.MusteriId == 23:
                model.musteri_id = item.MusteriId
                model.musteri = 'Eski Depo'
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci
                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat
                model.BuYil = item.BuYilCiro
                model.GecenYil = self.getisNoneType(item.GecenYilCiro)
                model.OncekiYil = self.getisNoneType(item.OncekiYilCiro)
                model.OnDokuzYili = self.getisNoneType(item.OndokuzYilCiro)
                model.OnSekizYili = self.getisNoneType(item.OnSekizYilCiro)
                model.OnYediYili = self.getisNoneType(item.OnYediYilCiro)
                model.OnAltiYili = self.getisNoneType(item.OnAltiYilCiro)
                model.OnBesYili = self.getisNoneType(item.OnBesYilCiro)
                model.OnDortYili = self.getisNoneType(item.OnDortYilCiro)
                model.OnUcYili = self.getisNoneType(item.OnUcYilCiro)
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                
                for i in result:
                    if i.MusteriId == 15:
                        model.BuYilUretim = self.getisNoneType(i.BuYilUretim)
                        model.BuYilSevkiyat = self.getisNoneType(i.BuYilSevkiyat)
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                    if i.MusteriId == 205:
                        model.BuYilUretim = self.getisNoneType(i.BuYilUretim)
                        model.BuYilSevkiyat = self.getisNoneType(i.BuYilSevkiyat)
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)    
                    if i.MusteriId == 12:
                        model.BuYilUretim = self.getisNoneType(i.BuYilUretim)
                        model.BuYilSevkiyat = self.getisNoneType(i.BuYilSevkiyat)
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)    
                    if i.MusteriId == 61:
                        model.BuYilUretim = self.getisNoneType(i.BuYilUretim)
                        model.BuYilSevkiyat = self.getisNoneType(i.BuYilSevkiyat)
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                        
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
                liste.append(model)
            elif item.MusteriId == 242:
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci
                model.BuYilUretim = self.getisNoneType(item.BuYilUretim)
                model.BuYilSevkiyat = self.getisNoneType(item.BuYilSevkiyat)
                model.BuYil = item.BuYilCiro
                model.GecenYil = self.getisNoneType(item.GecenYilCiro)
                model.OncekiYil = self.getisNoneType(item.OncekiYilCiro)
                model.OnDokuzYili = self.getisNoneType(item.OndokuzYilCiro)
                model.OnSekizYili = self.getisNoneType(item.OnSekizYilCiro)
                model.OnYediYili = self.getisNoneType(item.OnYediYilCiro)
                model.OnAltiYili = self.getisNoneType(item.OnAltiYilCiro)
                model.OnBesYili = self.getisNoneType(item.OnBesYilCiro)
                model.OnDortYili = self.getisNoneType(item.OnDortYilCiro)
                model.OnUcYili = self.getisNoneType(item.OnUcYilCiro)
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                
                for i in result:
                    if i.Marketing == 'İç Piyasa':
                        if i.MusteriId ==56:
                            continue
                        if i.MusteriId ==8:
                            continue
                        if i.MusteriId ==215:
                            continue
                        if i.MusteriId ==27:
                            continue
                        if i.MusteriId ==196:
                            continue
                        model.BuYilUretim += self.getisNoneType(i.BuYilUretim)
                        model.BuYilSevkiyat += self.getisNoneType(i.BuYilSevkiyat)
                        model.GecenYil += self.getisNoneType(i.GecenYilCiro)
                        model.OncekiYil += self.getisNoneType(i.OncekiYilCiro)
                        model.OnDokuzYili += self.getisNoneType(i.OndokuzYilCiro)
                        model.OnSekizYili += self.getisNoneType(i.OnSekizYilCiro)
                        model.OnYediYili += self.getisNoneType(i.OnYediYilCiro)
                        model.OnAltiYili += self.getisNoneType(i.OnAltiYilCiro)
                        model.OnBesYili += self.getisNoneType(i.OnBesYilCiro)
                        model.OnDortYili += self.getisNoneType(i.OnDortYilCiro)
                        model.OnUcYili += self.getisNoneType(i.OnUcYilCiro)
                        model.Toplam += self.getisNoneType(i.GenelCiro)
                
                
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
                liste.append(model)
            
            
            
            else:
                
                
                model.musteri_id = item.MusteriId
                model.musteri = item.MusteriAdi
                model.ulkeAdi = item.UlkeAdi
                model.logo = item.UlkeLogo
                model.temsilci = item.Temsilci

                model.BuYilUretim = item.BuYilUretim
                model.BuYilSevkiyat = item.BuYilSevkiyat

                model.BuYil = item.BuYilCiro
                model.GecenYil = item.GecenYilCiro
                model.OncekiYil = item.OncekiYilCiro
                model.OnDokuzYili = item.OndokuzYilCiro
                model.OnSekizYili = item.OnSekizYilCiro
                model.OnYediYili = item.OnYediYilCiro
                model.OnAltiYili = item.OnAltiYilCiro
                model.OnBesYili = item.OnBesYilCiro
                model.OnDortYili = item.OnDortYilCiro
                model.OnUcYili = item.OnUcYilCiro
                model.OnUcYiliOncesi = self.getisNoneType(item.OnUcYilOncesiCiro) + self.getisNoneType(item.RealOnUcCiro)
                model.Toplam = self.getisNoneType(item.GenelCiro) - self.getisNoneType(item.BuYilCiro) + self.getisNoneType(item.OnUcYilOncesiCiro)
                
                
                
                model.marketing = item.Marketing
                model.oncelik = item.MusteriOncelik
        
        

                liste.append(model)

           

        schema = KullaniciSchema(many=True)  


        return schema.dump(liste)     
    

            
    
    def isIcSiparis(self,id):
        icSiparisMusterileri=[7,
                20,
                27,
                29,
                40,
                54,
                59,
                80,
                82,
                84,
                88,
                90,
                93,
                94,
                95,
                96,
                99,
                100,
                101,
                113,
                119,
                121,
                128,
                146,
                147,
                176,
                181,
                182,
                183,
                190,
                192,
                194,
                199,
                200,
                202,
                203,
                204,
                216,
                230,
                237,
                239,
                246,
                250,
                262,
                285,
                299,
                305,
                315,
                327,
                1349,
                1363,
                1365,
                1364,
                2377,
                2393,
                2396,
                2403,
                2405,
                2413,
                2414,
                2415,
                3416,
                3445,
                3449,
                3451,
                3466,
                3483,
                4484,
                4488,
                5503,
                5504,
                5507,
                5512,
                5513,
                5514,
                6524,
                6526,
                7530,
                7538,
                7581,
                7647,
                7638,
                7636,
                7632,
                7629,
                7627,
                7623,
                7617,
                7613,
                7611,
                7609,
                7608,
                7606,
                7601,
                7598,
                7592,
                7591,
                7589
                ]
        for i in icSiparisMusterileri:
            if id == i:
                
                return id
            


    def getonuconcesi(self,musteriID):
        if musteriID == None:
            return
        else:
            
            result = self.data.getStoreList(
                """
                
                    select OnUcOncesi from MusteriBazindaOnUcOncesi where musteriId=?
                """,(musteriID)
            )
            return result[0][0]
        
    def getisNoneType(self,value):

        if value == None:
            return 0
        else:
            return float(value)
   
   
        
    def getCustomersDetailList(self,sipNo):
        try:
            data = self.data.getStoreList("""
                                            select 

                                                    su.SatisFiyati,
                                                    su.SatisToplam,
                                                    su.Miktar,
                                                    k.KategoriAdi,
                                                    urun.UrunAdi,
                                                    yk.YuzeyIslemAdi,
                                                    ol.En,
                                                    ol.Boy,
                                                    ol.Kenar,
                                                    ub.BirimAdi


                                                from 

                                                    SiparisUrunTB su
                                                    inner join UrunKartTB ur on ur.ID = su.UrunKartID
                                                    inner join KategoriTB k on k.ID = ur.KategoriID
                                                    inner join UrunlerTB urun on urun.ID = ur.UrunID
                                                    inner join YuzeyKenarTB yk on yk.ID = ur.YuzeyID
                                                    inner join OlculerTB ol on ol.ID = ur.OlcuID
                                                    inner join UrunBirimTB ub on ub.ID = su.UrunBirimID

                                                where su.SiparisNo=?
                                          
                                          """,(sipNo))
            
            liste = list()
            for item in data:
                model = CustomersDetailListModel()
                model.satisFiyati = item.SatisFiyati
                model.satisToplam = item.SatisToplam
                model.miktar = item.Miktar
                model.birimAdi = item.BirimAdi
                model.kategori = item.KategoriAdi
                model.urunAdi = item.UrunAdi
                model.yuzey = item.YuzeyIslemAdi
                model.en = item.En
                model.boy = item.Boy
                model.kenar = item.Kenar
                liste.append(model)
            schema = CustomersDetailListShema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getCustomersDetailList hata',str(e))
            return False