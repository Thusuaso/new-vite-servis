from helpers import SqlConnect,TarihIslemler
from models.satisci.satismusteri import *
import datetime
from datetime import date
from resource_api.customers.customersList import MusteriListem
from resource_api.customers.customersAyrinti import SatisciAyrinti
class SatisciIslem:

    def __init__(self): 

        self.data = SqlConnect().data

    def getSatisciList(self,musteriadi,id):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
          select k.KullaniciAdi,
                a.ID,
                a.MusteriAdi,
                a.Satisci_Cloud,
                a.Satisci_Cloud_Dosya,
                a.Aciklama,
                a.Baslik,
                a.Hatirlatma_Notu,
                a.Hatirlatma_Tarih,
                a.Tarih
       from SatisciAyrintiTB a , KullaniciTB k where k.ID = a.Temsilci and
        a.MusteriAdi = ? and a.ID = ?
            """,(musteriadi,id)
        )

        liste = list()

        for item in result:

            model = MusteriIslemModel()
            model.id = item.ID
            model.musteriadi = item.MusteriAdi
            model.satisci_cloud = item.Satisci_Cloud
            model.satisci_cloud_dosya = item.Satisci_Cloud_Dosya
            model.aciklama = item.Aciklama
            model.baslik = item.Baslik
            model.hatirlatma_notu = item.Hatirlatma_Notu
            model.hatirlatmaTarihi = tarihIslem.getDate(item.Hatirlatma_Tarih).strftime("%d-%m-%Y")
            model.tarih_giris = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
         
            liste.append(model)

        schema = MusteriIslemSchema(many=True)

        return schema.dump(liste)

    def getSatisciModel(self,musteriadi,id):

        model = MusteriIslemModel()
        model.musteriadi = musteriadi
        model.id = id
       

        schema = MusteriIslemSchema()

        return schema.dump(model)

    def getYeniSatisciModel(self):
        tarihIslem = TarihIslemler()
        model = MusteriIslemModel()
       
        model.tarih_giris =    tarihIslem.getDate( date.today()).strftime("%d-%m-%Y")    
        model.hatirlatmaTarihi = tarihIslem.getDate( date.today()).strftime("%d-%m-%Y")    
       
        schema = MusteriIslemSchema()
       
        return schema.dump(model)

    def satisciDosyaKaydet(self,item):
       
        try:
            self.data.update_insert(
                """
                update SatisciAyrintiTB set Satisci_Cloud=?,Satisci_Cloud_Dosya=? where Id=?
                """,
                (
                    item['satisci_cloud'],item['satisci_cloud_dosya'],item['id']
                )
            )
            return True
        except Exception as e:
            
            return False    
       
    def satisciKaydet(self,item):
        try:

            self.data.update_insert(
                """
                insert into SatisciAyrintiTB (
                    MusteriAdi,Aciklama,Baslik,
                    Tarih,Satisci_Cloud,Satisci_Cloud_Dosya,Hatirlatma_Tarih,Hatirlatma_Notu,Temsilci
                )
                values
                (?,?,?,?,?,?,?,?,?)
                """,
                (
                    item['musteriadi'],item['aciklama'],item['baslik'],
                    item['tarih_giris'],0,"",item['hatirlatmaTarihi'],item['hatirlatma_notu'],int(item['temsilci'])
                )
            )
            
            islem = MusteriListem()
            result = islem.getMusteriListesi(int(item['temsilci']))
            islem2 = SatisciAyrinti()
            result2 = islem2.getAyrintiList(item['musteriadi'])
            data={
                'status':True,
                'result':result,
                'result2':result2
            }
            
           
            return data
        except Exception as e:
            print('satisciKaydet Hata : ',str(e))
            return False

    def satisciGuncelle(self,item):
        
        try:

            self.data.update_insert(

                """
                update SatisciAyrintiTB set MusteriAdi=?,Aciklama=?,
                Baslik=?,Tarih=?,Satisci_Cloud=?,Satisci_Cloud_Dosya=?,Hatirlatma_Tarih=?,Hatirlatma_Notu=?,Temsilci=?
                where ID=?
                """,(
                    item['musteriadi'],item['aciklama'],item['baslik'],
                    item['tarih_giris'],item['satisci_cloud'],item['satisci_cloud_dosya'],item['hatirlatmaTarihi'],item['hatirlatma_notu'],item['temsilci'],item['id']
                )
            )
            # temsilci = self.data.getStoreList("""
            #                                     select ID from KullaniciTB where KullaniciAdi=?
                                              
            #                                   """,(item['temsilci']))
            
            # islem = MusteriListem()
            # result = islem.getMusteriListesi(temsilci[0][0])
            # islem2 = SatisciAyrinti()
            # result2 = islem2.getAyrintiList(item['musteriadi'])
            data={
                'status':True,
                # 'result':result,
                # 'result2':result2
            }

            return data
        except Exception as e:
            print('satisciGuncelle Hata : ',str(e))
            return False

    def satisciSilme(self,id):
        try:
            # satisci = self.data.getStoreList(

            #     """
            #     select MusteriAdi,Temsilci from SatisciAyrintiTB where ID=?
            #     """,(id)
            # )
            # musteriAdi = satisci[0][0]
            # temsilci = satisci[0][1]
            
            self.data.update_insert(
                """
                delete from SatisciAyrintiTB where ID=?
                """,(id)
            )
            # islem = MusteriListem()
            # result = islem.getMusteriListesi(temsilci)
            # islem2 = SatisciAyrinti()
            # result2 = islem2.getAyrintiList(musteriAdi)
            data={
                'status':True,
                # 'result':result,
                # 'result2':result2
            }
            
            
            return data
        except Exception as e:
            print('satisci Silme Hata : ',str(e))
            return False

    def getHatirlatmaList(self,kullanici_id):
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select 
	                s.Baslik,s.Hatirlatma_Tarih,s.Hatirlatma_Notu,s.Tarih,s.MusteriAdi,
					(select m.ID from MusterilerTB m where m.FirmaAdi = s.MusteriAdi) as MusteriID


            from 
                SatisciAyrintiTB s
                
            where 

                s.Temsilci=?	and
                YEAR(s.Hatirlatma_Tarih) = YEAR(GETDATE()) and
                MONTH(s.Hatirlatma_Tarih) = MONTH(GETDATE()) and
                DAY(s.Hatirlatma_Tarih) >= DAY(GETDATE()) and
				s.Tarih <= GETDATE()
            """,(kullanici_id)
        )

        liste = list()

        for item in result:

            model = MusteriIslemModel()
            model.id = item.MusteriID
            model.baslik = item.Baslik
            model.hatirlatma_notu = item.Hatirlatma_Notu
            model.hatirlatmaTarihi = tarihIslem.getDate(item.Hatirlatma_Tarih).strftime("%d-%m-%Y")
            model.musteriadi = item.MusteriAdi
            liste.append(model)

        schema = MusteriIslemSchema(many=True)

        return schema.dump(liste)

    
    def setPriority(self,customer,priority):
        try:
            satisci = self.data.getStoreList("""
                                            select MusteriTemsilciId from MusterilerTB where FirmaAdi=?
                                        
                                        """,(customer))
            customerID=0
            if len(satisci)>0:
                self.data.update_insert("""
                                        
                                        update MusterilerTB SET MusteriOncelik=? WHERE FirmaAdi=?
                                    
                                    """,(priority,customer))
                satisci = self.data.getStoreList("""
                                            select MusteriTemsilciId from MusterilerTB where FirmaAdi=?
                                        
                                        """,(customer))
                customerID = satisci[0][0]
                
            else:
                result = self.data.getStoreList("""
                                        select Id from YeniTeklif_MusterilerTB where MusteriAdi=?
                                       
                                       """,(customer))
                
                self.data.update_insert("""
                                            update YeniTeklifTB SET TeklifOncelik=? WHERE MusteriId=?
                                        
                                        """,(priority,result[0][0]))
                customer = self.data.getStoreList("""
                                                  
                                                    select KullaniciId from YeniTeklifTB where MusteriId=?
                                                  
                                                  """,(result[0][0]))
                customerID = customer[0][0]
                
            
            
            
            
            islem = MusteriListem()
            result = islem.getMusteriListesi(customerID)
            
            
            return True,result
        except Exception as e:
            print('setPriority hata',str(e))
            return False
        
    def setFollowing(self,customer,follow):
        try:
            result = self.data.getStoreList("""
                                                select * from MusterilerTB where FirmaAdi=?
                                            
                                            """,(customer))
            customerID=0
            
            if len(result)>0:
                
                self.data.update_insert("""
                                            
                                            update MusterilerTB SET Takip=? WHERE FirmaAdi=?
                                        
                                        """,(follow,customer))
                
                satisci = self.data.getStoreList("""
                                                select MusteriTemsilciId from MusterilerTB where FirmaAdi=?
                                            
                                            """,(customer))
                customerID = satisci[0][0]
            else:
                result = self.data.getStoreList("""
                                        select Id from YeniTeklif_MusterilerTB where MusteriAdi=?
                                       
                                       """,(customer))
                
                self.data.update_insert("""
                                            update YeniTeklifTB SET TakipEt=0 WHERE MusteriId=?
                                        
                                        """,(result[0][0]))
                customer = self.data.getStoreList("""
                                                  
                                                    select KullaniciId from YeniTeklifTB where MusteriId=?
                                                  
                                                  """,(result[0][0]))
                customerID = customer[0][0]
                
            # islem = MusteriListem()
            # result = islem.getMusteriListesi(customerID)
            
            
            return True
        except Exception as e:
            print('setFollowing hata',str(e))
            return False
        
    def getChangeRepresentative(self,customer,representative):
        try:
            self.data.update_insert("""

                                        update MusterilerTB SET MusteriTemsilciId=? WHERE FirmaAdi=?
                                   
                                   """,(representative,customer))
            islem = MusteriListem()
            result = islem.getMusteriListesi(representative)
            return True,result
        except Exception as e:
            print('getChangeRepresentative hata',str(e))
            return False