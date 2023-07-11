from flask import Flask,jsonify
from flask_restful import Api,Resource
from flask_cors import CORS,cross_origin 
import jwt
from functools import wraps
import datetime
from resource_api.siparisler import * 
from resource_api.dosya_islem_resource import DosyaIslemResource,ProductImage,ProductImageList
from resource_api.template_model_views import TemplateModelViews
from resource_api.teklifler import TeklifKategoriResource,MusteriResource,UlkeResource
from resource_api.listeler import *
from resource_api.shared import *
from resource_api.raporlar import *
from resource_api import Kullanici,DataKullanici
from resource_api.islemler import *
from resource_api.yeniTeklifler import *
from resource_api.bulut_islem import TestRaporIslem,MekmarCdnApi
from resource_api.yeniTeklifler.raporlar.teklif_takip import *
from resource_api.yeniTeklifler.raporlar import *
from resource_api.seleksiyon.uretimRestApi import *
from resource_api.sevkiyat import *
from resource_api.mekmar_com import *
from resource_api.operasyon import *
from resource_api.kontroller import *
from resource_api.finans import *
from resource_api.efesfinans import *
from resource_api.tedarikci import *
from resource_api.musteriler import *
from resource_api.maliyet_raporlar import *
from resource_api.shared import *
from resource_api.customers import *
from resource_api.numuneler import *
from resource_api.numunefinans import *
from resource_api.users import *
from resource_api.finans.odemeler_api import OdemelerListesiApi,OdemelerListesiAyrintiApi
from resource_api.raporlar.temsilciSatislari.temsilciSatislari import TemsilciSatislariApi
from resource_api.efesfinans.efinansRestApi import EfesGelenSiparisvYuklenenler
from resource_api.teklifler.bgpProject import *
from resource_api.mekmar_com.Galleria import *
from resource_api.notification import NotificationIslemApi,NotificationListApi,NotificationIslemAnsweredApi,NotificationIslemFollowApi,NotificationIslemFollowAnsweredApi
from resource_api.finansTest.finanstestapi import FinanceTestListApi,FinanceTestDetailListApi,FinanceTestListExcelApi
from resource_api.controls import ProformaKayitKontrolApi

app = Flask(__name__)

api = Api(app)

#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
#cors = CORS(app, resources={r"/foo": {"origins": "https://efes.mekmar.com"}})
#CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}})
#CORS(app, support_credentials=True)
#cors = CORS(app, resources={r"//*": {"origins": "*"}})




class MainDefaultResourece(Resource):

    def get(self):
       
        
        
        return jsonify("Hello Flask Fraework Service")



api.add_resource(UserPassGuncelleApi,'/user/userGuncelle',methods=['POST','GET'])


api.add_resource(FooterCanvasPDF,'/islemler/dosyalar/pdfciktim',methods=['POST','GET'])


api.add_resource(DovizListe,'/listeler/DovizListe/<string:yil>/<string:ay>/<string:gun>',methods=['GET'])

api.add_resource(MainDefaultResourece,'/')
api.add_resource(SiparisListResource,'/siparisler/<int:siparisDurum>/<string:yil>')



api.add_resource(SiparisHepsiListResource,'/siparislerhepsi/<int:siparisDurum>')
api.add_resource(UretimExcelCiktiApi,'/siparisler/dosyalar/uretimExcelCikti',methods=['POST','GET'])
api.add_resource(UretimExcelCiktiENApi,'/siparisler/dosyalar/uretimExcelCiktiEn',methods=['POST','GET'])
api.add_resource(IcSiparisExcelCiktiApi,'/siparisler/dosyalar/IcSiparisExcelCikti',methods=['POST','GET'])
api.add_resource(SiparisUrun,'/siparisler/siparisUrun/<string:siparisNo>')
api.add_resource(TeklifKategoriResource,'/teklifler/kategori')
api.add_resource(MusteriResource,'/teklifler/musteri')
api.add_resource(UlkeResource,'/teklifler/ulkeler')

################################################BGP Projects################################################
api.add_resource(BgpProjectApi,'/bgpProject/SaveBgpProject',methods=['POST'])
api.add_resource(BgpProjectChangeApi,'/bgpProject/SaveBgpProjectChange/<string:projectName>/<int:temsilci>/<string:bgpUlkeAdi>/<string:ulkeLogo>/<int:projectId>',methods=['GET'])
api.add_resource(BgpProjectApiList,'/bgpProject/getBgpProjectList/<int:temsilci>',methods=['GET'])
api.add_resource(BgpProjectAyrintiApi,'/bgpProject/getBgpProjectDetail/<string:projectName>',methods=['GET'])

api.add_resource(BgpProjectAyrintiSave,'/bgpProject/setBgpProjectDetailIslem',methods=['POST','PUT'])

api.add_resource(BgpProjectAyrintiForm,'/bgpProject/getBgpProjectDetailForm/<int:id>',methods=['GET'])
api.add_resource(BgpProjectAyrintiFormDelete,'/bgpProject/setBgpProjectDetailDelete/<int:id>',methods=['DELETE'])
api.add_resource(BgpProjectDelete,'/bgpProject/setBgpProjecDelete/<string:projectName>',methods=['DELETE'])
api.add_resource(BgpProjectHatirlatmaListApi,'/listeler/bgpProjects/bgpProjectsHatirlatmaList/<int:userId>',methods=['GET'])
api.add_resource(BgpProjectCompanyListApi,'/bgpProject/getBgpProjectCompanyList',methods=['GET'])
api.add_resource(BgpProjectCompanyStatusApi,'/bgpProject/getBgpProjectStatistics/<int:username>',methods=['GET'])
api.add_resource(BgpProjectCompanyStatusDetailApi,'/bgpProject/getBgpProjectStatisticsDetail/<string:ulkeAdi>',methods=['GET'])
api.add_resource(BgpProjectCompanyDetailListApi,'/bgpProject/getBgpProjectCompanyDetailList',methods=['GET'])
api.add_resource(BgpServiceSelectedCompanyApi,'/bgpProject/getBgpServiceSelectedCompany/<string:firmaAdi>',methods=['GET'])
api.add_resource(BgpProjectCountryListApi,'/bgpProject/getBgpProjectCountryList',methods=['GET'])
api.add_resource(BgpProjectByCountryandReseptationApi,'/bgpProject/getBgpProjectCountryandReseptation',methods=['GET'])
api.add_resource(BgpProjectFileSave,'/bgpProject/setBgpProjectFile',methods=['POST'])
api.add_resource(BgpDetailModelApi,'/bgpProject/detail/model',methods=['GET'])

api.add_resource(SiparisBolmeGuncellemeApi,'/siparis/siparisBolmeGuncelleme',methods=['POST','GET'])

api.add_resource(DosyaIslemResource,'/export/<string:path>')

api.add_resource(ProductImage,'/image/<imageName>',methods=['GET','POST'])
api.add_resource(ProductImageList,'/image')
api.add_resource(TemplateModelViews,'/model/<string:modelName>') 

#listeler
api.add_resource(UrunKartMenuList,'/listeler/urunKartMenuList')
api.add_resource(UrunBirimList,'/listeler/urunBirimList')
api.add_resource(TedarikciSiparisList,'/listeler/tedarikciSiparisList')
api.add_resource(TeslimTurList,'/listeler/teslimTurList')
api.add_resource(OdemeTurList,'/listeler/odemeTurList')
api.add_resource(FaturaKesimTurList,'/listeler/FaturaKesimTurList')
api.add_resource(UlkeList,'/listeler/ulkeList')
api.add_resource(MusteriList,'/listeler/musteriList')
api.add_resource(OcakListApi,'/listeler/ocakList')

api.add_resource(UlkeyeGoreMusteriListApi,'/listeler/ulkeyeGoreMusteriList/<int:year>',methods=['GET','POST'])
api.add_resource(UlkeyeGoreMusteriListAyrintiApi,'/listeler/ulkeyeGoreMusteriListAyrinti/<int:year>/<int:ulkeId>',methods=['GET'])
#api.add_resource(MusteriSiparisListesi,'/listeler/musteriSiparisList')
api.add_resource(KullaniciList,'/listeler/kullaniciList')
api.add_resource(OperasyonKullaniciList,'/listeler/OperasyonKullaniciList')

