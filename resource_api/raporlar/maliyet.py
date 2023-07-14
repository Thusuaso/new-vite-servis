from flask import jsonify,request,send_file
from flask_restful import Resource
from views.raporlar.maliyetHatalar import *
class MaliyetHataRaporIslemApi(Resource):
    def get(self):
        islem = MaliyetHatalari()
        liste = islem.getList()
        return jsonify(liste)
    def post(self):
        data = request.get_json()
        islem = MaliyetHatalari()
        status = islem.save(data)
        return {'status':status}
        
    def put(self):
        data = request.get_json()
        islem = MaliyetHatalari()
        status = islem.update(data)
        return {'status':status}
    
class MaliyetHataRaporModelApi(Resource):
    def get(self):
        islem = MaliyetHatalari()
        model = islem.getModel()
        users = islem.users()
        
        data = {
            'model' : model,
            'users' : users
            
        }
        
        return jsonify(data)
    

class MaliyetHataRaporDeleteApi(Resource):
    def delete(self,id):
        islem = MaliyetHatalari()
        status = islem.delete(id)
        return jsonify({'status':status})
    
class MaliyetHataRaporDetayApi(Resource):
    def get(self,id):
        islem = MaliyetHatalari()
        model = islem.detail(id)[0]
        users = islem.users()
        data = {
            'model':model,
            'users':users
        }
        
        return jsonify(data)