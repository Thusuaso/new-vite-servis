from helpers import SqlConnect
from models.raporlar.maliyet import *
class MaliyetHatalari:
    def __init__(self):
        self.sql = SqlConnect().data
        
    def getList(self):
        try:
            result = self.sql.getList("""
                                        select * from MaliyetHatalariTB
                                       """)
            liste = list()
            for item in result:
                model = MaliyetHatalarModel()
                model.id = item.ID
                model.hata = item.Hata
                model.maliyet = item.Maliyet
                model.kullanici_adi = item.KullaniciAdi
                model.kullanici_id = item.KullaniciId
                model.tarih = item.Tarih
                liste.append(model)
            schema = MaliyetHatalarSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getMaliyetHatalariListe hata',str(e))
            return False
        
    def getModel(self):
        model = MaliyetHatalarModel()
        schema = MaliyetHatalarSchema()
        return schema.dump(model)
    
    def save(self,data):
        try:
            self.sql.update_insert("""
                                        insert into MaliyetHatalariTB(Hata) VALUES(?)
                                    """,(data['hata']))
            return True
                
        except Exception as e:
            print('Maliyet Save Hata',str(e))
            return False
        
    def update(self,data):
        try:
            self.sql.update_insert("""
                                        update MaliyetHatalariTB SET Hata=? WHERE ID=?
                                    """,(data['hata'],data['id']))
            return True
        except Exception as e:
            print('Maliyet Update Hata',str(e))
            return False

    def delete(self,id):
        try:
            self.sql.update_insert("""
                                        delete MaliyetHatalariTB WHERe ID=?
                                    """,(id))
            return True
        except Exception as e:
            print('MaliyetHatalari delete',str(e))
            return False
        
    def detail(self,id):
        try:
            result = self.sql.getStoreList("""
                                            select * from MaliyetHatalariTB where ID=?
                                           """,(id))
            liste = list()
            for item in result:
                model = MaliyetHatalarModel()
                model.id = item.ID
                model.tarih = item.Tarih
                model.hata = item.Hata
                model.maliyet = item.Maliyet
                model.kullanici_id = item.KullaniciId
                model.kullanici_adi = item.KullaniciAdi
                liste.append(model)
            schema = MaliyetHatalarSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('maliye hata detay',str(e))
            return False
        
    def users(self):
        try:
            result = self.sql.getList("""
                                            select * from KullaniciTB where Aktif=1 and Satisci=1
                                      """)
            
            liste = list()
            for item in result:
                if item.ID == 9:
                    continue
                else:
                    model = MaliyetKullaniciModel()
                    model.id = item.ID
                    model.name = item.KullaniciAdi
                    liste.append(model)
            schema = MaliyetKullaniciSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('maliye hata users',str(e))
            return False