#raporlar
api.add_resource(IscilikList,'/raporlar/iscilikList/<string:siparisNo>/<int:urunKartId>')
api.add_resource(SiparisGiderTurList,'/raporlar/siparisGiderTurList')
#api.add_resource(SiparisOzet,'/raporlar/siparisOzet',methods=['GET','POST']) 
api.add_resource(KullaniciBazliAnasayfaApi,'/raporlar/anasayfamusterim/<string:username>')
api.add_resource(AnasayfaAyrintiSevk,'/raporlar/sevkayrinti/<string:firmaadi>',methods=['GET'])
api.add_resource(AnasayfaAyrintiTeklifler,'/raporlar/teklifayrinti/<string:kullaniciAdi>',methods=['GET'])
api.add_resource(AnasayfaAyrintiSiparisler,'/raporlar/siparisayrintiyil')
api.add_resource(AnasayfaTakipListesi,'/raporlar/takiplist')
api.add_resource(SiteYeniUrunListApi,'/raporlar/siteYeniUrunList',methods=['GET'])
api.add_resource(YeniEklenenSiparislerListApi,'/raporlar/yeniEklenenSiparisler',methods=['GET'])
api.add_resource(SiparisOzetRaporlarApi,'/raporlar/siparis/siparisOzetRaporlar/<int:userId>',methods=['GET'])
api.add_resource(SiparisBazindaOzetRaporlarApi,'/raporlar/siparis/siparisBazindeOzetRapor',methods=['GET'])
api.add_resource(SiparisOzetKullaniciApi,'/raporlar/siparisozet/siparisOzetRaporlar/<string:kullaniciAdi>')
api.add_resource(KullaniciSevSipAyrintiApi,'/raporlar/siparisozet/kullaniciOzet/<string:username>/<int:ay>',methods=['GET'])
api.add_resource(KullaniciBazliMusteriApi,'/raporlar/musteri/<string:username>')
api.add_resource(GenelMusteriApi,'/raporlar/musteri')
api.add_resource(KullaniciBazliAyrintiMusteriApi,'/raporlar/musteri/musteriDetay/<int:musteri_id>')
api.add_resource(MusteriExcellCikti,'/raporlar/musteri/musteriexcellCikti',methods=['GET','POST'])
api.add_resource(MusteriSiparisExcellCikti,'/raporlar/musteri/musterisipexcellcikti',methods=['GET','POST'])
api.add_resource(UlkeBazindaExcellCikti,'/raporlar/musteri/ulkebzindaSevkiyat',methods=['GET','POST'])
api.add_resource(SiparisGirisModel,'/siparis/siparisGirisModel/<string:siparisNo>')
api.add_resource(SiparisGirisBosModel,'/siparis/siparisGirisModel')
api.add_resource(CustomerDetailList,'/customers/products/detailList/<string:sipNo>',methods=['GET'])

api.add_resource(TemsilciSatislariApi,'/raporlar/temsilciSatislariAll/<string:username>',methods=['GET'])
api.add_resource(TemsilciSatislariApiDetayTamami,'/raporlar/temsilciSatislariAllDetay/<string:ay>/<string:username>',methods=['GET'])
api.add_resource(TemsilciSatislariApiDetaySatislar,'/raporlar/temsilciSatislariAllDetaySatislar/<string:ay>/<string:username>',methods=['GET'])
api.add_resource(TemsilciSatislariApiDetayYuklemeler,'/raporlar/temsilciSatislariAllDetayYuklemeler/<string:ay>/<string:username>',methods=['GET'])

api.add_resource(DashboardNewApi,'/raporlar/dashboard/dasboardNew',methods=['GET'])
api.add_resource(DashboardNewSatisciApi,'/raporlar/dashboard/dasboardNewSatisci/<string:username>',methods=['GET'])
api.add_resource(DashboardNewGrafikApi,'/raporlar/dashboard/dasboardNewSatisciGrafik',methods=['GET'])
api.add_resource(DashboardNewGrafikDataApi,'/raporlar/dashboard/dashboardNewGrafikData',methods=['GET'])
api.add_resource(DashboardNewSubApi,'/raporlar/dashboard/dashboardSubData',methods=['GET'])
api.add_resource(DashboardNewSubTedarikciAyrintiApi,'/raporlar/dashboard/tedarikciAyrinti/<int:tedarikciId>',methods=['GET'])
api.add_resource(DashboardFirmaBazindaAyrintiApi,'/raporlar/dashboard/firmaBazindaSipAyrinti/<int:firmaId>',methods=['GET'])
api.add_resource(DashboardTekliflerAyrintiApi,'/raporlar/dashboard/tekliflerAyrinti/<int:satisciId>',methods=['GET'])
api.add_resource(DashboardLogsAyrintiTarihApi,'/raporlar/logs/logsAyrinti',methods=['POST'])
api.add_resource(DashboardUlkeyeGoreTekliflerApi,'/raporlar/dashboard/ulkeTeklifler/<string:year>',methods=['GET'])
api.add_resource(DashboardUlkeyeGoreTekliflerAyrintiApi,'/raporlar/dashboard/ulkeTekliflerAyrinti/<string:year>/<int:ulkeId>',methods=['GET'])
#sipariş data kayıt işlemleri
api.add_resource(SiparisKayitIslem,'/siparis/kayitIslem',methods=['GET','POST','PUT'])
api.add_resource(IscilikDataIslem,'/siparis/iscilikIslem',methods=['GET','POST','PUT'])
api.add_resource(IscilikKayitSil,'/siparis/iscilikIslem/kayitSil/<int:id>',methods=['DELETE'])
api.add_resource(SiparisOpChangeApi,'/siparis/opChangeMailSend',methods=['POST'])
api.add_resource(SiparisOdemeSekliChangeApi,'/operasyon/fatura/changeOdemeBilgisi/<string:siparisNo>/<int:odemeTur>',methods=['GET'])
api.add_resource(SiparisOdemeSekliChangeExApi,'/operasyon/fatura/changeOdemeBilgisiEx/<string:siparisNo>/<int:odemeTur>',methods=['GET'])
api.add_resource(SiparisKayitIslemControlApi,'/siparis/kayitIslemControl/<string:siparis_no>',methods=['GET'])
api.add_resource(SiparisDegisimMailGonderApi,'/siparis/masraflar/change/sendmail',methods=['POST'])
api.add_resource(StokListFilterApi,'/uretim/stokList/filter',methods=['GET'])
api.add_resource(StokListFilterAyrintiApi,'/uretim/stokList/filter/ayrinti/<int:urunKartId>',methods=['GET'])
#numuneler
api.add_resource(NumuneListApi,'/numuneler/numunelist/<int:yil>',methods=['GET']) #Analiste
api.add_resource(NumuneAyrintiListApi,'/numuneler/numunelist/ayrinti/<string:po>') #Ayrinti Alani
api.add_resource(NumuneRaporYilListApi,'/islemler/numune/numuneYilListesi',methods=['GET'])

api.add_resource(NumuneFormListeler,'/listeler/numune/numuneFormListeler')
api.add_resource(NumuneKayitIslem,'/islemler/numune/numuneModel',methods=['POST','PUT'])
api.add_resource(NumuneFormModel,'/islemler/numune/numuneModel/<string:numunepo>')
 
api.add_resource(NumuneFinansAnaListeApi,'/numunefinans/listeler/NumuneFinansAnaListe/<int:yil>',methods=['GET'])
api.add_resource(NumuneAyrintRestList,'/numunefinans/listeler/numuneAyrintiListesi/<int:musteriid>/<int:yil>',methods=['GET'])

api.add_resource(NumuneBankayaGelenAyrinti,"/islemler/numune/bankayagelen/<string:banka>/<int:yil>",methods=['GET'])


api.add_resource(NumuneTahsilatIslemList,'/numune/finans/liste/musteriTahsilatListe/<int:musteriid>/<string:siparisno>',methods=['GET'])
api.add_resource(NumuneTahsilatKayitIslem,'/numune/finans/islemler/tahsilatKayitDegistirme',methods=['GET','POST','PUT'])
api.add_resource(NumuneTahsilatKayitSilme,'/numune/finans/islemler/tahsilatKayitSilme/<int:id>',methods=['GET','DELETE'])
api.add_resource(NumuneDosyaKaydet,'/islemler/numune/numuneDosyaKaydet',methods=['GET','POST','PUT']) #görsellerin ön yüzü için 
api.add_resource(NumuneDosyaKaydet2,'/islemler/numune/numuneDosyaKaydet/arka',methods=['GET','POST','PUT']) # görsellerin arka yüzü için

#ürünkart kayıt İşlemler
api.add_resource(UrunKartIslem,'/islemler/urunKart/kayit',methods=['GET','POST','PUT'])
api.add_resource(UrunKartModel,'/islemler/urunKart/getUrunKart/<int:urunKartId>')
api.add_resource(UrunKartSilModel,'/islemler/urunKart/getUrunKartSil/<int:urunKartId>/<string:username>',methods=['GET','DELETE'])

api.add_resource(UrunKartBosModel,'/islemler/urunKart/getUrunKartModel')
api.add_resource(UrunKartDetayList,'/islemler/urunKart/getUrunKartDetayList/<int:urunKartId>')
api.add_resource(UrunKartDetayListYeni,'/islemler/urunKart/getUrunKartDetayListYeni')
api.add_resource(KasaUrunKartGuncellemeApi,'/islemler/urunKart/setKasaYeniUrunKart/<int:kasaNo>/<int:urunKartId>/<string:username>',methods=['GET','PUT'])




