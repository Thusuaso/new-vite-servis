from resource_api.finans.konteyner_islem.konteyner import Konteyner
from resource_api.finans.konteyner_islem.musteri_ayrinti import MusteriAyrinti
from resource_api.finans.konteyner_islem.tahsilat_islem import TahsilatIslem
from resource_api.finans.depo import DepoAnaListe,DepoAyrinti
from flask_restful import Resource
from flask import jsonify,request,send_file
from resource_api.finans.konteyner_islem.excel_cikti import ExcelCiktiIslem
from resource_api.finans.depo.excel_cikti import ExcelCiktiIslem2
from resource_api.finans.odemeler.odeme_islem import OdemeIslem
from resource_api.finans.pesinat_islem_liste import PesinatIslemListe
from resource_api.finans.pesinat_islem import FinansPesinatIslem
from resource_api.finans.yeniFinans import YeniMusteriAnaIslem
from resource_api.finans.vade import VadeAnaliste
from resource_api.finans.guncel_kur import DovizListem
from resource_api.finans.konteyner_islem.marketing import Marketing
from resource_api.finans.konteyner_islem.konteyner import *

class KonteynerAnaListe(Resource): 

    def get(self,yil):

        konteyner = Konteyner(yil)
        depo = DepoAnaListe()
        vade = VadeAnaliste()
        konteyner_list = konteyner.getKonteynerList()
        depo_list = depo.getDepoList()
        vade_list = vade.getVadeList()
        data = {
                    "konteyner_list" : konteyner_list,
                    "depo_list" : depo_list,
                    "vade_list":vade_list
                }

        return jsonify(data)

class MarketingListeApi(Resource):
    
    def get(self):
        islem = Marketing()
        marketingBd = islem.getBdDepoList()
        marketingYuklemeAylik = islem.getYuklemeAylikList()
        data = {
            "marketingBd":marketingBd,
            "marketingYuklemeAylik":marketingYuklemeAylik,
        }
        
        return jsonify(data)

class ByMarketingYuklemeApi(Resource):
    def get(self,month):
        islem = Marketing()
        if(month == 0):
            marketingYukleme = islem.getMarketingYuklemeHepsi()
            marketingUretim = islem.getMarketingUretim()
            marketingDepo = islem.getMarketingDepoHepsi()
            marketingYuklemeDetail = islem.getMarketingDetailHepsi()
        else:
            marketingYukleme = islem.getMarketingYukleme(month)
            marketingUretim = islem.getMarketingUretim()
            marketingDepo = islem.getMarketingDepo(month)
            marketingYuklemeDetail = islem.getMarketingDetail(month)
        data={
            'marketingYukleme':marketingYukleme,
            'marketingUretim':marketingUretim,
            'marketingDepo':marketingDepo,
            'marketingYuklemeDetail':marketingYuklemeDetail
        }
        return jsonify(data)

class ByMarketingYuklemeExcelApi(Resource):
    def post(self):
        data = request.get_json()
        islem = Marketing()
        status = islem.byMarketingExcellCikti(data)
        return jsonify({'status':status})
    def get(self):
        excel_path = 'resource_api/raporlar/dosyalar/by_marketing_excel.xlsx'
        return send_file(excel_path,as_attachment=True)
    
class ByCustomersYuklemeExcelApi(Resource):
    def post(self):
        data = request.get_json()
        islem = Marketing()
        status = islem.byCustomersExcellCikti(data)
        return jsonify({'status':status})
    def get(self):
        excel_path = 'resource_api/raporlar/dosyalar/by_customers_excel.xlsx'
        return send_file(excel_path,as_attachment=True)


class ByMarketingDetailExcelApi(Resource):
    def post(self):
        data = request.get_json()
        islem = Marketing()
        status = islem.byMarketingDetailExcellCikti(data)
        return jsonify({'status':status})
    def get(self):
        excel_path = 'resource_api/raporlar/dosyalar/by_marketing_detail_excel.xlsx'
        return send_file(excel_path,as_attachment=True)





class MusteriAyrintiListApi(Resource):

    def get(self,musteriid):

        islem = MusteriAyrinti(musteriid)

        ayrinti_list = islem.getKonteynerAyrintiList()
        odeme_liste = islem.getOdemeListesi()
        po_list = islem.getByCustomersPo()

        data = {

            "ayrinti_list" : ayrinti_list,
            "odeme_liste" : odeme_liste,
            "po_list":po_list
        }


        return jsonify(data)


class OdemelerDegisimApi(Resource):
    def post(self):
        data = request.get_json()
        islem = TahsilatIslem()
        status = islem.setOdemeDegisim(data)
        
        return {'status':status}
        


class MusteriOdemeSecimList(Resource):

    def get(self,musteri_id,tarih):

        islem = MusteriAyrinti(musteri_id)

        secim_list = islem.getOdemeSecimPoList(tarih)

        return secim_list

