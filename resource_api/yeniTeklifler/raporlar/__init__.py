from resource_api.yeniTeklifler.raporlar.tumTeklifler import TumTeklifler 
from resource_api.yeniTeklifler.raporlar.eskiTeklifler import EskiTeklifler
from flask_restful import Resource
from flask import jsonify,request
class TumTeklifListApi(Resource):

    def get(self):

        teklifler = TumTeklifler()

        tekliflist = teklifler.getTumTeklifList()


        return tekliflist

class EskiTekliflerListApi(Resource):

    def get(self):

        teklifler = EskiTeklifler()

        tekliflist = teklifler.getEskiTeklifListesi()

        return tekliflist
    
class EnBoyEkleApi(Resource):
    def post(self):
        dat = request.get_json()
        teklifler = TumTeklifler()
        status,datas = teklifler.setEnBoyOlcu(dat)
        data = {
            'status':status,
            'datas':datas
        }
        return jsonify(data)
        

