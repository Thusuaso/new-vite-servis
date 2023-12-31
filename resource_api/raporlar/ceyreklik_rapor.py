from flask_restful import Resource
from views.raporlar.ceyreklikRapor.ceyreklikRapor import *
from flask import request,jsonify

class CeyreklikRaporlarApi(Resource):
    def get(self,year):
        islem = CeyreklikRaporlar(year)
        satislar = islem.getCeyreklikYear()
        chart = islem.getChartModel()
        statistics = islem.getStatistics()
        
        siparisler = islem.getCeyreklikYearSiparisler()
        siparislerChart = islem.getChartModelSiparisler()
        siparislerStatistics = islem.getStatisticsSiparisler()
        
        return jsonify({'satislar':satislar,'chart':chart,'statistics':statistics,'siparisler':siparisler,'siparislerChart':siparislerChart,'siparislerStatistics':siparislerStatistics})
    
