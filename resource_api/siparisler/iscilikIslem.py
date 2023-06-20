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
            iscilik.kaydet(giderVeri)

            return jsonify({'status' : True})
        except:
            return jsonify({'status' : False})

    def put(self):

        try:
            iscilik = Iscilik()
            giderVeri = request.get_json()
            iscilik.guncelle(giderVeri)

            return jsonify({'status' : True})
        except:
            return jsonify({'status' : False})

    

class IscilikKayitSil(Resource):

    def delete(self,id):
        try:
            iscilik = Iscilik()
            
            iscilik.sil(id)
            return jsonify({'status' : True})
        except Exception as e:
            print('delete : ', str(e))
            return jsonify({'status' : False})
