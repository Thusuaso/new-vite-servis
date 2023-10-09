from views.siparisler import Iscilik
from flask_restful import Resource
from flask import request,jsonify
from helpers import DegisiklikMain
class IscilikList(Resource): 
    def get(self,siparisNo,urunKartId):

        iscilik = Iscilik()

        result = iscilik.getIscilikList(siparisNo,urunKartId)

        return result
    
class IscilikDataIslem(Resource):
    def get(self):

        iscilik = Iscilik()

        result = iscilik.getIscilikModel()

        return result
    
    def post(self):

        try:
            iscilik = Iscilik()
            giderVeri = request.get_json()
            result = iscilik.kaydet(giderVeri)

            return jsonify(result)
        except:
            return jsonify(result)

    def put(self):

        try:
            iscilik = Iscilik()
            giderVeri = request.get_json()
            result = iscilik.guncelle(giderVeri)

            return jsonify(result)
        except:
            return jsonify(result)

    

class IscilikKayitSil(Resource):

    def delete(self,id):
        try:
            iscilik = Iscilik()
            
            result = iscilik.sil(id)
            return jsonify(result)
        except Exception as e:
            print('delete : ', str(e))
            return jsonify(result)
