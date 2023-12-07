from helpers import SqlConnect,TarihIslemler,DegisiklikMain
from models.numuneler import *
from models.yeniTeklifler import *
from models.shared import GenelListModel,GenelListSchema
from flask_restful import Resource
from flask import jsonify,request
import datetime
from resource_api.finans.caprazkur import DovizListem
from resource_api.finans.guncel_kur import DovizListem as GuncelKurList



class NumuneKayitIslem(Resource):
    def post(self):
        numuneIslem = NumuneIslem()

        veri = request.get_json()
        
        status = numuneIslem.kaydet(veri)

        return jsonify({'status' : status })


    def put(self):
        
        numuneIslem = NumuneIslem()

        data = request.get_json()

        result = numuneIslem.guncelleme(data)

        return jsonify({'status' : result})

class NumuneDosyaKaydet(Resource):
    
    def post(self):

        numune = request.get_json()

        numuneIslem = NumuneIslem()
        result = numuneIslem.numuneDosyaKaydet(numune)
        
        return jsonify({'Status' : result})

class NumuneDosyaKaydet2(Resource):
    
    def post(self):

        numune = request.get_json()

        numuneIslem = NumuneIslem()
        result = numuneIslem.numuneDosyaKaydet2(numune)
        
        return jsonify({'Status' : result})        


class NumuneFormListeler(Resource):
    
    def get(self):

        numune = NumuneIslem()

        data = {
            'model': numune.getNumuneModel(),
            'kategoriList' : numune.getKategoriList(),
            
            'musteriList' : numune.getMusteriList(),
            'ulkeList' : numune.getUlkeList(),
            
            'birimList' : numune.getBirimList(),
            'temsilciList' : numune.getTemsilciList(),
            'odemeler':[],
           
        }

        return jsonify(data)


class NumuneFormModel(Resource):
    
    def get(self,numunepo):
      
        numuneIslem = NumuneIslem()

        data = {

            'numune' : numuneIslem.getNumune(numunepo)
          
           
        }

        return jsonify(data)



