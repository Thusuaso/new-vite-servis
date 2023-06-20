from flask_restful import Resource
from views.siparisler.listeler import SiparisListe
from views.siparisler.listeler import UrunBirim
from views.listeler import Tedarikci
from views.siparisler import TeslimTur
from views.siparisler import OdemeTur
from views.siparisler import faturaKesimTur
from views.shared import Ulkeler
from views import Musteri
from views import Kullanici

class SiparisListResource(Resource):
    def get(self,siparisDurum,yil):

        siparis = SiparisListe(siparisDurum)
        urunBirim = UrunBirim()
        tedarikci = Tedarikci()
        teslimTur = TeslimTur()
        odemeTur = OdemeTur()
        faturaTur = faturaKesimTur()
        ulke = Ulkeler()
        musteri = Musteri()
        kullanici = Kullanici()

        products = siparis.getSiparisUrunList(yil)
        productUnit = urunBirim.getUrunBirimList()
        supplier = tedarikci.getTedarikciSiparisList()
        delivery = teslimTur.getTeslimTurList()
        payment = odemeTur.getOdemeTurList()
        invoice = faturaTur.getFaturaKesimTurList()
        country = ulke.getUlkeList()
        customers = musteri.getMusteriList()
        users = kullanici.getKullaniciList()
        
        
        
        
        data={
            'products':products,
            'productUnit':productUnit,
            'supplier':supplier,
            'delivery':delivery,
            'payment':payment,
            'invoice':invoice,
            'country':country,
            'customers':customers,
            'users':users
        }
        return data

class SiparisHepsiListResource(Resource):
    def get(self,siparisDurum):

        siparis = SiparisListe(siparisDurum)

        # result = siparis.getSiparisList()
       
        result2= siparis.getSiparisUrunHepsiList()
        
        return result2      
       