#teklifler
api.add_resource(TeklifAnaSayfaData,'/listeler/teklif/anaSayfaData/<int:userId>')
api.add_resource(TeklifFormListeler,'/listeler/teklif/teklifFormListeler')
api.add_resource(TeklifKayitIslem,'/islemler/teklif/teklifModel')
api.add_resource(TeklifSilmeIslem,'/islemler/teklif/teklifSil/<int:teklifid>')
api.add_resource(TeklifFormModel,'/islemler/teklif/teklifModel/<int:teklifId>')
api.add_resource(TeklifAyrintiListe,'/listeler/teklif/kullaniciAyrintiListe/<int:kullaniciId>')
api.add_resource(TeklifAyrintiListeHepsi,'/listeler/teklif/kullaniciAyrintiListe')
api.add_resource(TeklifProformaKaydet,'/islemler/teklif/proformaKaydet',methods=['GET','POST','PUT'])
api.add_resource(TeklifDosyaKaydet,'/islemler/teklif/teklifDosyaKaydet',methods=['GET','POST','PUT'])
api.add_resource(TeklifSonGorulmeKaydet,'/islemler/teklif/teklifSonGorulmeKaydet',methods=['GET','POST','PUT'])
api.add_resource(HatirlatmaDurumGuncellemesi,'/islemler/teklif/hatirlatilmaDurum',methods=['GET','POST','PUT'])
api.add_resource(TeklifMusterilerResourceApi,'/islemler/teklif/teklifMusteriler',methods=['GET'])



api.add_resource(TeklifNumuneKaydet,'/islemler/teklif/teklifNumuneKaydet',methods=['GET','POST','PUT'])
api.add_resource(TeklifDosyaSil,'/islemler/teklif/teklifDosyaSil/<int:id>',methods=['GET','DELETE'])
api.add_resource(TeklifListeGrafikApi,'/raporlar/teklif/teklifListe/grafikHepsi',methods=['GET'])
api.add_resource(TeklifOncelikGrafikRaporList,'/raporlar/teklif/teklifOncelikGrafikList',methods=['GET'])

api.add_resource(MusteriListApi,'/listeler/teklif/musteriList')
api.add_resource(MusteriDetaApi,'/listeler/teklif/musteriDetay/<int:musteriid>')
api.add_resource(MusteriTeklifIslemApi,'/islemler/teklif/musteriTeklifGuncelle',methods=['POST','GET'])
api.add_resource(TumTeklifListApi,'/listeler/teklif/tumTeklifList',methods=['GET'])
api.add_resource(EskiTekliflerListApi,'/listeler/teklif/eskiTeklifList',methods=['GET'])
api.add_resource(MusteriYeniModel,'/listeler/teklif/yeniMusteriModel',methods=['GET'])
api.add_resource(EnBoyEkleApi,'/listeler/teklif/addEnBoy',methods=['GET','POST'])





#satisci
api.add_resource(CustomersListeApi,'/listeler/customers/customersList/<int:users>',methods=['GET'])
api.add_resource(CustomersListeSatisciApi,'/listeler/customers/customersListSatisci/<int:users>',methods=['GET'])
api.add_resource(CustomersListeTekliflerApi,'/listeler/customers/customersListTeklifler/<int:users>',methods=['GET'])
api.add_resource(CustomersListeBGNApi,'/listeler/customers/customersListBGN/<int:users>',methods=['GET'])


api.add_resource(CustomersListeAllApi,'/listeler/customers/customersListAll',methods=['GET'])
api.add_resource(CustomersListeAllSatisciApi,'/listeler/customers/customersListAllSatisci',methods=['GET'])
api.add_resource(CustomersListeAllTekliflerApi,'/listeler/customers/customersListAllTeklifler',methods=['GET'])
api.add_resource(CustomersListeAllTekliflerBGNApi,'/listeler/customers/customersListAllBGN',methods=['GET'])

api.add_resource(CustomersDetayApi,'/listeler/customers/customersDetay/<string:musteri_adi>')
api.add_resource(CustomersKayitIslemModel,'/satisci/customers/satisciModel')
api.add_resource(CustomersKayitIslemList,'/satisci/customers/liste/musteriListe/<string:musteriadi>/<int:id>',methods=['GET'])
api.add_resource(CustomersKayitIslem,'/satisci/customers/islemler/satisciKayitDegistirme',methods=['GET','POST','PUT'])
api.add_resource(CustomersKayitSilme,'/satisci/customers/islemler/satisciKayitSilme/<int:id>',methods=['GET','DELETE'])

api.add_resource(CustomersChangePriority,'/satisci/customers/changePriority/<string:customer>/<string:priority>',methods=['GET'])

api.add_resource(CustomersChangeFollow,'/satisci/customers/Following/<string:customer>/<string:follow>',methods=['GET'])

api.add_resource(CustomersDosyaKaydet,'/islemler/customers/satisciDosyaKaydet',methods=['GET','POST','PUT'])
api.add_resource(CustomersTemsilciList,'/islemler/customers/temsilciList',methods=['GET'])
api.add_resource(CustomersHatirlatmaApi,'/listeler/customers/customersHatirlatma/<int:kullanici_id>')
api.add_resource(CustomersChangeRepresentative,'/islemler/customers/changeRepresentative/<string:customer>/<int:representative>',methods=['GET'])

#kullanıcı kontrol
api.add_resource(Kullanici,'/login',methods=['GET','POST'])
api.add_resource(DataKullanici,'/login/<string:username>/<string:password>',methods=['GET','POST'])

#spaces dosya işlemleri

api.add_resource(TestRaporIslem,'/spaces/mekmarcom/testRaporGonder',methods=['GET','POST'])
api.add_resource(MekmarCdnApi,'/spaces/mekmarcom/fotoGonder',methods=['PUT','GET'])

#seleksiyon
api.add_resource(UretimListApi,'/seleksiyon/listeler/uretimList',methods=['GET'])
api.add_resource(UretimListModelApi,'/seleksiyon/liste/uretim/<int:kasano>',methods=['GET'])
api.add_resource(UretimDetayApi,'/seleksiyon/listeler/uretimDetay/<int:kasano>',methods=['GET'])
api.add_resource(UretimDetayBosModelApi,'/seleksiyon/listeler/uretimDetayModel',methods=['GET'])
api.add_resource(UretimKayitIslemApi,'/seleksiyon/islemler/uretimKayitIslem',methods=['GET','POST','PUT'])
api.add_resource(UretimSilIslemApi,'/seleksiyon/islemler/uretimSilIslem/<int:kasano>',methods=['GET','DELETE'])
api.add_resource(UretimCokluKayitApi,'/seleksiyon/islemler/uretimCokluKaydet',methods=['GET','POST'])
api.add_resource(UretimDisFirmaKasaNoApi,'/seleksiyon/islemler/disFirmaKasaNo',methods=['GET'])
api.add_resource(UretimSeleksiyonFirmaKasaNoApi,'/seleksiyon/islemler/seleksiyonFirmaKasaNo',methods=['GET'])
api.add_resource(UretimUrunKartKasaKontrolApi,'/seleksiyon/islemler/getUrunKartSeleksiyonKasaKontrol/<int:urunKartId>',methods=['GET'])
api.add_resource(CreateSetAllApi,'/seleksiyon/setCrateAll',methods=['GET','POST'])
api.add_resource(ProductCrateControlApi,'/islemler/seleksiyon/productCrateControl',methods=['POST'])
api.add_resource(PoProductList,'/islemler/seleksiyon/seleksiyonProductList/<string:po>',methods=['GET'])
api.add_resource(UretimSeleksiyonUrunKartApi,'/seleksiyon/islemler/urunKartBilgileri',methods=['GET'])

api.add_resource(UretimSeleksiyonFazlasiMiApi,'/seleksiyon/islemler/uretimFazlasiMi/<string:po>/<int:urunkartid>',methods=['POST','GET'])



api.add_resource(UretimOzetListApi,'/seleksiyon/listeler/uretimOzetList',methods=['GET'])
api.add_resource(UretimSiparisKalemDetay,'/seleksiyon/listeler/siparisUretimDetay/<string:siparisno>',methods=['GET'])
api.add_resource(SeleksiyonRaporApi,'/siparisler/dosyalar/seleksiyonExcelCikti',methods=['POST','GET'])
api.add_resource(SeleksiyonEtiketApi,'/siparisler/dosyalar/seleksiyonEtiketCikti',methods=['POST','GET'])




api.add_resource(SeleksiyonEtiketTarihApi,'/seleksiyon/listeler/seleksiyonEtiketTarih/<string:tarih>',methods=['GET'])

