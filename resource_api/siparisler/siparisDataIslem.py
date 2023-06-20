from flask_restful import Resource
from flask import request,jsonify
from views.siparisler import SiparisGiris
from views.siparisler.siparisBolme import SiparisBolme
from resource_api.kontroller.uretim_takip_mail import UretimTakipMail


class SiparisKayitIslem(Resource):

    def post(self):
        data = request.get_json()
        siparisGiris = SiparisGiris()
        siparis = data['siparis']
        urunler = data['siparisUrunler']
        status = siparisGiris.siparisKaydet(urunler,siparis,)
        data = {
            'status':status
        }
        return jsonify(data)

    def put(self):

        data = request.get_json()

        siparisGiris = SiparisGiris()

        siparis = data['siparis']
        urunlerYeni = data['urunlerYeni']
        urunlerDegisenler = data['urunlerDegisenler']
        urunlerSilinenler = data['urunlerSilinenler']
        degisenMasraflar = data['degisimMasraflar']
        result = siparisGiris.siparisGuncelle(siparis,urunlerYeni,urunlerDegisenler,urunlerSilinenler,degisenMasraflar)
      
      
        
        
        return jsonify(result)

class SiparisDegisimMailGonderApi(Resource):
    def post(self):
        datas = request.get_json()
        islem = SiparisGiris()
        print(datas)
        


class SiparisKayitIslemControlApi(Resource):
    def get(self,siparis_no):
        islem = SiparisGiris()
        result = islem.siparisDataKayitControl(siparis_no)
        return result
        


class SiparisBolmeGuncellemeApi(Resource):

    def post(self):
        sipDatas = request.get_json()
        sipBolmeClass = SiparisBolme(sipDatas)
        sipBolmeClass.siparisBolme()
        
        return True
        

class SiparisOpChangeApi(Resource):
    def post(self):
        datas = request.get_json()
        siparisGiris = SiparisGiris()
        result = siparisGiris.opChange(datas)
        return result
    
class SiparisOdemeSekliChangeApi(Resource):
    def get(self,siparisNo,odemeTur):
        siparisGiris = SiparisGiris()
        status = siparisGiris.getchangeOdemeBilgisi(siparisNo,odemeTur)
        return {'status':status}
    
class SiparisOdemeSekliChangeExApi(Resource):
    def get(self,siparisNo,odemeTur):
        siparisGiris = SiparisGiris()
        status = siparisGiris.getchangeOdemeBilgisiEx(siparisNo,odemeTur)
        return {'status':status}