class TahsilatIslemList(Resource):

    def get(self,musteriid,siparisno):

        islem = TahsilatIslem()

        musteri_list = islem.getTahsilatList(musteriid,siparisno)
        musteri_model = islem.getTahsilatModel(musteriid,siparisno)

        data = {

            "musteri_list" : musteri_list,
            "musteri_model" : musteri_model
        }

        return jsonify(data)

class TahsilatKayitIslem(Resource):

    def post(self):

        item = request.get_json()

        islem = TahsilatIslem()

        result = islem.tahsilatKaydet(item)

        return jsonify(result)

    def put(self):

        item = request.get_json()
        islem = TahsilatIslem()

        result = islem.tahsilatGuncelle(item)

        return jsonify(result)

class TahsilatKayitSilme(Resource):

    def delete(self,id):

        islem = TahsilatIslem()

        result = islem.tahsilatSilme(id)

        return jsonify({'status' : result})

class DepoAyrintList(Resource):

    def get(self,musteriid):

        islem = DepoAyrinti()

        ayrinti_list = islem.getAyrintiList(musteriid)
        odeme_ayrinti_list = islem.getOdemeAyrintiList(musteriid)

        data = {

            "ayrinti_list" : ayrinti_list,
            "musteriid" : musteriid,
            "odeme_ayrinti_list": odeme_ayrinti_list
        }

        return jsonify(data)

class VadeOdemeListesiApi(Resource):

    def get(self):

        islem = VadeAnaliste()

        result = islem.getVadeList()

        return result        

class DepoAyrintiListExcell(Resource):

    def post(self):
        
        data_list = request.get_json()
        
        islem = ExcelCiktiIslem2()
        
        result = islem.getExcelAyrintiList(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/depo/dosyalar/depo_ayrinti_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

     

class KonteynerExcelCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.konteynerCikti(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/konteyner_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class KonteynerOdemelerListesiExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.odemelerCikti(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/odemeler_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)






class DepoExcelCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.depoCikti(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/depo_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class KonteynerAyrintiCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.konteyner_ayrinti_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/konteyner_ayrinti_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class KonteynerOdemeCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.konteyner_odeme_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/konteyner_odeme_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class MusteriOdemeCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.musteri_odeme_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/musteri_odeme_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class MusteriOdemeListesiApi(Resource):

    def get(self,yil,ay):

        islem = OdemeIslem()

        odeme_listesi = islem.getOdemeListesi(yil,ay)

        return odeme_listesi

class MusteriOdemeYilListesiApi(Resource):

    def get(self):

        islem = OdemeIslem()

        yil_listesi = islem.getYilListesi()

        return yil_listesi

class MusteriOdemeAyListesi(Resource):

    def get(self,yil):

        islem = OdemeIslem()

        ay_listesi = islem.getAyListesi(yil)

        return ay_listesi

class PesinatIslemListeApi(Resource):

    def get(self):

        pesinat_islem_listesi = PesinatIslemListe().getPesinatIslemListe()

        return pesinat_islem_listesi

    def post(self):

        data = request.get_json()

        result = FinansPesinatIslem().pesinat_kaydet(data)

        return jsonify({'status' : result})


class YeniFinansAnaListe(Resource): 

    def get(self):

        islem = YeniMusteriAnaIslem()
        print("YeniFinansAnaListe",islem)

        result = islem.getFinansMusteriler()

        return result     

 
class DovizListe(Resource): 

    def get(self,yil,ay,gun):

        islem = DovizListem()
      

        result = islem.getDovizKurListe(yil,ay,gun)

        data = {

            "result" : result
          
        }

        return jsonify(data)
    
class ByMarketingMonthLoadApi(Resource):
    def get(self):
        islem = Marketing()
        icPiyasa = islem.getMarketingMonthIcPiyasaLoad()
        mekmer = islem.getMarketingMonthMekmerLoad()
        data = {
            'icPiyasa':icPiyasa,
            'mekmer':mekmer
            
        }
        return data

class ByMarketingMonthLoadIcPiyasaAyrintiApi(Resource):
    def get(self,month):
        islem = Marketing()
        icPiyasa = islem.getMarketingMonthIcPiyasaAyrintiLoad(month)

        return icPiyasa

class ByMarketingMonthLoadMekmerAyrintiApi(Resource):
    def get(self,month):
        islem = Marketing()
        icPiyasa = islem.getMarketingMonthMekmerAyrintiLoad(month)

        return icPiyasa      

class MayaNumSipGelenApi(Resource):
    def get(self,month,year):
        islem = MayaGelenBedeller()
        result = islem.getMayaGelenBedeller(month,year)
        return jsonify(result)
    
class MayaNumSipGelenYearApi(Resource):
    def get(self,year):
        islem = MayaGelenBedeller()
        result = islem.getMayaGelenBedellerYear(year)
        return jsonify(result)
    
class MayaGelenBedellerCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.maya_gelen_bedeller_cikti(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/finans/konteyner_islem/dosyalar/maya_gelen_bedeller_cikti.xlsx'

        return send_file(excel_path,as_attachment=True)





