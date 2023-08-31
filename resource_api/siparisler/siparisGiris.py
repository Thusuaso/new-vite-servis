from views.siparisler import SiparisGiris
from views.raporlar import SiparisMasraf
from views.raporlar import SiparisCeki
from resource_api.siparisler.tedarikciurunlist import TedarikciSiparisUrunListe
from resource_api.siparisler.tedarikcicsiparis import TedarikciIcSiparisListe
from resource_api.operasyon.evrakYukleme.evrakYuklemeListeler import EvrakListeler
from resource_api.raporlar.orderProducts import Order
from views import Kullanici 
from resource_api.kontroller.chat_mail import ChatGiris
from views.listeler import Tedarikci
from flask_restful import Resource,request


class SiparisGirisModel(Resource):
    def get(self,siparisNo):

        product = SiparisGiris()
        cost = SiparisMasraf()
        check = SiparisCeki()
        supplier = TedarikciSiparisUrunListe(siparisNo)
        supplierKind = TedarikciIcSiparisListe()
        documents = EvrakListeler()
        order = Order()
        users = Kullanici()
        chat = ChatGiris()
        productList = product.getSiparis(siparisNo)
        costList = cost.getMasrafListesi(siparisNo)
        checkList = check.getCekiList(siparisNo)
        documentList = documents.getEvrakList(siparisNo)
        supplierProductList = supplier.getTedarikciSiparisAyrintiList()
        supplierList = supplier.getTedarikciSiparisTedarikciAyrintiList()
        supplierDeliveryList = supplierKind.getTedarikciTeslimTurList()
        supplierInvoiceList = supplierKind.getTedariciFaturaTurList()
        orderInformationList = order.getOrderProducts(siparisNo)
        usersList = users.getChatKullaniciList()
        chatList = chat.getChatList(siparisNo)
        
        data = {
            'productList':productList,
            'costList':costList,
            'checkList':checkList,
            'supplierProductList':supplierProductList,
            'supplierList':supplierList,
            'supplierDeliveryList':supplierDeliveryList,
            'supplierInvoiceList':supplierInvoiceList,
            'documentList':documentList,
            'orderInformationList':orderInformationList,
            'usersList':usersList,
            'chatList':chatList
        }

        return data


class SiparisTedarikciList(Resource):
    def get(self):
        tedarikci = Tedarikci()
        supplier = tedarikci.getTedarikciSiparisList()
        return supplier
    


class SiparisGirisBosModel(Resource):
    def get(self):

        siparis = SiparisGiris()

        result = siparis.getSiparisModel()

        return result
    
class ContainerAddApi(Resource):
    def post(self):
        data = request.get_json()
        
        siparis = SiparisGiris()
        result = siparis.setContainerAdd(data)
        return result
    
class ContainerAmountApi(Resource):
    def get(self,sipNo):
        siparis = SiparisGiris()
        result = siparis.getContainerAmount(sipNo)
        return result
