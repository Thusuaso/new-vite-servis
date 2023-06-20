from resource_api.seleksiyon.uretim_liste import UretimListe
from resource_api.seleksiyon.listeler import SeleksiyonListeler,UretimUrunKartKasaKontrol
from resource_api.seleksiyon.uretim import Uretim
from flask_restful import Resource 
from flask import request,jsonify
from resource_api.seleksiyon.kasa_detay import KasaDetayListesi,KasaDetayExcell,KasaDetayGuncelle,TedarikciList,KasaDetayKaydet,KasaDetaySil
from flask_restful import Resource
from flask import jsonify,request,send_file
class SeleksiyonKasaDetay(Resource):
    def get(self):
        kasa_detay = KasaDetayListesi()
        kasa_detay_result = kasa_detay.getKasaDetay()
        return kasa_detay_result
    
class SeleksiyonKasaDetayGuncelleApi(Resource):
    def post(self):
        data = request.get_json()
        islem = KasaDetayGuncelle()
        status = islem.setKasaDetayGuncelle(data)
        kasa_detay = KasaDetayListesi()
        kasaList = kasa_detay.getKasaDetay()
        return jsonify({'status' : status,'kasaList':kasaList})

class SeleksiyonKasaExcell(Resource):
    def post(self):

        data_list = request.get_json()
        islem = KasaDetayExcell()

        result = islem.kasa_detay_excell(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/kasadetay_listesi.xlsx'

        return send_file(excel_path,as_attachment=True) 


class TedarikcilerListApi(Resource):
    def get(self):
        
        islem = TedarikciList()
        result = islem.getTedarikciList()
        return jsonify({'tedarikciList':result})

class SeleksiyonKasaDetayKaydetApi(Resource):
    def post(self):
        datas = request.get_json()
        islem = KasaDetayKaydet()
        status = islem.kaydet(datas)
        kasa_detay = KasaDetayListesi()
        kasaList = kasa_detay.getKasaDetay()
        return jsonify({'status':status,'kasaList':kasaList})
        
class SeleksiyonKasaDetaySilApi(Resource):
    def delete(self,id):
        islem = KasaDetaySil()
        status =  islem.sil(id)
        kasa_detay = KasaDetayListesi()
        kasaList = kasa_detay.getKasaDetay()
        return jsonify({'status':status,'kasaList':kasaList})

class UretimListApi(Resource):

    def get(self):

        production = UretimListe()
        order = SeleksiyonListeler()

        productionList = production.getUretimList()
        orderList = order.getUretimSiparisListe()
        orderDetailList = order.getUretimSiparisDetayList()
        mineList = order.getOcakList()
        supplierList = order.getTedarikciList()
        productUnitList = order.getUrunBirimList()
        productSummaryList = order.getUretimOzetList()


        data = {

            "productionList" : productionList,
            "orderList" : orderList,
            "orderDetailList" : orderDetailList,
            "mineList" : mineList,
            "supplierList" : supplierList,
            "productUnitList" : productUnitList,
            "productSummaryList" : productSummaryList
        }

        return jsonify(data)


class CreateSetAllApi(Resource):
    def post(self):
        
        data = request.get_json()
        islem = UretimListe()
        status = islem.setCrateAll(data)
        uretim = UretimListe()
        siparis = SeleksiyonListeler()

        uretimlist = uretim.getUretimList()
        siparislist = siparis.getUretimSiparisListe()
        siparis_ayrintilist = siparis.getUretimSiparisDetayList()
        ocaklist = siparis.getOcakList()
        tedarikcilist = siparis.getTedarikciList()
        urunbirimlist = siparis.getUrunBirimList()
        uretimozetlist = siparis.getUretimOzetList()
        data = {

            "uretimlist" : uretimlist,
            "siparislist" : siparislist,
            "siparis_ayrintilist" : siparis_ayrintilist,
            "ocaklist" : ocaklist,
            "tedarikcilist" : tedarikcilist,
            "urunbirimlist" : urunbirimlist,
            "uretimozetlist" : uretimozetlist
        }
        return {'status':status,'data':data}



class UretimListModelApi(Resource):

    def get(self,kasano):

        islem = UretimListe()

        result = islem.getUretim(kasano)


        return result

class UretimDetayApi(Resource):

    def get(self,kasano):
        islem = Uretim()

        result = islem.getUrunModel(kasano)

        return result

class UretimDetayBosModelApi(Resource):

    def get(self):

        islem = Uretim()

        result = islem.getBosUrunModel()

        return result

class UretimKayitIslemApi(Resource):
    
    def post(self):

        data = request.get_json()

        islem = Uretim()

        kasa_kontrol = islem.kasaKayitKontrol(data)

        kayit_durum = False

        if kasa_kontrol == True:
            kayit_durum = islem.kaydet(data,None)
            
        uretim = UretimListe()
        siparis = SeleksiyonListeler()

        uretimlist = uretim.getUretimList()
        siparislist = siparis.getUretimSiparisListe()
        siparis_ayrintilist = siparis.getUretimSiparisDetayList()
        ocaklist = siparis.getOcakList()
        tedarikcilist = siparis.getTedarikciList()
        urunbirimlist = siparis.getUrunBirimList()
        uretimozetlist = siparis.getUretimOzetList()


        data2 = {

            "uretimlist" : uretimlist,
            "siparislist" : siparislist,
            "siparis_ayrintilist" : siparis_ayrintilist,
            "ocaklist" : ocaklist,
            "tedarikcilist" : tedarikcilist,
            "urunbirimlist" : urunbirimlist,
            "uretimozetlist" : uretimozetlist
        }
        data = {

            'kayit_durum' : kayit_durum,
            'kasa_kontrol' : kasa_kontrol,
            'data2':data2
        }

        return jsonify(data)

    def put(self):

        islem = Uretim()

        data = request.get_json()

        result = islem.guncelle(data)
        uretim = UretimListe()
        siparis = SeleksiyonListeler()

        uretimlist = uretim.getUretimList()
        siparislist = siparis.getUretimSiparisListe()
        siparis_ayrintilist = siparis.getUretimSiparisDetayList()
        ocaklist = siparis.getOcakList()
        tedarikcilist = siparis.getTedarikciList()
        urunbirimlist = siparis.getUrunBirimList()
        uretimozetlist = siparis.getUretimOzetList()


        data2 = {

            "uretimlist" : uretimlist,
            "siparislist" : siparislist,
            "siparis_ayrintilist" : siparis_ayrintilist,
            "ocaklist" : ocaklist,
            "tedarikcilist" : tedarikcilist,
            "urunbirimlist" : urunbirimlist,
            "uretimozetlist" : uretimozetlist
        }

        return jsonify({'status' : result,'data2':data2})

class UretimSilIslemApi(Resource):

    def delete(self,kasano):

        islem = Uretim()

        result = islem.sil(kasano)
        uretim = UretimListe()
        siparis = SeleksiyonListeler()

        uretimlist = uretim.getUretimList()
        siparislist = siparis.getUretimSiparisListe()
        siparis_ayrintilist = siparis.getUretimSiparisDetayList()
        ocaklist = siparis.getOcakList()
        tedarikcilist = siparis.getTedarikciList()
        urunbirimlist = siparis.getUrunBirimList()
        uretimozetlist = siparis.getUretimOzetList()


        data2 = {

            "uretimlist" : uretimlist,
            "siparislist" : siparislist,
            "siparis_ayrintilist" : siparis_ayrintilist,
            "ocaklist" : ocaklist,
            "tedarikcilist" : tedarikcilist,
            "urunbirimlist" : urunbirimlist,
            "uretimozetlist" : uretimozetlist
        }
        return jsonify({'status' : result,'data2':data2})
    
    


class UretimCokluKayitApi(Resource):

    def post(self):

        islem = Uretim()

        item = request.get_json()

        kayit_durum = False 

        kasa_kontrol = islem.kasaKayitKontrol(item)
        kasa_list = None
        if kasa_kontrol == True:
            kayit_durum,str_kasalar = islem.cokluKaydet(item,item['kayit_sayisi'])

            if kayit_durum == True:
                kasa_list = UretimListe().getUretimKasaList(str_kasalar)
        uretim = UretimListe()
        siparis = SeleksiyonListeler()

        uretimlist = uretim.getUretimList()
        siparislist = siparis.getUretimSiparisListe()
        siparis_ayrintilist = siparis.getUretimSiparisDetayList()
        ocaklist = siparis.getOcakList()
        tedarikcilist = siparis.getTedarikciList()
        urunbirimlist = siparis.getUrunBirimList()
        uretimozetlist = siparis.getUretimOzetList()


        data2 = {

            "uretimlist" : uretimlist,
            "siparislist" : siparislist,
            "siparis_ayrintilist" : siparis_ayrintilist,
            "ocaklist" : ocaklist,
            "tedarikcilist" : tedarikcilist,
            "urunbirimlist" : urunbirimlist,
            "uretimozetlist" : uretimozetlist
        }
        data = {

            'kasa_kontrol' : kasa_kontrol,
            'kayit_durum' : kayit_durum,
            'kasa_list' : kasa_list,
            'data2':data2
        }

        return jsonify(data)

class UretimDisFirmaKasaNoApi(Resource):

    def get(self):

        islem = Uretim()

        kasaNo = islem.getDisFirmaKasaNo()


        return jsonify({'kasano' : kasaNo})
    
class ProductCrateControlApi(Resource):
    def post(self):
        data = request.get_json()
        islem = Uretim()
        status = islem.getProductCrateControl(data)
        return jsonify({'status':status})
class PoProductList(Resource):
    def get(self,po):
        islem = Uretim()
        productList = islem.getPoProductList(po)
        return jsonify({'productList':productList})

class UretimSeleksiyonFirmaKasaNoApi(Resource):

    def get(self):

        islem = Uretim()

        kasaNo = islem.getSeleksiyonFirmaKasaNo()


        return jsonify({'kasano' : kasaNo})


class UretimSeleksiyonUrunKartApi(Resource):

    def get(self,urunkartid):

        islem = Uretim()

        kasaNo = islem.getSeleksiyonUrunKartBilgileri(urunkartid)


        return jsonify({'urunbilgileri' : kasaNo})

class UretimSeleksiyonFazlasiMiApi(Resource):

    def post(self,po,urunkartid):
        islem = Uretim()
        
        data = islem.getUretimFazlasiMi(po,urunkartid)
        

        return jsonify(data)

class UretimOzetListApi(Resource):

    def get(self):

        siparis = SeleksiyonListeler()

        uretimozetlist = siparis.getUretimOzetList()

        data = {

            'uretimozetlist' : uretimozetlist
        }

        return jsonify(data)
  
class UretimSiparisKalemDetay(Resource):

    def get(self,siparisno):

        islem = SeleksiyonListeler()

        result = islem.getUretimSiparisDetay(siparisno)

        return result


class UretimSipListesi(Resource):

    def get(self):

        siparis = SeleksiyonListeler()

        data = siparis.getUretimSipListesi()

        

        return jsonify(data)
class UretimUrunKartKasaKontrolApi(Resource):
    def get(self,urunKartId):
        islem = UretimUrunKartKasaKontrol()
        result = islem.getUretimUrunKartKasaKontrol(urunKartId)
        return jsonify(result)