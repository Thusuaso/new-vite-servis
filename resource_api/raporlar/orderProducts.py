from helpers import SqlConnect
import datetime
from models.raporlar.orderProducts import OrderSchema,OrderModel,MusteriBazindaUretimModel,MusteriBazindaUretimSchema

class Order:
    
    def __init__(self):
        self.data = SqlConnect().data
        
    def getOrderProducts(self,po):
        try:
            siparisUrunresult = self.data.getStoreList("""
                                                select 

                                                su.ID,
                                                (select ur.BirimAdi from UrunBirimTB ur where ur.ID = su.UrunBirimID) as Birim,
                                                su.Miktar,
                                                su.OzelMiktar,
                                                su.Ton,
                                                su.UrunKartID,
                                                (select (select o.En from OlculerTB o where o.ID = urk.OlcuID) from UrunKartTB urk where urk.ID = su.UrunKartID) as En,
                                                (select (select o.Boy from OlculerTB o where o.ID = urk.OlcuID) from UrunKartTB urk where urk.ID = su.UrunKartID) as Boy,
                                                (select (select o.Kenar from OlculerTB o where o.ID = urk.OlcuID) from UrunKartTB urk where urk.ID = su.UrunKartID) as Kenar,
                                                (select (select kt.KategoriAdi from KategoriTB kt where kt.ID=urk.KategoriID) from UrunKartTB urk where urk.ID = su.UrunKartID) as Kategori,
                                                (select (select urun.UrunAdi from UrunlerTB urun where urun.ID=urk.UrunID) from UrunKartTB urk where urk.ID = su.UrunKartID) as UrunAdi,
                                                (select (select yk.YuzeyIslemAdi from YuzeyKenarTB yk where yk.ID=urk.YuzeyID) from UrunKartTB urk where urk.ID = su.UrunKartID) as Yuzey,
                                                (select sum(ur.Miktar) from UretimTB ur where ur.SiparisAciklama = su.SiparisNo and ur.UrunKartID = su.UrunKartID) as UretilenMiktar,
                                                (select sum(ur.Adet) from UretimTB ur where ur.SiparisAciklama = su.SiparisNo and ur.UrunKartID = su.UrunKartID) as UretilenAdet



                                            from 
                                                SiparisUrunTB su
                                                

                                            where 
                                                SiparisNo=?
                                            
                                            
                                            """,po)
            patternKasaMetreKaresi = 0.1239
            setKasaMetreKaresi = 0.011903
            
            liste = list()
            for item in siparisUrunresult:
                model = OrderModel()
                model.id = item.ID
                model.birim = item.Birim
                if item.Birim == 'M2':
                    model.birimBackground = 'yellow'
                elif item.Birim == 'Adet':
                    model.birimBackground = '#98FFA4'
                else:
                    model.birimBackground ='#80ABC5'
                model.miktar = item.Miktar
                model.ozelMiktar = item.OzelMiktar
                model.ton = item.Ton
                model.en = item.En
                model.boy = item.Boy
                model.kenar= item.Kenar
                model.kategori = item.Kategori
                model.urunAdi = item.UrunAdi
                model.yuzey = item.Yuzey
                model.boyut = item.En + 'x' + item.Boy + 'x' + item.Kenar
                if item.UretilenMiktar != None:
                    model.uretimMiktari = item.UretilenMiktar
                    model.kalanMiktar = item.Miktar - item.UretilenMiktar
                    
                                
                    if model.kategori == 'Travertine Mosaic' or model.kategori == 'Marble Mosaic':
                        if model.birim =='M2':
                            model.kalanAdet = float(model.kalanMiktar) / 0.305 / 0.305
                            model.kalanAdet = round(model.kalanAdet)
                    else:
                        
                        if model.birim == 'M2':
                            if model.en == 'ANT':
                                model.kalanAdet = float(model.kalanMiktar) / patternKasaMetreKaresi
                                model.kalanAdet = round(model.kalanAdet)
                                
                            elif model.boy == 'SET':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = float(model.kalanMiktar) /  0.07069
                                model.kalanAdet = round(model.kalanAdet)
                            elif model.en == 'SLAB' or model.boy == 'SLAB':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                            elif model.en == 'Free' or model.boy == 'Free' or model.boy == 'FREE' or model.en=='FR':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                            elif model.en == 'VAR' or model.boy == 'VAR':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                            elif model.en == 'Various' or model.boy == 'Various':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                            elif model.en == 'OZEL' or model.boy == 'OZEL' or model.en == 'Crazy' or model.boy=='Crazy' or model.boy=='Paver':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                            elif model.en == 'Mini':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                            else:
                                model.kalanAdet = float(model.kalanMiktar) / (self.formatDecimal(model.en) / 100) / (self.formatDecimal(model.boy) / 100)
                                model.kalanAdet = round(model.kalanAdet)
                        elif model.birim == 'Adet':
                            model.kalanAdet = model.miktar - model.uretimMiktari
                    if model.kalanMiktar > 0:
                        model.kalanBilgisi = 'Üretilmesi Gerekiyor'
                        model.kalanRenk = 'red'
                    elif model.kalanMiktar < 0:
                        model.kalanBilgisi = 'Kasa Eksiltilmesi Gerekiyor'
                        model.kalanRenk = 'yellow'
                    else:
                        model.kalanBilgisi='Üretim Tamamlanmıştır'
                        model.kalanRenk = 'green'
                        model.fontColor = 'white'
                else:
                    model.uretimMiktari = 0
                    model.kalanBilgisi = 'Hiç Üretilmemiş'
                    model.kalanRenk = 'black'
                    model.fontColor = 'white'
                    model.kalanMiktar = model.miktar - model.uretimMiktari
                    if model.birim == 'M2':
                        if model.boy == 'Free' or model.boy =='FREE' or model.en=='FR':
                            model.kalanMiktar = model.miktar
                            model.kalanAdet = 0
                        elif model.en == 'Various' or model.boy == 'Various':
                            model.kalanMiktar = model.miktar
                            model.kalanAdet = 0
                        elif model.en == 'ANT':
                            model.kalanMiktar = model.miktar
                            model.kalanAdet = float(model.kalanMiktar) / patternKasaMetreKaresi
                            model.kalanAdet = round(model.kalanAdet)
                        elif model.boy == 'SET':
                            model.kalanMiktar = model.miktar - model.uretimMiktari
                            model.kalanAdet = float(model.kalanMiktar) / 0.07069
                            model.kalanAdet = round(model.kalanAdet)
                        elif model.en == 'SLAB' or model.boy == 'SLAB':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                        elif model.en == 'Mini':
                            model.kalanMiktar = model.miktar - model.uretimMiktari
                            model.kalanAdet = 0
                        elif model.en == 'VAR' or model.boy == 'VAR':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                        elif model.en == 'OZEL' or model.boy == 'OZEL' or model.en == 'Crazy' or model.boy == 'Crazy' or model.boy=='Paver':
                                model.kalanMiktar = model.miktar - model.uretimMiktari
                                model.kalanAdet = 0
                        elif self.formatDecimal(model.en) <= 10:
                            if model.kategori == 'Travertine Mosaic' or model.kategori == 'Marble Mosaic':
                                model.kalanMiktar = model.miktar
                                model.kalanAdet = float(model.kalanMiktar) / 0.305 / 0.305
                                model.kalanAdet = round(model.kalanAdet)
                        else:
                            model.kalanMiktar = model.miktar
                            model.kalanAdet = float(model.kalanMiktar) / (self.formatDecimal(model.en) / 100) / (self.formatDecimal(model.boy) / 100)
                            model.kalanAdet = round(model.kalanAdet)
                    elif model.birim == 'Adet':
                        model.kalanAdet = model.kalanMiktar
                        
                if item.UretilenAdet != None:
                    model.uretimAdet = item.UretilenAdet
                else:
                    model.uretilenAdet = 0

                liste.append(model)
            schema = OrderSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getOrderProducts hata",str(e))
            return False
        
    def formatDecimal(self,value):
        value = value.replace(',','.')
        return float(value)
        
