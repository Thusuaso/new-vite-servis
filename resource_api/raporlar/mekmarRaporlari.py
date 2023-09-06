from flask import jsonify,request,send_file
from flask_restful import Resource
from views.raporlar.mekmarRaporlari import *
from views.raporlar.mkRaporlar import *
from views.raporlar.guRaporlar import *
from resource_api.shared.excel_liste_islem import * 
from resource_api.maliyet_raporlar.maliyet_rapor_islem import MaliyetRaporIslemKarAyrinti
from resource_api.raporlar.ayrintiliMusterilist import GenelMusteriListesi
class MekmarUlkeRaporuApi(Resource):
    def get(self,year):
        islem = MekmarRaporlari()
        result = islem.getUlkeRaporlari(year)
        return jsonify(result)

class MekmarUlkeRaporuAyrintiApi(Resource):
    def get(self,ulke_id,year):
        islem = MekmarRaporlari()
        result = islem.getUlkeRaporlariAyrinti(ulke_id,year)
        return jsonify(result)
    
class MekmarMusteriRaporuApi(Resource):
    def get(self,year):
        islem = MekmarRaporlari()
        result = islem.getMusteriRaporlari(year)
        return result
    
class MekmarMusteriRaporuAyrintiApi(Resource):
    def get(self,musteri_id,year):
        islem = MekmarRaporlari()
        result = islem.getMusteriRaporlariAyrinti(musteri_id,year)
        return jsonify(result)    

    
class MekmarTedarikciRaporuApi(Resource):
    def get(self,year):
        islem = MekmarRaporlari()
        result = islem.getTedarikciRaporlari(year)
        return result
    
    
class MekmarTedarikciRaporuAyrintiApi(Resource):
    def get(self,tedarikci_id,year):
        islem = MekmarRaporlari()
        result = islem.getTedarikciAyrintiRaporlari(tedarikci_id,year)
        return jsonify(result)
    
class MkRaporlariApi(Resource):
    def get(self,year):
        mk = MkRaporlari()
        byCust = GenelMusteriListesi()
        
        byCustomerOrder = byCust.getGenelMusteriSiparis()
        byPo = mk.getPoBazindaYillikSiparisler(year)
        byCustomer = mk.getMusteriBazindaUretim(year)
        byMarketing = mk.getMarketing(year)
        byMarketingYukleme = mk.getMarketingYukleme(year)
        byMarketingDetayYukleme = mk.getMarketingDetail(year)
        byYuklemevSiparisler = mk.mkRaporlarSevkSip(year)
        data = {
            'byPo':byPo,
            'byCustomer':byCustomer,
            'byMarketing':byMarketing,
            'byMarketingYukleme':byMarketingYukleme,
            'byMarketingDetayYukleme':byMarketingDetayYukleme,
            'byYuklemevSiparisler':byYuklemevSiparisler,
            'byCustomerOrder':byCustomerOrder
        }
        return jsonify(data)

class MkRaporlariExcelApi(Resource):
    def post(self):
        data = request.get_json()
        mk = MkRaporlari()
        status = mk.getMkRaporlariExcelList(data)
        return {'status':status}
    
    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/mkRaporlari.xlsx'

        return send_file(excel_path,as_attachment=True)
    
class GuRaporlariApi(Resource):
    def get(self,year):
        islem = MaliyetRaporIslemKarAyrinti(year)
        gu = GuRaporlari()
        # ayo = gu.getMaliyetListesiKar(year)
        ayoDetail = islem.getMaliyetListesiKarAyrinti()
        ulke = gu.getUlkeRaporlari(year)
        musteri = gu.getMusteriRaporlari(year)
        tedarikci = gu.getTedarikciRaporlari(year)
        mekus = gu.getMekusMasraflar(year)
        logs = gu.getLogsMaliyet(year)
        data = {
            # 'ayo':ayo,
            'ayoDetail':ayoDetail,
            'ulke':ulke,
            'musteri':musteri,
            'tedarikci':tedarikci,
            'mekus':mekus,
            'logs':logs
        }
        return jsonify(data)
        