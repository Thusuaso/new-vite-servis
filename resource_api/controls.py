from flask import request,jsonify
from flask_restful import Resource
from views.controls import Controls
class ProformaKayitKontrolApi(Resource):
    def get(self,siparisNo):
        islem = Controls()
        result = islem.getProformaControl(siparisNo)
        return jsonify(result)
        