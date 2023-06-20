from resource_api.raporlar.site_yeni_urunler import SiteYeniUrunler
from resource_api.raporlar.siparis_ozet import SiparisOzetListeler
from resource_api.raporlar.kullaniciSiparisOzet import KullaniciSiparisOzetListeler
from resource_api.raporlar.uretim_rapor import UretimRapor
from resource_api.raporlar.excel_cikti import ExcelCiktiIslem
from resource_api.raporlar.sevkiyat_rapor import SevkiyatRapor
from resource_api.raporlar.sev_sip_ayrinti import SevSipAyrinti
from resource_api.raporlar.kullaniciSiparisO_Ayrinti  import KullaniciSevSipAyrinti
from resource_api.raporlar.musteriListe import MusteriListesi
from resource_api.raporlar.ayrintiliMusterilist import GenelMusteriListesi
from resource_api.raporlar.yukleme import YuklemeListeler
from resource_api.raporlar.atlanta_rapor import AtlantaYuklemeListeler
from flask_restful import Resource
from flask import jsonify,request,send_file
from resource_api.raporlar.stokraporu import StokRapor
from resource_api.raporlar.atlanta_stok import DepoStokListesi
from resource_api.raporlar.pdf_cikti import FooterCanvas
from resource_api.raporlar.ocakListesiRaporu import OcakListesiRapor
from resource_api.raporlar.SeleksiyonOcakListesiRaporApiExcell import OcakRaporuExcelCiktiIslem
from resource_api.raporlar.musteriListesi_ExcelCikti import ExcelCiktiIslemMusteri
from resource_api.raporlar.siparisBazindaOzetRapor import SiparisBazindaOzetRapor
from resource_api.raporlar.musteriBazindaAyrinti import MusBazYilAyrinti
from resource_api.raporlar.MusteriBazindaRaporApiExcell import MusteriBazindaExcellCikti
from resource_api.raporlar.ulkeBazindaSevkiyat import UlkeBazindaSevkiyat
from resource_api.raporlar.allOrders import AllOrders
from resource_api.raporlar.orderProducts import Order
from views.raporlar.anaSayfaDegisiklik import UretimUrunler
from resource_api.raporlar.uretimTedarikciBazinda import UretimTedarikci
from resource_api.raporlar.nakliyeBazindaRapor import NakliyeBazinda
from resource_api.raporlar.fobMasraflar import FobMasraflari
from resource_api.raporlar.navlunMasraflar import NavlunMasraflar
from resource_api.raporlar.digerMasraflar import DigerMasraflar
from resource_api.raporlar.mekusMasrafları import MekusMasraflar
from resource_api.raporlar.komisyonMasrafları import KomisyonMasraflar
from resource_api.raporlar.bankaVeEvrakMasraflar import BankaVeEvrakMasraflar
from resource_api.raporlar.orderProducts import MusteriBazindaUretim
class SiteYeniUrunListApi(Resource):

    def get(self):

        urunler = SiteYeniUrunler()

        liste = urunler.getYeniUrunList()


        return liste

class YeniEklenenSiparislerListApi(Resource):

    def get(self):

        urunler = SiteYeniUrunler()

        liste = urunler.getYeniSiparisList()
        mekmar_liste = urunler.getYeniSiparisMekmarList()

        data = {

            "liste" : liste,
            "mekmar_liste" : mekmar_liste
        }

        return jsonify(data)  

class SiparisOzetRaporlarApi(Resource):

    def get(self,userId):

        islem = SiparisOzetListeler()
        kullanici = KullaniciSiparisOzetListeler(userId)
        siparis_list = islem.getSiparisAyOzetList()
        sevk_list = islem.getSevkiyatAyOzetList()
        siparis_gecen_yil_list = kullanici.getAyOzetList_gecenYil()
        siparis_bu_yil_list = kullanici.getAyOzetList_buYil()
        sevkiyat_gecen_yil_list = kullanici.getAyOzetList_SevkiyatgecenYil()
        sevkiyat_bu_yil_list = kullanici.getAyOzetList_SevkiyatbuYil()
        data = {

            "siparis_list" : siparis_list,
            "sevk_list" : sevk_list,
            'siparis_gecen_yil_list':siparis_gecen_yil_list,
            'siparis_bu_yil_list':siparis_bu_yil_list,
            'sevkiyat_gecen_yil_list':sevkiyat_gecen_yil_list,
            'sevkiyat_bu_yil_list':sevkiyat_bu_yil_list
            
          
        }

        return jsonify(data)



