from models import *
from helpers import SqlConnect,TarihIslemler,DegisiklikMain
from views.siparisler.listeler import UrunKartMenu
class UrunKart:

    def __init__(self):
        self.data = SqlConnect().data

    def kaydet(self,kart):
        try:
            kart['urunId'] = self.__urunId(kart['urunAdi'])
            kart['olcuId'] = self.__olcuId(kart['en'],kart['boy'],kart['kenar'])
            kart['kategoriId'] = self.__kategoriId(kart['kategoriAdi'])
            kart['yuzeyId'] = self.__yuzeyId(kart['yuzeyIslem'])
            kayitKontrol = self.__kartKontrol(kart)
            if kayitKontrol == False:
                return { 'status' : False,'errorMessage' : "Bu Kart Zaten Kaydedilmiş." }
            self.data.update_insert( 
                """
                insert into UrunKartTB (UrunID,YuzeyID,OlcuID,KategoriID,Kod)
                values
                (?,?,?,?,?)
                """,(
                    kart['urunId'],kart['yuzeyId'],kart['olcuId'],kart['kategoriId'],kart['kod']
                )
            )
            kart['username'] = kart['username'].capitalize()
            info = kart['username'] + ', ' + 'Yeni Kart Girişi Yaptı'
            DegisiklikMain().setYapilanDegisiklikBilgisi(kart['username'],info)
            return {'status' : True} 
        except Exception as e:
            print('Ürün Kart kaydet hata kod : ', str(e))
            return { 'status' : False, 'errorMessage' : str(e) }

    def guncelle(self,kart):
        result = {

        }

        try:
            self.data.update_insert(
                """
                update UrunKartTB set UrunID=?,YuzeyID=?,OlcuID=?,
                KategoriID=?,Kod=? where ID=?
                """,(
                   self.__urunId(kart['urunAdi']),self.__yuzeyId(kart['yuzeyIslem']),
                   self.__olcuId(kart['en'],kart['boy'],kart['kenar']),
                   self.__kategoriId(kart['kategoriAdi']),kart['kod'],kart['id']
                )
            )
            result['status'] = True
            kart['username'] = kart['username'].capitalize()
            info = kart['username'] + ', ' + 'Ürün Kartı Güncellemesi Yaptı'
            DegisiklikMain().setYapilanDegisiklikBilgisi(kart['username'],info)
            return result 
        except Exception as e:
            print("ÜrünKart gümcelle hata kod : ",str(e))
            result['status'] = False
            result['errorMessage'] = str(e)
            return result

    def getUrunKartSil(self,urunKartId,username):
        try:
            
            self.data.update_insert("""
                        delete from UrunKartTB WHERE ID = ?           
                                
                                
                """,(urunKartId))
            info = username + ', ' + 'Ürün Kartı Silme İşlemi Yaptı.'
            DegisiklikMain().setYapilanDegisiklikBilgisi(username,info)
            return True
        except Exception as e:
            print('Urun Kart Hata sil : ', str(e))

            return False
    
    def __urunId(self,urunAdi):
        kontrol = self.data.getStoreList("Select count(*) as durum from UrunlerTB where UrunAdi=?",(urunAdi))[0].durum

        urunId = None 
        if kontrol > 0:
            
            urunId = self.data.getStoreList("Select ID from UrunlerTB where UrunAdi=?",(urunAdi))[0].ID
        else:
            self.data.update_insert("insert into UrunlerTB (UrunAdi) values (?)",(urunAdi))
            urunId = self.data.getList("Select Max(ID) as id from UrunlerTB")[0].id
       

        return urunId

    def __yuzeyId(self,yuzeyIslem):
      
        yuzeyId = None 
        kontrol = self.data.getStoreList("Select count(*) as durum from YuzeyKenarTB where YuzeyIslemAdi=?",(yuzeyIslem))[0].durum 

        if kontrol > 0 :
            yuzeyId = self.data.getStoreList("Select ID from YuzeyKenarTB where YuzeyIslemAdi=?",(yuzeyIslem))[0].ID
        else:
           
            self.data.update_insert("insert into YuzeyKenarTB (YuzeyIslemAdi) values (?)",(yuzeyIslem))
            yuzeyId = self.data.getList("Select Max(ID) as id from YuzeyKenarTB")[0].id
        return yuzeyId

    def __kategoriId(self,kategoriAdi):
        
        kategoriId = None

        kontrol = self.data.getStoreList("Select count(*) as durum from KategoriTB where KategoriAdi=?",(kategoriAdi))[0].durum 

        if kontrol > 0:
            kategoriId = self.data.getStoreList("Select ID from KategoriTB where KategoriAdi=?",(kategoriAdi))[0].ID 
        else:
            self.data.update_insert("insert into KategoriTB (KategoriAdi) values (?)",(kategoriAdi))
            kategoriId = self.data.getList("Select Max(ID) as id from KategoriTB")[0].id 

        return kategoriId

    def __olcuId(self,en,boy,kenar):
        olcuId = None 
        
        kontrol = self.data.getStoreList("Select count(*) as durum from OlculerTB where En=? and Boy=? and Kenar=?",(en,boy,kenar))[0].durum 

        if kontrol > 0:
            olcuId = self.data.getStoreList("Select ID from OlculerTB where En=? and Boy=? and Kenar=?",(en,boy,kenar))[0].ID
            self.data.update_insert("update OlculerTB SET en=? ,boy=?,kenar=? WHERE ID=? ",(en,boy,kenar,olcuId))
        else:
            self.data.update_insert("insert into OlculerTB (En,Boy,Kenar) values (?,?,?)",(en,boy,kenar))
            olcuId = self.data.getList("Select Max(ID) as id from OlculerTB")[0].id 

        return olcuId

    def __getUrunKartMusteriList(self,urunKartId):
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(
            """
            select
            su.ID,
            m.FirmaAdi,
            su.SiparisNo,
            su.SatisFiyati,
            su.Miktar
           
            from
            SiparisUrunTB su,SiparislerTB s,MusterilerTB m
            where
            su.SiparisNo=s.SiparisNo and m.ID=s.MusteriID
            
            and su.UrunKartID=?
            """,(urunKartId)
        )
        musteriListe = list()
        for item in result:

            model = UrunKartMusteriSatisModel()

            model.id = item.ID
            model.musteriAdi = item.FirmaAdi 
            model.siparisNo = item.SiparisNo 
            model.satisFiyati = item.SatisFiyati 
            model.miktar = item.Miktar 
            #model.tarih = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")

            musteriListe.append(model)
       
        return musteriListe

    def __kartKontrol(self,kart):
        result = self.data.getStoreList(
            """
            Select count(*) as Durum from UrunKartTB
            where UrunID=? and YuzeyID=? and OlcuID=?
            and KategoriID=?
            """,(
                kart['urunId'],kart['yuzeyId'],kart['olcuId'],
                kart['kategoriId']
            )
        )[0].Durum
        if result > 0:
            return False
        
        print("Ürün Kart Metot Sonu")
        return True

    def getUrunKartDetayListe(self,urunKartId):
        model = UrunKartListeModel()
        
        model.kategoriList = self.__getKategoriList()
        model.urunList = self.__getUrunList()
        model.olcuList = self.__getOlcuList()
        model.yuzeyList = self.__getYuzeyList()
        model.musteriSatisList = self.__getUrunKartMusteriList(urunKartId)
        schema = UrunKartListeSchema()

        return schema.dump(model)

    def getUrunKartDetayListeYeni(self):
        model = UrunKartListeModel()

        model.kategoriList = self.__getKategoriList()
        model.urunList = self.__getUrunList()
        model.olcuList = self.__getOlcuList()
        model.yuzeyList = self.__getYuzeyList()
        model.musteriSatisList = list()

        schema = UrunKartListeSchema()

        return schema.dump(model)
      
    def __getSonDataKayitId(self):

        result = self.data.getList("Select Max(ID) as Id from UrunKartTB")[0]

        return result.Id
    
    def __getKategoriList(self):

        liste = list()

        result = self.data.getList("Select * from KategoriTB")

        for item in result:
           
            model = KategoriModel()
            model.id = item.ID 
            model.kategoriAdi = item.KategoriAdi 

            liste.append(model)

        return liste

    def __getUrunList(self):

        liste = list()

        result = self.data.getList("Select * from UrunlerTB")

        for item in result:
            
            model = UrunlerModel()
            model.id = item.ID 
            model.urunAdi = item.UrunAdi 

            liste.append(model)

        return liste

    def __getOlcuList(self):

        liste = list() 

        result = self.data.getList("Select * from OlculerTB") 
        for item in result:

            model = OlculerModel()
            model.id = item.ID 
            model.en = item.En
            model.boy = item.Boy
            model.kenar = item.Kenar

            liste.append(model)
        return liste

    def __getYuzeyList(self):

        liste = list()

        result = self.data.getList("Select * from YuzeyKenarTB")

        for item in result:

            model = YuzeyKenarModel() 
            model.id = item.ID 
            model.yuzeyIslemAdi = item.YuzeyIslemAdi 

            yuzeyler = model.yuzeyIslemAdi.split('&')

            model.yuzey_1 = yuzeyler[0]

            if len(yuzeyler) == 2:
                model.yuzey_2 = yuzeyler[1]
            if len(yuzeyler) == 3:
                model.yuzey_2 = yuzeyler[1]
                model.yuzey_3 = yuzeyler[2]

            liste.append(model)

        return liste
      
          
    def getUrunKart(self,urunKarId):

        model = UrunKartModel()

        result = self.data.getStoreList(
           """
            select
            ID as Id,
            dbo.Get_KategoriAdi(ID) as KategoriAdi,
            dbo.Get_UrunAdi(ID) as UrunAdi,
            dbo.Get_KenarIslem(ID) as YuzeyIslem,
            dbo.Get_Olcu_En(ID) as En,
            dbo.Get_Olcu_Boy(ID) as Boy,
            dbo.Get_Olcu_Kenar(ID) as Kenar,
            KategoriID,
            UrunID,
            OlcuID,
            YuzeyID
            from
            UrunKartTB
            where ID=?
            """,(urunKarId)
        )[0]

        model.id = result.Id 
        model.kategoriAdi = result.KategoriAdi 
        model.urunAdi = result.UrunAdi 
        model.yuzeyIslem = result.YuzeyIslem 
        model.en = result.En 
        model.boy = result.Boy 
        model.kenar = result.Kenar
        model.kategoriId = result.KategoriID 
        model.urunId = result.UrunID 
        model.olcuId = result.OlcuID 
        model.yuzeyId = result.YuzeyID
        yuzey_1,yuzey_2,yuzey_3 = self.__getYuzey(model.yuzeyIslem.split(('&')))
        model.yuzey_1 = yuzey_1
        model.yuzey_2 = yuzey_2 
        model.yuzey_3 = yuzey_3 

        schema = UrunKartSchema()

        return schema.dump(model)

    def getUrunKartModel(self):

        model = UrunKartModel()
        schema = UrunKartSchema()

        return schema.dump(model)
    
    def __getYuzey(self,yuzey):

        yuzey_1 = ""
        yuzey_2 = ""
        yuzey_3 = ""

        yuzey_1 = yuzey[0]

        if len(yuzey) == 2:
            yuzey_2 = yuzey[1]
        if len(yuzey) == 3:
            yuzey_2 = yuzey[1]
            yuzey_3 = yuzey[2]

        return yuzey_1,yuzey_2,yuzey_3
    
    