api.add_resource(SeleksiyonKasaDetay,'/seleksiyon/listeler/kasaDetay',methods=['GET'])
api.add_resource(SeleksiyonKasaDetayKaydetApi,'/seleksiyon/listeler/kasaDetay/kaydet',methods=['POST'])
api.add_resource(SeleksiyonKasaDetayGuncelleApi,'/seleksiyon/listeler/kasaDetay/guncelle',methods=['POST'])
api.add_resource(SeleksiyonKasaDetaySilApi,'/seleksiyon/listeler/kasaDetay/sil/<int:id>',methods=['DELETE'])
api.add_resource(TedarikcilerListApi,'/seleksiyon/listeler/tedarikciler',methods=['GET'])

api.add_resource(SeleksiyonKasaExcell,'/siparisler/dosyalar/kasaOlculeriExcelCikti',methods=['GET','POST'])

api.add_resource(UretimSipListesi,'/seleksiyon/listeler/uretimSipListesi',methods=['GET'])




#sevkiyat

api.add_resource(SevkiyatNewModel,'/sevkiyat/islemler/sevkiyatNewModel',methods=['GET'])
api.add_resource(SiparisKalemList,'/sevkiyat/listeler/siparisKalemList/<string:siparisNo>',methods=['GET'])
api.add_resource(SevkiyatKayitIslem,'/sevkiyat/islemler/sevkiyatKayit',methods=['GET','PUT'])

#mekmar_com
api.add_resource(SiteMusteriList,'/mekmarcom/listeler/musteriListesi',methods=['GET'])
api.add_resource(SiteMusteriIslem,'/mekmarcom/islemler/musteriIslem',methods=['GET','POST','PUT'])
api.add_resource(SiteMusteriSil,'/mekmarcom/islemler/musteriSil/<int:id>',methods=['DELETE'])
api.add_resource(SiteMusteriDetay,'/mekmarcom/listeler/musteriDetay/<int:id>',methods=['GET'])
api.add_resource(SiteYeniMusteri,'/mekmarcom/listeler/yeniMusteriDetayModel',methods=['GET'])

#operasyon
api.add_resource(SevkTakipListesi,'/operasyon/listeler/sevkTakipListesi',methods=['GET'])
api.add_resource(SevkTakipDusenlerListesi,'/operasyon/listeler/sevkTakipDusenListesi',methods=['GET'])
api.add_resource(SevkTakipDetay,'/operasyon/listeler/sevkTakipDetay/<int:id>',methods=['GET'])
api.add_resource(SevkTakipIslem,'/operasyon/islemler/sevkTakipGuncelle',methods=['PUT','GET'])
#operasyonlar konteyner girişi
api.add_resource(KonteynerListe,'/operasyon/listeler/KonteynerList',methods=['GET'])
api.add_resource(KonteynerFormIslem,'/operasyon/form/KonteynerForm/islem/<int:fatura_id>/<int:tur>/<string:siparis_no>',methods=['GET'])
api.add_resource(KonteynerIslemListApi,'/operasyon/listeler/KonteynerFormListeler',methods=['GET'])
api.add_resource(KonteynerKayitIslem,'/operasyon/islemler/konteynerKayit',methods=['GET','POST','PUT'])
api.add_resource(KonteynerDosyaKaydet,'/operasyon/islemler/konteyner/konteynerDosyaKaydet',methods=['GET','POST','PUT'])
api.add_resource(KonteynerDosyaGuncelle,'/operasyon/islem/konteyner/konteynerDosyaGuncelle',methods=['POST','PUT'])

api.add_resource(KonteynerIslemModelListApi,'/operasyon/islemler/konteynermodel/<string:urunId>',methods=['GET'])

api.add_resource(EvrakFirmaListe,'/operasyon/listeler/FirmaList',methods=['GET'])
api.add_resource(EvrakFirmaIslem,'/operasyon/islemler/FirmaKayit',methods=['GET','POST','PUT'])
api.add_resource(FirmaModelIslem,'/operasyon/listeler/FirmaModel',methods=['GET'])

#operasyonlar nakliye girişi
api.add_resource(NakliyeListeApi,'/operasyon/listeler/nakliyeListesi',methods=['GET'])
api.add_resource(NakliyeIslemListApi,'/operasyon/listeler/nakliyebilgilistesi',methods=['GET']) ##nakliye bilgi girişi için bilgierlin getirilmesi
api.add_resource(NakliyeKayitIslem,'/operasyon/islemler/nakliyeKayit',methods=['GET','POST','PUT'])
api.add_resource(NakliyeFormIslem,'/operasyon/form/NakliyeForm/islem/<int:firmaId>/<string:evrakAdi>/<string:siparisNo>',methods=['GET'])
api.add_resource(NakliyeDosyaKaydet,'/operasyon/islemler/nakliye/nakliyeDosyaKaydet',methods=['GET','POST','PUT'])
api.add_resource(NakliyeIslemModelListApi,'/operasyon/islemler/nakliyemodel/<string:urunId>',methods=['GET'])
api.add_resource(NakliyeIslemModelApi,'/operasyon/islemler/nakliyemodel',methods=['GET'])
api.add_resource(NakliyeFaturaSil,'/operasyon/form/NakliyeFaturaSil/islem/<string:siparisNo>/<string:evrakAdi>')
api.add_resource(NakliyeFaturaChange,'/operasyon/form/NakliyeFaturaChange',methods=['GET', 'POST'])
#operasyonlar tedarikçi ft . girişi 
api.add_resource(TedarikciEvrakKaydet,'/operasyon/islemler/tedarikci/tedarikciKayit',methods=['GET','POST','PUT']) 
api.add_resource(TedarikciDosyaKaydet,'/operasyon/islemler/tedarikci/tedarikciDosyaKaydet',methods=['GET','POST','PUT'])
api.add_resource(TedarikciEvrakKontrolApi,'/operasyon/islemler/tedarikci/tedarikciKontrol/<string:tedarikci>/<string:siparis_no>')
#operasyonlar denizcilik ft . girişi 
api.add_resource(DenizcilikEvrakKaydet,'/operasyon/islemler/denizcilik/denizcilikKayit',methods=['GET','POST','PUT']) 
api.add_resource(DenizcilikDosyaKaydet,'/operasyon/islemler/denizcilik/denizcilikDosyaKaydet',methods=['GET','POST','PUT'])

#operasyonlar gumruk ve ilaçlama ft . girişi 
api.add_resource(GumrukEvrakKaydet,'/operasyon/islemler/gumruk/gumrukKayit',methods=['GET','POST','PUT']) 
api.add_resource(GumrukDosyaKaydet,'/operasyon/islemler/gumruk/gumrukDosyaKaydet',methods=['GET','POST','PUT'])
 
#operasyon ozel ıscılık
api.add_resource(OzelIscilikDosyaKaydet,'/operasyon/islemler/ekstra/ozelIscilikDosyaKaydet',methods=['GET','POST','PUT'])

#evrakyukleme
api.add_resource(EvrakSiparisListeApi,'/evrak/listeler/siparisListe',methods=['GET'])
api.add_resource(EvrakFaturaListeApi,'/evrak/faturaList/<string:siparisNo>',methods=['GET'])
api.add_resource(EvrakTedarikciListeApi,'/evrak/tedarikci/faturaList/<string:siparisNo>',methods=['GET'])
api.add_resource(EvrakFaturaKayitIslem,'/islemler/evrak/evrakFaturaModel',methods=['GET','POST','PUT'])

api.add_resource(EtiketKayitIslemApi,'/islemler/evrak/etiket',methods=['GET','POST','PUT'])
api.add_resource(EtiketListApi,'/islemler/evrak/etiketList/<string:etiketNo>',methods=['GET'])

api.add_resource(EvrakSilmeIslemApi,'/operasyon/fatura/deleteFaturaEvrak/<int:id>/<string:siparisNo>',methods=['GET'])

#operasyon data işlemleri
#api.add_resource(KonteynerFaturatIslem,'/konteynerfatura/kayitIslem',methods=['GET','POST','PUT'])
#api.add_resource(FaturaDetayListeYeni,'/islemler/fatura/getFaturaDetayListeYeni')

api.add_resource(ProformaKayitKontrolApi,'/controls/proforma/<string:siparisNo>',methods=['GET'])

#kontrol işlemleri
api.add_resource(MusteriEtaMailIslem,'/kontroller/musterietatakipislem',methods=['GET'])
api.add_resource(FinansVadeMailIslem,'/kontroller/finansVadeTakipIslem',methods=['GET'])
api.add_resource(UretimTakipIslem,'/kontroller/UretimTakipIslem/',methods=['GET'])
api.add_resource(TedarikciTakipIslem,'/kontroller/TedarikciTakipIslem/',methods=['GET'])
api.add_resource(ChatMailGonderim,'/kontroller/chatIslem',methods=['GET','POST','PUT'])
api.add_resource(ChatMailler,'/kontroller/listeler/chatmailler/<string:po>',methods=['GET'])
#finans işlemler yeni
api.add_resource(KonteynerAnaListeYeni,'/finans/listeler/konteynerAnaListe/yeni/<int:yil>',methods=['GET'])

