from helpers import SqlConnect
from helpers import MailService
from models.siparisler_model.siparis_info import *
class SatisciInfo:
    def __init__(self):
        self.data = SqlConnect().data
        
    def getSiparisSatisciInfo(self):
        
        try:
            
            result = self.data.getList("""
                                            select 

                                                s.SiparisNo as Po,
                                                s.ID,
                                                s.SiparisSahibi as SatisciId,
                                                s.Operasyon as OperasyonId,
                                                (select k.KullaniciAdi from KullaniciTB k where k.ID = s.SiparisSahibi) as SiparisSahibi,
                                                (select k.KullaniciAdi from KullaniciTB k where k.ID = s.Operasyon) as Operasyon



                                            from SiparislerTB s
                                            where
                                                s.SiparisDurumID=2 and s.FaturaKesimTurID=1
                                            order by s.ID desc
                                       
                                       """)
            
            liste = list()
            for item in result:
                model = SatisciInfoModel()
                model.id = item.ID
                model.po = item.Po
                model.satisci_id = item.SatisciId
                model.satisci_adi = item.SiparisSahibi
                model.operasyon_id = item.OperasyonId
                model.operasyon_adi = item.Operasyon
                liste.append(model)
            schema = SatisciInfoSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getSiparisSatisciInfo hata',str(e))
            return False
        
    def getSiparisSatisciOzet(self):
        try:
            
            result = self.data.getList("""
                                            select 

 												count(s.Operasyon) as OpCount,
												(select k.KullaniciAdi from KullaniciTB k where k.ID = s.Operasyon) as OperasyonAdi



                                            from SiparislerTB s
                                            where
                                                s.SiparisDurumID=2 and s.FaturaKesimTurID=1
											group by s.Operasyon

                                       
                                       """)
            
            liste = list()
            for item in result:
                model = SatisciInfoOzetModel()
                model.ad = item.OperasyonAdi
                model.adet = item.OpCount
                liste.append(model)
            schema = SatisciInfoOzetSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getSiparisSatisciInfo hata',str(e))
            return False
        
    def getSiparisSahibiOzet(self):
        try:
            
            result = self.data.getList("""
                                            select 
 												count(s.SiparisSahibi) as SpCount,
												(select k.KullaniciAdi from KullaniciTB k where k.ID = s.SiparisSahibi) as SiparisciAdi
                                            from SiparislerTB s
                                            where
                                                s.SiparisDurumID=2 and s.FaturaKesimTurID=1
											group by s.SiparisSahibi
                                       """)
            
            liste = list()
            for item in result:
                model = SatisciInfoOzetModel()
                model.ad = item.SiparisciAdi
                model.adet = item.SpCount
                liste.append(model)
            schema = SatisciInfoOzetSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getSiparisSatisciInfo hata',str(e))
            return False
        
    def setSatisciInfo(self,po,ss,op):
        try:
            
            old = self.data.getStoreList("""
                                        select 
										
										
										s.SiparisSahibi,
										s.Operasyon,
										(select k.KullaniciAdi from KullaniciTB k where k.ID = s.SiparisSahibi) as SiparisSahibiAd,
										(select k.KullaniciAdi from KullaniciTB k where k.ID = s.Operasyon) as OperasyonAd

										
										
										from SiparislerTB s where s.SiparisNo=?
                                   """,(po))[0]
            
            if(old.SiparisSahibi != ss and old.Operasyon == op):
                self.data.update_insert("""
                                           update SiparislerTB SET SiparisSahibi=? where SiparisNo=? 
                                        """,(ss,po))
                mail = self.data.getStoreList("""
                                        select MailAdres,KullaniciAdi from KullaniciTB where ID=?
                                   """,(ss))[0]
                
                MailService(po + ' ya ait satışçı değişti.',mail.MailAdres, po + ' ya ait satışçı ' + old.SiparisSahibiAd + ' => ' + mail.KullaniciAdi + ' devredilmiştir.')
            elif (old.SiparisSahibi == ss and old.Operasyon != op):
                self.data.update_insert("""
                                           update SiparislerTB SET Operasyon=? where SiparisNo=? 
                                        """,(op,po))
                mail = self.data.getStoreList("""
                                        select MailAdres,KullaniciAdi from KullaniciTB where ID=?
                                   """,(op))[0]
                
                MailService(po + ' ya ait satışçı değişti.',mail.MailAdres, po + ' ya ait operasyoncu ' + old.OperasyonAd + ' => ' + mail.KullaniciAdi + ' devredilmiştir.')
            
            elif (old.SiparisSahibi != ss and old.Operasyon != op):
                self.data.update_insert("""
                                           update SiparislerTB SET SiparisSahibi=? , Operasyon=? where SiparisNo=? 
                                        """,(ss,op,po))
                siparisSahibiMail = self.data.getStoreList("""
                                        select MailAdres,KullaniciAdi from KullaniciTB where ID=?
                                   """,(ss))[0]
                operasyonMail = self.data.getStoreList("""
                                        select MailAdres,KullaniciAdi from KullaniciTB where ID=?
                                   """,(op))[0]
                
                MailService(po + ' ya ait satışçı değişti.',siparisSahibiMail.MailAdres, po + ' ya ait satışçı ' + old.SiparisSahibiAd + ' => ' + siparisSahibiMail.KullaniciAdi + ' devredilmiştir.')
                MailService(po + ' ya ait satışçı değişti.',operasyonMail.MailAdres, po + ' ya ait operasyoncu ' + old.OperasyonAd + ' => ' + operasyonMail.KullaniciAdi + ' devredilmiştir.')
                
            
            
            return True
        except Exception as e:
            return False