from flask import request,jsonify
from flask_restful import Resource
from resource_api.operasyon.konteyner_fatura_giris import KonteynerFaturalar


class KonteynerIslemListApi(Resource):

    def get(self):

        islem = KonteynerFaturalar()

        data = {
            "konteyner_liste" : islem.getKonteynerList(),
            "siparis_list" : islem.getSiparisList()
        }

        return jsonify(data)  

class KonteynerKayitIslem(Resource):

    def post(self):

        data = request.get_json()

        islem = KonteynerFaturalar()

        result = islem.konteynerKaydet(data)

        return jsonify(result)  

class KonteynerDosyaGuncelle(Resource):

    def post(self):

        islem = KonteynerFaturalar()

        data = request.get_json()

        result = islem.KonteynerDosyaGuncelle(data)

        return jsonify({'Status' : result})             

class KonteynerDosyaKaydet(Resource):

    def post(self):

        data = request.get_json()

        konteynerIslem = KonteynerFaturalar()
        result = konteynerIslem.KonteynerDosyaKaydet(data)

        return jsonify({'status' : result})         

class KonteynerIslemModelListApi(Resource):

    def get(self,urunId):

        islem = KonteynerFaturalar()

        data = {

           
            "konteyner_liste" : islem.getKonteynerModel(urunId)
           
        }

        return jsonify(data)     

class KonteynerFormIslem(Resource):

    def get (self ,fatura_id,tur,siparis_no):

        islem = KonteynerFaturalar()
        result = islem.getFormIslem(fatura_id,tur,siparis_no)

        return result   