api.add_resource(FinanceTestListApi,'/finance/reports/test',methods=['GET'])
api.add_resource(FinanceTestDetailListApi,'/finance/reports/test/detail/<int:customer_id>',methods=['GET'])
api.add_resource(FinanceTestListExcelApi,'/finance/reports/test/excel',methods=['GET','POST'])

#finans işlemler 
api.add_resource(KonteynerAnaListe,'/finans/listeler/konteynerAnaListe/<int:yil>',methods=['GET'])
api.add_resource(MusteriAyrintiListApi,'/finans/listeler/konteynerAyrintiList/<int:musteriid>',methods=['GET'])
api.add_resource(MusteriOdemeSecimList,'/finans/listeler/odemeSecimList/<int:musteri_id>/<string:tarih>',methods=['GET'])
api.add_resource(TahsilatIslemList,'/finans/listeler/musteriTahsilatListe/<int:musteriid>/<string:siparisno>',methods=['GET'])
api.add_resource(TahsilatKayitIslem,'/finans/islemler/tahsilatKayitDegistirme',methods=['GET','POST','PUT'])
api.add_resource(TahsilatKayitSilme,'/finans/islemler/tahsilatKayitSilme/<int:id>',methods=['GET','DELETE'])
api.add_resource(DepoAyrintList,'/finans/listeler/depoAyrintiListesi/<int:musteriid>',methods=['GET'])
api.add_resource(DepoAyrintiListExcell,'/finans/listeler/depoAyrintiExcellListe',methods=['POST','GET'])
api.add_resource(KonteynerExcelCiktiApi,'/finans/dosyalar/konteynerExcelCikti',methods=['POST','GET'])
api.add_resource(KonteynerOdemelerListesiExcelApi,'/finans/listeler/odemelerAyrintiListesiExcel',methods=['POST','GET'])
api.add_resource(DepoExcelCiktiApi,'/finans/dosyalar/depoExcelCikti',methods=['GET','POST'])
api.add_resource(KonteynerAyrintiCiktiApi,'/finans/dosyalar/konteynerAyrintiExcelListe',methods=['GET','POST'])
api.add_resource(KonteynerOdemeCiktiApi,'/finans/dosyalar/konteynerOdemeExcelListe',methods=['GET','POST'])
api.add_resource(MusteriOdemeListesiApi,'/finans/listeler/musteriOdemeListesi/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(MusteriOdemeYilListesiApi,'/finans/listeler/musteriOdemeYilListesi',methods=['GET'])
api.add_resource(MusteriOdemeAyListesi,'/finans/listeler/musteriOdemeAyListesi/<int:yil>',methods=['GET'])
api.add_resource(MusteriOdemeCiktiApi,'/finans/dosyalar/musteriOdemeExcelListesi',methods=['POST','GET'])
api.add_resource(PesinatIslemListeApi,'/finans/listeler/pesinatIslemListesi',methods=['GET','POST'])
api.add_resource(VadeOdemeListesiApi,'/finans/listeler/vadeYeniAnaListe',methods=['GET'])
api.add_resource(OdemelerListesiApi,'/finans/listeler/odemelerAnaListe',methods=['GET'])
api.add_resource(OdemelerListesiAyrintiApi,'/finans/listeler/odemelerAyrintiListesi/<int:musteriId>',methods=['GET'])
api.add_resource(MayaNumSipGelenApi,'/finans/listeler/mayaNumuneSiparisOdemeleri/<int:month>/<int:year>',methods=['GET'])
api.add_resource(MayaNumSipGelenYearApi,'/finans/listeler/mayaNumuneSiparisOdemeleri/<int:year>',methods=['GET'])
api.add_resource(MayaGelenBedellerCiktiApi,'/finans/listeler/mayaNumuneSiparisOdemeleriCikti',methods=['GET','POST'])

api.add_resource(OdemelerDegisimApi,"/finans/listeler/odemelerDegisim",methods=['POST'])

api.add_resource(FinansTakipListesi,'/anasayfa/finans/takipListesi/<string:kullaniciAdi>',methods=['GET'])
#yeniFinans
api.add_resource(YeniFinansAnaListe,'/finans/yeni/listeler/konteynerYeniAnaListe',methods=['GET'])
#efesfinans işlemler
api.add_resource(EfesKonteynerAnaListe,'/efesfinans/listeler/EfesKonteynerAnaListe/<int:yil>',methods=['GET'])
api.add_resource(EfesKonteynerGelenOdemelerYil,'/efesfinans/listeler/EfesKonteynerGelenOdemelerYil',methods=['GET'])
api.add_resource(EfesMusteriAyrintiListApi,'/efesfinans/listeler/EfeskonteynerAyrintiList/<int:musteriid>',methods=['GET'])
api.add_resource(EfesMusteriOdemeSecimList,'/efesfinans/listeler/EfesodemeSecimList/<int:musteri_id>/<string:tarih>',methods=['GET'])
api.add_resource(EfesTahsilatIslemList,'/efesfinans/listeler/EfesmusteriTahsilatListe/<int:musteriid>/<string:siparisno>',methods=['GET'])
api.add_resource(EfesMusteriOdemeListesiApi,'/efesfinans/listeler/efesmusteriOdemeListesi/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(EfesMusteriOdemeYilListesiApi,'/efesfinans/listeler/EfesmusteriOdemeYilListesi',methods=['GET'])
api.add_resource(EfesMusteriOdemeAyListesi,'/efesfinans/listeler/EfesmusteriOdemeAyListesi/<int:yil>',methods=['GET'])
api.add_resource(EfesPesinatIslemListeApi,'/efesfinans/listeler/EfespesinatIslemListesi',methods=['GET','POST'])
api.add_resource(EfesKonteynerExcelCiktiApi,'/efesfinans/dosyalar/EfeskonteynerExcelCikti',methods=['POST','GET'])
api.add_resource(EfesTahsilatExcelCiktiApi,'/efesfinans/dosyalar/EfestahsilatExcelCikti',methods=['POST','GET'])
api.add_resource(EfesGelenSiparisvYuklenenler,'/efesfinans/raporlar/efesYuklenenvGelen',methods=['GET'])
api.add_resource(EfesGelenSiparisBilgileriApi,'/efesfinans/raporlar/efesGelenSipBilgileri',methods=['GET'])
api.add_resource(EfesGelenSiparisBilgileriAllApi,'/efesfinans/raporlar/efesGelenSipBilgileriAll',methods=['GET'])

api.add_resource(EfesGelenSiparisBilgileriAyrintiApi,'/efesfinans/raporlar/efesGelenSipBilgileriAyrinti/<string:siparisNo>',methods=['GET'])


#tedarikçiler
api.add_resource(TedarikciListApi,'/tedarikci/listeler/tedarikciListesi',methods=['GET'])
api.add_resource(TedarikciModelApi,'/tedarikci/listeler/tedarikciModel',methods=['GET'])

api.add_resource(TedarikciIslemApi,'/tedarikci/kayitIslem/tedarikciKaydet',methods=['POST','PUT','GET'])
api.add_resource(TedarikciSilmeIslemApi,'/tedarikci/kayitIslem/tedarikciSil/<int:id>',methods=['DELETE','GET'])
api.add_resource(WoTedarikcilerApi,'/tedarikci/icsiparisformu/listeler',methods=['GET'])
api.add_resource(TedarikciAyrintiListApi,'/tedarikci/listeler/tedarikciurun/<string:siparisno>',methods=['GET'])
api.add_resource(IcSiparisKaydet,'/islemler/tedarikci/icsiparisKaydet',methods=['GET','POST','PUT'])

api.add_resource(IcSiparisDosyaKaydet,'/islemler/tedarikci/icsiparis/IcSiparisDosyaKaydet',methods=['GET','POST','PUT'])

api.add_resource(IcSiparisDosyaSilme,'/listeler/tedarikciDeleteForm/<int:tedarikciId>/<string:siparisNo>',methods=['GET'])
api.add_resource(IcSiparisFormSilKontrol,'/listeler/tedarikciDeleteFormKontrol/<int:tedarikciId>/<string:siparisNo>',methods=['GET'])
api.add_resource(IsfControlApi,'/islemler/tedarikci/isfControl/<string:evrakAdi>',methods=['GET'])




#musteriler
api.add_resource(MusteriListeApi,'/musteriler/listeler/musteriListesi',methods=['GET'])
api.add_resource(MusteriSiparisListesiApi,'/musteriler/listeler/musteriSiparisListesi',methods=['GET'])
api.add_resource(MusteriSiparisAyrintiCardApi,'/musteriler/listeler/musteriSiparisAyrintiCard',methods=['GET'])
api.add_resource(MusteriYeniModelApi,'/musteriler/listeler/yeniMusteriModel',methods=['GET'])
api.add_resource(MusteriDetayApi,'/musteriler/listeler/musteriDetay/<int:id>',methods=['GET'])
api.add_resource(MusteriSiparisAyrintApi,'/musteriler/listeler/musteri/siparisDetay/<int:yil>/<int:id>',methods=['GET'])
api.add_resource(MusteriKayitIslemApi,'/musteriler/islemler/musteriKayitIslem',methods=['GET','POST','PUT'])
api.add_resource(MusteriKayitSilmeApi,'/musteriler/islemler/musteriKayitSilme/<int:id>',methods=['DELETE','GET'])
api.add_resource(MusteriListesiYazdirmaApi,'/musteriler/dosya_islemleri/excelMusterilerDetayListesi',methods=['GET','POST'])
api.add_resource(CustomerChangeFollowApi,'/customers/follow/<string:customer>/<string:follow>',methods=['GET'])

api.add_resource(CustomersSurfaceSaveApi,'/listeler/musteriler/musteriSurface',methods=['POST','PUT'])
api.add_resource(CustomersSurfaceListApi,'/listeler/musteriler/musteriSurfaceList/<int:user_id>',methods=['GET'])
api.add_resource(CustomersSurfaceDeleteApi,'/listeler/musteriler/musteriSurface/delete/<int:id>/<int:user_id>',methods=['DELETE'])
api.add_resource(CustomersTeklifMusteriListesiApi,'/listeler/musteriler/teklifMusteriListesi',methods=['GET'])
api.add_resource(CustomersModelApi,'/listeler/musteriler/seleksiyon/model/<int:user_id>',methods=['GET'])
api.add_resource(CustomersDetailApi,'/listeler/musteriler/seleksiyon/detail/<int:user_id>/<int:id>',methods=['GET'])


#Teklif Müşterileri
api.add_resource(TeklifMusterilerApi,"/listeler/teklifMusteriler",methods=['GET'])
api.add_resource(TeklifMusteriModelApi,"/listeler/teklif/musteriler/model",methods=['GET'])
api.add_resource(TeklifMusterilerAyrintiApi,"/listeler/teklifMusterilerAyrinti/<int:id>",methods=['GET'])
api.add_resource(TeklifMusterilerYeniKayitApi,"/listeler/setNewTeklifMusteriler",methods=['POST','PUT'])
api.add_resource(TeklifMusterilerSilApi,"/listeler/setNewTeklifMusterilerSil/<int:id>",methods=['DELETE'])
api.add_resource(TeklifMusKopyalamaApi,"/listeler/teklifmusteriler/customersCopyto",methods=['POST'])


#Fuar Müşterileri
api.add_resource(FuarMusterilerListApi,"/listeler/getFuarMusterilerList",methods=['GET'])
api.add_resource(FuarMusterilerYeniKayitApi,"/listeler/setNewFuarMusteriler",methods=['POST','PUT'])
api.add_resource(FuarMusterilerListAyrintiApi,"/listeler/getFuarMusterilerAyrintiList/<int:id>",methods=['GET'])
api.add_resource(FuarMusterilerSilApi,"/listeler/setNewFuarMusterilerSil/<int:id>",methods=['DELETE'])
api.add_resource(FuarMusterilerModelApi,"/listeler/fuar/model",methods=['GET'])
#Bgp Müşterileri
api.add_resource(BgpMusterilerListApi,"/listeler/getBgpMusterilerList",methods=['GET'])
api.add_resource(BgpMusterilerYeniKayitApi,"/listeler/setNewBgpMusteriler",methods=['POST','PUT'])
api.add_resource(BgpMusterilerListAyrintiApi,"/listeler/getBgpMusterilerAyrintiList/<int:id>",methods=['GET'])
api.add_resource(BgpMusterilerSilApi,"/listeler/setNewBgpMusterilerSil/<int:id>",methods=['DELETE'])
api.add_resource(BgpMusterilerModelApi,"/listeler/bgp/model",methods=['GET'])



#raporlar
api.add_resource(YuklemeRaporIslemApi,'/raporlar/listeler/yukleme/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(YuklemeRaporIslemYearApi,'/raporlar/listeler/yuklemeYear/<int:year>',methods=['GET'])


api.add_resource(YuklemeAtlantaRaporIslemApi,'/raporlar/listeler/atlantayukleme/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(YuklemeRaporYilListApi,'/raporlar/listeler/yuklemeYilListesi',methods=['GET'])
api.add_resource(YuklemeRaporIslemAyListesi,'/raporlar/listeler/yuklemeAyListesi/<int:yil>',methods=['GET'])
api.add_resource(YuklemePoExcelApi,'/raporlar/listeler/yuklemepoExcelCikti',methods=['POST','GET'])
api.add_resource(YuklemeMusteriExcelApi,'/raporlar/listeler/yuklememusExcelCikti',methods=['POST','GET'])
api.add_resource(YuklemeYilExcelApi,'/raporlar/listeler/yuklemeYilExcelCikti',methods=['POST','GET'])
api.add_resource(SiparisOzetExcelApi,'/raporlar/listeler/siparisOzetExcelCikti',methods=['POST','GET'])
api.add_resource(SeleksiyonOcakListesiRaporApi,'/raporlar/listeler/ocakListesiRapor',methods=['GET'])
api.add_resource(SeleksiyonOcakListesiDetayApi,'/raporlar/listeler/ocakListesiDetayListe/<string:ocakadi>',methods=['GET'])
api.add_resource(AllOrdersRaporApi,'/islemler/listeler/allOrders',methods=['GET'])
api.add_resource(OrderRaporApi,'/islemler/listeler/order/<string:po>',methods=['GET','POST'])

api.add_resource(OcakRaporExcellApi,'/raporlar/listeler/ocakListesiRaporExcell',methods=['GET','POST'])
api.add_resource(SipKalanExcellApi,'/raporlar/listeler/sipKalanListesiExcell',methods=['GET','POST'])

api.add_resource(MusteriBazindaRaporExcellApi,'/raporlar/listeler/musteriBazindaRaporExcell',methods=['GET','POST'])
api.add_resource(MusteriBazindaRaporToplamExcellApi,'/raporlar/listeler/musteriBazindaToplamExcell',methods=['GET','POST'])

api.add_resource(StokRaporRaporApi,'/raporlar/listeler/stokRaporuHepsi',methods=['GET'])
api.add_resource(StokRaporOlculeriApi,'/raporlar/listeler/stokRaporuOlculeri',methods=['GET'])
api.add_resource(StokRaporAnaListeApi,'/raporlar/listeler/stokRaporuAnaListe',methods=['GET'])
api.add_resource(StokRaporOnylMekmerApi,'/raporlar/listeler/stokRaporuOnlyMekmer',methods=['GET'])
api.add_resource(StokRaporAnaListeFilterApi,'/raporlar/listeler/stokRaporuAnaListeFilter/<int:tedarikci>',methods=['GET'])

api.add_resource(StokRaporMekmerMekmozApi,'/raporlar/listeler/stokRaporuMekmerMekmoz',methods=['GET'])
api.add_resource(StokRaporDisApi,'/raporlar/listeler/stokRaporuDis',methods=['GET'])
api.add_resource(StokRaporDisMekmardaOlanlarApi,'/raporlar/listeler/stokRaporuDisMekmardaOlanlar',methods=['GET'])

api.add_resource(StokRaporMekmerMekmozAyrintiApi,'/raporlar/listeler/stokRaporuMekmerMekmozAyrinti/<int:urunId>',methods=['GET'])
api.add_resource(StokRaporDisAyrintiApi,'/raporlar/listeler/stokRaporuDisAyrinti/<int:urunId>',methods=['GET'])
api.add_resource(StokRaporDisMekmardaOlanAyrintiApi,'/raporlar/listeler/stokRaporuDisMekmardaOlanAyrinti/<int:urunId>',methods=['GET'])

api.add_resource(StokRaporuFiyatliExcelCiktiApi,'/raporlar/listeler/stokRaporuFiyatli',methods=['GET','POST'])

api.add_resource(StockPriceAddApi,'/raporlar/listeler/setAddPrice',methods=['POST'])

api.add_resource(TahminiDegisiklikApi,'/raporlar/anaSayfa/tahminiDegisiklik',methods=['GET'])



api.add_resource(StokAyrintiRaporApi,'/raporlar/listeler/stokRaporAyrintiHepsi/<string:en>/<string:boy>/<string:kenar>/<string:yuzeyIslem>/<string:urunAdi>/<int:listDurum>',methods=['GET'])

api.add_resource(SevkiyatBuYilAyrintiListesiApi,'/raporlar/listeler/sevkiyatBuyilAyrinti/<int:ay>',methods=['GET'])
api.add_resource(SevkiyatGecenYilAyrintiListesiApi,'/raporlar/listeler/sevkiyatGecenAyrinti/<int:ay>',methods=['GET'])
api.add_resource(SevkiyatOncekiYilAyrintiListesiApi,'/raporlar/listeler/sevkiyatOncekiyilAyrinti/<int:ay>',methods=['GET'])

api.add_resource(SiparisGecenYilAyrintiListesiApi,'/raporlar/listeler/siparisGecenAyrinti/<int:ay>',methods=['GET'])
api.add_resource(SiparisBuYilAyrintiListesiApi,'/raporlar/listeler/siparisBuyilAyrinti/<int:ay>',methods=['GET'])
api.add_resource(SiparisOncekiYilAyrintiListesiApi,'/raporlar/listeler/siparisOncekiyilAyrinti/<int:ay>',methods=['GET']) #2020nin sipariş ayrıntısı

##############################SURA###################################
api.add_resource(MusteriBazindaAyrintiApi,'/raporlar/siparis/musteriBazindaAyrinti/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(UreticiBazindaApi,'/islemler/listeler/ureticiDagilimi/<int:year>',methods=['GET'])
api.add_resource(UreticiBazindaExcelApi,'/islemler/listeler/ureticiDagilimiExcelList',methods=['GET','POST'])
api.add_resource(UlkeBazindaSevkiyatApi,'/raporlar/siparis/ulkeBazindaSevkiyat',methods=['GET'])
api.add_resource(UlkeBazindaSevkiyatAyrintiApi,'/raporlar/siparis/ulkeBazindaSevkiyatAyrinti/<int:ulkeId>/<int:year>',methods=['GET'])
api.add_resource(UlkeBazindaSevkiyaYearsListApi,'/raporlar/siparis/ulkeBazindaSevkiyatYears',methods=['GET'])


api.add_resource(UlkeBazindaSevkiyatYearsApi,'/raporlar/siparis/ulkeBazindaSevkiyatYears/<int:year>',methods=['GET'])
api.add_resource(NakliyeBazindaApi,'/islemler/listeler/nakliyeciDagilimi/<int:year>',methods=['GET'])
api.add_resource(NakliyeBazindaExcelApi,'/islemler/listeler/nakliyeciDagilimiExcel',methods=['GET','POST'])
api.add_resource(FobMasraflarApi,'/islemler/listeler/fobMasraflar/<int:year>',methods=['GET'])
api.add_resource(FobMasraflarExcelApi,'/islemler/listeler/fobMasraflarExcel',methods=['GET','POST'])
api.add_resource(NavlunMasraflarApi,'/islemler/listeler/navlunMasraflar/<int:year>',methods=['GET'])
api.add_resource(NavlunMasraflarExcelApi,'/islemler/listeler/navlunMasraflarExcel',methods=['GET','POST'])
api.add_resource(DigerMasraflarApi,'/islemler/listeler/digerMasraflar/<int:year>',methods=['GET'])
api.add_resource(DigerMasraflarExcelApi,'/islemler/listeler/digerMasraflarExcel',methods=['GET','POST'])
api.add_resource(MekusMasraflarApi,'/islemler/listeler/mekusMasraflar/<int:year>',methods=['GET'])
api.add_resource(MekusMasraflarExcelApi,'/islemler/listeler/mekusMasraflarExcel',methods=['GET','POST'])
api.add_resource(KomisyonMasraflarApi,'/islemler/listeler/komisyonMasraflar/<int:year>',methods=['GET'])
api.add_resource(KomisyonMasraflarExcelApi,'/islemler/listeler/komisyonMasraflarExcel',methods=['GET','POST'])
api.add_resource(BankaVeEvrakMasraflarApi,'/islemler/listeler/bankaVeEvrakMasraflar/<int:year>',methods=['GET'])
api.add_resource(BankaVeEvrakMasraflarExcelApi,'/islemler/listeler/bankaVeEvrakMasraflarExcel',methods=['GET','POST'])

######################################################################


api.add_resource(CeyreklikRaporlarApi,'/raporlar/ceyreklikSatislar/<string:year>',methods=['GET'])


######################################################################



api.add_resource(UretimRaporApi,'/raporlar/listeler/uretimRaporuHepsi',methods=['GET'])
api.add_resource(UretimRaporTarihApi,'/raporlar/listeler/uretimRaporTarih/<string:tarih>',methods=['GET'])
api.add_resource(UretimRaporIkiTarihApi,'/raporlar/listeler/uretimRaporIkiTarih/<string:ilk_tarih>/<string:son_tarih>',methods=['GET'])
api.add_resource(UretimRaporExcelApi,'/raporlar/dosyalar/uretimRaporExcelListe',methods=['GET','POST'])
api.add_resource(UretimRaporBuYilApi,'/raporlar/listeler/uretim/yil/<int:yil>',methods=['GET'])

api.add_resource(SevkiyatRaporHepsiMekmerApi,'/raporlar/listeler/sevkiyatRaporHepsiMekmer/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporAllMekmerApi,'/raporlar/listeler/sevkiyatRaporAllMekmer',methods=['GET'])

api.add_resource(SevkiyatRaporHepsiMekmarApi,'/raporlar/listeler/sevkiyatRaporHepsiMekmar/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporAllMekmarApi,'/raporlar/listeler/sevkiyatRaporAllMekmar',methods=['GET'])

api.add_resource(SevkiyatRaporTarihMekmarApi,'/raporlar/listeler/sevkiyatRaporTarihMekmar/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporTekTarihMekmarApi,'/raporlar/listeler/sevkiyatRaporTekTarihMekmar/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporIkiTarihMekmarApi,'/raporlar/listeler/sevkiyatRaporIkiTarihMekmar/<string:ilk_tarih>/<string:son_tarih>',methods=['GET'])

api.add_resource(SevkiyatRaporTarihMekmerApi,'/raporlar/listeler/sevkiyatRaporTarihMekmer/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporTekTarihMekmerApi,'/raporlar/listeler/sevkiyatRaporTekTarihMekmer/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporIkiTarihMekmerApi,'/raporlar/listeler/sevkiyatRaporIkiTarihMekmer/<string:ilk_tarih>/<string:son_tarih>',methods=['GET'])



api.add_resource(SevkiyatRaporHepsiAllApi,'/raporlar/listeler/sevkiyatRaporHepsiAll/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporAllAllApi,'/raporlar/listeler/sevkiyatRaporAllAll',methods=['GET'])
api.add_resource(SevkiyatRaporTarihAllApi,'/raporlar/listeler/sevkiyatRaporTarihAll/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporTekTarihAllApi,'/raporlar/listeler/sevkiyatRaporTekTarihAll/<string:tarih>',methods=['GET'])
api.add_resource(SevkiyatRaporIkiTarihAllApi,'/raporlar/listeler/sevkiyatRaporIkiTarihAll/<string:ilk_tarih>/<string:son_tarih>',methods=['GET'])



api.add_resource(SevkiyatRaporExcelApi,'/raporlar/dosyalar/sevkiyatRaporExcelListe',methods=['GET','POST'])
api.add_resource(StokRaporExcelApi,'/raporlar/listeler/stokRaporExcelListe',methods=['GET','POST'])
api.add_resource(StokRaporAyrintiExcelApi,'/raporlar/listeler/stokRaporAyrintiExcelListe',methods=['GET','POST'])

api.add_resource(AtlantaStokApi,'/raporlar/listeler/atlanta/stoklistesi',methods=['GET'])
api.add_resource(AtlantaStokAyrintiApi,'/raporlar/listeler/atlanta/ayrinti/stoklistesi/<string:skuNo>',methods=['GET'])

api.add_resource(AtlantaStokExcelApi,'/raporlar/listeler/atlanta/stokExcelCikti', methods=['GET','POST'])
api.add_resource(UrunlerUretimListApi,'/raporlar/listeler/urunlerUretimListesi',methods=['GET'])
api.add_resource(UrunlerUretimListAyrintiApi,'/raporlar/listeler/urunlerUretimAyrintiListesi/<int:urunKartId>',methods=['GET'])
api.add_resource(UrunlerUretimExcelApi,'/raporlar/listeler/uretilenSipExcelListe',methods=['GET','POST'])
api.add_resource(UrunlerUretimListAyrintiMekmarApi,'/raporlar/listeler/urunlerUretimAyrintiListesiMekmar/<int:urunKartId>',methods=['GET'])
api.add_resource(UrunlerUretimListAyrintiMekmerApi,'/raporlar/listeler/urunlerUretimAyrintiListesiMekmer/<int:urunKartId>',methods=['GET'])
api.add_resource(UrunlerUretimListMekmarApi,'/raporlar/listeler/urunlerUretimListesiMekmar',methods=['GET','POST'])
api.add_resource(UrunlerUretimListMekmerApi,'/raporlar/listeler/urunlerUretimListesiMekmer',methods=['GET','POST'])


#logs
api.add_resource(LogsMaliyetApi,'/raporlar/mekmar/logs/<int:year>',methods=['GET'])

#maliyet
api.add_resource(MaliyetRaporIslemApi,'/maliyet/listeler/maliyetListesi/<int:yil>/<int:ay>',methods=['GET'])
api.add_resource(MaliyetRaporIslemKarApi,'/maliyet/listeler/maliyetListesiKar/<int:yil>',methods=['GET'])
api.add_resource(MaliyetRaporIslemKarAyrintiApi,'/maliyet/listeler/maliyetListesiKarAyrinti/<int:yil>',methods=['GET'])


api.add_resource(MaliyetRaporIslemYilApi,'/maliyet/listeler/maliyetListesi/<int:yil>',methods=['GET'])
api.add_resource(MaliyetRaporYilListApi,'/maliyet/listeler/maliyetYilListesi',methods=['GET'])
api.add_resource(MaliyetRaporIslemAyListesi,'/maliyet/listeler/maliyetAyListesi/<int:yil>',methods=['GET'])
api.add_resource(MaliyetRaporExcelApi, '/maliyet/dosyalar/maliyetRaporExcelListe', methods=['GET','POST'])

api.add_resource(MaliyetRaporuAyrintiApi,'/maliyet/ayrinti/listeler/maliyetListesi/<string:siparisno>',methods=['GET'])


api.add_resource(MarketingListeApi,'/finans/listeler/marketing',methods=['GET'])
api.add_resource(ByMarketingYuklemeApi,'/finans/listeler/byMarketing/<int:month>',methods=['GET'])
api.add_resource(ByMarketingYuklemeExcelApi,"/raporlar/dosyalar/marketingExcellCikti",methods=['POST','GET'])
api.add_resource(ByCustomersYuklemeExcelApi,"/raporlar/dosyalar/customersExcellCikti",methods=['POST','GET'])
api.add_resource(ByMarketingDetailExcelApi,"/raporlar/dosyalar/byMarketingAyrintiExcellCikti",methods=['POST','GET'])
api.add_resource(MusteriBazindaUretimApi,'/raporlar/musteri/uretim',methods=['GET','POST'])
api.add_resource(ByMarketingMonthLoadApi,'/raporlar/marketing/ayBazinda/yukleme',methods=['POST','GET'])
api.add_resource(ByMarketingMonthLoadIcPiyasaAyrintiApi,'/raporlar/marketing/ayBazinda/yuklemeIcPiyasaAyrinti/<int:month>',methods=['POST','GET'])
api.add_resource(ByMarketingMonthLoadMekmerAyrintiApi,'/raporlar/marketing/ayBazinda/yuklemeMekmerAyrinti/<int:month>',methods=['POST','GET'])

api.add_resource(MonthMarketingExcellCikti,'/raporlar/musteri/monthMarketingExcell',methods=['GET','POST'])
api.add_resource(MonthMarketingAyrintiExcellCikti,'/raporlar/musteri/monthMarketingAyrintiExcell',methods=['GET','POST'])

#Mekmer Dış Faturalama
api.add_resource(MekmerDisFaturaModelApi,'/mekmer/disFaturaModel',methods=['GET','POST'])
api.add_resource(MekmerDisFaturaIslemApi,'/mekmer/disFaturaIslem/kaydet',methods=['GET','POST'])
api.add_resource(MekmerDisFaturaIslemGuncelleApi,'/mekmer/disFaturaIslem/guncelle',methods=['GET','POST'])
api.add_resource(MekmerDisFaturaListApi,'/mekmer/disFaturaIslem/getMekmerDisFatura',methods=['GET','POST'])

api.add_resource(MekmerDisFaturaKaydetApi,'/mekmer/disFaturaIslem/setMekmerFatura/<int:id>/<string:evrakAdi>',methods=['GET','POST'])

api.add_resource(AyoAlisFiyatiDegistirApi,'/raporlar/ayo/alisFiyatiControlChange',methods=['GET','POST'])
api.add_resource(GalleriaAddApi,'/panel/mekmarcom/galleria/add',methods=['POST'])
api.add_resource(GalleriaPhotosApi,'/panel/mekmarcom/galleri/getPhotos/<int:product_id>',methods=['GET'])
api.add_resource(GalleriaPhotosDeleteApi,'/panel/mekmarcom/galeri/deletePhotos/<int:id>',methods={'GET'})
api.add_resource(GalleryVideosAddApi,"/panel/mekmarcom/gallery/videos",methods=['POST'])

#excel çıktı işlemler

api.add_resource(SiparisCekiListesiApi, '/excel/listeler/siparisCekiListesi', methods=['GET','POST'])

api.add_resource(SiparisEtiketListesiApi, '/excel/listeler/siparisEtiketListesi/<string:etiketAdi>', methods=['GET'])       


api.add_resource(ContainerAddApi,"/operasyon/containeramount",methods=['POST'])
api.add_resource(ContainerAmountApi,"/ayo/getOrderContainerAmount/<string:sipNo>",methods=['GET'])

#Mekmar Raporları Alanı
api.add_resource(MekmarUlkeRaporuApi,"/raporlar/mekmarraporlari/ulke/<int:year>",methods=['GET'])
api.add_resource(MekmarUlkeRaporuAyrintiApi,"/raporlar/mekmarraporlari/ulke/ayrinti/<int:ulke_id>/<int:year>",methods=['GET'])

api.add_resource(MekmarMusteriRaporuApi,"/raporlar/mekmarraporlari/musteri/<int:year>",methods=['GET'])
api.add_resource(MekmarMusteriRaporuAyrintiApi,"/raporlar/mekmarraporlari/musteri/ayrinti/<int:musteri_id>/<int:year>",methods=['GET'])


api.add_resource(MekmarTedarikciRaporuApi,"/raporlar/mekmarraporlari/tedarikci/<int:year>",methods=['GET'])

api.add_resource(MekmarTedarikciRaporuAyrintiApi,'/raporlar/mekmarraporlari/tedarikci/ayrinti/<int:tedarikci_id>/<int:year>',methods=['GET'])

api.add_resource(MkRaporlariApi,'/raporlar/listeler/mkraporlari/<int:year>',methods=['GET'])
api.add_resource(MkRaporlariExcelApi,'/raporlar/listeler/mkraporlari/excel',methods=['GET','POST'])

api.add_resource(GuRaporlariApi,'/raporlar/listeler/guraporlari/<int:year>',methods=['GET'])


#Notifications
api.add_resource(NotificationIslemApi,'/notification/islemler',methods=['POST','PUT'])
api.add_resource(NotificationListApi,'/notification/getList/<int:id>',methods=['GET'])
api.add_resource(NotificationIslemAnsweredApi,'/notification/islemler/ansered',methods=['POST','PUT'])
api.add_resource(NotificationIslemFollowApi,'/notification/islemler/follow',methods=['POST'])
api.add_resource(NotificationIslemFollowAnsweredApi,'/notification/islemler/follow/answered',methods=['POST'])

#Yapilacaklar
api.add_resource(YapilacaklarApi,'/raporlar/yapilacaklar/list',methods=['GET'])
api.add_resource(YapilacaklarModelApi,'/yapilacaklar/model',methods=['GET'])
api.add_resource(YapilacaklarIslemApi,'/yapilacaklar/islem',methods=['POST','PUT'])
api.add_resource(YapilacaklarKullaniciListApi,'/yapilacaklar/kullanici/list/<int:userId>',methods=['GET'])
api.add_resource(YapilacaklarSilApi,'/yapilacaklar/delete/<int:id>',methods=['DELETE'])
api.add_resource(YapilacaklarChangeStatusApi,'/yapilacaklar/yapildi',methods=['PUT'])
api.add_resource(YapilacaklarDetailApi,'/yapilacaklar/list/detail/<int:id>',methods=['GET'])
api.add_resource(YapilacaklarAllApi,'/yapilacaklar/list/all',methods=['GET'])
#Maliyet Hatalar
api.add_resource(MaliyetHataRaporIslemApi,'/raporlar/maliyet/hatalar',methods=['GET','POST','PUT'])
api.add_resource(MaliyetHataRaporModelApi,'/raporlar/maliyet/hatalar/model',methods=['GET'])
api.add_resource(MaliyetHataRaporDeleteApi,'/raporlar/maliyet/hatalar/delete/<int:id>',methods=['DELETE'])
api.add_resource(MaliyetHataRaporDetayApi,'/raporlar/maliyet/hatalar/detay/<int:id>',methods=['GET'])

#Eta Yaklaşan Bildirimi
api.add_resource(EtaYaklasanTarihBildirimApi,'/eta/yaklasan/bildirim/list',methods=['GET'])
api.add_resource(EtaYaklasanTarihBildirimStatusApi,'/eta/yaklasan/bildirim/status/<string:po>/<string:etaSure>',methods=['GET'])

#Satışçı ve Operasyon Özet
api.add_resource(SiparisSatisciInfoApi,'/uretim/satisci/info',methods=['GET'])
api.add_resource(SsOpChangeApi,'/uretim/satisci/change/<string:po>/<int:ss>/<int:op>',methods=['GET'])
if __name__ == '__main__':
    app.run(port=5000,debug=True) #https://doktor-servis.mekmar.com/raporlar/listeler/uretimRaporuHepsi
