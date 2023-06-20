from resource_api.sevkiyat.listeler import Listeler
from resource_api.sevkiyat.sevkiyat_islem import SevkiyatKayit
from flask_restful import Resource
from resource_api.sevkiyat.sevkiyat_model import SevkiyatIslem
from flask import jsonify,request
from flask import jsonify,request,send_file
from resource_api.siparisler.excel_cikti import ExcelCiktiIslem


class SiparisListeApi(Resource): 

    def get(self):

        islem = Listeler()

        siparis_liste = islem.getSiparisListe()

        return siparis_liste

class UretimExcelCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()
     
        result = islem.uretimCikti(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/siparisler/dosyalar/Uretim_list.xlsx'

        return send_file(excel_path,as_attachment=True)

class UretimExcelCiktiENApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()
     
        result = islem.uretimCiktiEn(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/siparisler/dosyalar/Uretim_list.xlsx'

        return send_file(excel_path,as_attachment=True)  

class IcSiparisExcelCiktiApi(Resource):

    def post(self):
       
        data_list  = request.get_json()
       
        islem = ExcelCiktiIslem()
      
        result = islem.IcSiparisExcelCikti(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/siparisler/dosyalar/İç Sipariş Formu.xlsx'

        return send_file(excel_path,as_attachment=True)               


class SiparisKalemList(Resource):

    def get(self,siparisNo):

        islem = Listeler()

        siparis_kalem_list = islem.getSiparisKalemList(siparisNo)
        siparis_kalem_kasa_list = SevkiyatIslem().getKasaListesi(siparisNo)

        data = {

            "siparis_kalem_list" : siparis_kalem_list,
            "siparis_kalem_kasa_list" : siparis_kalem_kasa_list
        }

        return jsonify(data)

class SevkiyatNewModel(Resource):

    def get(self):

        model = SevkiyatIslem().newSevkiyatModel()
        islem = Listeler()
        siparis_liste = islem.getSiparisListe()
        data = {
            'model':model,
            'siparis_liste':siparis_liste
            
        }
        return data

class SevkiyatKayitIslem(Resource):

    def put(self):

        data = request.get_json()

        islem = SevkiyatKayit()

        status = islem.siparisKayitIslemi(data)

        return jsonify({'status' : status})

