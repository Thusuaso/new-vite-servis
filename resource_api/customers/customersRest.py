from resource_api.customers.customersList import MusteriListem
from resource_api.customers.customersAyrinti import SatisciAyrinti
from resource_api.customers.customers_Islem import SatisciIslem
from resource_api.musteriler.musteri_detay import MusteriDetayIslem
from flask_restful import Resource
from flask import jsonify,request,send_file


class CustomersListeApi(Resource):

    def get(self,users):
        if (users == 47):
            islem = MusteriListem()
            musteri_listesi = islem.getMusteriListesiAll()
            return musteri_listesi
        else:
            islem = MusteriListem()
            musteri_listesi = islem.getMusteriListesi(users)
            return musteri_listesi


class CustomersListeSatisciApi(Resource):
    def get(self,users):
        islem = MusteriListem()
        must = islem.getMusteriListesiSatisci(users)
        return must

class CustomersListeTekliflerApi(Resource):
    def get(self,users):
        islem = MusteriListem()
        must = islem.getMusteriListesiTeklifler(users)
        return must
    
class CustomersListeBGNApi(Resource):
    def get(self,users):
        islem = MusteriListem()
        must = islem.getMusteriListesiBGN(users)
        return must



class CustomersListeAllApi(Resource):
    def get(self):
        islem = MusteriListem()
        musteri_listesi = islem.getMusteriListesiAll()
        return musteri_listesi
    
class CustomersListeAllSatisciApi(Resource):
    def get(self):
        islem = MusteriListem()
        result = islem.getMusteriListesiAllSatisci()
        return result
    
class CustomersListeAllTekliflerApi(Resource):
    def get(self):
        islem = MusteriListem()
        result = islem.getMusteriListesiAllTeklifler()
        return result
    
    
class CustomersListeAllTekliflerBGNApi(Resource):
    def get(self):
        islem = MusteriListem()
        result = islem.getMusteriListesiAllTekliflerBGN()
        return result





class CustomersDetayApi(Resource):

    def get(self,musteri_adi):

        musteri = SatisciAyrinti()

        musteriDetay = musteri.getAyrintiList(musteri_adi)
        tekliflermusteriDetay = musteri.getTeklifAyrintiList(musteri_adi)
        data = {
            'musteriDetay':musteriDetay,
            'tekliflermusteriDetay':tekliflermusteriDetay
        }
        return data

class CustomersKayitIslemList(Resource):

    def get(self,musteriadi,id):

        islem = SatisciIslem()

        musteri_list = islem.getSatisciList(musteriadi,id)
        musteri_data = islem.getSatisciModel(musteriadi,id)
        

        data = {

            "musteri_list" : musteri_list,
            "musteri_data" : musteri_data
        }

        return jsonify(data)

class CustomersKayitIslemList(Resource):

    def get(self,musteriadi,id):

        islem = SatisciIslem()

        musteri_list = islem.getSatisciList(musteriadi,id)
        musteri_data = islem.getSatisciModel(musteriadi,id)
        

        data = {

            "musteri_list" : musteri_list,
            "musteri_data" : musteri_data
        }

        return jsonify(data) 

class CustomersDosyaKaydet(Resource):

    def post(self):

        islem = request.get_json()

        satisciIslem = SatisciIslem()
        result = satisciIslem.satisciDosyaKaydet(islem)

        return jsonify({'Status' : result})        

class CustomersKayitIslemModel(Resource):

    def get(self):

        islem = SatisciIslem()

        musteri_list = islem.getYeniSatisciModel()
        
        

        return jsonify(musteri_list)        

class CustomersKayitIslem(Resource):

    def post(self):

        item = request.get_json()
        islem = SatisciIslem()

        data = islem.satisciKaydet(item)

        return jsonify(data)

    def put(self):

        item = request.get_json()
        print(item)
        
        islem = SatisciIslem()
        data = islem.satisciGuncelle(item)

        return jsonify(data)

class CustomersKayitSilme(Resource):

    def delete(self,id):

        islem = SatisciIslem()

        data = islem.satisciSilme(id)

        return jsonify(data)            


class CustomersHatirlatmaApi(Resource):

    def get(self,kullanici_id):

        islem = SatisciIslem()

        musteri_list = islem.getHatirlatmaList(kullanici_id)

        return jsonify(musteri_list) 

class CustomersChangePriority(Resource):
    def get(self,customer,priority):
        islem = SatisciIslem()
        status,changePriority = islem.setPriority(customer,priority)
        data = {
            'status':status,
            'changePriority':changePriority
        }
        return jsonify(data)
    
class CustomersChangeFollow(Resource):
    def get(self,customer,follow):
        islem = SatisciIslem()
        status = islem.setFollowing(customer,follow)
        data = {
            'status':status,
        }
        return jsonify(data)
class CustomersTemsilciList(Resource):
    def get(self):
        islem = MusteriDetayIslem()
        result = islem.getTemsilciList()
        return jsonify(result)
    
class CustomersChangeRepresentative(Resource):
    def get(self,customer,representative):
        islem = SatisciIslem()
        status,result = islem.getChangeRepresentative(customer,representative)
        data = {
            'status':status,
            'customerData':result
        }
        return jsonify(data)




