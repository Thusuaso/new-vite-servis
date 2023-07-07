from resource_api.finans.konteyner_islem.siparisler import Siparisler,SiparislerNew
from resource_api.finans.konteyner_islem.siparis_urunler import SiparisUrunlerNew
from models.finans import FinansAnaSayfaModel,FinansAnaSayfaSchema
from resource_api.finans.konteyner_islem.odemeler import Odemeler,OdemelerNew
from resource_api.finans.konteyner_islem.finansMailGonder import MailAttempt
import datetime
from helpers import SqlConnect
from helpers.sqlServer import SqlIslem
from models.finans.maya_gelen_bedeller import *
class Konteyner:

    def __init__(self,yil):

        siparis = Siparisler(yil)

        self.siparis_list = siparis.siparis_list
        self.eski_siparis_list = siparis.eski_siparis_list
        self.pesinat_list = siparis.pesinat_listesi
        self.bekleyen_listesi = siparis.bekleyen_listesi
        self.odeme = Odemeler(yil)


    def getKonteynerList(self):

        groupList = set(map(lambda x:(x['musteriadi'],x['musteriid'],x['temsilci'],x['marketing']),self.siparis_list))
        eski_groupList = set(map(lambda x:(x['musteriadi'],x['musteriid'],x['temsilci'],x['marketing']),self.eski_siparis_list))        

        liste = list()
        for item in groupList:
                model = self.__getModel(item[0],item[1])
                model.id = item[1] 
                model.musteriadi = item[0]
                model.temsilci = item[2]
                
                model.marketing = item[3]
                
                liste.append(model)
        """
        for item in self.pesinat_list: 

            if self.__getMusteriKontrol(item['musteriid'],liste) == False:
                model = FinansAnaSayfaModel()
                model.id = item['musteriid']
                model.musteriadi = item['musteriadi']
                model.pesinat = item['pesinat']
                model.genel_bakiye = model.pesinat * -1

                liste.append(model)
        """

        for item in eski_groupList:

                
                if self.__getMusteriKontrol(item[1],liste) == False:
                
                    model = self.__getModel_Eski(item[0],item[1])
                
                    model.id = item[1] 
                    model.musteriadi = item[0]   
                    model.temsilci = item[2]  
                
                    model.marketing = item[3]          
                    liste.append(model)
             
        for item in self.bekleyen_listesi:
            if self.__getMusteriKontrol(item['musteriid'],liste) == False:
                model = FinansAnaSayfaModel()
                model.id = item['musteriid']
                model.musteriadi = item['musteriadi']
                model.pesinat = float(item['pesinat'])
                model.genel_bakiye = model.pesinat
                model.marketing = item['marketing']
                model.temsilci = item['temsilci']
                liste.append(model)
        
        
        _liste = list()
        
        
        for item in liste:
            model = self.__getBekleyenPesinat(item)
            if model != None:
                _liste.append(model)
        

        
        
        for item in liste:
            
            for bekleyen in self.bekleyen_listesi:
                try:
                    if item.id == bekleyen['musteriid']:
                        if item.genel_bakiye < 8:
                            item.pesinat = bekleyen['pesinat']
                            #item.genel_bakiye += item.pesinat
                            
                            
                except Exception as e:
                    print('Bekleyen Listesi Hata : ', bekleyen)
                    print('Hata Kodu : ',str(e))
        

        for item in _liste:
            if self.__getMusteriKontrol(item.id,liste) == False:
                liste.append(item)

        musteriler = []
        genelBakiye = []
        for item in liste:

            if item.pesinat > 0:
                item.pesinat = float(item.pesinat) - float(item.eski_pesinat)

            item.bakiye = (float(item.devir + item.ciro) - float(item.odenen))
            pesinatlar = float(item.eski_pesinat) + float(item.pesinat)
            item.genel_bakiye = float(item.bakiye) - pesinatlar
            
            tarih = datetime.datetime.now()
            gun = tarih.day
            if gun == 26:

                if item.genel_bakiye > 8:
                    musteriler.append(item.musteriadi)
                    genelBakiye.append(round(item.genel_bakiye,3))
        

        
        sql = SqlConnect().data
        result = sql.getList("select mailControl from MailControl_")
        tarih = datetime.datetime.now()
        gun = tarih.day
        
        
        if result[0][0] == True :
            tarih = datetime.datetime.now()
            gun = tarih.day
            
            
            if gun == 26:
                mail = MailAttempt()
                mail.mailSend(musteriler,genelBakiye,"bilgiislem@mekmar.com")
                mail.mailSend(musteriler,genelBakiye,"mehmet@mekmer.com")
                sql.update_insert("""
                                    update MailControl_ Set mailControl = ? WHERE ID = ?
                                  
                                  """,(0,1))
            else:
                pass
        if result[0][0] != True:
            if gun == 27:
                sql.update_insert("""
                                update MailControl_ Set mailControl = ? WHERE ID = ?
                                """,(1,1))
        


        
            


            #print("item.genel_bakiye",item.genel_bakiye)
            #print("item.musteri_adi",item.musteriadi)

        

        schema = FinansAnaSayfaSchema(many=True)

        return schema.dump(liste)

    def __getBekleyenPesinat(self,data):

        model = None
       
        for item in self.bekleyen_listesi:
            
            try:
               
                if item['musteriid'] == data.id and data.genel_bakiye < 8:
                    model = FinansAnaSayfaModel()
                    model.id = item['musteriid']
                    model.musteriadi = item['musteriadi']
                    model.pesinat = float(item['pesinat'])
                    model.genel_bakiye =  model.pesinat * -1
                    model.temsilci = item['temsilci']
                    
            except:
                print('__getBekleyenPesinat Hata : ',data)
                

        return model
        
    def __getMusteriKontrol(self,musteriid,liste):

        kontrol = False 

        result = list(filter(lambda x:x.id == musteriid,liste))
       
        if len(result) > 0:
            kontrol = True

        return kontrol

    def __getModel(self,musteriadi,musteriid):
        

        model = FinansAnaSayfaModel()
        ciro = 0
        top = 0
        kalan = 0
        masraf = 0
        for item in self.siparis_list:
            
            if musteriid == item['musteriid']:
                top = float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                ciro +=  (float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])) 
                if item['Odemeler'] == None :
                   item['Odemeler'] = 0
                if top - item['Odemeler'] > 10 : 
                  masraf +=top
                  kalan += top - item['Odemeler']
                else :
                 masraf = masraf
        model.kapanmayan_siparis = masraf 
        if musteriid == 37:
            
            model.kapanmayan_kalan = kalan - 1400
        else:
            model.kapanmayan_kalan = kalan
        model.ciro = ciro
        top = 0
        kalan = 0
        masraf = 0
        for item in self.eski_siparis_list:
            if musteriadi == item['musteriadi']:
                top = float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                model.devir += float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                if item['Odemeler'] == None :
                   item['Odemeler'] = 0
                if top - item['Odemeler'] > 10 : 
                  masraf +=top
                  kalan += top - item['Odemeler']
                else :
                 masraf = masraf
                
                model.eski_pesinat = self.odeme.getEskiPesinat(musteriid)
                
        
        model.kapanmayan_siparis += masraf 
        model.kapanmayan_kalan += kalan
        eski_odenen = float(self.odeme.getOdeme_GecenYil(musteriid))
        model.devir = model.devir - eski_odenen
        model.eski_pesinat = self.odeme.getEskiPesinat(musteriid)
        model.odenen = float(self.odeme.getOdeme(musteriid))
        model.pesinat = float(self.odeme.getPesinat(musteriid))
       
      #  model.kapanmayan_siparis , model.kapanmayan_kalan =(self.odeme.getKapanmayanSiparis(musteriid))
       # print("__getModel",musteriadi)
        model.kapanmayan_odenen = model.kapanmayan_siparis - model.kapanmayan_kalan
        

        #model.bakiye = (float(model.ciro) + float(model.devir) ) - float(model.odenen)
        #model.genel_bakiye = float(model.bakiye) - float(model.pesinat)
        

        return model

    def __getModel_Eski(self,musteriadi,musteriid):
        
        model = FinansAnaSayfaModel()
        top = 0
        kalan = 0
        masraf = 0
        for item in self.eski_siparis_list:
            if musteriadi == item['musteriadi']:
                top = float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                model.devir += item['navlunsatis'] + item['detaytutar_1'] + item['detaytutar_2'] + item['detaytutar_3']  +item['urunbedel'] + float(item['sigorta_tutar_satis'])
                if item['Odemeler'] == None :
                   item['Odemeler'] = 0
                if top - item['Odemeler'] > 10 : 
                  masraf +=top
                  kalan += top - item['Odemeler']
                else :
                 masraf = masraf
        model.kapanmayan_siparis = masraf 
        model.kapanmayan_kalan = kalan
        model.odenen = self.odeme.getOdeme(musteriid)        
        eski_odenen = self.odeme.getOdeme_GecenYil(musteriid)
        model.eski_pesinat = self.odeme.getEskiPesinat(musteriid)
        model.devir = model.devir - eski_odenen 
        
        #model.kapanmayan_siparis , model.kapanmayan_kalan =(self.odeme.getKapanmayanSiparis(musteriid))
        #print("__getModel_Eski",musteriadi)
        model.kapanmayan_odenen = model.kapanmayan_siparis - model.kapanmayan_kalan
        if musteriadi == 'Nijerya-Balogun':
            model.devir = 0
            
        """
        if model.odenen < 0 :
            model.bakiye = model.devir + model.odenen
        else:
            model.bakiye = model.devir - model.odenen
        
        model.genel_bakiye = float(model.bakiye) - float(model.eski_pesinat)
        """

        
      

        return model

