import json
from flask_restful import Resource
from flask import jsonify,request
from views.raporlar.dashboard.dashboard import DashboardNew
from resource_api.finans.konteyner_islem.konteyner import Konteyner
import datetime
from views.shared.degisiklikTahmin import *
from resource_api.raporlar.ulkeBazindaSevkiyat import UlkeBazindaSevkiyat

class DashboardNewApi(Resource):
    def get(self):
        
        dashboard = DashboardNew()
        now = datetime.datetime.now()
        year = now.year
        konteyner = Konteyner(year)
        konteyner.getKonteynerList()
        gelenSiparisMekmar = dashboard.getDashboardGelenSiparis()
        gelenSiparisMekmarYuklenen = dashboard.getDashboardGelenSiparisYuklenen()
        
        # gelenSiparisAll = dashboard.getDashboardGelenSiparisAll()
        # gelenSiparisAllYuklenen = dashboard.getDashboardGelenSiparisAllYuklenen()
        
        
        gelenSiparisYearMekmar = dashboard.getDashboardGelenSiparisYillikMekmar()
        gelenSiparisYearAll = dashboard.getDashboardGelenSiparisYillikAll()
        
        gelenSiparisYearYuklenenMekmar = dashboard.getDashboardYuklenenSiparisYillikMekmar()
        gelenSiparisYearYuklenenAll = dashboard.getDashboardYuklenenSiparisYillikAll()
        
        # gelenSiparisEfes = dashboard.getDashboardGelenSiparisEfes()
        # gelenSiparisYillikEfes = dashboard.getDashboardGelenSiparisYillikEfes()
        # gelenSiparisEfesYuklenen = dashboard.getDashboardGelenSiparisEfesYuklenen()
        # gelenSiparisYillikEfesYuklenen = dashboard.getDashboardGelenSiparisYillikEfesYuklenen()
        buYilSipTop,buYilYukTop,gecenYilSipTop,gecenYilYukTop=dashboard.getSiparisGrafikYuklenenvSiparis()
        grafikMekmar = dashboard.getsiparisGrafikRapor()
        data = {
            'gelenSiparisMekmar':gelenSiparisMekmar,
            # 'gelenSiparisAll':gelenSiparisAll,
            'gelenSiparisYearMekmar':gelenSiparisYearMekmar,
            'gelenSiparisYearAll':gelenSiparisYearAll,
            'gelenSiparisMekmarYuklenen':gelenSiparisMekmarYuklenen,
            # 'gelenSiparisAllYuklenen':gelenSiparisAllYuklenen,
            'gelenSiparisYearYuklenenMekmar':gelenSiparisYearYuklenenMekmar,
            'gelenSiparisYearYuklenenAll':gelenSiparisYearYuklenenAll,
            'grafik':grafikMekmar,
            'grafikSipBuYilTop':buYilSipTop,
            'grafikYukBuYilTop':buYilYukTop,
            'grafikSipGecenYilTop':gecenYilSipTop,
            'grafikYukGecenYilTop':gecenYilYukTop,
            
            
            
            
            # 'gelenSiparisEfes':gelenSiparisEfes,
            # 'gelenSiparisYillikEfes':gelenSiparisYillikEfes,
            # 'gelenSiparisEfesYuklenen':gelenSiparisEfesYuklenen,
            # 'gelenSiparisYillikEfesYuklenen':gelenSiparisYillikEfesYuklenen,
            
        }
        return jsonify(data)
class DashboardNewSatisciApi(Resource):
    def get(self,username):
        
        dashboard = DashboardNew()
        gelenSiparisSatisciOzel = dashboard.getDashboardGelenSiparisSatisci(username)

        return jsonify(gelenSiparisSatisciOzel)
class DashboardNewGrafikApi(Resource):
    def get(self):
        grafik = DashboardNew()
        grafikMekmar = grafik.getsiparisGrafikRapor()
        grafikHepsi = grafik.getsiparisGrafikRaporHepsi()
        data = {
            'grafikMekmar':grafikMekmar,
            'grafikHepsi':grafikHepsi, 
        }
        return data
    
