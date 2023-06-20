from flask_restful import Resource
from views import Kullanici 
from views.satisciInfo import SatisciInfo

class SiparisSatisciInfoApi(Resource):
    def get(self):
        
        islem = SatisciInfo()
        kullanici = Kullanici()

        kullaniciList = kullanici.getKullaniciList()
        info = islem.getSiparisSatisciInfo()
        opOzet = islem.getSiparisSatisciOzet()
        ssOzet = islem.getSiparisSahibiOzet()
        data = {
            'infoList':info,
            'opOzet':opOzet,
            'ssOzet':ssOzet,
            'kullaniciList':kullaniciList
            
        }
        return data
    
class SsOpChangeApi(Resource):
    def get(self,po,ss,op):
        
        islem = SatisciInfo()
        status = islem.setSatisciInfo(po,ss,op)
        
        return {'status':status}