class KonteynerYeni:

    def __init__(self,yil):

        siparis = SiparislerNew(yil)

        self.siparis_list = siparis.siparis_list
        self.eski_siparis_list = siparis.eski_siparis_list
        self.pesinat_list = siparis.pesinat_listesi
        self.bekleyen_listesi = siparis.bekleyen_listesi
        self.odeme = OdemelerNew(yil)


    def getKonteynerList(self):

        groupList = set(map(lambda x:(x['musteriadi'],x['musteriid'],x['temsilci'],x['marketing']),self.siparis_list))
        eski_groupList = set(map(lambda x:(x['musteriadi'],x['musteriid'],x['temsilci'],x['marketing']),self.eski_siparis_list))        

        liste = list()
        for item in groupList:
                model = self.__getModel(item[0],item[1])
                model.id = item[1] 
                model.musteriadi = item[0]
                model.temsilci = item[2]
                
                model.marketing = item[3]
                
                liste.append(model)
        """
        for item in self.pesinat_list: 

            if self.__getMusteriKontrol(item['musteriid'],liste) == False:
                model = FinansAnaSayfaModel()
                model.id = item['musteriid']
                model.musteriadi = item['musteriadi']
                model.pesinat = item['pesinat']
                model.genel_bakiye = model.pesinat * -1

                liste.append(model)
        """

        for item in eski_groupList:

                
                if self.__getMusteriKontrol(item[1],liste) == False:
                
                    model = self.__getModel_Eski(item[0],item[1])
                
                    model.id = item[1] 
                    model.musteriadi = item[0]   
                    model.temsilci = item[2]  
                
                    model.marketing = item[3]          
                    liste.append(model)
             
        for item in self.bekleyen_listesi:
            if self.__getMusteriKontrol(item['musteriid'],liste) == False:
                model = FinansAnaSayfaModel()
                model.id = item['musteriid']
                model.musteriadi = item['musteriadi']
                model.pesinat = float(item['pesinat'])
                model.genel_bakiye = model.pesinat
                model.marketing = item['marketing']
                model.temsilci = item['temsilci']
                liste.append(model)
        
        
        _liste = list()
        
        
        for item in liste:
            model = self.__getBekleyenPesinat(item)
            if model != None:
                _liste.append(model)
        

        
        
        for item in liste:
            
            for bekleyen in self.bekleyen_listesi:
                try:
                    if item.id == bekleyen['musteriid']:
                        if item.genel_bakiye < 8:
                            item.pesinat = bekleyen['pesinat']
                            #item.genel_bakiye += item.pesinat
                            
                            
                except Exception as e:
                    print('Bekleyen Listesi Hata : ', bekleyen)
                    print('Hata Kodu : ',str(e))
        

        for item in _liste:
            if self.__getMusteriKontrol(item.id,liste) == False:
                liste.append(item)

        musteriler = []
        genelBakiye = []
        for item in liste:
            if item.pesinat > 0:
                item.pesinat = float(item.pesinat) - float(item.eski_pesinat)

            item.bakiye = (float(item.devir + item.ciro) - float(item.odenen))

            pesinatlar = float(item.eski_pesinat) + float(item.pesinat)
            item.genel_bakiye = float(item.bakiye) - pesinatlar
            
            tarih = datetime.datetime.now()
            gun = tarih.day
            if gun == 26:

                if item.genel_bakiye > 8:
                    musteriler.append(item.musteriadi)
                    genelBakiye.append(round(item.genel_bakiye,3))
        

        
        sql = SqlConnect().data
        result = sql.getList("select mailControl from MailControl_")
        tarih = datetime.datetime.now()
        gun = tarih.day
        
        
        if result[0][0] == True :
            tarih = datetime.datetime.now()
            gun = tarih.day
            
            
            if gun == 26:
                mail = MailAttempt()
                mail.mailSend(musteriler,genelBakiye,"bilgiislem@mekmar.com")
                mail.mailSend(musteriler,genelBakiye,"mehmet@mekmer.com")
                sql.update_insert("""
                                    update MailControl_ Set mailControl = ? WHERE ID = ?
                                  
                                  """,(0,1))
            else:
                pass
        if result[0][0] != True:
            if gun == 27:
                sql.update_insert("""
                                update MailControl_ Set mailControl = ? WHERE ID = ?
                                """,(1,1))
        


        
            


            #print("item.genel_bakiye",item.genel_bakiye)
            #print("item.musteri_adi",item.musteriadi)

        

        schema = FinansAnaSayfaSchema(many=True)

        return schema.dump(liste)

    def __getBekleyenPesinat(self,data):

        model = None
       
        for item in self.bekleyen_listesi:
            
            try:
               
                if item['musteriid'] == data.id and data.genel_bakiye < 8:
                    model = FinansAnaSayfaModel()
                    model.id = item['musteriid']
                    model.musteriadi = item['musteriadi']
                    model.pesinat = float(item['pesinat'])
                    model.genel_bakiye =  model.pesinat * -1
                    model.temsilci = item['temsilci']
                    
            except:
                print('__getBekleyenPesinat Hata : ',data)
                

        return model
        
    def __getMusteriKontrol(self,musteriid,liste):

        kontrol = False 

        result = list(filter(lambda x:x.id == musteriid,liste))
       
        if len(result) > 0:
            kontrol = True

        return kontrol

    def __getModel(self,musteriadi,musteriid):
        

        model = FinansAnaSayfaModel()
        ciro = 0
        top = 0
        kalan = 0
        masraf = 0
        for item in self.siparis_list:
            
            if musteriid == item['musteriid']:
                top = float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                ciro +=  (float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])) 
                if item['Odemeler'] == None :
                   item['Odemeler'] = 0
                if top - item['Odemeler'] > 10 : 
                  masraf += top
                  kalan += top - item['Odemeler']
                else :
                 masraf = masraf
        model.kapanmayan_siparis = masraf 
        if musteriid == 37:
            
            model.kapanmayan_kalan = kalan - 1400
        else:
            model.kapanmayan_kalan = kalan
        model.ciro = ciro
        top = 0
        kalan = 0
        masraf = 0
        for item in self.eski_siparis_list:
            if musteriadi == item['musteriadi']:
                top = float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                model.devir += float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                if item['Odemeler'] == None :
                   item['Odemeler'] = 0
                if top - item['Odemeler'] > 10 : 
                  masraf +=top
                  kalan += top - item['Odemeler']
                else :
                 masraf = masraf
                
                model.eski_pesinat = self.odeme.getEskiPesinat(musteriid)
                
        
        model.kapanmayan_siparis += masraf 
        model.kapanmayan_kalan += kalan
        eski_odenen = float(self.odeme.getOdeme_GecenYil(musteriid))
        model.devir = model.devir - eski_odenen
        model.eski_pesinat = self.odeme.getEskiPesinat(musteriid)
        model.odenen = float(self.odeme.getOdeme(musteriid))
        model.pesinat = float(self.odeme.getPesinat(musteriid))
       
      #  model.kapanmayan_siparis , model.kapanmayan_kalan =(self.odeme.getKapanmayanSiparis(musteriid))
       # print("__getModel",musteriadi)
        model.kapanmayan_odenen = model.kapanmayan_siparis - model.kapanmayan_kalan
        

        #model.bakiye = (float(model.ciro) + float(model.devir) ) - float(model.odenen)
        #model.genel_bakiye = float(model.bakiye) - float(model.pesinat)
        

        return model

    def __getModel_Eski(self,musteriadi,musteriid):
        
        model = FinansAnaSayfaModel()
        top = 0
        kalan = 0
        masraf = 0
        for item in self.eski_siparis_list:
            if musteriadi == item['musteriadi']:
                top = float(item['navlunsatis']) + float(item['detaytutar_1']) + float(item['detaytutar_2']) + float(item['detaytutar_3'])  + float(item['urunbedel']) + float(item['sigorta_tutar_satis'])
                model.devir += item['navlunsatis'] + item['detaytutar_1'] + item['detaytutar_2'] + item['detaytutar_3']  +item['urunbedel'] + float(item['sigorta_tutar_satis'])
                if item['Odemeler'] == None :
                   item['Odemeler'] = 0
                if top - item['Odemeler'] > 10 : 
                  masraf +=top
                  kalan += top - item['Odemeler']
                else :
                 masraf = masraf
        model.kapanmayan_siparis = masraf 
        model.kapanmayan_kalan = kalan
        model.odenen = self.odeme.getOdeme(musteriid)        
        eski_odenen = self.odeme.getOdeme_GecenYil(musteriid)
        model.eski_pesinat = self.odeme.getEskiPesinat(musteriid)
        model.devir = model.devir - eski_odenen 
        
        #model.kapanmayan_siparis , model.kapanmayan_kalan =(self.odeme.getKapanmayanSiparis(musteriid))
        #print("__getModel_Eski",musteriadi)
        model.kapanmayan_odenen = model.kapanmayan_siparis - model.kapanmayan_kalan
        if musteriadi == 'Nijerya-Balogun':
            model.devir = 0
            
        """
        if model.odenen < 0 :
            model.bakiye = model.devir + model.odenen
        else:
            model.bakiye = model.devir - model.odenen
        
        model.genel_bakiye = float(model.bakiye) - float(model.eski_pesinat)
        """

        
      

        return model