class MusteriBazindaUretim:
    
    def __init__(self):
        self.data = SqlConnect().data
        self.result = self.data.getList("""
                                            select            
                 m.ID as MusteriId,            
                 m.FirmaAdi as MusteriAdi,               
                 m.Marketing,
                (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId ) as Ulke,
          
 
                           
    (          
     Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo and s.SiparisDurumID=2 and s.MusteriID=m.ID and Year(s.SiparisTarihi)=Year(GetDate())          
          
    ) as BuYilUretim ,
	(          
     Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo and s.SiparisDurumID=2 and s.MusteriID=m.ID and Year(s.SiparisTarihi)=Year(GetDate())   - 1       
          
    ) as GecenYilUretim ,
	(          
     Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo and s.SiparisDurumID=2 and s.MusteriID=m.ID and Year(s.SiparisTarihi)=Year(GetDate())  -2        
          
    ) as OncekiYilUretim ,
	(          
     Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo and s.SiparisDurumID=2 and s.MusteriID=m.ID and Year(s.SiparisTarihi)=Year(GetDate()) -3         
          
    ) as OnDokuzYilUretim ,
	(          
     Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo and s.SiparisDurumID=2 and s.MusteriID=m.ID and Year(s.SiparisTarihi)=Year(GetDate()) -4        
          
    ) as OnSekizYilUretim 
                       
          
                     
          
            
                from            
                MusterilerTB m
                                           
                                           
                                           """)
        self.navlun = self.data.getList("""
                                            select            
                 m.ID as MusteriId,            
                 m.FirmaAdi as MusteriAdi,               
                 m.Marketing,
				 (select yu.UlkeAdi from YeniTeklif_UlkeTB yu where yu.Id = m.UlkeId ),
 
                 (
					select sum(s.NavlunSatis) from SiparislerTB s where s.SiparisDurumID=2 and s.MusteriID = m.ID 
				 ) + 
				 (
					select sum(s.DetayTutar_1) from SiparislerTB s where s.SiparisDurumID=2 and s.MusteriID = m.ID 
					
				 )+

				 (
					select sum(s.DetayTutar_2) from SiparislerTB s where s.SiparisDurumID=2 and s.MusteriID = m.ID 
					
				 )
				 +

				 (
					select sum(s.DetayTutar_3) from SiparislerTB s where s.SiparisDurumID=2 and s.MusteriID = m.ID 
					
				 )
				 +

				 (
					select sum(s.DetayTutar_4) from SiparislerTB s where s.SiparisDurumID=2 and s.MusteriID = m.ID 
					
				 )
                    as Digerleri
                       
          
                     
          
            
                from            
                MusterilerTB m

				order by Marketing
                                        
                                        
                                        """)
    def getMusteriBazindaUretim(self):
        liste= list()
        for item in self.result:
            if(item.BuYilUretim == None and item.GecenYilUretim == None and item.OncekiYilUretim == None and item.OnDokuzYilUretim == None):
                continue
            else:
                model = MusteriBazindaUretimModel()
                model.musteriAdi = item.MusteriAdi
                if(item.MusteriId == 37):
                    model.marketing = 'Imperial Homes'
                else:
                    model.marketing = item.Marketing
                model.ulkeAdi = item.Ulke
                model.satisToplamiBuYil =  item.BuYilUretim
                model.satisToplamiGecenYil = item.GecenYilUretim
                model.satisToplamiOncekiYil = item.OncekiYilUretim
                model.satisToplamiOnDokuzYil = item.OnDokuzYilUretim
                model.satisToplamiOnSekizYil = item.OnSekizYilUretim
                model.toplam  = self.__getNone(item.BuYilUretim) + self.__getNone(item.GecenYilUretim) + self.__getNone(item.OncekiYilUretim) + self.__getNone(item.OnDokuzYilUretim) + self.__getNone(item.OnSekizYilUretim)
                model.toplamCfr = self.__getNone(item.BuYilUretim) + self.__getNone(item.GecenYilUretim) + self.__getNone(item.OncekiYilUretim) + self.__getNone(item.OnDokuzYilUretim) + self.__getNone(item.OnSekizYilUretim) + self.__getNavlun(item.MusteriId)
                liste.append(model)
                
        schema = MusteriBazindaUretimSchema(many=True)
        return schema.dump(liste) 
        
    
    def __getNavlun(self,musteriId):
        for item in self.navlun:
            if item.MusteriId != musteriId:
                continue
            else:
                return self.__getNone(item.Digerleri)
    
            
    def __getNone(self,result):
        if(result == None):
            return 0
        else:
            return result   
  