class NumuneIslem:

    def __init__(self):
        self.data = SqlConnect().data
        self.tarihIslem = TarihIslemler()

    
    def getNumuneModel(self):
        model = NumuneModel()
        schema = NumuneSchema()
        return schema.dump(model)

   

    def getNumune(self,numunepo):
        
        item = self.data.getStoreList(
            """
          select

            *,
            (select m.MusteriAdi from YeniTeklif_MusterilerTB m where n.MusteriID=m.Id ) as  MusteriAdi,
            (select k.Urun from NumuneKategoriTB k where k.ID=n.KategoriID) as KategoriAdi,
            (select u.BirimAdi from UrunBirimTB u where u.ID= n.UrunBirimi) as BirimAdi,
            (select g.GonderiAdi from NumuneGonderiTipi g where g.ID=n.GonderiTipi) as GonderiAdi,
            (select b.BankaAdi from NumuneBankaSecim b where b.ID=N.BankaSecim) as BankaAdi
            from NumunelerTB n  
            where n.NumuneNo=?
            """,(numunepo)
        )[0]

        model = NumuneModel()
        model.id = item.ID
        model.numuneNo = item.NumuneNo
     
        model.giristarih = self.tarihIslem.getDate(item.NumuneTarihi).strftime("%d-%m-%Y")
      
        model.musteriId = item.MusteriID
        model.musteriAdi = item.MusteriAdi
        model.adres = item.Adres
        model.aciklama = item.Aciklama
        model.temsilci_id = item.NumuneTemsilci
        model.ulke = item.Ulke
        model.parite = item.Parite
        model.takip_No  = item.TrackingNo
        if item.YuklemeTarihi != None:
         model.yukleme_tarihi =  self.tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")
        
        model.gonderiId = item.GonderiTipi
        model.gonderiAdi = item.GonderiAdi

        model.bankaId = item.BankaSecim
        model.bankaAdi = item.BankaAdi
       

        model.kuryeAlis = item.KuryeAlis
        model.kuryeSatis = item.KuryeSatis

        model.TL_Alis = item.TL_Alis
        model.TL_Satis = item.TL_Satis  

        model.Euro_Alis = item.Euro_Alis
        model.Euro_Satis = item.Euro_Satis 

        model.kategoriAdi = item.KategoriAdi 
        model.kategoriId = item.KategoriID
        model.Miktar = item.Miktar
        model.urunBirim = item.BirimAdi
        model.urunBirimId = item.UrunBirimi
        if item.BirimAdi != None:
                if item.BirimAdi == 'M2' :
                    model.m2 = item.Miktar
                if item.BirimAdi == 'Adet' :
                    model.adet = item.Miktar 
                if item.BirimAdi == 'Mt' :
                    model.mt = item.Miktar  
                if item.BirimAdi == 'Ton' :
                    model.ton = item.Miktar    
        
        model.numuneCloud = item.Numune_Cloud
        model.numuneCloudDosya = item.Numune_Cloud_Dosya
        model.numuneCloud2 = item.Numune_Cloud2
        model.numuneCloudDosya2 = item.Numune_Cloud_Dosya2


        schema = NumuneSchema()
       
        return schema.dump(model)
    
    def numuneDosyaKaydet(self,numune): ## ön yüz görsel
       
        try:
            self.data.update_insert(
                """
                update NumunelerTB set Numune_Cloud=?,Numune_Cloud_Dosya=? where ID=?
                """,
                (
                    numune['numuneCloud'],numune['numuneCloudDosya'],numune['id']
                )
            )
            return True
        except Exception as e:
            print('numuneDosyaKaydet Hata : ',str(e))
            return False
     
    def numuneDosyaKaydet2(self,numune): ## arka yüz görsel
       
        try:
            self.data.update_insert(
                """
                update NumunelerTB set Numune_Cloud2=?,Numune_Cloud_Dosya2=? where ID=?
                """,
                (
                    numune['numuneCloud2'],numune['numuneCloudDosya2'],numune['id']
                )
            )
            return True
        except Exception as e:
            print('numuneDosyaKaydet2 Hata : ',str(e))
            return False


    def kaydet(self,numune):
        try:
            
            dtMusteriler = self.data.getList("Select * from YeniTeklif_MusterilerTB")
        
            status = self.__numuneKayit(numune,numune['userId'],dtMusteriler)
            info = numune['username'] + ',' + numune['numuneNo'] + ' Numunesinin Kaydını Yaptı.'
            DegisiklikMain().setYapilanDegisiklikBilgisi(numune['username'],info)
            return status
        except Exception as e:
            print('numune kaydet hata',str(e))
            return False
    
    def guncelleme(self,item):
        try:
            g_tarihi = item['giristarih']
            y_tarihi = item['yukleme_tarihi']
            # if float(item['Euro_Alis']) >0:
                
            #     item['kuryeAlis'] = float(item['Euro_Alis']) * float(self.__getCrossRange(g_tarihi))
            #     item['TL_Alis'] = float(item['kuryeAlis']) * float(self.__getNormalRange(g_tarihi))
                    
            # if float(item['kuryeSatis']) >0:
            #     item['Euro_Satis'] = float(item['kuryeSatis']) / float(self.__getCrossRange(g_tarihi))
            #     item['TL_Satis'] = float(item['kuryeSatis']) * float(self.__getNormalRange(g_tarihi))
            musteriId = self.__musteriKayit(item)
            self.data.update_insert(
                """
                update NumunelerTB set 
                    NumuneTarihi=?,
                    MusteriID=?,
                    NumuneTemsilci=?,
                    Ulke=?,
                    Adres =?,
                    TrackingNo=?,
                    Parite =?,
                    Aciklama=?,               
                    YuklemeTarihi=?,
                    KuryeAlis =?,
                    KuryeSatis =?,
                    TL_Alis =?,
                    TL_Satis =?,
                    Euro_Alis =?,
                    Euro_Satis =?,

                    GonderiTipi=?,
                    BankaSecim=?,
                    KategoriID=?,
                    UrunBirimi=?,
                    Miktar =? 
                where ID=?
                """,
                (
                    g_tarihi,
                   
                    musteriId,
                    
                    item['temsilci_id'],
                    item['ulke'],
                    item['adres'],
                   
                    item['takip_No'],
                    item['parite'],
                    item['aciklama'],

                    y_tarihi,

                    item['kuryeAlis'],
                    item['kuryeSatis'],

                    item['TL_Alis'],
                    item['TL_Satis'],

                    item['Euro_Alis'],
                    item['Euro_Satis'],

                    item['gonderiId'],
                    item['bankaId'],

                    item['kategoriId'],
                    item['urunBirimId'],
                    item['Miktar'],
                   
                    item['id']
                   
                )
            )
            info = item['username'] + ',' + item['numuneNo'] + ' Numunesini Güncelledi.'
            DegisiklikMain().setYapilanDegisiklikBilgisi(item['username'],info)
            return True 
        except Exception as e:
            print('numune Güncelleme Hata :', str(e))
            return False
    

            
 
    def __numuneKayit(self,item,userId,musteriler):
        print(item)
        g_tarihi = item['giristarih']
        y_tarihi = item['yukleme_tarihi']
        
        # if float(item['Euro_Alis']) >0:
        #     item['kuryeAlis'] = float(item['Euro_Alis']) * float(self.__getCrossRange(g_tarihi))
        #     item['TL_Alis'] = float(item['kuryeAlis']) * float(self.__getNormalRange(g_tarihi))

        
        # if float(item['kuryeSatis']) >0:
        #     item['Euro_Satis'] = float(item['kuryeSatis']) / float(self.__getCrossRange(g_tarihi))
        #     item['TL_Satis'] = float(item['kuryeSatis']) * float(self.__getNormalRange(g_tarihi))
            
        forMat = '%d-%m-%Y'
        g_tarihi = datetime.datetime.strptime(g_tarihi, forMat)
        y_tarihi = datetime.datetime.strptime(y_tarihi, forMat)
        g_tarihi = g_tarihi.date()
        y_tarihi = y_tarihi.date()
        

        durum = 2
        try:
          
          
            musteriId = self.__musteriKayit(item)
                
            
            
            self.data.update_insert(
                """
                insert into NumunelerTB (
                    NumuneNo,
                    NumuneTarihi,
                    MusteriID,
                   NumuneTemsilci,
                    Ulke,
                    Adres,
                    TrackingNo,
                    Parite,

                    KuryeAlis,
                    KuryeSatis, 

                    TL_Alis,
                    TL_Satis,

                    Euro_Alis,
                    Euro_Satis,
                           
                    YuklemeTarihi,
                    
                    GonderiTipi,
                    BankaSecim,
                    KategoriID,
                    UrunBirimi,
                    Miktar,
                    Aciklama
                   
                   
                )
                values
                   (
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                    )
                """,(
                    
                    item['numuneNo'],g_tarihi,  musteriId,  item['temsilci_id'],
                    item['ulke'],  item['adres'], item['takip_No'], item['parite'] , item['kuryeAlis'],item['kuryeSatis'],item['TL_Alis'],item['TL_Satis'],
                    item['Euro_Alis'],item['Euro_Satis'],y_tarihi,item['gonderiId']
                    ,item['bankaId'],item['kategoriId'],item['urunBirimId'],item['Miktar'],item['aciklama']
                    
                )
            )
            return True
        except Exception as e:
            print('numune kaydet hata : ', str(e))
            return False

   
             

    def __numuneMusteriGuncelle(self,item):
      try:
            self.data.update_insert(
                """
                update YeniTeklif_MusterilerTB set MusteriAdi=?,UlkeId=?
                where Id=?
                """,
                (
                    item['musteriAdi'],
                    item['ulkeId'],
                    item['id']
                )
            )
          
            return True
      except Exception as e:
            print('__teklifMusteriGuncelle Hata : ', str(e))
            return False


                



    def getKategoriList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            NumuneKategoriTB
           
            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.ID
            model.name = item.Urun

            liste.append(model)

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def getTedarikciList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            TedarikciTB
          

            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.ID
            model.name = item.FirmaAdi

            liste.append(model)

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def getBirimList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            UrunBirimTB
          

            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.ID
            model.name = item.BirimAdi

            liste.append(model)

        schema = GenelListSchema(many=True)

        return schema.dump(liste)  

    def getTemsilciList(self):
        
        liste = list()

        result = self.data.getList(
            """
           select * from KullaniciTB
          

            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.ID
            model.name = item.KullaniciAdi

            liste.append(model)

        schema = GenelListSchema(many=True)

        return schema.dump(liste)     

    def __kategoriId(self,item):
       
        kategoriId = None

        kontrol = self.data.getStoreList("Select count(*) as durum from NumuneKategoriTB where Urun=?",item['kategoriAdi'])[0].durum 

        if kontrol > 0:
            kategoriId = self.data.getStoreList("Select ID from NumuneKategoriTB where Urun=?",item['kategoriAdi'])[0].ID 
        else:
            self.data.update_insert("insert into NumuneKategoriTB (Urun) values (?)",item['kategoriAdi'])
            kategoriId = self.data.getList("Select Max(ID) as id from NumuneKategoriTB")[0].id 

        return kategoriId 

    

                     

    def getUrunList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from 
            YeniTeklif_UrunlerTB
            where UrunAdi is not null
            and UrunAdi != ''
            order by Sira asc

            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.Id
            model.name = item.UrunAdi

            liste.append(model)
           

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def __getCrossRange(self,g_tarihi):
        year = int(g_tarihi.split("-")[2])
        month = int(g_tarihi.split("-")[1])
        day = int(g_tarihi.split("-")[0])
        
        islem = DovizListem()
        crossRange = islem.getDovizKurListe(year,month,day)
        return crossRange
    
    def __getNormalRange(self,g_tarihi):
        year = g_tarihi.split("-")[2]
        month = g_tarihi.split("-")[1]
        day = g_tarihi.split("-")[0]
        
        islem = GuncelKurList()
        crossRange = islem.getDovizKurListe(str(year),str(month),str(day))
        return crossRange
  

   

    def getMusteriList(self):

        liste = list()

        result = self.data.getList("Select * from YeniTeklif_MusterilerTB")

        for item in result:

            model = MusteriModel()
            model.id = item.Id 
            model.musteriAdi = item.MusteriAdi 
            model.ulkeId = item.UlkeId

            liste.append(model)

        schema = MusteriSchema(many=True)

        return schema.dump(liste)

    def getUlkeList(self):

        liste = list()

        result = self.data.getList("select * from YeniTeklif_UlkeTB")

        for item in result:
            model = UlkeModel()
            model.id = item.Id 
            model.ulkeAdi = item.UlkeAdi 
            model.kod = item.Kod 
            model.iconFlags = item.Icon_Flags 
            model.pngFlags = item.Png_Flags
            liste.append(model)

        schema = UlkeSchema(many=True)

        return schema.dump(liste)

    def __dateConvert(self,value):

        _tarih = str(value).split('-')

        gun = int(_tarih[0])
        ay = int(_tarih[1])
        yil = int(_tarih[2])

        return datetime.datetime(yil,ay,gun)

    def __dateAdd(self,tarih):

        return tarih + datetime.timedelta(days=2)

    def __musteriKayit(self,item):
       
        musteriId = None
      
        kontrol = self.data.getStoreList("Select count(*) as durum from YeniTeklif_MusterilerTB where MusteriAdi=?",item['musteriAdi'])[0].durum 

        if kontrol > 0:
            musteriId = self.data.getStoreList("Select Id from YeniTeklif_MusterilerTB where MusteriAdi=?",item['musteriAdi'])[0].Id 
        else:
            self.data.update_insert("insert into YeniTeklif_MusterilerTB (musteriAdi) values (?)",item['musteriAdi'])
            musteriId = self.data.getList("Select Max(Id) as Id from YeniTeklif_MusterilerTB")[0].Id

        return musteriId 
         