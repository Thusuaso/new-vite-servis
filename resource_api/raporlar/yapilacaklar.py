from flask_restful import Resource
from flask import jsonify,request,send_file
from views.raporlar.yapilacaklar import *
class YapilacaklarApi(Resource):
    def get(self):
        islem = Yapilacaklar()
        yapildi = islem.getYapilacaklarYapildiList()
        yapilacak = islem.getYapilacaklarYapilacakList()
        data = {
            'yapildi':yapildi,
            'yapilacak':yapilacak
        }
        return jsonify(data)
    
class YapilacaklarModelApi(Resource):
    def get(self):
        islem = Yapilacaklar()
        model = islem.getYapilacaklarModel()
        users = islem.getYapilacaklarKullaniciList()
        data = {
            'model':model,
            'users':users,
        }
        return jsonify(data)
    
class YapilacaklarUsersModelApi(Resource):
    def get(self):
        islem = Yapilacaklar()
        users = islem.getYapilacaklarKullaniciList()
        return jsonify(users)
    
class YapilacaklarKullaniciListApi(Resource):
    def get(self,username):
        islem = Yapilacaklar()
        yapildi = islem.getYapilacaklarKullaniciYapildiList(username)
        yapilmadi = islem.getYapilacaklarKullaniciYapilmadiList(username)
        data = {
            'yapildi':yapildi,
            'yapilmadi':yapilmadi
        }
        return jsonify(data)

class YapilacaklarIslemApi(Resource):
    def post(self):
        data = request.get_json()
        islem = Yapilacaklar()
        status = islem.save(data)
        return {'status':status}
    def put(self):
        data = request.get_json()
        islem = Yapilacaklar()
        status = islem.update(data)
        return {'status':status}
    
class YapilacaklarSilApi(Resource):
    def delete(self,id):
        islem = Yapilacaklar()
        status = islem.delete(id)
        return {'status':status}
class YapilacaklarChangeStatusApi(Resource):
    def put(self):
        data = request.get_json()
        islem = Yapilacaklar()
        status = islem.changeStatus(data)
        return {'status':status}
    
    
class YapilacaklarDetailApi(Resource):
    def get(self,id):
        islem = Yapilacaklar()
        model = islem.getYapilacaklarDetay(id)[0]
        users = islem.getYapilacaklarKullaniciList()
        data = {
            'model':model,
            'users':users,
        }
        return jsonify(data)
    
    
class YapilacaklarAllApi(Resource):
    def get(self):
        islem = Yapilacaklar()
        yapilmadiA = islem.getYapilacaklarYapilmadiListAllA()
        yapilmadiC = islem.getYapilacaklarYapilmadiListAllC()
        
        yapilmadi = {
            'yapilmadiA':yapilmadiA,
            'yapilmadiC':yapilmadiC
            
        }
        
        yapildi = islem.getYapilacaklarYapildiListAll()
        data = {
            'yapilmadi':yapilmadi,
            'yapildi':yapildi
        }
        return jsonify(data)

class TodoMainApi(Resource):
    def get(self,userid):
        islem = Yapilacaklar()
        results = islem.getYapilacaklarAnaList(userid)
        return results
    
class TodoMainQueueChangeApi(Resource):
    def post(self):
        data = request.get_json()
        islem = Yapilacaklar()
        status = islem.setYapilacaklarAnaListSiraDegistir(data)
        return {'status':status}

class TodoMainSeeingApi(Resource):
    def get(self,id):
        islem = Yapilacaklar()
        status = islem.setYapilacaklarGorulduDegistir(id)
        return {'status':status}