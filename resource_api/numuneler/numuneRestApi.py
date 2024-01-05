from resource_api.numuneler.numuneliste import NumuneListe
from resource_api.numuneler.numune_ayrinti import NumuneAyrinti
from resource_api.numuneler.numuneIslem import *
from flask_restful import Resource
from flask import jsonify,request


class NumuneListApi(Resource):

    def get(self,yil):

        islem = NumuneListe()
        numuneList = islem.getNumuneList(yil)
        numuneYil = islem.getYilListesi()
        numune = {
            'numuneYil':numuneYil,
            'numuneList':numuneList,
            
        }
        return jsonify(numune)
    
class NumuneYearListApi(Resource):
    def get(self):
        islem = NumuneListe()
        numuneYil = islem.getYilListesi()
        return jsonify(numuneYil)


class NumuneAyrintiListApi(Resource): 

    def get(self,po):

        numuneDetail = NumuneAyrinti(po)
        numune = NumuneIslem()

        data = {
            'model': numuneDetail.getNumuneAyrintiList()[0],
            'kategoriList' : numune.getKategoriList(),
            
            'musteriList' : numune.getMusteriList(),
            'ulkeList' : numune.getUlkeList(),
            
            'birimList' : numune.getBirimList(),
            'temsilciList' : numune.getTemsilciList(),
            'odemeler':numuneDetail.getNumuneOdemelerList()
           
        }

        return jsonify(data)   

