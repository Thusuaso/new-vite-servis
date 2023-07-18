from resource_api.musteriler.musteri_liste import *
from resource_api.musteriler.musteri_detay import MusteriDetayIslem
from models.musteriler_model.musteri import TeklifMusterilerModel,TeklifMusterilerSchema,BgpMusterilerModel,BgpMusterilerSchema,FuarMusterilerModel,FuarMusterilerSchema
from models.musteriler_model.musteri_liste import CustomersSurfaceListModel,CustomersSurfaceListSchema
from views.shared import Ulkeler
from flask_restful import Resource
from flask import jsonify,request,send_file


class MusteriListeApi(Resource):

    def get(self):
        islem = MusteriIslem()
        customer_list = islem.getMusteriListesi()
        customer_po_list = islem.getMusteriPoListesi()
        data = {
            'customer_list':customer_list,
            'customer_po_list':customer_po_list,
            
        }
        return jsonify(data)

class MusteriSiparisListesiApi(Resource):
    def get(self):

        islem = MusteriSiparisIslem()
        musteri_siparis_listesi = islem.getMusteriSiparisListesi()
        return musteri_siparis_listesi

class MusteriSiparisAyrintiCardApi(Resource):
    def get(self):

        islem = MusteriSiparisAyrintiCardIslem()
        musteri_ayrinti_card_list = islem.getMusteriSiparisAyrintiCard()
        return musteri_ayrinti_card_list

class MusteriDetayApi(Resource):

    def get(self,id):
        islem = MusteriDetayIslem()

        musteri_model = islem.getMusteriDetay(id)
        siparis_ozet  = islem.getSiparisBedeliDetay(id)
        temsilci_list = islem.getTemsilciList()
        ulke_list  = islem.getUlkeList()

        data = {

            "musteri_model" : musteri_model,
            "siparis_ozet" : siparis_ozet ,
            "temsilci_list" : temsilci_list,
            "ulke_list" : ulke_list
        }


        return jsonify(data)

class MusteriSiparisAyrintApi(Resource):

    def get(self,yil,id):

        islem = MusteriDetayIslem()

        siparis_detay = islem.getSiparisAyrintiDetay(yil,id)
      

        data = {

            "siparis_detay" : siparis_detay,
           
        }


        return jsonify(data)       

class MusteriYeniModelApi(Resource):

    def get(self):

        islem = MusteriDetayIslem()

        musteri_model = islem.getYeniMusteriModel()

        temsilci_list = islem.getTemsilciList()
        ulke_list  = islem.getUlkeList()
        siparis_ozet = []
        data = {

            "musteri_model" : musteri_model,
            "temsilci_list" : temsilci_list,
            "ulke_list" : ulke_list,
            "siparis_ozet":siparis_ozet
        }


        return jsonify(data)

class MusteriKayitIslemApi(Resource):

    def post(self):

        data = request.get_json()

        islem = MusteriDetayIslem()

        result = islem.musteriKaydet(data)

        return jsonify({'status' : result})

    def put(self):

        data = request.get_json()

        islem = MusteriDetayIslem()

        result = islem.musteriGuncelle(data)

        return jsonify({'status' : result})

class MusteriKayitSilmeApi(Resource):

    def delete(self,id):

        islem = MusteriDetayIslem()

        result = islem.musteriSilme(id)

        return jsonify({'status' : result})

class MusteriListesiYazdirmaApi(Resource):
    def post(self):
        data_list = request.get_json()
        

        islem = MusteriIslem()
        result = islem.excelCiktiAl(data_list)
        return jsonify({'status' : result})


    def get(self):

        excel_path = 'resource_api/musteriler/dosyalar/musteriDetayListesi.xlsx'

        return send_file(excel_path,as_attachment=True)


