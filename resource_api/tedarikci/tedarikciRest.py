from resource_api.tedarikci.tedarikci_islem import TedarikciIslem
from flask_restful import Resource
from flask import jsonify,request

class TedarikciListApi(Resource):

    def get(self):

        islem = TedarikciIslem()

        result = islem.getTedarikciList()

        return jsonify(result)

class TedarikciModelApi(Resource):
    def get(self):

        islem = TedarikciIslem()


        result = islem.getTedarikciModel(),

        return jsonify(result)
    

class TedarikciIslemApi(Resource):

    def post(self):

        data = request.get_json()

        islem = TedarikciIslem()

        status = islem.tedarikciKaydet(data)

        return jsonify({'status' : status })

    def put(self):

        data = request.get_json()

        islem = TedarikciIslem()

        status = islem.tedarikciGuncelle(data)

        return jsonify({'status' : status })

class TedarikciSilmeIslemApi(Resource):

    def delete(self,id):

        islem = TedarikciIslem()

        status = islem.tedarikciSilme(id)

        return jsonify({'status' : status})

        
class IcSiparisDosyaKaydet(Resource):

    def post(self):

        data = request.get_json()
        islem = TedarikciIslem()
        result = islem.IcSiparisDosyaKaydet(data)

        return jsonify({'Status' : result})
    
class IsfControlApi(Resource):
    def get(self,evrakAdi):
        islem = TedarikciIslem()
        result = islem.getIsfControl(evrakAdi)
        return jsonify(result)
    
    
class IcSiparisDosyaSilme(Resource):
    def get(self,tedarikciId,siparisNo):
        islem = TedarikciIslem()
        status = islem.setIcSiparisFormSil(tedarikciId,siparisNo)
        return jsonify({'status':status})

class IcSiparisFormSilKontrol(Resource):
    def get(self,tedarikciId,siparisNo):
        islem = TedarikciIslem()
        status = islem.IcSiparisFormSilKontrol(tedarikciId,siparisNo)
        return jsonify({'status':status})