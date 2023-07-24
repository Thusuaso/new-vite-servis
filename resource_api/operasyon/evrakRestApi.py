from flask_restful import Resource
from flask import jsonify,request
from flask import jsonify,request,send_file
from resource_api.operasyon.evrakYukleme.evrakYuklemeListeler import EvrakListeler



class EvrakSiparisListeApi(Resource): 

    def get(self):

        islem = EvrakListeler()
        islem1 = EvrakListeler()
      

        siparis_liste = islem.getSiparisListe()
        evrak_listesi = islem1.getEvrakTurListe()
      
       
        data = {

            "siparis_liste" : siparis_liste,
            "evrak_listesi" : evrak_listesi,
         
       }

        return jsonify(data)


class EvrakIscilikTedarikciApi(Resource): 
    def get(self,po):
        islem = EvrakListeler()
        liste = islem.getIscilikTedarikciList(po)
        return jsonify(liste)


class EvrakFaturaListeApi(Resource): 

    def get(self,siparisNo):

        islem2 = EvrakListeler()

       
        fatura_listesi = islem2.getEvrakList(siparisNo)
        color_listesi = islem2.getEvrakRenkListe(siparisNo)
        data = {

            "fatura_listesi" : fatura_listesi,
            "color_listesi" : color_listesi,
         
       }

        return jsonify(data)
          
        

class EvrakTedarikciListeApi(Resource): 

    def get(self,siparisNo):

        islem = EvrakListeler()

       
        result = islem.getTedarikciList(siparisNo)
        return result          
  
  