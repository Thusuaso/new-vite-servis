from helpers import SqlConnect,TarihIslemler
from flask_restful import Resource
from flask import jsonify,request,send_file
from models.operasyon.evrakYukleme import *
import datetime

class EvrakFaturaKayitIslem(Resource):
    def post(self):  # post veri eklemek için kullanılır
        faturaIslem =EvrakFaturaIslem()

        islem = request.get_json()
       
        evrak = islem
       
        kayitDurum = faturaIslem.kaydet(evrak)
       
        return jsonify({'status' : kayitDurum}) 

    def get(self):

        faturaIslem = EvrakFaturaIslem()

        data = {
            'evrak' : faturaIslem.getEvrakFaturaModel(),
            
        }
       
        return jsonify(data)  
class EvrakFaturaIslem:

    def __init__(self):
        self.data = SqlConnect().data
        self.tarihIslem = TarihIslemler()

     
    def getEvrakFaturaModel(self):
        model = FaturaKayitModel()
        schema = FaturaKayitSchema()
        return schema.dump(model)

    def kaydet(self,item):
       
        
        kayitDurum = self.__faturaKayit(item)
        return kayitDurum

    def __faturaKayit(self,item):
        try:    
            date = datetime.datetime.now()    
            self.data.update_insert(
                """
                insert into SiparisFaturaKayitTB 
                   
                  (  
                   Tarih,
                   FaturaKayitID,
                   SiparisFaturaTurID,
                   SiparisNo,
                   YuklemeEvrakID,
                   YuklemeEvrakDurumID,
                   EvrakAdi,
                   EvrakYuklemeTarihi,KullaniciID)
                   
                values (?, ?,?,?,?,?,?,?,?)
                """,(date, 0,0,item['siparisno'],item['id'],2,item['siparisno'] + '.pdf' ,date,item['kullaniciId'])
            )
            return True
        except Exception as e:
            print('__fatura Kayit kaydet hata : ', str(e))
            return False
        
        
class EtiketKayitIslemApi(Resource):
    def post(self):
        datas = request.get_json()
        islem = EtiketIslem()
        result = islem.kaydet(datas)
        return jsonify({'status' : result}) 

class EtiketListApi(Resource):
    def get(self,etiketNo):
        islem = EtiketIslem()
        result = islem.getEtiketLink(etiketNo)
        return jsonify(result)
    
class EtiketIslem:
    def __init__(self):
        self.data = SqlConnect().data
        
    def kaydet(self,datas):
        try:
            
            musteriNo = datas['musterino']
            etiketDosyaAdi = datas['dosya_adi']
            etiketKodu = datas['etiketKodu']
            self.data.update_insert("""
                                insert into Etiketler(musteriID,etiketDosyaAdi,etiketKodu) VALUES(?,?,?)
                            
                            
                            """,(musteriNo,etiketDosyaAdi,etiketKodu))
            print('Etiket Dosya Bilgileri Kaydedildi')
            return True
        except Exception as e:
            print('Etiket Kaydetme Hatalı',str(e))
            return False
    
    def getEtiketLink(self,etiketkodu):
        result = self.data.getStoreList("""
                                        
                                            select musteriID,etiketDosyaAdi from Etiketler where etiketKodu=?
                                        
                                        """,(etiketkodu))
        link =  f"https://file-service.mekmar.com/file/download/etiket/{result[0][0]}/{result[0][1]}"
        return link
    
    
class EvrakSilmeIslemApi(Resource):
    def get(self,id,siparisNo):
        islem = EvrakSilmeIslem()
        result = islem.setDeleteEvrak(id,siparisNo)
        
        return jsonify(result)
    
class EvrakSilmeIslem:
    def __init__(self):
        self.data = SqlConnect().data
    
    def setDeleteEvrak(self,id,siparisNo):
        try:
            
            self.data.update_insert("""
                                        delete SiparisFaturaKayitTB where ID=? and SiparisNo=?
                                    
                                    """,(id,siparisNo))
            return True
        except Exception as e:
            print("setDeleteEvrak hata",str(e))
            return False