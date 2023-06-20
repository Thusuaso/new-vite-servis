from helpers import SqlConnect,DegisiklikMain
from flask import request,jsonify
from flask_restful import Resource
import jwt
import datetime
from models import KullaniciModel,KullaniciSchema

class Kullanici(Resource):

    def post(self):
        user = request.get_json()

        username = user['username']
        password = user['password']
        print(user)
        data = SqlConnect().data
        result = data.getStoreList('Select count(*) as Durum from KullaniciTB where KullaniciAdi=? and YSifre=?',(username,password))
        username = username.capitalize()
        info = username + ' ' + 'Giriş Yaptı'
        DegisiklikMain().setYapilanDegisiklikBilgisi(username,info)
        
        
        secret_key = '1LAM1vvkeAmzxfRaCSbTksDnZNVsE1jrV6'
        
        durum = result[0].Durum
        if durum > 0:
            token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=12)},secret_key)
            model = KullaniciModel()
            dtKullanici = data.getStoreList('Select * from KullaniciTB where KullaniciAdi=? and YSifre=?',(username,password))
            user = dtKullanici[0]
            model.kullaniciAdi = user.KullaniciAdi 
          
            model.kullaniciSoyAd = user.KullaniciSoyAd 
            model.satisci = user.Satisci
            model.teklif = user.Teklif
            model.token = token.decode('UTF-8')
            model.image = user.Image
            model.id = user.ID
            schema = KullaniciSchema()
            

           
            return jsonify({'user' : schema.dump(model)})
           
        return jsonify({'token' : None})
class DataKullanici(Resource):

    def get(self,username,password):
        data = SqlConnect().data
        result = data.getStoreList('Select count(*) as Durum from KullaniciTB where KullaniciAdi=? and YSifre=?',(username,password))

        secret_key = '1LAM1vvkeAmzxfRaCSbTksDnZNVsE1jrV6'
        
        durum = result[0].Durum
        if durum > 0:
            token = jwt.encode({'user' : username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=12)},secret_key)
            model = KullaniciModel()
            dtKullanici = data.getStoreList('Select * from KullaniciTB where KullaniciAdi=? and YSifre=?',(username,password))
            user = dtKullanici[0]
            model.kullaniciAdi = user.KullaniciAdi 
            model.kullaniciSoyAd = user.KullaniciSoyAd
            model.teklif = user.Teklif 
            model.satisci = user.Satisci
            # model.token = token.decode('UTF-8')
            model.image = user.Image
            model.id = user.ID
            schema = KullaniciSchema()
            
            return jsonify({'user' : schema.dump(model)})

        return jsonify({'token' : None})
       