class CustomersSurfaceSaveApi(Resource):
    def post(self):
        data = request.get_json()
        islem = MusteriIslem()
        status = islem.setSurfaceCustomers(data)
        customerList = islem.getCustomerSurfaceList(data['user_id'])
        surfaceList = islem.getSurfaceList(data['user_id'])
        data2={
            "surfaceList":surfaceList,
            "customersList":customerList
        }
        data={
            'status':status,
            
            'customerList':data2
        }
        return jsonify(data)
    
    def put(self):
        data = request.get_json()
        islem = MusteriIslem()
        status = islem.setSurfaceCustomersUpdate(data)
        customerList = islem.getCustomerSurfaceList(data['user_id'])
        surfaceList = islem.getSurfaceList(data['user_id'])
        data2={
            "surfaceList":surfaceList,
            "customersList":customerList
        }
        data={
            'status':status,
            
            'customerList':data2
        }
        return jsonify(data)
 
class CustomersModelApi(Resource):
    def get(self,user_id):
        model = CustomersSurfaceListModel()
        schema = CustomersSurfaceListSchema()
        modelAct = schema.dump(model)
        islem = MusteriIslem()
        country = Ulkeler()
        countryList = country.getUlkeList()

        customerList = islem.getCustomerSurfaceList(user_id)
        surfaceList = islem.getSurfaceList(user_id)
        data = {
            'model':modelAct,
            'customer':customerList,
            'country':countryList,
            'surface':surfaceList,
        }
        return data
    
class CustomersDetailApi(Resource):
    def get(self,user_id,id):
        islem = MusteriIslem()
        country = Ulkeler()
        modelAct = islem.getCustomerSurfaceDetail(id)[0]
        countryList = country.getUlkeList()
        customerList = islem.getCustomerSurfaceList(user_id)
        surfaceList = islem.getSurfaceList(user_id)
        data = {
            'model':modelAct,
            'customer':customerList,
            'country':countryList,
            'surface':surfaceList,
        }
        return data
        


    
class CustomersSurfaceDeleteApi(Resource):
    def delete(self,id,user_id):
        islem = MusteriIslem()
        status = islem.setSurfaceCustomersDelete(id)
        customerList = islem.getCustomerSurfaceList(user_id)
        surfaceList = islem.getSurfaceList(user_id)
        data2={
            "surfaceList":surfaceList,
            "customersList":customerList
        }
        data={
            'status':status,
            
            'customerList':data2
        }
        return jsonify(data)
    
    
class CustomersTeklifMusteriListesiApi(Resource):
    def get(self):
        islem = MusteriIslem()
        datas = islem.getTekliflerMusteriListesi()
        return jsonify(datas)

class CustomersSurfaceListApi(Resource):
    def get(self,user_id):
        islem = MusteriIslem()
        surfaceList = islem.getSurfaceList(user_id)
        customersList = islem.getCustomerSurfaceList(user_id)
        data={
            "surfaceList":surfaceList,
            "customersList":customersList
        }
        return jsonify(data)


class CustomerChangeFollowApi(Resource):
    def get(self,customer,follow):
        islem = MusteriIslem()
        result = islem.setCustomerFollowing(customer,follow)
        
        return jsonify(result)

class TeklifMusterilerApi(Resource):
    def get(self):
        islem = TeklifMusteriler()
        result = islem.getTeklifMusteriler()
        return jsonify(result)
    
class TeklifMusterilerAyrintiApi(Resource):
    def get(self,id):
        islem = TeklifMusteriler()
        ulkeler = Ulkeler()
        model = islem.getTeklifMusterilerAyrinti(id)[0]
        ulkelerList = ulkeler.getUlkeList()
        data = {
            'model':model,
            'ulkeler':ulkelerList
        }
        return jsonify(data)
    
    
class TeklifMusteriModelApi(Resource):
    def get(self):
        model = TeklifMusterilerModel()
        schema = TeklifMusterilerSchema()
        modelAct = schema.dump(model)
        ulkeler = Ulkeler()
        ulkelerList = ulkeler.getUlkeList()
        data = {
            'model':modelAct,
            'ulkeler':ulkelerList
        }
        return jsonify(data)
    
    
class TeklifMusterilerYeniKayitApi(Resource):
    def post(self):
        data = request.get_json()
        islem = TeklifMusteriler()
        status = islem.setTeklifMusterilerKayit(data)
        data = {
            'status':status
        }
        return jsonify(data)
    
    def put(self):
        data = request.get_json()
        islem = TeklifMusteriler()
        status = islem.setTeklifMusteriler(data)
        data = {
            'status':status,
        }
        return jsonify(data)
    