class SiparisBazindaOzetRaporlarApi(Resource):

    def get(self):

        islem = SiparisBazindaOzetRapor()

        bu_yil = islem.getSiparisBazindaAyListesiBuYil()
        gecen_yil = islem.getSiparisBazindaAyListesiGecenYil()
        onceki_yil = islem.getSiparisBazindaAyListesiOncekiYil()
        data = {

            "bu_yil" : bu_yil,
            "gecen_yil" : gecen_yil,
            "onceki_yil":onceki_yil
          
        }

        return jsonify(data)





class SiparisOzetKullaniciApi(Resource):

    def get(self,kullaniciAdi):

        islem = KullaniciSiparisOzetListeler(kullaniciAdi)

        siparis_gecen_yil_list = islem.getAyOzetList_gecenYil()
        siparis_bu_yil_list = islem.getAyOzetList_buYil()
        sevkiyat_gecen_yil_list = islem.getAyOzetList_SevkiyatgecenYil()
        sevkiyat_bu_yil_list = islem.getAyOzetList_SevkiyatbuYil()

        #fark yüzdelerinin yüklenmesi
        

        data = {

            "gecenYilSip" : siparis_gecen_yil_list,
            "buYilSip" : siparis_bu_yil_list,
            "gecenYilYukleme" : sevkiyat_gecen_yil_list,
            "buYilYukleme" : sevkiyat_bu_yil_list
        }

        return jsonify(data)   

class FinansTakipListesi(Resource):
   
    def get(self,kullaniciAdi): 

        islem = KullaniciSiparisOzetListeler(kullaniciAdi) 

        result = islem.getFinansTakipListesi()

        return jsonify(result)      

class UretimRaporApi(Resource):

    def get(self):

        islem = UretimRapor()

        uretim_listesi = islem.getUretimListesiHepsi()

        return uretim_listesi
    
class UretimRaporBuYilApi(Resource):
    def get(self,yil):
        islem = UretimRapor()
        uretim_listesi = islem.getUretimListesiYil(yil)
        return uretim_listesi

class UretimRaporTarihApi(Resource):

    def get(self,tarih):

        islem = UretimRapor()

        uretim_listesi = islem.getUretimListesiSonTariheGore(tarih)

        return uretim_listesi

class UretimRaporIkiTarihApi(Resource):

    def get(self,ilk_tarih,son_tarih):

        islem = UretimRapor()

        uretim_listesi = islem.getUretimListesiIkiTarihArasi(ilk_tarih,son_tarih)

        return uretim_listesi

class UretimRaporExcelApi(Resource):

    def post(self):

        data_list = request.get_json()
        
        islem = ExcelCiktiIslem()
        
        result = islem.uretim_rapor_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/uretim_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class OcakRaporExcellApi(Resource):

    def post(self):

        data_list = request.get_json()
        
        islem = OcakRaporuExcelCiktiIslem()
        
        result = islem.ocak_rapor_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/ocak_listesi_raporu.xlsx'

        return send_file(excel_path,as_attachment=True)
    
class SipKalanExcellApi(Resource):

    def post(self):

        data_list = request.get_json()
        
        islem = OcakRaporuExcelCiktiIslem()
        
        result = islem.sip_kalan_listesi_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/sipKalanListesiExcell.xlsx'

        return send_file(excel_path,as_attachment=True)



class MusteriBazindaRaporToplamExcellApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = MusteriBazindaExcellCikti()

        result = islem.musteri_bazinda_toplam_excell(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/musterisip_bazinda_rapor_toplam.xlsx'

        return send_file(excel_path,as_attachment=True)


class MusteriBazindaRaporExcellApi(Resource):

    def post(self):

        data_list = request.get_json()
        
        islem = MusteriBazindaExcellCikti()
        if len(data_list)==1:
            data = data_list['datas']
            result = islem.musteri_bazinda_rapor_cikti_tekli(data) 
        elif len(data_list) != 1:
            data = data_list['datas']
            dataSum = data_list['dataSum']
            result = islem.musteri_bazinda_rapor_cikti_coklu(data,dataSum)
        
        

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/musterisip_bazinda_rapor.xlsx'

        return send_file(excel_path,as_attachment=True)

class SevkiyatRaporHepsiMekmerApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeHepsiMekmer()

        return sevkiyat_listesi
    
    
class SevkiyatRaporAllMekmerApi(Resource):

    def get(self):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeAllMekmer()

        return sevkiyat_listesi
    

class SevkiyatRaporHepsiMekmarApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeHepsiMekmar()

        return sevkiyat_listesi
    
    
class SevkiyatRaporAllMekmarApi(Resource):

    def get(self):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeAllMekmar()

        return sevkiyat_listesi
    
    

class SevkiyatRaporTarihMekmarApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeTarihMekmar(tarih)

        return sevkiyat_listesi
    
class SevkiyatRaporTekTarihMekmarApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeTekTarihMekmar(tarih)

        return sevkiyat_listesi    
    
class SevkiyatRaporIkiTarihMekmarApi(Resource):

    def get(self,ilk_tarih,son_tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeIkiTarihMekmar(ilk_tarih,son_tarih)

        return sevkiyat_listesi
    
    
    
class SevkiyatRaporTarihMekmerApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeTarihMekmer(tarih)

        return sevkiyat_listesi
    
class SevkiyatRaporTekTarihMekmerApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeTekTarihMekmer(tarih)

        return sevkiyat_listesi    
    
class SevkiyatRaporIkiTarihMekmerApi(Resource):

    def get(self,ilk_tarih,son_tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeIkiTarihMekmer(ilk_tarih,son_tarih)

        return sevkiyat_listesi






class SevkiyatRaporExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.sevkiyat_rapor_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/sevkiyat_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class StokRaporRaporApi(Resource):

    def get(self):

        islem = StokRapor()

        stok_listesi = islem.getStokListesiHepsi()
        stok_top_listesi = islem.getStokTopListesi()

        data = {

            "stok_listesi" : stok_listesi,
            "stok_top_listesi" : stok_top_listesi
        }

        return jsonify(data)


class StokRaporOlculeriApi(Resource):

    def get(self):

        islem = StokRapor()

        data = islem.getStokOlculerListesi()
       
        return jsonify(data)
    
class StokRaporAnaListeApi(Resource):

    def get(self):

        islem = StokRapor()

        data = islem.getStokAnaList()
       
        return jsonify(data)
    
class StokRaporOnylMekmerApi(Resource):

    def get(self):

        islem = StokRapor()

        data = islem.getStokOnlyMekmer()
       
        return jsonify(data)

class StokRaporAnaListeFilterApi(Resource):

    def get(self,tedarikci):
        
        islem = StokRapor()

        data = islem.getStokFilterList(tedarikci)
       
        return jsonify(data)
    
    
class StokRaporMekmerMekmozApi(Resource):
    def get(self):
        islem = StokRapor()
        data = islem.getStokRaporMekmerMekmoz()
        return jsonify(data)
    
class StokRaporDisApi(Resource):
    def get(self):
        islem = StokRapor()
        data = islem.getStokRaporDis()
        return jsonify(data)
    
    
class StokRaporDisMekmardaOlanlarApi(Resource):
    def get(self):
        islem = StokRapor()
        data = islem.getStokRaporDisMekmardaOlanlar()
        return jsonify(data)
    
class StokRaporMekmerMekmozAyrintiApi(Resource):
    def get(self,urunId):
        islem = StokRapor()
        data = islem.getStokRaporMekmerMekmozAyrinti(urunId)
        return jsonify(data)
    
class StokRaporDisAyrintiApi(Resource):
    def get(self,urunId):
        islem = StokRapor()
        data = islem.getStokRaporDisAyrinti(urunId)
        return jsonify(data)
    
    
    
class StokRaporDisMekmardaOlanAyrintiApi(Resource):
    def get(self,urunId):
        islem = StokRapor()
        data = islem.getStokRaporDisMekmardaOlanAyrinti(urunId)
        return jsonify(data)


class StokRaporuFiyatliExcelCiktiApi(Resource):

    def post(self):

        data_list = request.get_json()
        
        islem = StokRapor()
        
        result = islem.setStockExcellCikti(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/stock_list_fiyatli.xlsx'

        return send_file(excel_path,as_attachment=True)




class StokAyrintiRaporApi(Resource):
     
       def get(self,en,boy,kenar,yuzeyIslem,urunAdi,listDurum):

        islem = StokRapor()
        if listDurum == 1:
            
            stok_ayrinti_listesi = islem.getStokTopAyrintiListesi(en,boy,kenar,yuzeyIslem,urunAdi)
        elif listDurum ==2:
            stok_ayrinti_listesi = islem.getStokTopAyrintiListesiMekmer(en,boy,kenar,yuzeyIslem,urunAdi)
        elif listDurum == 3:
            
            stok_ayrinti_listesi = islem.getStokTopAyrintiListesiMekmoz(en,boy,kenar,yuzeyIslem,urunAdi)
        elif listDurum == 4:
            stok_ayrinti_listesi = islem.getStokTopAyrintiListesiOnlyStockMekmer(en,boy,kenar,yuzeyIslem,urunAdi)
        
        data = {

            "stok_ayrinti_listesi" : stok_ayrinti_listesi
        
              }

        return jsonify(data)

class KullaniciSevSipAyrintiApi(Resource):

    def get(self,username,ay):

        islem = KullaniciSevSipAyrinti(username)

        sevkiyat_bu_yil = islem.getBuYilSevkiyatAyrinti(ay)
        sevkiyat_gecen_yil = islem.getGecenYilSevkiyatAyrinti(ay)
        siparis_gecen_yil = islem.getGecenYilSiparisAyrinti(ay)
        siparis_bu_yil = islem.getBuYilSiparisAyrinti(ay)

        data = {

            "sevkiyat_bu_yil" : sevkiyat_bu_yil,
            "sevkiyat_gecen_yil" : sevkiyat_gecen_yil,
            "siparis_gecen_yil" : siparis_gecen_yil,
            "siparis_bu_yil" : siparis_bu_yil
            }
       
        return jsonify(data)             


        

class SevkiyatBuYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getBuYilSevkiyatAyrinti(ay)

        return ayrinti_listesi  

class SevkiyatOncekiYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getOncekiYilSevkiyatAyrinti(ay)

        return ayrinti_listesi          

class SevkiyatGecenYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getGecenYilSevkiyatAyrinti(ay)

        return ayrinti_listesi     

class SiparisGecenYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getGecenYilSiparisAyrinti(ay)

        return ayrinti_listesi  

class SiparisGecenYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getGecenYilSiparisAyrinti(ay)

        return ayrinti_listesi         

class SiparisBuYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getBuYilSiparisAyrinti(ay)

        return ayrinti_listesi     

class SiparisOncekiYilAyrintiListesiApi(Resource):

    def get(self,ay):

        islem = SevSipAyrinti()

        ayrinti_listesi = islem.getOncekiilSiparisAyrinti(ay)

        return ayrinti_listesi 
    
    
class MusteriBazindaAyrintiApi(Resource):

    def get(self,yil,ay):

        islem = MusBazYilAyrinti()
        if ay == 1:
            
            data = islem.getMusSipAyrinti(yil,ay)

            return jsonify(data)
        elif ay == 2:
            
            subat = islem.getMusSipAyrinti(yil,ay)
            subatToplami = islem.getMusSipAyrintiToplami(yil,ay)
            
            result = {
                'subat':subat,
                'subatToplami':subatToplami
            }
            return jsonify(result)
        elif ay == 3:
            mart = islem.getMusSipAyrinti(yil,ay)
            martToplami = islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'mart':mart,
                'martToplami':martToplami
            }
            return jsonify(result)
        elif ay == 4:
            nisan = islem.getMusSipAyrinti(yil,ay)
            nisanToplami = islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'nisan':nisan,
                'nisanToplami':nisanToplami
            }
            return jsonify(result)
        elif ay == 5:
            mayis = islem.getMusSipAyrinti(yil,ay)
            mayisToplami = islem.getMusSipAyrintiToplami(yil,ay)

            result = {
                'mayis':mayis,
                'mayisToplami':mayisToplami
            }
            
            return jsonify(result)
        elif ay == 6:
            haziran = islem.getMusSipAyrinti(yil,ay)
            haziranToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'haziran':haziran,
                'haziranToplami':haziranToplami
                
            }
            
            return jsonify(result)
        elif ay == 7:
            temmuz = islem.getMusSipAyrinti(yil,ay)
            temmuzToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'temmuz':temmuz,
                'temmuzToplami':temmuzToplami
                
            }
            
            return jsonify(result)
        elif ay == 8:
            agustos = islem.getMusSipAyrinti(yil,ay)
            agustosToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'agustos':agustos,
                'agustosToplami':agustosToplami
                
            }
            
            return jsonify(result)
        elif ay == 9:
            eylul = islem.getMusSipAyrinti(yil,ay)
            eylulToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'eylul':eylul,
                'eylulToplami':eylulToplami
                
            }
            
            return jsonify(result)
        elif ay == 10:
            ekim = islem.getMusSipAyrinti(yil,ay)
            ekimToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'ekim':ekim,
                'ekimToplami':ekimToplami
                
            }
            
            return jsonify(result)
        elif ay == 11:
            kasim = islem.getMusSipAyrinti(yil,ay)
            kasimToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'kasim':kasim,
                'kasimToplami':kasimToplami
                
            }
            
            return jsonify(result)
        elif ay == 12:
            aralik = islem.getMusSipAyrinti(yil,ay)
            aralikToplami= islem.getMusSipAyrintiToplami(yil,ay)
            result = {
                'aralik':aralik,
                'aralikToplami':aralikToplami
                
            }
            
            return jsonify(result)

