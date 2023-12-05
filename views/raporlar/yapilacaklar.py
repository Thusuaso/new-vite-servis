from helpers import SqlConnect 
from models.raporlar.yapilacaklar import *
class Yapilacaklar:
    def __init__(self):
        self.sql = SqlConnect().data
    
    def getYapilacaklarYapildiList(self):
        try:
            yapildiList = self.sql.getList("""
                                            select 
                                                y.GirisTarihi,
                                                y.YapildiTarihi,
                                                y.GorevVerenAdi,
                                                y.GorevSahibiAdi,
                                                y.Yapilacak,
                                                y.YapilacakOncelik,
                                                y.Acil
                                            from Yapilacaklar y where y.Yapildi=1
                                            order by y.GirisTarihi desc
                                        """)
            liste = list()
            for item in yapildiList:
                model = YapilacaklarModel()
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.gorev_veren_adi = item.GorevVerenAdi
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.yapilacak = item.Yapilacak
                model.oncelik = item.YapilacakOncelik
                model.aciliyet = item.Acil
                liste.append(model)
            schema = YapilacaklarSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarYapildiList hata',str(e))
            return False
        
    def getYapilacaklarYapilacakList(self):
        try:
            yapilacakList = self.sql.getList("""
                                            select 
                                                y.GirisTarihi,
                                                y.GorevVerenAdi,
                                                y.GorevSahibiAdi,
                                                y.Yapilacak,
                                                y.YapilacakOncelik,
                                                y.Acil
                                            from Yapilacaklar y where y.Yapildi=0
                                            order by y.GirisTarihi desc

                                        """)
            liste = list()
            for item in yapilacakList:
                model = YapilacaklarModel()
                model.girisTarihi = item.GirisTarihi
                model.gorev_veren_adi = item.GorevVerenAdi
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.yapilacak = item.Yapilacak
                model.oncelik = item.YapilacakOncelik
                model.aciliyet = item.Acil
                liste.append(model)
            schema = YapilacaklarSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarYapilacakList hata',str(e))
            return False
    
    def getYapilacaklarKullaniciYapildiList(self,userId):
        try:
            data = self.sql.getStoreList("""
                                             select 
                                                ID,
                                                GorevSahibiAdi,
                                                GorevSahibiId,
                                                Yapilacak,
                                                Yapildi,
                                                GorevVerenID,
                                                GorevVerenAdi,
                                                GirisTarihi,
                                                YapildiTarihi,
                                                YapilacakOncelik,
                                                Acil

                                            from Yapilacaklar

                                            where OrtakGorev LIKE '%' + ? + '%' and Yapildi=1
                                            order by
												YapilacakOncelik 
                                        """,(userId))
            liste = list()
            for item in data:
                model = YapilacaklarModel()
                model.id = item.ID
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.gorev_sahibi_id = item.GorevSahibiId
                model.yapilacak = item.Yapilacak
                model.gorev_veren_id = item.GorevVerenID
                model.gorev_veren_adi = item.GorevVerenAdi
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.oncelik = item.YapilacakOncelik
                model.userStatus = False
                model.aciliyet = item.Acil
                liste.append(model)
            schema = YapilacaklarSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarYapilmadiList hata',str(e))
            return False 
    
    def getYapilacaklarKullaniciYapilmadiList(self,userId):
        try:
            data = self.sql.getStoreList("""
                                             select 
                                                ID,
                                                GorevSahibiAdi,
                                                GorevSahibiId,
                                                Yapilacak,
                                                Yapildi,
                                                GorevVerenID,
                                                GorevVerenAdi,
                                                GirisTarihi,
                                                YapildiTarihi,
                                                YapilacakOncelik,
                                                Acil
                                            from Yapilacaklar

                                            where OrtakGorev LIKE '%' + ? + '%' and Yapildi=0
                                            order by
												YapilacakOncelik 
                                        """,(userId))
            liste = list()
            for item in data:
                model = YapilacaklarModel()
                model.id = item.ID
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.gorev_sahibi_id = item.GorevSahibiId
                model.yapilacak = item.Yapilacak
                model.gorev_veren_id = item.GorevVerenID
                model.gorev_veren_adi = item.GorevVerenAdi
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.oncelik = item.YapilacakOncelik
                model.userStatus = False
                model.aciliyet = item.Acil
                
                liste.append(model)
            schema = YapilacaklarSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarYapilmadiList hata',str(e))
            return False
    
    
    def getYapilacaklarModel(self):
        
        model = YapilacaklarModel()
        schema = YapilacaklarSchema()
        return schema.dump(model)
    
    def getYapilacaklarKullaniciList(self):
        try:
            data = self.sql.getList("""
                                select ID,KullaniciAdi,MailAdres from KullaniciTB where Aktif=1 and Satisci=1 and VersiyonDegisim=1
                             """)
            liste = list()
            for item in data:
                if(item.ID == 44 or item.ID == 19 or item.ID == 47 or item.ID == 10):
                    model = YapilacaklarKullanicilarModel()
                    model.id = item.ID
                    model.username = item.KullaniciAdi
                    model.email = item.MailAdres
                    liste.append(model)
            schema = YapilacaklarKullanicilarSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarKullaniciList hata',str(e))
            return False
    def getYapilacaklarDetay(self,id):
        try:
            result = self.sql.getStoreList("""
                                            select * from Yapilacaklar where ID=?

                                           """,(id))
            liste = list()
            for item in result:
                model = YapilacaklarModel()
                model.id = item.ID
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.gorev_sahibi_id = item.GorevSahibiId
                model.yapilacak = item.Yapilacak
                model.oncelik = item.YapilacakOncelik
                model.aciliyet = item.Acil
                model.ortak_gorev = item.OrtakGorev
                liste.append(model)
            schema = YapilacaklarSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarDetay hata',str(e))
            return False

    def save(self,data):
        try:
            sira = 0
            if data['gorev_veren_id'] == '10':
                sira = self.sql.getStoreList("""
                                                select top 1 Sira + 1 as Sira from Yapilacaklar y where y.GorevVerenID=? and y.Yapildi=0 order by Sira desc
                                             """,(data['gorev_veren_id']))[0][0]
            else:
                sira = 0
                
                
            self.sql.update_insert("""
                                        insert into Yapilacaklar
                                        (
                                        Yapilacak,
                                        Yapildi,
                                        GorevVerenAdi,
                                        GorevVerenID,
                                        GirisTarihi,
                                        YapilacakOncelik,
                                        Acil,
                                        OrtakGorev,
                                        Sira,
                                        Goruldu
                                        ) VALUES(?,?,?,?,?,?,?,?,?,?)

                                    """,(
  
                                            data['yapilacak'],
                                            data['yapildi'],
                                            data['gorev_veren_adi'],
                                            data['gorev_veren_id'],
                                            data['girisTarihi'],
                                            data['oncelik'],
                                            data['aciliyet'],
                                            data['ortak_gorev'],
                                            sira,
                                            0
                                        )
                                   )
            return True
        except Exception as e:
            print('yapilacaklar save hata',str(e))
            return False
    def delete(self,id):
        try:
            self.sql.update_insert("""
                                    delete Yapilacaklar WHERE ID=?
                                  
                                  """,(id))
            return True
        except Exception as e:
            print('Yapilacaklar delete hata',str(e))
            return False
    def changeStatus(self,data):
        try:
            self.sql.update_insert("""
                                    update Yapilacaklar SET Yapildi=?,YapildiTarihi=? where ID=?
                                   """,(data['status'],data['yapildiTarihi'],data['id']))
            return True
        except Exception as e:
            print('durum değiştir hata',str(e))
            return False    
    def update(self,data):
        try:
            self.sql.update_insert("""
                                    update Yapilacaklar SET Yapilacak=?,YapilacakOncelik=?,Acil=?,OrtakGorev=? where ID=? 
                                """,(data['yapilacak'],data['oncelik'],data['aciliyet'],data['ortak_gorev'],data['id']))
            return True
        except Exception as e:
            print('yapilacaklar update hata',str(e))
            return False
        
    def getYapilacaklarYapilmadiListAllA(self):
        try:
            data = self.sql.getList("""
                                            select 
                                                ID,
                                                GorevSahibiAdi,
                                                GorevSahibiId,
                                                Yapilacak,
                                                Yapildi,
                                                GorevVerenID,
                                                GorevVerenAdi,
                                                GirisTarihi,
                                                YapildiTarihi,
                                                YapilacakOncelik,
                                                Acil,
                                                OrtakGorev

                                            from Yapilacaklar

                                            where Yapildi=0 and YapilacakOncelik in ('A','B')
                                            order by
												GirisTarihi desc
                                        """)
            listA = list()
            for item in data:
                model = YapilacaklarModel()
                model.id = item.ID
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.gorev_sahibi_id = item.GorevSahibiId
                model.yapilacak = item.Yapilacak
                model.gorev_veren_id = item.GorevVerenID
                model.gorev_veren_adi = item.GorevVerenAdi
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.oncelik = item.YapilacakOncelik
                model.userStatus = False
                model.aciliyet = item.Acil
                model.ortak_gorev  = item.OrtakGorev
                listA.append(model)

            schema = YapilacaklarSchema(many = True)
            return schema.dump(listA)

            
            
        except Exception as e:
            print('getYapilacaklarYapilmadiList hata',str(e))
            return False     
        
        
    # def getYapilacaklarYapilmadiListAllB(self):
    #     try:
    #         data = self.sql.getList("""
    #                                         select 
    #                                             ID,
    #                                             GorevSahibiAdi,
    #                                             GorevSahibiId,
    #                                             Yapilacak,
    #                                             Yapildi,
    #                                             GorevVerenID,
    #                                             GorevVerenAdi,
    #                                             GirisTarihi,
    #                                             YapildiTarihi,
    #                                             YapilacakOncelik,
    #                                             Acil,
    #                                             OrtakGorev

    #                                         from Yapilacaklar

    #                                         where Yapildi=0 and YapilacakOncelik='B'
    #                                         order by
	# 											GirisTarihi desc
    #                                     """)
    #         listB = list()
    #         for item in data:
    #             model = YapilacaklarModel()
    #             model.id = item.ID
    #             model.gorev_sahibi_adi = item.GorevSahibiAdi
    #             model.gorev_sahibi_id = item.GorevSahibiId
    #             model.yapilacak = item.Yapilacak
    #             model.gorev_veren_id = item.GorevVerenID
    #             model.gorev_veren_adi = item.GorevVerenAdi
    #             model.girisTarihi = item.GirisTarihi
    #             model.yapildiTarihi = item.YapildiTarihi
    #             model.oncelik = item.YapilacakOncelik
    #             model.userStatus = False
    #             model.aciliyet = item.Acil
    #             model.ortak_gorev  = item.OrtakGorev
                
    #             listB.append(model)

    #         schema = YapilacaklarSchema(many = True)
    #         return schema.dump(listB)

            
            
    #     except Exception as e:
    #         print('getYapilacaklarYapilmadiList hata',str(e))
    #         return False
        
    def getYapilacaklarYapilmadiListAllC(self):
        try:
            data = self.sql.getList("""
                                            select 
                                                ID,
                                                GorevSahibiAdi,
                                                GorevSahibiId,
                                                Yapilacak,
                                                Yapildi,
                                                GorevVerenID,
                                                GorevVerenAdi,
                                                GirisTarihi,
                                                YapildiTarihi,
                                                YapilacakOncelik,
                                                Acil,
                                                OrtakGorev

                                            from Yapilacaklar

                                            where Yapildi=0 and YapilacakOncelik='C'
                                            order by
												GirisTarihi desc
                                        """)
            listC = list()
            for item in data:
                model = YapilacaklarModel()
                model.id = item.ID
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.gorev_sahibi_id = item.GorevSahibiId
                model.yapilacak = item.Yapilacak
                model.gorev_veren_id = item.GorevVerenID
                model.gorev_veren_adi = item.GorevVerenAdi
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.oncelik = item.YapilacakOncelik
                model.userStatus = False
                model.aciliyet = item.Acil
                model.ortak_gorev  = item.OrtakGorev
                
                listC.append(model)

            schema = YapilacaklarSchema(many = True)
            return schema.dump(listC)

            
            
        except Exception as e:
            print('getYapilacaklarYapilmadiList hata',str(e))
            return False  
        
                  
    def getYapilacaklarYapildiListAll(self):
        try:
            data = self.sql.getList("""
                                            select 
                                                ID,
                                                GorevSahibiAdi,
                                                GorevSahibiId,
                                                Yapilacak,
                                                Yapildi,
                                                GorevVerenID,
                                                GorevVerenAdi,
                                                GirisTarihi,
                                                YapildiTarihi,
                                                YapilacakOncelik,
                                                Acil,
                                                OrtakGorev

                                            from Yapilacaklar

                                            where Yapildi=1
                                            order by
												GirisTarihi  desc
                                        """)
            liste = list()
            for item in data:
                model = YapilacaklarModel()
                model.id = item.ID
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.gorev_sahibi_id = item.GorevSahibiId
                model.yapilacak = item.Yapilacak
                model.gorev_veren_id = item.GorevVerenID
                model.gorev_veren_adi = item.GorevVerenAdi
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.oncelik = item.YapilacakOncelik
                model.userStatus = False
                model.aciliyet = item.Acil
                model.ortak_gorev  = item.OrtakGorev
                
                liste.append(model)
            schema = YapilacaklarSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarYapilmadiList hata',str(e))
            return False 
    
    def getYapilacaklarAnaList(self,id):
        try:
            results = self.sql.getStoreList("""
                                                select * from Yapilacaklar y where y.GorevVerenID=? and y.Yapildi=0  and y.Goruldu = 0 order by Sira 


                                            """,(id))
            liste = list()
            for item in results:
                model = YapilacaklarModel()
                model.id = item.ID
                model.girisTarihi = item.GirisTarihi
                model.yapildiTarihi = item.YapildiTarihi
                model.gorev_veren_adi = item.GorevVerenAdi
                model.gorev_sahibi_adi = item.GorevSahibiAdi
                model.yapilacak = item.Yapilacak
                model.oncelik = item.YapilacakOncelik
                model.aciliyet = item.Acil
                model.ortak_gorev = item.OrtakGorev
                model.sira = item.Sira
                liste.append(model)
            schema = YapilacaklarSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print('getYapilacaklarAnaList hata',str(e))
            return False

    def setYapilacaklarAnaListSiraDegistir(self,data):
        try:
            for item in data:
                self.sql.update_insert("""
                                            update Yapilacaklar SET Sira=? where ID=?
                                       """,(item['sira'],item['id']))
            return True
        except Exception as e:
            print('setYapilacaklarAnaListSiraDegistir hata',str(e))
            return False
        
    def setYapilacaklarGorulduDegistir(self,id):
        try:
            self.sql.update_insert("""
                                        Update Yapilacaklar SET Goruldu=1 WHERE ID=?
                                   """,(id))
            return True
        except Exception as e:
            print('',str(e))
            return False