from flask_restful import Resource
from flask import jsonify,request
from resource_api.operasyon.nakliye_listeler import Listeler
from resource_api.operasyon.nakliye_islem import NakliyeIslem

class NakliyeListeApi(Resource): 

    def get(self):

        islem = Listeler()

        siparis_liste = islem.getNakliyeFirmaListe()

        return siparis_liste

class NakliyeIslemListApi(Resource):

    def get(self):

        islem = NakliyeIslem()

        data = {

           
            "nakliye_liste" : islem.getNakliyeList(),
            "siparis_list" : islem.getSiparisList()
        }

        return jsonify(data)    

class NakliyeKayitIslem(Resource):

    def post(self):

        data = request.get_json()

        islem = NakliyeIslem()

        result = islem.nakliyeKaydet(data)

        return jsonify(result)       


class NakliyeDosyaKaydet(Resource):

    def post(self):

        nakliye = request.get_json()

        nakliyeIslem = NakliyeIslem()
        result = nakliyeIslem.NakliyeDosyaKaydet(nakliye)

        return jsonify({'status' : result})            

class NakliyeIslemModelListApi(Resource):

    def get(self,urunId):

        islem = NakliyeIslem()

        data = {
           
             "nakliye_liste" : islem.getNakliyeModel(urunId)
         }

        return jsonify(data)   

class NakliyeIslemModelApi(Resource):

    def get(self):

        islem = NakliyeIslem()

        data = {
        
          "nakliye_model"  : islem.getTNakliyeUrunModel()
           
        }

        return jsonify(data)          
        
class NakliyeFormIslem(Resource):

    def get (self ,firmaId,evrakAdi,siparisNo):
        islem = NakliyeIslem()
        result = islem.getFormIslem(firmaId,evrakAdi,siparisNo)

        return result         

class NakliyeFaturaSil(Resource):
    def get(self,siparisNo,evrakAdi):
        islem = NakliyeIslem()
        status = islem.getNakliyeDosyaSil(siparisNo,evrakAdi)
        islem = Listeler()
        nakliye_listesi = islem.getNakliyeFirmaListe()
        return jsonify({'status':status,'nakliyeList':nakliye_listesi})
    
class NakliyeFaturaChange(Resource):
    def post(self):
        datas = request.get_json()
        islem = NakliyeIslem()
        status = islem.setChangeNakliye(datas)
        islem = Listeler()
        nakliye_listesi = islem.getNakliyeFirmaListe()
        return jsonify({'status':status,'nakliyeList':nakliye_listesi})