class UreticiBazindaApi(Resource):
    def get(self,year):
        islem = UretimTedarikci()
        result = islem.getUretimTedarikci(year)
        return result

class NakliyeBazindaApi(Resource):
    def get(self,year):
        islem = NakliyeBazinda()
        result = islem.getNakliyeBazinda(year)
        return result
    
class NakliyeBazindaExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = NakliyeBazinda()
        result = islem.getNakliyeExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/nakliyeciRapor.xlsx'

        return send_file(excel_path,as_attachment=True)

class FobMasraflarApi(Resource):
    def get(self,year):
        islem = FobMasraflari()
        result = islem.getFobMasraflari(year)
        return result
    
class FobMasraflarExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = FobMasraflari()
        result = islem.getFobMasrafExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/fobMasraflar.xlsx'

        return send_file(excel_path,as_attachment=True)
    



class NavlunMasraflarApi(Resource):
    def get(self,year):
        islem = NavlunMasraflar()
        result = islem.getNavlunMasraflar(year)
        return result
    
class NavlunMasraflarExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = NavlunMasraflar()
        result = islem.getNavlunMasraflarExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/navlunMasraflar.xlsx'

        return send_file(excel_path,as_attachment=True) 



class DigerMasraflarApi(Resource):
    def get(self,year):
        islem = DigerMasraflar()
        result = islem.getDigerMasraflar(year)
        return result
    
class DigerMasraflarExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = DigerMasraflar()
        result = islem.getDigerMasraflarExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/digerMasraflar.xlsx'

        return send_file(excel_path,as_attachment=True) 






class MekusMasraflarApi(Resource):
    def get(self,year):
        islem = MekusMasraflar()
        result = islem.getMekusMasraflar(year)
        return result
    
class MekusMasraflarExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = MekusMasraflar()
        result = islem.getMekusMasraflarExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/mekusMasraflar.xlsx'

        return send_file(excel_path,as_attachment=True) 





class KomisyonMasraflarApi(Resource):
    def get(self,year):
        islem = KomisyonMasraflar()
        result = islem.getKomisyonMasraflar(year)
        return result
    
class KomisyonMasraflarExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = KomisyonMasraflar()
        result = islem.getKomisyonMasraflarExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/komisyonMasraflar.xlsx'

        return send_file(excel_path,as_attachment=True) 


class BankaVeEvrakMasraflarApi(Resource):
    def get(self,year):
        islem = BankaVeEvrakMasraflar()
        result = islem.getBankaVeEvrakMasraflar(year)
        return result
    
class BankaVeEvrakMasraflarExcelApi(Resource):
    def post(self):
        data_list = request.get_json()
        islem = BankaVeEvrakMasraflar()
        result = islem.getBankaVeEvrakMasraflarExcel(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/bankaVeEvrakMasraflar.xlsx'

        return send_file(excel_path,as_attachment=True) 








    
class UreticiBazindaExcelApi(Resource):

    def post(self):

        data_list = request.get_json()
        islem = UretimTedarikci()

        result = islem.getUretimTedarikciExcel(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/uretimTedarikciRapor.xlsx'

        return send_file(excel_path,as_attachment=True) 



class UlkeBazindaSevkiyatApi(Resource):

    def get(self):

        islem = UlkeBazindaSevkiyat()
        
        
        result = islem.getUlkeBazindaSevkiyat()
            
        return jsonify(result)
    
class UlkeBazindaSevkiyaYearsListApi(Resource):
    def get(self):
        islem = UlkeBazindaSevkiyat()
        result = islem.getUlkeBazindaSevkiyatYearsList()
        return jsonify(result)
    
class UlkeBazindaSevkiyatAyrintiApi(Resource):

    def get(self,ulkeId,year):

        islem = UlkeBazindaSevkiyat()
        
        
        result = islem.getUlkeBazindaSevkiyatAyrinti(ulkeId,year)
            
        return jsonify(result)
    
class UlkeBazindaSevkiyatYearsApi(Resource):

    def get(self,year):
        
        islem = UlkeBazindaSevkiyat()
        result = islem.getUlkeBazindaSevkiyatYear(year)
        return jsonify(result)
            
    










class SeleksiyonRaporApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.seleksiyon_rapor_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/seleksiyon_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)  





class SeleksiyonEtiketApi(Resource):

    def post(self):

        data_list = request.get_json()
        islem = ExcelCiktiIslem()

        result = islem.seleksiyon_etiket_ciktisi(data_list)

        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/Seleksiyon Üretim Etiket.xlsx'

        return send_file(excel_path,as_attachment=True)    

class SeleksiyonEtiketTarihApi(Resource):
    def get(self,tarih):

        islem = UretimRapor()

        uretim_listesi = islem.getSeleksiyonEtiketTariheGore(tarih)

        return uretim_listesi   


class StokRaporExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.stok_rapor_ciktisi(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/Stok_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)      




class StokRaporAyrintiExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = OcakRaporuExcelCiktiIslem()

        result = islem.stok_rapor_ciktisi_ayrinti(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/Stok_listesi_ayrinti.xlsx'

        return send_file(excel_path,as_attachment=True)      







class KullaniciBazliMusteriApi(Resource):

    def get(self,username):

        islem = MusteriListesi(username)

        data = islem.getMusteriSiparis()
        
       
        return jsonify(data)

class GenelMusteriApi(Resource):

    def get(self):

        islem = GenelMusteriListesi()
        
        data = islem.getGenelMusteriSiparis()
       
        return jsonify(data)  
    
class CustomerDetailList(Resource):
    def get(self,sipNo):
        islem = GenelMusteriListesi()
        data = islem.getCustomersDetailList(sipNo)
        return data  

class KullaniciBazliAyrintiMusteriApi(Resource):

    def get(self,kullanici_id):

        islem = MusteriListesi()

        data = islem.getKullaniciAySiparisAyrinti(kullanici_id)
       
        return jsonify(data)


class MusteriExcellCikti(Resource):
    def post(self):

        data_list = request.get_json()
        islem = ExcelCiktiIslemMusteri()

        result = islem.musteri_rapor_ciktisi(data_list)
        
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/musteri_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)

class MusteriSiparisExcellCikti(Resource):
    def post(self):

        data_list = request.get_json()
        islem = ExcelCiktiIslemMusteri()

        result = islem.musteri_sip_rapor_ciktisi(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/musteriSipYilListesi.xlsx'

        return send_file(excel_path,as_attachment=True)


class UlkeBazindaExcellCikti(Resource):
    def post(self):

        data_list = request.get_json()
        islem = ExcelCiktiIslemMusteri()

        result = islem.get_ulke_bazinda_sip_top(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/ulkebzindaSevkiyat.xlsx'

        return send_file(excel_path,as_attachment=True)
    
    
class MonthMarketingExcellCikti(Resource):
    def post(self):

        data_list = request.get_json()
        islem = ExcelCiktiIslemMusteri()

        result = islem.get_month_marketing_excel_cikti(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/monthMarketingExcel.xlsx'

        return send_file(excel_path,as_attachment=True)

class MonthMarketingAyrintiExcellCikti(Resource):
    def post(self):

        data_list = request.get_json()
        islem = ExcelCiktiIslemMusteri()

        result = islem.get_month_marketing_ayrinti_excel_cikti(data_list)
        return jsonify({'status' : result})

    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/monthMarketingAyrintiExcel.xlsx'

        return send_file(excel_path,as_attachment=True)
    
            

class MusteriBazindaSiparisAyrintiApi(Resource):
    def get(self,year,month):

        islem = MusteriListesi()

        data = islem.getKullaniciAySiparisAyrinti(kullanici_id)
       
        return jsonify(data)      




class KullaniciBazliAnasayfaApi(Resource):

    def get(self,username):

        islem = MusteriListesi(username)

        KullaniciSiparis = islem.getKullaniciAySiparisAyrinti()
        TakipList = islem.getKullaniciTakipListesi()
        YillikSiparis = islem.getKullaniciSiparisYilAyrinti()
        AylikSiparis = islem.getKullaniciSiparisAyAyrinti()
        AylikSevk = islem.getKullaniciSevkAyAyrinti()
        YillikSevk = islem.getKullaniciSevkYilAyrinti()

        data = {

            "KullaniciSiparis" : KullaniciSiparis,
            "TakipList" : TakipList,
            "YillikSiparis" : YillikSiparis,
            "AylikSiparis" : AylikSiparis,
            "AylikSevk" : AylikSevk,
            "YillikSevk" : YillikSevk

              }
       
        return jsonify(data)             

class YuklemeRaporIslemApi(Resource):

    def get(self,yil,ay):

        islem = YuklemeListeler()

        aylik_yukleme_listesi = islem.getYuklemeRaporAylik(yil,ay)
        yillik_yukleme_listesi = islem.getYuklemeRaporYillik(yil,ay)
        #aylik_sayim_listesi = islem.getYuklemeSayimAylik(yil,ay)
        yillik_sayim_listesi = islem.getYuklemeSayimYillik(yil,ay)
        musteribazinda_aylik =  islem.getYuklemeRaporAylikMusteriBazinda(yil,ay)
        
        data = {

            "aylik_yukleme_listesi" : aylik_yukleme_listesi,
            "yillik_yukleme_listesi" : yillik_yukleme_listesi,
          #  "aylik_sayim_listesi" : aylik_sayim_listesi,
            "yillik_sayim_listesi" : yillik_sayim_listesi,
            "musteribazinda_aylik" : musteribazinda_aylik
        }
      
        return jsonify(data)


class YuklemeRaporIslemYearApi(Resource):
    def get(self,year):
        islem = YuklemeListeler()
        result = islem.getYuklemeRaporuYillik(year)
        return jsonify(result)


class IstatistiklerApi(Resource):
    def get(self):
        
        islem = Istatistikler()
        result = islem.getNewCustomerDataList()
        return result
        
        
        

class YuklemeAtlantaRaporIslemApi(Resource):

    def get(self,yil,ay):

        islem = AtlantaYuklemeListeler()

        aylik_yukleme_listesi = islem.getYuklemeRaporAylik(yil,ay)
        yillik_yukleme_listesi = islem.getYuklemeRaporYillik(yil,ay)
        
        musteribazinda_aylik =  islem.getYuklemeRaporAylikMusteriBazinda(yil,ay)
        
        data = {

            "aylik_yukleme_listesi" : aylik_yukleme_listesi,
            "yillik_yukleme_listesi" : yillik_yukleme_listesi,
             "musteribazinda_aylik" : musteribazinda_aylik
        }
      
        return jsonify(data)         

class YuklemeRaporYilListApi(Resource):

    def get(self):

        islem = YuklemeListeler()

        yil_listesi = islem.getYilListesi()
        

        return yil_listesi

class YuklemeRaporIslemAyListesi(Resource):

    def get(self,yil): 

        islem = YuklemeListeler()

        ay_listesi = islem.getAyListesi(yil)

        return ay_listesi      

class YuklemePoExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.yukleme_po_ciktisi(data_list)
        
        return jsonify({'status' : result}) 
  
    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/yukleme_po_bazında.xlsx'

        return send_file(excel_path,as_attachment=True)
  
class YuklemeMusteriExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.yukleme_musteri_ciktisi(data_list)
        
        return jsonify({'status' : result}) 
  
    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/Yukleme-Musteri.xlsx'

        return send_file(excel_path,as_attachment=True) 

class YuklemeYilExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.yukleme_Yil_ciktisi(data_list)
        
        return jsonify({'status' : result}) 
  
    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/Yukleme-Yil.xlsx'

        return send_file(excel_path,as_attachment=True)    

class SiparisOzetExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.siparis_ozet_rapor_ciktisi(data_list)
        
        return jsonify({'status' : result}) 
  
    def get(self):

        excel_path = 'resource_api/raporlar/dosyalar/SiparisOzet.xlsx'

        return send_file(excel_path,as_attachment=True)        
           


class SeleksiyonOcakListesiRaporApi(Resource):
    def get(self):

        urunler = OcakListesiRapor()

        liste = urunler.getOcakListesi()


        return liste
class SeleksiyonOcakListesiDetayApi(Resource):
    def get(self,ocakadi):
        urunler = OcakListesiRapor()

        liste = urunler.getOcakListesiDetaylı(ocakadi)
        liste2 = urunler.getOcakListesiDetaylUretim(ocakadi)
        data = {

            "ocakDetay" : liste,
            "ocakDetayUretim":liste2
       }
        return jsonify(data)
class AllOrdersRaporApi(Resource):
    def get(self):
        
        islem = AllOrders()
        result = islem.getAllOrders()
        return jsonify(result)
    
class OrderRaporApi(Resource):
    def get(self,po):
        islem = Order()
        resultProducts = islem.getOrderProducts(po)
        return jsonify(resultProducts)
    
    
class MusteriBazindaUretimApi(Resource):
    def get(self):
        islem = MusteriBazindaUretim()
        result = islem.getMusteriBazindaUretim()
        return jsonify(result)

    
        

        

class AtlantaStokApi(Resource):

    def get(self):

        urunler = DepoStokListesi()

        liste = urunler.getAtlantaStok()

        return liste

class AtlantaStokAyrintiApi(Resource):

    def get(self,skuNo):

        urunler = DepoStokListesi()

        stok_liste = urunler.getStokList(skuNo)
        su_liste = urunler.getSuList(skuNo)
        satis_liste = urunler.getSatisList(skuNo)
        maliyet = urunler.getMaliyetList(skuNo)

        data = {

            "stok_liste" : stok_liste,
            "su_liste" : su_liste,
            "satis_liste" : satis_liste,
            "maliyet" : maliyet

         
        }
      
        return jsonify(data)


              

class AtlantaStokExcelApi(Resource):

    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.depo_stok_ciktisi(data_list)
        
        return jsonify({'status' : result}) 
  
    def get(self):
        
        excel_path = 'resource_api/raporlar/dosyalar/Atlanta_SM_stock.xlsx'

        return send_file(excel_path,as_attachment=True)      

class FooterCanvasPDF(Resource):

    def post(self):

        data_list = request.get_json()

        islem = FooterCanvas()
        result = islem.pdfciktisi(data_list)
        
        
        return jsonify({'status' : result}) 
  
    def get(self):
        
        excel_path = 'Form.pdf'

        return send_file(excel_path,as_attachment=True)      

    
    
    
class UrunlerUretimListApi(Resource):
    def get(self):
        
        islem = UretimUrunler()
        result = islem.getUretimUrunlerListesi()
        return jsonify(result)
    
    
class UrunlerUretimListMekmarApi(Resource):
    def get(self):
        
        islem = UretimUrunler()
        result = islem.getUretimUrunlerListesiMekmar()
        return jsonify(result)
    
class UrunlerUretimListMekmerApi(Resource):
    def get(self):
        
        islem = UretimUrunler()
        result = islem.getUretimUrunlerListesiMekmer()
        return jsonify(result)
    
    
    
class UrunlerUretimListAyrintiApi(Resource):
    def get(self,urunKartId):
        
        islem = UretimUrunler()
        result = islem.getUretimUrunlerAyrintiListesi(urunKartId)
        return jsonify(result)
   
class UrunlerUretimListAyrintiMekmarApi(Resource):
    def get(self,urunKartId):
        
        islem = UretimUrunler()
        result = islem.getUretimUrunlerAyrintiListesiMekmar(urunKartId)
        return jsonify(result)
    
class UrunlerUretimListAyrintiMekmerApi(Resource):
    def get(self,urunKartId):
        
        islem = UretimUrunler()
        result = islem.getUretimUrunlerAyrintiListesiMekmer(urunKartId)
        return jsonify(result)
   
   
   
   
    
class UrunlerUretimExcelApi(Resource):
    
    def post(self):

        data_list = request.get_json()

        islem = ExcelCiktiIslem()

        result = islem.urunler_uretim_excel(data_list)
        
        return jsonify({'status' : result}) 
  
    def get(self):
        
        excel_path = 'resource_api/raporlar/dosyalar/uretilen_listesi.xlsx'

        return send_file(excel_path,as_attachment=True)
    
    
class SevkiyatRaporHepsiAllApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeHepsiAll()

        return sevkiyat_listesi
    
    
class SevkiyatRaporAllAllApi(Resource):

    def get(self):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeAllAll()

        return sevkiyat_listesi
    


class SevkiyatRaporTarihAllApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeTarihAll(tarih)

        return sevkiyat_listesi
    
class SevkiyatRaporTekTarihAllApi(Resource):

    def get(self,tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeTekTarihAll(tarih)

        return sevkiyat_listesi    
    
class SevkiyatRaporIkiTarihAllApi(Resource):

    def get(self,ilk_tarih,son_tarih):

        islem = SevkiyatRapor()

        sevkiyat_listesi = islem.getSevkiyatListeIkiTarihAll(ilk_tarih,son_tarih)

        return sevkiyat_listesi