class MayaGelenBedeller:
    def __init__(self):
        self.data  = SqlConnect().data
        
    def getMayaGelenBedeller(self,month,year):
        try:
            siparisOdemeleri = self.data.getStoreList("""
                                                select 


                                                    ID,
                                                    Tarih,
                                                    SiparisNo,
                                                    Tutar,
                                                    Masraf


                                                    from 


                                                    OdemelerTB 


                                                    where MusteriID=1373 and YEAR(Tarih) = ? and MONTH(Tarih) = ?
                                            """,(year,month))
            
            siparisList = list()
            for item in siparisOdemeleri:
                model = MayaGelenBedellerModel()
                model.id = item.ID
                model.tarih = item.Tarih
                model.po = item.SiparisNo
                model.tutar = item.Tutar
                model.masraf = item.Masraf
                siparisList.append(model)
                
            schema = MayaGelenBedellerSchema(many= True)
            data1 = schema.dump(siparisList)
            numuneList = list()
            numuneOdemeleri = self.data.getStoreList("""
                                                        select 


                                                            nuo.ID,
                                                            nuo.Tarih,
                                                            nuo.NumuneNo,
                                                            nuo.Tutar,
                                                            nuo.Banka,
                                                            nuo.Masraf,
                                                            ytm.MusteriAdi,
                                                            n.NumuneTarihi,
                                                            n.YuklemeTarihi

                                                        from NumuneOdemelerTB nuo 
                                                            inner join YeniTeklif_MusterilerTB ytm on ytm.Id = nuo.MusteriID
                                                            inner join NumunelerTB n on n.NumuneNo = nuo.NumuneNo


                                                        where nuo.Banka in ('Maya Paypal','Maya Bank') 
                                                        and YEAR(nuo.Tarih) = ?
                                                        and MONTH(nuo.Tarih) = ?
                                                     
                                                     
                                                     """,(year,month))
            for item2 in numuneOdemeleri:
                model = MayaGelenBedellerModel()
                model.id = item2.ID
                model.tarih = item2.Tarih
                model.numuneTarihi = item2.NumuneTarihi
                model.numuneYuklemeTarihi = item2.YuklemeTarihi
                model.banka = item2.Banka
                model.po = item2.NumuneNo
                model.tutar = item2.Tutar
                model.masraf = item2.Masraf
                model.musteriAdi = item2.MusteriAdi
                numuneList.append(model)
                
            schema2 = MayaGelenBedellerSchema(many=True)
            data2 = schema2.dump(numuneList)
            
            datas = {
                'siparis':data1,
                'numune':data2
            }
            return datas
            
            
                    
        
            
        
        except Exception as e:
            print('getMayaGelenBedeller hata',str(e))
            return False
    
    def getMayaGelenBedellerYear(self,year):
        try:
            siparisOdemeleri = self.data.getStoreList("""
                                                select 


                                                    ID,
                                                    Tarih,
                                                    SiparisNo,
                                                    Tutar,
                                                    Masraf


                                                    from 


                                                    OdemelerTB 


                                                    where MusteriID=1373 and YEAR(Tarih) = ?
                                            """,(year))
            
            siparisList = list()
            for item in siparisOdemeleri:
                model = MayaGelenBedellerModel()
                model.id = item.ID
                model.tarih = item.Tarih
                model.po = item.SiparisNo
                model.tutar = item.Tutar
                model.masraf = item.Masraf
                siparisList.append(model)
                
            schema = MayaGelenBedellerSchema(many= True)
            data1 = schema.dump(siparisList)
            numuneList = list()
            numuneOdemeleri = self.data.getStoreList("""
                                                        select 


                                                            nuo.ID,
                                                            nuo.Tarih,
                                                            nuo.NumuneNo,
                                                            nuo.Tutar,
                                                            nuo.Banka,
                                                            nuo.Masraf,
                                                            ytm.MusteriAdi,
                                                            n.NumuneTarihi,
                                                            n.YuklemeTarihi

                                                        from NumuneOdemelerTB nuo 
                                                            inner join YeniTeklif_MusterilerTB ytm on ytm.Id = nuo.MusteriID
                                                            inner join NumunelerTB n on n.NumuneNo = nuo.NumuneNo


                                                        where nuo.Banka in ('Maya Paypal','Maya Bank') 
                                                        and YEAR(nuo.Tarih) = ?
                                                     
                                                     
                                                     """,(year))
            for item2 in numuneOdemeleri:
                model = MayaGelenBedellerModel()
                model.id = item2.ID
                model.tarih = item2.Tarih
                model.numuneTarihi = item2.NumuneTarihi
                model.numuneYuklemeTarihi = item2.YuklemeTarihi
                model.banka = item2.Banka
                model.po = item2.NumuneNo
                model.tutar = item2.Tutar
                model.masraf = item2.Masraf
                model.musteriAdi = item2.MusteriAdi
                numuneList.append(model)
                
            schema2 = MayaGelenBedellerSchema(many=True)
            data2 = schema2.dump(numuneList)
            
            datas = {
                'siparis':data1,
                'numune':data2
            }
            return datas
        except Exception as e:
            print('getMayaGelenBedeller hata',str(e))
            return False
          
    