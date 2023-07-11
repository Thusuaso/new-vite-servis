from helpers import SqlConnect
from models.tedarikci_model import TedarikciListeSchema,TedarikciListeModel
import datetime
from views.listeler.tedarikci import Tedarikci
from views.siparisler.listeler.siparisListe import *

class TedarikciIslem:

    def __init__(self):

        self.data = SqlConnect().data

    
    def getTedarikciList(self):

        result = self.data.getList(

            """
            select 
            t.ID,
            t.FirmaAdi,
            (
            select count(*) from SiparisUrunTB s where s.TedarikciID=t.ID
            ) as SiparisSayisi
            from TedarikciTB t
            """
        )

        liste = list()

        for item in result:

            model = TedarikciListeModel()
            model.id = item.ID
            model.tedarikciadi = item.FirmaAdi
            model.siparis_sayisi = item.SiparisSayisi

            liste.append(model)

        schema = TedarikciListeSchema(many=True)

        return schema.dump(liste)
            
    def getTedarikciModel(self):

        model = TedarikciListeModel()

        schema = TedarikciListeSchema()

        return schema.dump(model)

    def tedarikciKaydet(self,item):

        try:
            print("tedarikciKaydet",item['tedarikciadi'])
            self.data.update_insert(
                """
                insert into TedarikciTB (FirmaAdi)
                values
                (?)
                """,(item['tedarikciadi'])
            )
            return True
        except Exception as e:
            print('TedarikciIslem tedarikciKaydet Hata : ',str(e))
            return False

    def tedarikciGuncelle(self,item):

        try:
            self.data.update_insert(
                """
                update TedarikciTB set FirmaAdi=? where ID=?
                """,(
                    item['tedarikciadi'],item['id']
                )
            )

            return True
        except Exception as e:
            print('TedarikciIslem tedarikciGuncelle Hata : ',str(e))
            return False

    def tedarikciSilme(self,id):
        try:
            if self.__tedarikciKontrol(id) == True:
                self.data.update_insert(
                    """
                    delete from TedarikciTB where ID=?
                    """,(id)
                )
                return True
            return False
        except Exception as e:
            print('TedarikciIslem tedarikciSilme Hata : ',str(e))
            return False

    def __tedarikciKontrol(self,id):

        kontrol = False

        siparis_kontrol = self.data.getStoreList(
            """
            select count(*) as durum from SiparisUrunTB where TedarikciID=?
            """,(id)
        )[0].durum

        uretim_kontrol = self.data.getStoreList(
            """
            select count(*) as durum from UretimTB where TedarikciID=?
            """,(id)
        )[0].durum

        if uretim_kontrol <= 0 and siparis_kontrol <= 0:
            kontrol = True

        return kontrol

    def IcSiparisDosyaKaydet(self,item):
        
        date = datetime.datetime.now()
        
        urunID = self.__evrakId(item)
        try:
            self.data.update_insert(
                """
                INSERT INTO SiparisFaturaKayitTB (
                    Tarih,
                    FaturaKayitID,
                    SiparisFaturaTurID, 
                    SiparisNo,
                    Tutar,
                   
                    YuklemeEvrakID,
                    YeniEvrakID,
                    YuklemeEvrakDurumID,
                    EvrakYuklemeTarihi,
                    EvrakAdi,KullaniciID ,Evrak_Kontrol
                    )   
                     values
                    (?,?,?, ?,?,?,?,?,?,?,?,?)
                """,(date,0,0,item['siparisno'],0,3,urunID,2,date, item['evrak'],item['kullaniciId'],1)
            )
          
            return True
        except Exception as e:
            print('IcSiparisDosyaKaydet Hata : ',e)
            return False   
    
    def setIcSiparisFormSil(self,tedarikciId,siparisNo):
        try:
            tedarikciAdi = self.data.getStoreList("""
                                                    select FirmaAdi from TedarikciTB where ID=?
                                                  """,(tedarikciId))
            tedarikciAdi = tedarikciAdi[0][0]
            
            evrakAdi = self.data.getStoreList("""
                                                select EvrakAdi,ID from SiparisFaturaKayitTB where SiparisNo=?
                                              """,(siparisNo))

            
            for item in evrakAdi:
                evrakAdi = item.EvrakAdi
                evrakAdi = evrakAdi.split('-')[0]
                if(tedarikciAdi.strip() == evrakAdi.strip()):
                    
                    self.data.update_insert("""
                                                delete SiparisFaturaKayitTB where ID=?
                                           """,(item.ID))
                    
                    
            
            result = self.data.getStoreList("""
                                        select * from SiparisUrunTedarikciFormTB where TedarikciID=? and SiparisNo=?
                                   """,(tedarikciId,siparisNo))
            if len(result)>0:
                self.data.update_insert("""
                                            delete SiparisUrunTedarikciFormTB where TedarikciID=? and SiparisNo=?
                                
                                    """,(tedarikciId,siparisNo))
                
            
                

                
                return True
        
        except Exception as e:
            print('setIcSiparisFormSil hata',str(e))
            return False
    
    def IcSiparisFormSilKontrol(self,tedarikciId,siparisNo):
        result = self.data.getStoreList("""
                                        select * from SiparisUrunTedarikciFormTB where TedarikciID=? and SiparisNo=?
                                   """,(tedarikciId,siparisNo))
        if (len(result)>0):
            return True
        else:
            return False
    
    def getIsfControl(self,evrakAdi):

        self.data.update_insert("""
                                    delete SiparisFaturaKayitTB where YuklemeEvrakID=3 and EvrakAdi=?
                                
                                """,(evrakAdi))
        evrakAdiS = evrakAdi.split('-')
        tedarikciAdi = evrakAdiS[0]
        siparisNo = evrakAdiS[1].split('.')[0]
        tedarikciId = self.data.getStoreList("""
                                    select ID from TedarikciTB where FirmaAdi=?
                                
                                """,(tedarikciAdi))[0].ID
        self.data.update_insert("""
                                    delete SiparisUrunTedarikciFormTB where TedarikciID =? and SiparisNo=?
                                
                                """,(tedarikciId,siparisNo))
        return True
    
    
    def __evrakId(self,item):

        try:
            
         
            harf = ["A", "B", "C", "Ç" ,"D" ,"E", "F", "G", "Ğ", "H", "İ", "I", "J" ,"K" ,"L", "M", "N", "O", "Ö", "P", "R", "S", "Ş", "T" ,"U", "Ü", "V", "Y", "Z"]
            kontrol = self.data.getStoreList("Select count(*) as durum from YeniIcSiparisFaturaTB where SiparisNo=?",item['siparisno'])[0].durum 
            
            if kontrol == 0:
                id = "3"+harf[kontrol]
            else : 
                id = "3"+harf[kontrol] 
            self.data.update_insert(
                """
                INSERT INTO YeniIcSiparisFaturaTB (EvrakID, SiparisNo, EvrakAdi)    values
                (?,?,?)
                """,( id ,item['siparisno'],item['evrak'])
            )
            

            return id
        except Exception as e:
            print('__evrakId Hata : ',str(e))
            return False   

    def __urunId(self,item):
        
        kontrol = self.data.getStoreList("select count(*) as durum from YeniIcSiparisFaturaTB where EvrakAdi=?",item['evrak'])[0].durum
       
        urunId = None 
        if kontrol > 0:
            urunId = self.data.getStoreList("Select ID from YeniIcSiparisFaturaTB where  EvrakAdi=?",item['evrak'])[0].ID 
           
           
           
          
        else:
           
         print('urun id çalıştı')

        return urunId        