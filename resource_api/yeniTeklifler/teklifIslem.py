from helpers import SqlConnect,TarihIslemler,DegisiklikMain
from models.yeniTeklifler import *
from models.shared import GenelListModel,GenelListSchema
from flask_restful import Resource
from flask import jsonify,request
import datetime

class TeklifSilmeIslem(Resource):

    def delete(self,teklifid):

        teklifIslem = TeklifIslem()

        result = teklifIslem.teklifSil(teklifid)

        return jsonify({'status' : result})

class TeklifKayitIslem(Resource):
    def post(self):
        teklifIslem =TeklifIslem()

        veri = request.get_json()
        teklif = veri['teklif']
        urunler = veri['urunler']

        kayitDurum = teklifIslem.kaydet(teklif,urunler)

        return jsonify({'status' : kayitDurum})


    def put(self):
        
        teklifIslem = TeklifIslem()

        data = request.get_json()
        teklif = data['teklif']
        eklenenUrunler = data['eklenenUrunler']
        guncellenenUrunler = data['guncellenenUrunler']
        silinenUrunler = data['silinenUrunler']
        kullaniciAdi = data['kullaniciAdi']
        guncellenenMusteri = data['guncellenenMusteri']

        result = teklifIslem.guncelleme(teklif,eklenenUrunler,guncellenenUrunler,silinenUrunler,kullaniciAdi,guncellenenMusteri)

        return jsonify({'status' : result})


    def get(self):

        teklifIslem = TeklifIslem()

        data = {
            'teklif' : teklifIslem.getTeklifModel(),
            'teklifUrun' : teklifIslem.getTeklifUrunModel()
        }

        return jsonify(data)

class HatirlatmaDurumGuncellemesi(Resource):
    def put(self):
        
        teklifIslem = TeklifIslem()

        data = request.get_json()
        
        id = data['id']
        durum = data['isFalse']
        result = teklifIslem.getHatirlatmaGuncelleme(id,durum)

        return jsonify({'status' : result})



class TeklifProformaKaydet(Resource):

    def post(self):

        teklif = request.get_json()

        teklifIslem = TeklifIslem()
        result = teklifIslem.proformaKaydet(teklif)

        return jsonify({'Status' : result})

class TeklifDosyaKaydet(Resource):

    def post(self):

        teklif = request.get_json()

        teklifIslem = TeklifIslem()
        status = teklifIslem.teklifDosyaKaydet(teklif)

        return jsonify({'status' : status})

class TeklifSonGorulmeKaydet(Resource):

    def post(self):

        teklif = request.get_json()

        teklifIslem = TeklifIslem()
        result = teklifIslem.teklifSonGorulmeKaydet(teklif)

        return jsonify({'Status' : result})        

class TeklifNumuneKaydet(Resource):

    def post(self):

        teklif = request.get_json()

        teklifIslem = TeklifIslem()
        result = teklifIslem.teklifNumuneKaydet(teklif)

        return jsonify({'Status' : result})

class TeklifFormListeler(Resource):
    
    def get(self):

        teklif = TeklifIslem()

        data = {
            'teklifModel':teklif.getTeklifModel(),
            'teklifUrunModel':teklif.getTeklifUrunModel(),
            'kategoriList' : teklif.getKategoriList(),
            'urunList' : teklif.getUrunList(),
            'enBoyList' : teklif.getEnBoyList(),
            'kalinlikList' : teklif.getKalinlikList(),
            'yuzeyList' : teklif.getYuzeyList(),
            'musteriList' : teklif.getMusteriList(),
            'ulkeList' : teklif.getUlkeList(),
            'urunler':[]
        }

        return jsonify(data)

class TeklifMusterilerResourceApi(Resource):
    def get(self):
        teklif = TeklifIslem()
        customers = teklif.getMusteriList()
        return jsonify(customers)




class TeklifFormModel(Resource):
    
    def get(self,teklifId):

        teklif = TeklifIslem()

        data = {
            'teklifModel':teklif.getTeklif(teklifId),
            'teklifUrunModel':teklif.getTeklifUrunModel(),
            'kategoriList' : teklif.getKategoriList(),
            'urunList' : teklif.getUrunList(),
            'enBoyList' : teklif.getEnBoyList(),
            'kalinlikList' : teklif.getKalinlikList(),
            'yuzeyList' : teklif.getYuzeyList(),
            'musteriList' : teklif.getMusteriList(),
            'ulkeList' : teklif.getUlkeList(),
            'urunler':teklif.getTeklifUrun(teklifId),
        }

        return jsonify(data)

