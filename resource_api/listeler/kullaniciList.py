from views import Kullanici 
from flask_restful import Resource

class KullaniciList(Resource):
    def get(self):

        kullanici = Kullanici()

        result = kullanici.getKullaniciList()

        return result

class OperasyonKullaniciList(Resource):
    def get(self):

        kullanici = Kullanici()

        result = kullanici.getOperasyonKullaniciList()

        return result
 