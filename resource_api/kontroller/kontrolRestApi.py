from resource_api.kontroller.musteri_eta import MusteriEta
from resource_api.kontroller.finans_vade import FinansVade
from resource_api.kontroller.chat_mail import ChatGiris
from flask import jsonify,request
from flask_restful import Resource


class MusteriEtaMailIslem(Resource):

    def get(self):

        islem = MusteriEta()

        result = True
        islem.getEtaControl()
        # islem.finansBolmeKontrol()
        # islem.etaKontrol()


        return jsonify({'status' : result})


class EtaYaklasanTarihBildirimApi(Resource):
    def get(self):
        islem = MusteriEta()
        result = islem.getEtaControlNotification()
        return jsonify(result)
    
    
class EtaYaklasanTarihBildirimStatusApi(Resource):
    def get(self,po,etaSure):
        islem = MusteriEta()
        result = islem.setEtaControlNotificationStatus(po,etaSure)
        return result

    
class FinansVadeMailIslem(Resource):

    def get(self):

        islem = FinansVade()

        result = False

        try:
            islem.vadeKontrol()
            result = True 
        except:
            result = False

        return jsonify({'status' : result})       

class ChatMailGonderim(Resource):

    def post(self):

        data = request.get_json()
        
        islem = ChatGiris()
        try:
         
         islem.mailGonderInsert(data)
         result = True 
        except:
            result = False 

        return jsonify({'Status' : result})    

    

class ChatMailler(Resource): 

    def get(self,po):

        islem = ChatGiris()
      
        result = islem.getChatList(po)
       


        return result
    