class DashboardNewGrafikDataApi(Resource):
    def get(self):
        grafik = DashboardNew()
        buYilSipTop,buYilYukTop,gecenYilSipTop,gecenYilYukTop=grafik.getSiparisGrafikYuklenenvSiparis()
        data = {
            'buYilSipTop':buYilSipTop,
            'buYilYukTop':buYilYukTop,
            'gecenYilSipTop':gecenYilSipTop,
            'gecenYilYukTop':gecenYilYukTop
        }
        return data



class DashboardNewSubApi(Resource):
    def get(self):
        
        satis = DashboardNew()
        islem = UlkeBazindaSevkiyat()
        
        
        konteynir = satis.getDashboardKonteynir()
        finans = satis.getDashboardFinans()
        tedarikci = satis.getDashboardTedarikci()
        tedarikciSiparisler = satis.getDashboardTedarikciSiparisler()
        musteriSiparisler = satis.getDashboardMusteriSiparisleri()
        teklifler = satis.getDashboardTeklifler()
        tekliflerYillik = satis.getDashboardTekliflerYillik()
        sonEklenenSiparisler = satis.getDashboardSonSiparisler()
        ulkeyeGore = islem.getUlkeBazindaSevkiyat()
        
            
        data = {
            'konteynir':konteynir,
            'finans':finans,
            'tedarikci':tedarikci,
            'tedarikciSiparisler':tedarikciSiparisler,
            'musteriSiparisler':musteriSiparisler,
            'teklifler':teklifler,
            'tekliflerYillik':tekliflerYillik,
            'sonEklenenSiparisler':sonEklenenSiparisler,
            'ulkeyeGore':ulkeyeGore
        }
        
        
        return jsonify(data)

class DashboardNewSubTedarikciAyrintiApi(Resource):
    def get(self,tedarikciId):
        
        islem = DashboardNew()
        tedarikciAyrinti = islem.getTedarikciAyrinti(tedarikciId)
        tedarikciAyrintiAll = islem.getTedarikciAyrintiAll(tedarikciId)
        data = {
            'tedarikciAyrinti':tedarikciAyrinti,
            'tedarikciAyrintiAll':tedarikciAyrintiAll
        }
        return jsonify(data)
        
class DashboardFirmaBazindaAyrintiApi(Resource):
    def get(self,firmaId):
        islem = DashboardNew()
        result = islem.getFirmaBazindaAyrintiSiparis(firmaId)
        return jsonify(result)
    
    
class DashboardTekliflerAyrintiApi(Resource):
    def get(self,satisciId):
        
        teklif = DashboardNew()
        aylikTeklifler = teklif.getTeklifAyrintiAylik(satisciId)
        yillikTeklifler = teklif.getTeklifAyrintiYillik(satisciId)
        data = {
            'aylikTeklifler':aylikTeklifler,
            'yillikTeklifler':yillikTeklifler
        }
        return jsonify(data)
    
class DashboardLogsAyrintiTarihApi(Resource):
    def post(self):
        dates = request.get_json()
        logs = DashboardNew()
        result = logs.postAnaSayfaLogsTarihli(dates)
        return jsonify(result)
    
class DashboardUlkeyeGoreTekliflerApi(Resource):
    def get(self,year):
        
        teklif = DashboardNew()
        result = teklif.getUlkeTeklifler(year)
        return jsonify(result)
    
class DashboardUlkeyeGoreTekliflerAyrintiApi(Resource):
    def get(self,year,ulkeId):
        
        teklif = DashboardNew()
        result = teklif.getUlkeTekliflerAyrinti(year,ulkeId)
        return jsonify(result)
    
class TahminiDegisiklikApi(Resource):
    def get(self):
        islem = DegisiklikTahmin()
        result = islem.getDegisiklikTahmin()
        return jsonify(result)