class TeklifMusterilerSilApi(Resource):
    def delete(self,id):
        islem = TeklifMusteriler()
        status = islem.setTeklifMusterilerSil(id)
        data = {
            'status':status,
        }
        return jsonify(data)
    
class TeklifMusKopyalamaApi(Resource):
    def post(self):
        data = request.get_json()
        islem = TeklifMusteriler()
        status = islem.setTeklifMusterilerKopyala(data)
        return jsonify(status)
        

class FuarMusterilerYeniKayitApi(Resource):
    def post(self):
        data = request.get_json()
        islem = FuarMusteriler()
        status = islem.setFuarMusterilerKayit(data)
        data = {
            'status':status,
        }
        return jsonify(data)
    
    def put(self):
        data = request.get_json()
        islem = FuarMusteriler()
        status = islem.setFuarMusterilerGuncelle(data)
        data = {
            'status':status,
        }
        return jsonify(data)
    

    
class FuarMusterilerListApi(Resource):
    def get(self):
        islem = FuarMusteriler()
        result = islem.getFuarMusterileriList()
        return jsonify(result)
    
class FuarMusterilerListAyrintiApi(Resource):
    def get(self,id):
        islem = FuarMusteriler()
        country = Ulkeler()
        model = islem.getFuarMusterileriListAyrinti(id)[0]
        countryList = country.getUlkeList()
        data = {
            'model':model,
            'country':countryList,
        }
        return jsonify(data)
    
class FuarMusterilerSilApi(Resource):
    def delete(self,id):
        islem = FuarMusteriler()
        status = islem.getFuarMusterileriListSil(id)
        data = {
            'status':status,
        }
        return jsonify(data)

class FuarMusterilerModelApi(Resource):
    def get(self):
        country = Ulkeler()
        model = FuarMusterilerModel()
        schema = FuarMusterilerSchema()
        modelAct = schema.dump(model)
        countryList = country.getUlkeList()
        data = {
            'model':modelAct,
            'country':countryList
        }
        return data
            
    
class BgpMusterilerYeniKayitApi(Resource):
    def post(self):
        data = request.get_json()
        islem = BgpMusteriler()
        status = islem.setBgpMusterilerKayit(data)
        data = {
            'status':status,
        }
        return jsonify(data)
    
    def put(self):
        data = request.get_json()
        islem = BgpMusteriler()
        status = islem.setBgpMusterilerGuncelle(data)
        data = {
            'status':status,
        }
        return jsonify(data)

class BgpMusterilerModelApi(Resource):
    def get(self):
        country = Ulkeler()
        model = BgpMusterilerModel()
        schema = BgpMusterilerSchema()
        modelAct = schema.dump(model)
        countryList = country.getUlkeList()
        data = {
            'model':modelAct,
            'country':countryList,
        }
        return data

class BgpMusterilerGuncelleApi(Resource):
    def post(self):
        data = request.get_json()
        islem = BgpMusteriler()
        status = islem.setBgpMusterilerGuncelle(data)
        liste = islem.getBgpMusterileriList()
        data = {
            'status':status,
            'liste':liste
        }
        return jsonify(data)
    
class BgpMusterilerListApi(Resource):
    def get(self):
        islem = BgpMusteriler()
        result = islem.getBgpMusterileriList()
        return jsonify(result)
    
class BgpMusterilerListAyrintiApi(Resource):
    def get(self,id):
        islem = BgpMusteriler()
        country = Ulkeler()
        
        model = islem.getBgpMusterileriListAyrinti(id)[0]
        countryList = country.getUlkeList()
        data = {
            'model':model,
            'country':countryList,
        }
        return data
    
class BgpMusterilerSilApi(Resource):
    def delete(self,id):
        islem = BgpMusteriler()
        status = islem.getBgpMusterileriListSil(id)
        data = {
            'status':status,
        }
        return jsonify(data)
   