class TeklifDosyaSil(Resource):

    def delete(self,id):

        teklifIslem = TeklifIslem()

        status = teklifIslem.teklifDosyaSil(id)

        return jsonify({'status' : status})

class TeklifIslem:

    def __init__(self):
        self.data = SqlConnect().data
        self.tarihIslem = TarihIslemler()

    
    def getTeklifModel(self):
        model = TeklifModel()
        schema = TeklifSchema()
        return schema.dump(model)

    def getTeklifUrunModel(self):
        model = TeklifUrunKayitModel()
        schema = TeklifUrunKayitSchema()
        return schema.dump(model)

    def getTeklif(self,teklifId):

        item = self.data.getStoreList(
            """
            Select 

                yt.*,
                (select ym.Company from YeniTeklif_MusterilerTB ym where ym.Id =yt.MusteriId ) CompanyN,
                (select ym.Phone from YeniTeklif_MusterilerTB ym where ym.Id =yt.MusteriId ) PhoneN,
                (select ym.Mail from YeniTeklif_MusterilerTB ym where ym.Id =yt.MusteriId ) MailN,
                (select ym.Adress from YeniTeklif_MusterilerTB ym where ym.Id =yt.MusteriId ) Adress
                
                


            from YeniTeklifTB yt where Id=?
            """,(teklifId)
        )[0]

        model = TeklifModel()
        model.id = item.Id
        model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
        if item.HatirlatmaTarihi != None:
            model.hatirlatmaTarihi = self.tarihIslem.getDate(item.HatirlatmaTarihi).strftime("%d-%m-%Y")
        model.musteriId = item.MusteriId
        model.aciklama = item.Aciklama
        model.cfr = item.Cfr
        model.fob = item.Fob
        model.dtp = item.Dtp
        model.fca = item.Fca
        model.goruldu = item.Goruldu
        model.kullaniciId = item.KullaniciId
        model.takipEt = item.TakipEt
        model.kaynakYeri = item.KaynakYeri
        model.teklifYeri = item.TeklifYeri
        model.saritasNot = item.SaritasNot
        model.hatirlatmaAciklama = item.HatirlatmaAciklama
        model.satis = item.Satis
        if item.Numune_Giris_Tarihi != None:
            model.numuneGirisTarihi = self.tarihIslem.getDate(item.Numune_Giris_Tarihi).strftime("%d-%m-%Y")
        if item.Numune_Hatirlatma_Tarihi != None:
            model.numuneHatirlatmaTarihi = self.tarihIslem.getDate(item.Numune_Hatirlatma_Tarihi).strftime("%d-%m-%Y")
        model.numuneTrackingNo = item.Numune_Tracking_No
        model.numuneOdenenTutar = item.Numune_Odenen_Tutar
        model.numuneAlinanTutar = item.Numune_Musteriden_Alinan
        model.proformaPoNo = item.Proforma_Po_No
        if item.Proforma_Tarih != None:
            model.proformaTarih = self.tarihIslem.getDate(item.Proforma_Tarih).strftime("%d-%m-%Y")
        model.proformaTutar = item.Proforma_Tutar
        model.teklifCloud = item.Teklif_Cloud
        model.teklifCloudDosya = item.Teklif_Cloud_Dosya
        model.sonGorulmeCloud = item.SonGorulme_Cloud
        model.sonGorulmeCloudDosya = item.SonGorulme_Cloud_Dosya
        model.proformaCloud = item.Proforma_Cloud
        model.proformaCloudDosya = item.Proforma_Cloud_Dosya
        model.numuneCloud = item.Numune_Cloud
        model.numuneCloudDosya = item.Numune_Cloud_Dosya
        model.teklifOncelik = item.TeklifOncelik
        model.proformaNot = item.ProformaNot 
        model.numuneNot = item.NumuneNot
        model.blist = item.BList 
        model.company = item.CompanyN
        model.email = item.MailN
        model.phone = item.PhoneN
        model.adress = item.Adress
        schema = TeklifSchema()

        return schema.dump(model)
    def getHatirlatmaGuncelleme(self,id,durum):
        if durum == False:
            durum = 0
        try:
            self.data.update_insert(
                """
                    update YeniTeklifTB SET HatirlatilmaDurumu=? where Id =?
                
                """,(durum,id)
            )
        
            return True 
        except Exception as e:
            print('Teklif Güncelleme Hata :', str(e))
            return False
    def getTeklifUrun(self,teklifId):

        result = self.data.getStoreList(
            """
            select
            t.Id,
            t.TeklifId,
            t.Tarih,
            t.KategoriId,
            k.KategoriAdi,
            t.UrunId,
            u.UrunAdi,
            t.EnBoyId,
            e.EnBoy,
            t.KalinlikId,
            o.Kalinlik,
            t.YuzeyIslemId,
            y.IslemAdi,
            t.FobFiyat,
            t.TeklifFiyat,
            t.Birim,
            yt.Cfr,
            yt.Fob,
            yt.Dtp,
            yt.Fca,
            t.FcaFiyat,
            t.CFiyat,
            t.DFiyat
            from
            YeniTeklif_UrunKayitTB t,YeniTeklif_KategorilerTB k,YeniTeklif_UrunlerTB u,
            YeniTeklif_Olcu_EnBoyTB e,YeniTeklif_Olcu_KalinlikTB o,YeniTeklif_YuzeyIslemTB y,
            YeniTeklifTB yt
            where
            t.KategoriId = k.Id and u.Id=t.UrunId and e.id = t.EnBoyId
            and o.id = t.KalinlikId and y.Id=t.YuzeyIslemId and yt.Id=t.TeklifId and t.TeklifId=?
            """,(teklifId)
        )

        liste = list()

        for item in result:

            model = TeklifUrunKayitModel()
            model.id = item.Id
            model.teklifId = item.TeklifId
            yuklemeTip = ""
            if item.Cfr == True:
                yuklemeTip = "Cfr"
            if item.Dtp == True:
                yuklemeTip = "Ddp"
            if item.Fca == True:
                yuklemeTip = "Fca"
            if item.Fob == True:
                yuklemeTip = "Fob"
            
            

            model.yuklemeTipi = yuklemeTip

            if item.Tarih != None:
                model.tarih = self.tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            model.kategoriId = item.KategoriId 
            model.kategoriAdi = item.KategoriAdi 
            model.urunId = item.UrunId 
            model.urunAdi = item.UrunAdi 
            model.enBoyId = item.EnBoyId 
            model.enBoy = item.EnBoy 
            model.kalinlikId = item.KalinlikId 
            model.kalinlik = item.Kalinlik 
            model.yuzeyIslemId = item.YuzeyIslemId
            model.yuzeyIslem = item.IslemAdi
            if item.FobFiyat != None:
                
                model.fobFiyat = item.FobFiyat
            else:
                model.fobFiyat = 0
                
                
            if item.FcaFiyat != None:
                
                model.fcaFiyat = item.FcaFiyat
            else:
                model.fcaFiyat = 0
                
            if item.CFiyat != None:
                
                model.cFiyat = item.CFiyat
            else:
                model.cFiyat = 0
                
            if item.DFiyat != None:
                
                model.dFiyat = item.DFiyat
            else:
                model.dFiyat = 0
            
            model.teklifFiyat = item.TeklifFiyat
            model.birim = item.Birim

            liste.append(model)

        schema = TeklifUrunKayitSchema(many=True)

        return schema.dump(liste)


    def kaydet(self,teklif,urunler):
        
        dtMusteriler = self.data.getList("Select * from YeniTeklif_MusterilerTB")
     
        kayitDurum = self.__teklifKayit(teklif,dtMusteriler)
        teklifId = None
        if kayitDurum == True:
            teklifId = self.data.getStoreList("Select Max(Id) as Id from YeniTeklifTB where KullaniciId=?",(teklif['kullaniciId']))[0].Id
            for item in urunler:
                kayitDurum = self.__teklifUrunKayit(item,teklifId)
        kullaniciAdi = teklif['kullaniciAdi'].capitalize()
        info = kullaniciAdi + ' ' + 'Yeni Teklif Girişi Yaptı'
        DegisiklikMain().setYapilanDegisiklikBilgisi(kullaniciAdi,info)

        return kayitDurum
    
    def guncelleme(self,teklif,eklenenUrunler,guncellenenUrunler,silinenUrunler,kullaniciAdi,guncellenenMusteri):

        dtKullanici = self.data.getStoreList("Select * from KullaniciTB where KullaniciAdi=?",(kullaniciAdi))
        dtMusteriler = self.data.getList("Select * from YeniTeklif_MusterilerTB ")
        kullaniciId = int(dtKullanici[0].ID)
        
    
        kayitDurum = self.__teklifGuncelleme(teklif)
        
        
            
        if len(guncellenenUrunler) > 0:
            for item in guncellenenUrunler:
                
                self.__teklifUrunGuncelle(item)

        
        if len(guncellenenMusteri) > 0:
            for item in guncellenenMusteri:
                self.__teklifMusteriGuncelle(item)
                 
      
            

        if len(eklenenUrunler) > 0:
            
            for item in eklenenUrunler:
                
                result = self.__eklenenUrunKontrol(item['teklifId'],item['kategoriId'],item['urunId'],item['enBoyId'],item['yuzeyIslemId'],item['kalinlikId'],item['fobFiyat'],item['birim'])
                
                if result == True:
                    pass
                else:
                    
                    self.__teklifUrunKayit(item,teklif['id'])
                

        if len(silinenUrunler) > 0:
            for item in silinenUrunler:
              
                self.__teklifUrunSil(item['id'])
        kullaniciAdi = kullaniciAdi.capitalize()
        info = kullaniciAdi + ' ' + 'Teklif Kaydını Güncelledi'
        DegisiklikMain().setYapilanDegisiklikBilgisi(kullaniciAdi,info)
        return kayitDurum
    
    def teklifSil(self,teklifid):

        try:

            #teklif sil
            self.data.update_insert("Delete from YeniTeklifTB where Id=?",(teklifid))
            #teklif urun kayıt silme
            self.data.update_insert("Delete from YeniTeklif_UrunKayitTB where TeklifId=?",(teklifid))

            return True
        except Exception as e:
            print('teklifSil Hata : ', str(e))
            return False

    def __eklenenUrunKontrol(self,teklifid,kategoriId,urunId,enBoyId,yuzeyIslemId,kalinlik,fobFiyat,birim):
        result = self.data.getStoreList("""
                                            select * from YeniTeklif_UrunKayitTB where 
                                            TeklifId =? and 
                                            KategoriId=? and 
                                            UrunId=? and 
                                            EnBoyId=? and 
                                            YuzeyIslemId=? and 
                                            KalinlikId=? and 
                                            FobFiyat=? and 
                                            Birim=?
                                        
                                        """,(int(teklifid),int(kategoriId),int(urunId),int(enBoyId),int(yuzeyIslemId),int(kalinlik),int(fobFiyat),birim))
        if len(result)>0:
            return True
    
    
    def proformaKaydet(self,teklif):

        try:
            self.data.update_insert(
                """
                update YeniTeklifTB set Proforma_Po_No=?,Proforma_Tarih=?,Proforma_Tutar=?,
                Proforma_Cloud=1,Proforma_Cloud_Dosya=?,ProformaNot=? where Id=?
                """,(
                    teklif['proformaPoNo'],teklif['proformaTarih'],teklif['proformaTutar'],
                    teklif['proformaCloudDosya'],teklif['proformaNot'], teklif['id']
                )
            )
            return True
        except Exception as e:
            print("proformaKaydet Hata : ", str(e))
    
    def teklifDosyaKaydet(self,teklif):
        try:
            self.data.update_insert(
                """
                update YeniTeklifTB set Teklif_Cloud=?,Teklif_Cloud_Dosya=? where Id=?
                """,
                (
                    teklif['teklifCloud'],teklif['teklifCloudDosya'],teklif['id']
                )
            )
            return True
        except Exception as e:
            print('teklifDosyaKaydet Hata : ',str(e))
            return False

    def teklifSonGorulmeKaydet(self,teklif):
        try:
            self.data.update_insert(
                """
                update YeniTeklifTB set SonGorulme_Cloud=?,SonGorulme_Cloud_Dosya=? where Id=?
                """,
                (
                    teklif['sonGorulmeCloud'],teklif['sonGorulmeCloudDosya'],teklif['id']
                )
            )
            return True
        except Exception as e:
            print('teklifSonGorulmeKaydet Hata : ',str(e))
            return False        

    def teklifNumuneKaydet(self,teklif):
        try:
            print('numune dosya : ', teklif['numuneCloudDosya'])

            numuneGirisTarihi = None
            numuneHatirlatmaTarihi = None
            numuneHatirlatmaSonTarih = None
            if len(teklif['numuneGirisTarihi']) > 0:
                #numuneGirisTarihi = teklif['numuneGirisTarihi']
                numuneGirisTarihi = teklif['numuneGirisTarihi']
                forMat = '%d-%m-%Y'
                numuneGirisTarihi = datetime.datetime.strptime(numuneGirisTarihi, forMat)
                numuneGirisTarihi = numuneGirisTarihi.date()
            if len(teklif['numuneHatirlatmaTarihi']) > 0:
                numuneHatirlatmaTarihi = self.__dateConvert(teklif['numuneHatirlatmaTarihi'])
                numuneHatirlatmaSonTarih = self.__dateAdd(numuneHatirlatmaTarihi)
            self.data.update_insert(
                """
                update YeniTeklifTB set Numune_Giris_Tarihi=?,Numune_Hatirlatma_Tarihi=?,Numune_Hatirlatma_SonTarih=?,
                Numune_Tracking_No=?,Numune_Odenen_Tutar=?,Numune_Musteriden_Alinan=?,Numune_Cloud=1,
                Numune_Cloud_Dosya=?,NumuneNot=? where Id=?

                """,(
                    numuneGirisTarihi,numuneHatirlatmaTarihi,numuneHatirlatmaSonTarih,teklif['numuneTrackingNo'],
                    teklif['numuneOdenenTutar'],teklif['numuneAlinanTutar'],teklif['numuneCloudDosya'],
                    teklif['numuneNot'], teklif['id']
                )
            )

            return True
        except Exception as e:
            print('teklifNumuneKaydet Hata : ',str(e))
            return False

    def teklifDosyaSil(self,teklifId):
        try:
            self.data.update_insert(
                """
                update YeniTeklifTB set Teklif_Cloud=0,Teklif_Cloud_Dosya='' where Id=?
                """,
                (teklifId)
            )

            return True
        except Exception as e:
            print('teklifDosyaSil Hata : ',str(e))
            return False

    def __teklifKayit(self,item,dtMusteriler):
        try:
            musteriId = item['musteriId']
            if musteriId == None:
                musteriId = self.__musteriKayit(item['musteriAdi'],item['ulkeId'],item,item['kullaniciId'])
            else:
                musteriId = self.__musteriGuncelle(musteriId,item)
                
            teklifTarihi = self.__dateControl(item['tarih'])
            hatirlatmaTarihiİlk = self.__dateControl(item['hatirlatmaTarihi'])
            numuneGirisTarihi = self.__dateControl(item['numuneGirisTarihi'])
            numuneHatirlatmaTarihiİlk = self.__dateControl(item['numuneHatirlatmaTarihi'])
            proformaTarihi = self.__dateControl(item['proformaTarih'])
            
            self.data.update_insert(
                """
                insert into YeniTeklifTB (
                    Tarih,
                    HatirlatmaTarihi,
                    HatirlatmaSonTarih,
                    MusteriId,
                    Aciklama,
                    Cfr,
                    Fob,
                    Dtp,
                    Fca,
                    Goruldu,
                    KullaniciId,
                    TakipEt,
                    KaynakYeri,
                    TeklifYeri,
                    SaritasNot,
                    HatirlatmaAciklama,
                    Satis,
                    Numune_Giris_Tarihi,
                    Numune_Hatirlatma_Tarihi,
                    Numune_Hatirlatma_SonTarih,
                    Numune_Tracking_No,
                    Numune_Odenen_Tutar,
                    Numune_Musteriden_Alinan,
                    Proforma_Po_No,
                    Proforma_Tarih,
                    Proforma_Tutar,
                    Teklif_Cloud,
                    Teklif_Cloud_Dosya,
                    Proforma_Cloud,
                    Proforma_Cloud_Dosya,
                    Numune_Cloud,
                    Numune_Cloud_Dosya,
                    TeklifOncelik,
                    ProformaNot,
                    NumuneNot,
                    BList,
                    Company,
                    Email,
                    Phone
                )
                values
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                    )
                """,(
                    teklifTarihi,
                    hatirlatmaTarihiİlk,
                    hatirlatmaTarihiİlk,
                    musteriId,
                    item['aciklama'],
                    item['cfr'],
                    item['fob'],
                    item['dtp'],
                    item['fca'],
                    item['goruldu'],
                    item['kullaniciId'],
                    item['takipEt'],
                    item['kaynakYeri'],
                    item['teklifYeri'],
                    item['saritasNot'],
                    item['hatirlatmaAciklama'],
                    item['satis'],
                    numuneGirisTarihi,
                    numuneHatirlatmaTarihiİlk,
                    numuneHatirlatmaTarihiİlk,
                    item['numuneTrackingNo'],
                    item['numuneOdenenTutar'],
                    item['numuneAlinanTutar'],
                    item['proformaPoNo'],
                    proformaTarihi,
                    item['proformaTutar'],
                    item['teklifCloud'],
                    item['teklifCloudDosya'],                    
                    item['proformaCloud'],
                    item['proformaCloudDosya'],
                    item['numuneCloud'],
                    item['numuneCloudDosya'],
                    item['teklifOncelik'],
                    item['proformaNot'],
                    item['numuneNot'],
                    item['blist'],item['company'],item['email'],item['phone']
                )
            )
            
            
            
            return True
        except Exception as e:
            print('Teklif kaydet hata : ', str(e))
            return False

    def __dateControl(self,value):
        if(value == None or value == ""):
            return None
        else:
            date = value.split('-')
            return date[2] + '-' + date[1] + '-' + date[0]
    
    def __teklifUrunKayit(self,item,teklifId):
        try:
           
            item['kategoriId'] = self.__kategoriId(item)
            item['urunId'] = self.__urunId(item)
            item['enBoyId'] = self.__enboyId(item)
            item['kalinlikId'] = self.__KalinliKId(item)  
            item['yuzeyIslemId'] = self.__yuzeyisleMId(item)

            self.data.update_insert(
                """
                insert into YeniTeklif_UrunKayitTB (Tarih,TeklifId,KategoriId,UrunId,EnBoyId,
                YuzeyIslemId,KalinlikId,FobFiyat,TeklifFiyat,Birim,FcaFiyat,CFiyat,DFiyat)
                values
                (?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,(
                    item['tarih'],teklifId,item['kategoriId'],item['urunId'],item['enBoyId'],
                    item['yuzeyIslemId'],item['kalinlikId'],item['fobFiyat'],item['teklifFiyat'],
                    item['birim'],item['fcaFiyat'],item['cFiyat'],item['dFiyat']
                )
            )
            
           
            return True 
        except Exception as e:
            print('Teklif Kaydet Ürün Hata : ',str(e))
            return False

    def __teklifGuncelleme(self,item):
        
        try:
            
            musteriId = item['musteriId']
            if musteriId == None:
                musteriId = self.__musteriKayit(item['musteriAdi'],item['ulkeId'])
               
            teklifTarihi = self.__dateControl(item['tarih'])
            hatirlatmaTarihiİlk = self.__dateControl(item['hatirlatmaTarihi'])
            numuneGirisTarihi = self.__dateControl(item['numuneGirisTarihi'])
            numuneHatirlatmaTarihiİlk = self.__dateControl(item['numuneHatirlatmaTarihi'])
            proformaTarihi = self.__dateControl(item['proformaTarih'])
            self.data.update_insert(
                """
                update YeniTeklifTB set 
                Tarih=?,
                HatirlatmaTarihi=?,
                HatirlatmaSonTarih=?,
                MusteriId=?,
                Aciklama=?,
                Cfr=?,
                Fob=?,
                Dtp=?,
                Fca=?,
                Goruldu=?,               
                TakipEt=?,
                KaynakYeri=?,
                TeklifYeri=?,
                SaritasNot=?,
                HatirlatmaAciklama=?,
                Satis=?,
                Numune_Giris_Tarihi=?,
                Numune_Hatirlatma_Tarihi=?,
                Numune_Hatirlatma_SonTarih=?,
                Numune_Tracking_No=?,
                Numune_Odenen_Tutar=?,
                Numune_Musteriden_Alinan=?,
                Proforma_Po_No=?,
                Proforma_Tarih=?,
                Proforma_Tutar=?,
                Teklif_Cloud=?,
                Teklif_Cloud_Dosya=?,
                Proforma_Cloud=?,
                Proforma_Cloud_Dosya=?,
                SonGorulme_Cloud=?,
                SonGorulme_Cloud_Dosya=?,
                Numune_Cloud=?,
                Numune_Cloud_Dosya=?,
                TeklifOncelik=?,
                ProformaNot=?,
                NumuneNot=?,
                BList=?,
                HatirlatilmaDurumu=?,
                Company=?,
                Email=?,
                Phone=?
                where Id=?
                """,
                (
                    teklifTarihi,
                    hatirlatmaTarihiİlk,
                    hatirlatmaTarihiİlk,
                    musteriId,
                    item['aciklama'],
                    item['cfr'],
                    item['fob'],
                    item['dtp'],
                    item['fca'],
                    item['goruldu'],                    
                    item['takipEt'],
                    item['kaynakYeri'],
                    item['teklifYeri'],
                    item['saritasNot'],
                    item['hatirlatmaAciklama'],
                    item['satis'],
                    numuneGirisTarihi,
                    numuneHatirlatmaTarihiİlk,
                    numuneHatirlatmaTarihiİlk,
                    item['numuneTrackingNo'],
                    item['numuneOdenenTutar'],
                    item['numuneAlinanTutar'],
                    item['proformaPoNo'],
                    proformaTarihi,
                    item['proformaTutar'],
                    item['teklifCloud'],
                    item['teklifCloudDosya'],
                    item['proformaCloud'],
                    item['proformaCloudDosya'],
                    item['sonGorulmeCloud'],
                    item['sonGorulmeCloudDosya'],
                    item['numuneCloud'],
                    item['numuneCloudDosya'],
                    item['teklifOncelik'],
                    item['proformaNot'],
                    item['numuneNot'],
                    item['blist'],
                    item['hatirlatmaDurum'],
                    item['company'],
                    item['email'],
                    item['phone'],
                    
                    item['id']
                )
            )

            return True 
        except Exception as e:
            print('Teklif Güncelleme Hata :', str(e))
            return False
    
    def __teklifMusteriGuncelle(self,item):
      try:
            self.data.update_insert(
                """
                update YeniTeklif_MusterilerTB set MusteriAdi=?,UlkeId=?,Company=?,Mail=?,Phone=?,Adress=?
                where Id=?
                """,
                (
                    item['musteriAdi'],
                    item['ulkeId'],
                    item['company'],
                    item['email'],
                    item['phone'],
                    item['adress'],
                    item['id']
                )
            )

            return True
      except Exception as e:
            print('__teklifMusteriGuncelle Hata : ', str(e))
            return False

    def __teklifUrunGuncelle(self,item):
        try:
            enboyID = self.__enboyId(item)
            tarih = item['tarih']
            forMat = '%d-%m-%Y'
            tarih = datetime.datetime.strptime(tarih, forMat)
            tarih = tarih.date()
            self.data.update_insert(
                """
                update YeniTeklif_UrunKayitTB set 
                Tarih=?,
                KategoriId=?,
                UrunId=?,
                EnBoyId=?,
                YuzeyIslemId=?,
                KalinlikId=?,
                FobFiyat=?,
                TeklifFiyat=?,
                Birim=?,
                FcaFiyat=?,
                CFiyat=?,
                DFiyat=?
                
                where Id=?
                 
                """,(
                    tarih,
                    item['kategoriId'],
                    item['urunId'],
                    enboyID,
                    item['yuzeyIslemId'],
                    item['kalinlikId'],
                    item['fobFiyat'],
                    item['teklifFiyat'],
                    item['birim'],
                    item['fcaFiyat'],
                    item['cFiyat'],
                    item['dFiyat'],
                    item['id']
                )
            )



            return True
        except Exception as e:
            print('__teklifUrunGuncelle hata ',str(e))
            return False

    def __teklifUrunSil(self,kayitId):
        try:

            self.data.update_insert(
                """
                delete from YeniTeklif_UrunKayitTB where Id=?
                """,(kayitId)
            )

            return True
        except Exception as e:
            print('__teklifUrunSil hata : ',str(e))
            return False

    def getKategoriList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            YeniTeklif_KategorilerTB
            order by Sira asc

            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.Id
            model.name = item.KategoriAdi

            liste.append(model)

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def __kategoriId(self,item):
        
        kategoriId = None

        kontrol = self.data.getStoreList("Select count(*) as durum from YeniTeklif_KategorilerTB where KategoriAdi=?",item['kategoriAdi'])[0].durum 

        if kontrol > 0:
            kategoriId = self.data.getStoreList("Select ID from YeniTeklif_KategorilerTB where KategoriAdi=?",item['kategoriAdi'])[0].ID 
        else:
            self.data.update_insert("insert into YeniTeklif_KategorilerTB (KategoriAdi) values (?)",item['kategoriAdi'])
            kategoriId = self.data.getList("Select Max(ID) as id from YeniTeklif_KategorilerTB")[0].id 

        return kategoriId 

    def __urunId(self,item):  
       
        urunId = None
        kontrol = self.data.getStoreList("Select count(*) as durum from YeniTeklif_UrunlerTB where UrunAdi=?",item['urunAdi'])[0].durum 
       
        if kontrol > 0:
            urunId = self.data.getStoreList("Select ID from YeniTeklif_UrunlerTB where UrunAdi=?",item['urunAdi'])[0].ID 
           
        else:
            self.data.update_insert("insert into YeniTeklif_UrunlerTB (UrunAdi) values (?)",item['urunAdi'])
            urunId = self.data.getList("Select Max(ID) as id from YeniTeklif_UrunlerTB")[0].id
             
      
        return urunId   

    def __enboyId(self,item):
        
        enBoyId = None

        kontrol = self.data.getStoreList("Select count(*) as durum from YeniTeklif_Olcu_EnBoyTB where EnBoy=?",item['enBoy'])[0].durum 

        if kontrol > 0:
            enBoyId = self.data.getStoreList("Select id from YeniTeklif_Olcu_EnBoyTB where EnBoy=?",item['enBoy'])[0].id 
           
        else:
            self.data.update_insert("insert into YeniTeklif_Olcu_EnBoyTB (EnBoy) values (?)",item['enBoy'])
            enBoyId = self.data.getList("Select Max(id) as id from YeniTeklif_Olcu_EnBoyTB")[0].id
            
       
        return enBoyId 

    def __KalinliKId(self,item):  
       
        kalinlikId = None
       
        kontrol = self.data.getStoreList("Select count(*) as durum from YeniTeklif_Olcu_KalinlikTB where Kalinlik=?",item['kalinlik'])[0].durum 
       
        if kontrol > 0:
            kalinlikId = self.data.getStoreList("Select id from YeniTeklif_Olcu_KalinlikTB where Kalinlik=?",item['kalinlik'])[0].id 
           
        else:
            self.data.update_insert("insert into YeniTeklif_Olcu_KalinlikTB (Kalinlik) values (?)",item['kalinlik'])
            kalinlikId = self.data.getList("Select Max(id) as id from YeniTeklif_Olcu_KalinlikTB")[0].id
            
       
        return kalinlikId  

    def __yuzeyisleMId(self,item):
        
        yuzeyIslemId = None
       
        kontrol = self.data.getStoreList("Select count(*) as durum from YeniTeklif_YuzeyIslemTB where IslemAdi=?",item['yuzeyIslem'])[0].durum 
       
        if kontrol > 0:
            yuzeyIslemId = self.data.getStoreList("Select Id from YeniTeklif_YuzeyIslemTB where IslemAdi=?",item['yuzeyIslem'])[0].Id
           
        else:
            self.data.update_insert("insert into YeniTeklif_YuzeyIslemTB (IslemAdi) values (?)",item['yuzeyIslem'])
            yuzeyIslemId = self.data.getList("Select Max(Id) as id from YeniTeklif_YuzeyIslemTB")[0].id
            
       
        return yuzeyIslemId                    

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

    def getEnBoyList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            YeniTeklif_Olcu_EnBoyTB           
            order by Sira asc

            """
        )        
        for item in result:
            model = GenelListModel()
            model.id = item.id
            model.name = item.EnBoy

            liste.append(model)

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def getYuzeyList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            YeniTeklif_YuzeyIslemTB           
            order by Sira

            """
        )
        
        for item in result:
            model = GenelListModel()
            model.id = item.Id
            model.name = item.IslemAdi

            liste.append(model)
           

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def getKalinlikList(self):
        
        liste = list()

        result = self.data.getList(
            """
            select
            *
            from
            YeniTeklif_Olcu_KalinlikTB            
            order by Sira
            """
        )
       
        for item in result:
            model = GenelListModel()
            model.id = item.id
            model.name = item.Kalinlik

            liste.append(model)
            

        schema = GenelListSchema(many=True)

        return schema.dump(liste)

    def getMusteriList(self):

        liste = list()

        result = self.data.getList("Select * from YeniTeklif_MusterilerTB")

        for item in result:

            model = MusteriModel()
            model.id = item.Id 
            model.musteriAdi = item.MusteriAdi 
            model.ulkeId = item.UlkeId
            model.company = item.Company
            model.email = item.Mail
            model.phone = item.Phone
            model.adress = item.Adress

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

    def __musteriKayit(self,musteriAdi,ulkeId,item,kullaniciId):
        try:
            
            self.data.update_insert(
                """
                insert into YeniTeklif_MusterilerTB(MusteriAdi,Company,Mail,Phone,UlkeId,Adress,Kullanici) VALUES(?,?,?,?,?,?,?)
                """,(musteriAdi,item['company'],item['email'],item['phone'],ulkeId,item['adress'],kullaniciId)
            )
            
            musteriId = self.data.getStoreList(
                """
                Select Id from YeniTeklif_MusterilerTB where MusteriAdi=? and
                UlkeId=?
                """,
                (musteriAdi,ulkeId)
            )[0].Id
            return musteriId
        except Exception as e:
            print("__musteriKayit Hata : ",str(e))
            return False

    def __musteriGuncelle(self,musteriId,item):
        try:
            self.data.update_insert("""

                                        update YeniTeklif_MusterilerTB SET Company=?,Mail=?,Phone=?,Adress=? where Id=?
                                    """,(item['company'],item['email'],item['phone'],item['adress'],musteriId))
            return musteriId
            
        except Exception as e:
            print('__musteriGuncelle hata',str(e))
            return False
    
    