
from resource_api.numunefinans.numune_analist import NumuneFinansAnaListe 
from resource_api.numunefinans.numune_ayrinti import  NumuneFinansAyrinti
from resource_api.numunefinans.numune_pesinat_list import TahsilatIslem
from flask_restful import Resource
from flask import jsonify,request,send_file



class NumuneFinansAnaListeApi(Resource): 

    def get(self,yil):

       
        islem = NumuneFinansAnaListe()

       
        numune_list = islem.getNumuneList(yil)
        banka_list = islem.getNumuneBankaList(yil)
        yil_list = islem.getYilListesi()
        data = {

            
            "numune_list" : numune_list,
            "banka_list" : banka_list,
            'yil_list':yil_list
        }

        return jsonify(data)

class NumuneAyrintRestList(Resource):

    def get(self,musteriid,yil):

        islem = NumuneFinansAyrinti()

        ayrinti_list = islem.getAyrintiList(musteriid,yil)

        return jsonify(ayrinti_list) 

class NumuneRaporYilListApi(Resource):

    def get(self):

        islem = NumuneFinansAnaListe()

        yil_listesi = islem.getYilListesi() ##finans için yıl seceneği
        yil_listesi2 = islem.getTakipYilListesi() ## takip listesi içn yıl seceneği

        data = {
           "yil_listesi" : yil_listesi,
           "yil_listesi2" : yil_listesi2

        }

        return jsonify(data)          


class NumuneTahsilatIslemList(Resource):

    def get(self,musteriid,siparisno):

        islem = TahsilatIslem()

        musteri_list = islem.getTahsilatList(musteriid,siparisno)
        musteri_data = islem.getTahsilatModel(musteriid,siparisno)

        data = {

            "musteri_list" : musteri_list,
            "musteri_data" : musteri_data
        }

        return jsonify(data)

class NumuneTahsilatKayitIslem(Resource):

    def post(self):

        item = request.get_json()

        islem = TahsilatIslem()

        result = islem.tahsilatKaydet(item)

        return jsonify({'status' : result})

    def put(self):

        item = request.get_json()
        islem = TahsilatIslem()

        result = islem.tahsilatGuncelle(item)

        return jsonify({'status' : result})

class NumuneTahsilatKayitSilme(Resource):

    def delete(self,id):

        islem = TahsilatIslem()

        result = islem.tahsilatSilme(id)

        return jsonify({'status' : result})            

class NumuneBankayaGelenAyrinti(Resource):
    def get(self,banka,yil):
        islem = NumuneFinansAnaListe()
        banka_list_ayrinti = islem.getBankayaGelenOdemelerAyrinti(banka,yil)
        return jsonify(banka_list_ayrinti)


        
































