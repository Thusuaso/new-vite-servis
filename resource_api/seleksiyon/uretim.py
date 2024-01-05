from models.seleksiyon import *
from resource_api.seleksiyon.listeler import SeleksiyonListeler
from helpers import SqlConnect,TarihIslemler


class Uretim:

    def __init__(self):  

        self.data = SqlConnect().data


    def getUrunModel(self,kasano):

        tarihIslem = TarihIslemler()
        
        item = self.data.getStoreList(
            """
            select
            *,
            dbo.Get_KategoriAdi(u.UrunKartID) as kategori,
            dbo.Get_Ebat(u.UrunKartID) as ebat,
            dbo.Get_KenarIslem(u.UrunKartID) as kenarislem,
            dbo.Get_UrunAdi(u.UrunKartID) as urunadi,
            (Select t.FirmaAdi from TedarikciTB t where t.ID=u.TedarikciID) as tedarikci
            from
            UretimTB u
            where u.KasaNo=?
            """,(kasano)
        )[0]

        model = UretimModel()

        model.id = item.ID 
        model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
        model.kasano = item.KasaNo 
        model.urunkartid = item.UrunKartID 
        model.tedarikciid = item.TedarikciID 
        model.urunbirimid = item.UrunBirimID 
        model.urunocakid = item.UrunOcakID 
        if item.Adet != None:
            model.adet = float(item.Adet)
            model.kasaadet =  float(item.Adet)
        model.kutuadet = item.KutuAdet
       
        if item.Miktar != None:
            model.miktar = float(item.Miktar)
        if item.OzelMiktar != None:
            model.ozelmiktar = float(item.OzelMiktar)
        model.aciklama = item.Aciklama 
        if item.SqmMiktar != None:
            model.sqm_miktar = float(item.SqmMiktar)
        model.uretimturid = item.UretimTurID 
        model.uretimturaciklama = item.UretimTurAciklama 
        model.urundurumid = item.UrunDurumID 
        model.siparisaciklama = item.SiparisAciklama
        model.duzenleyen = item.Duzenleyen 
        model.kasalayan = item.Kasalayan 
        model.disarda = item.Disarda 
        model.kullaniciid = item.KullaniciID 
        model.sirano = item.SiraNo 
        model.kutuiciadet = item.KutuIciAdet
        model.kategoriadi = item.kategori 
        model.ebat = item.ebat 
        model.kenarislem = item.kenarislem 
        model.urunadi = item.urunadi 
        model.kayit_tur = item.UretimTurAciklama
        model.tanim = f"{item.tedarikci}/{item.kategori}/{item.urunadi}/{item.kenarislem}/{item.ebat}"
        model.kutu = item.Kutu
        model.disarda = item.Disarda
        model.bagli = item.Bagli
        model.bulunamayan = item.Bulunamadi

        if model.uretimturid == 2:

            siparisIslem = SeleksiyonListeler() 

            model.sipariskart = siparisIslem.getUretimSiparisDetay_UrunKart(model.siparisaciklama,model.urunkartid)

            
            
        schema = UretimSchema()

        return schema.dump(model)

    
    def getBosUrunModel(self):
        model = UretimModel()

        schema = UretimSchema()

        return schema.dump(model)

    def cokluKaydet(self,item,kayit_sayisi):
        try:
            str_kasalar = "("
            
            for key in range(0,int(kayit_sayisi)):
                kasano = int(item['kasano'])
                if key == 0:
                    str_kasalar += str(kasano)
                if key != 0:
                    kasano +=  key                    
                    str_kasalar += "," + str(kasano)

               
                self.kaydet(item,kasano)
                
            
            str_kasalar += ")"
            
            return True,str_kasalar
        except Exception as e:
            print('Üretim Çoklu Kayıt Hata : ',str(e))
            return False,""

    def kaydet(self,item,kasano):
        
        item['miktar'] = float(item['miktar'])
        try:
            self.data.update_insert(
                """
                insert into UretimTB (
                    Tarih,
                    KasaNo,
                    UrunKartID,
                    TedarikciID,
                    UrunBirimID,
                    UrunOcakID,
                    Adet,
                    KutuAdet,
                    Miktar,
                    Aciklama,
                    UretimTurID,
                    UretimTurAciklama,
                    UrunDurumID,
                    SiparisAciklama,
                    Kutu,
                    Bagli,
                    Duzenleyen,
                    Kasalayan,
                    Disarda,
                    KullaniciID,
                    KutuIciAdet,
                    SqmMiktar,
                    Bulunamadi
                )
                values (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    item['tarih'],
                    kasano,
                    item['urunkartid'],
                    item['tedarikciid'],
                    item['urunbirimid'],
                    item['urunocakid'],
                    item['adet'],
                    item['kutuadet'],
                    item['miktar'],
                    item['aciklama'],
                    item['uretimturid'],
                    item['uretimturaciklama'],
                    item['urundurumid'],
                    item['siparisaciklama'],
                    item['kutu'],
                    item['bagli'],
                    item['duzenleyen'],
                    item['kasalayan'],
                    item['disarda'],
                    item['kullaniciid'],
                    item['kutuiciadet'],
                    item['sqm_miktar'],item['bulunamayan']
                )
            )

            return True
        except Exception as e:
            print('Üretim Kaydet Hata : ', str(e))
            return False

    def kasaKayitKontrol(self,item):

        kontrol = self.data.getStoreList(
                """
                select count(*) as durum from UretimTB where KasaNo=?
                """,(item['kasano'])
            )[0].durum 
        
        if kontrol > 0:
            return False 

        else :
            return True

    def guncelle(self,item):
        try:
            self.data.update_insert(
                """
                update UretimTB set 
                Tarih=?,
                KasaNo=?,
                UrunKartID=?,
                TedarikciID=?,
                UrunBirimID=?,
                UrunOcakID=?,
                Adet=?,
                KutuAdet=?,
                Miktar=?,
                Aciklama=?,
                UretimTurID=?,
                UretimTurAciklama=?,
                UrunDurumID=?,
                SiparisAciklama=?,
                Kutu=?,
                Bagli=?,
                Duzenleyen=?,
                Kasalayan=?,
                Disarda=?,
                KullaniciID=?,
                KutuIciAdet=? ,
                SqmMiktar = ?,
                Bulunamadi=?
                where ID=?
                """,
                (
                    item['tarih'],
                    item['kasano'],
                    item['urunkartid'],
                    item['tedarikciid'],
                    item['urunbirimid'],
                    item['urunocakid'],
                    item['adet'],
                    item['kutuadet'],
                    item['miktar'],
                    item['aciklama'],
                    item['uretimturid'],
                    item['uretimturaciklama'],
                    item['urundurumid'],
                    item['siparisaciklama'],
                    item['kutu'],
                    item['bagli'],
                    item['duzenleyen'],
                    item['kasalayan'],
                    item['disarda'],
                    item['kullaniciid'],
                    item['kutuiciadet'],
                    item['sqm_miktar'],
                    item['bulunamayan'],
                    item['id']
                )
            ) 
            
            return True
        except Exception as e:
            print('Üretim Güncelleme Hata : ',str(e))

            return False

    def sil(self,kasano):
        try:
            self.data.update_insert(
                """
                Delete from UretimTB where KasaNo=?
                """,
                (
                    kasano
                )
            )

            return False
        except Exception as e:
            print('Üretim Hata sil : ', str(e))

            return False

    def getDisFirmaKasaNo(self):

        dtKasaNo = self.data.getList(
            """
                select
                Max(KasaNo) + 1 as KasaNo
                from
                UretimTB
                where TedarikciID not in (1,123)
            """
        )[0].KasaNo

        return dtKasaNo

    def getSeleksiyonFirmaKasaNo(self):

        dt2KasaNo = self.data.getList(
            """
            select max(KasaNo)+1 as KasaNo from UretimTB where TedarikciID in (1,123) and YEAR(Tarih) = '2024' 
            """
        )[0].KasaNo

        return dt2KasaNo


    def getSeleksiyonUrunKartBilgileri(self,urunkartid):
        

        dt2KasaNo = self.data.getList(
            """
            select max(KasaNo)+1 as KasaNo from UretimTB where TedarikciID in (1,123) and YEAR(Tarih) in ('2024','2023') 
            """
        )[0].KasaNo

        return dt2KasaNo
    
    
    def getUretimFazlasiMi(self,po,urunkartid):

        siparis = self.data.getStoreList("""
                                            select Miktar from SiparisUrunTB where SiparisNo=? and UrunKartID=?
                                        
                                        """,(po,urunkartid))
        uretim = self.data.getStoreList("""
                                            select sum(Miktar) as Toplam from UretimTB where SiparisAciklama=? and UrunKartID=? group by SiparisAciklama   
                                                 
                                    """,(po,urunkartid))
        
        model = UretimFazlaMiModel()
        model.siparismiktari = siparis[0].Miktar
        if len(uretim)>0:
            model.uretimtoplami = uretim[0].Toplam
        else:
            model.uretimtoplami=0
        
        schema = UretimFazlaMiSchema()

        return schema.dump(model)
        
    def getProductCrateControl(self,data):
        try:
            print("getProductCrateControl",data)
            uretim = self.data.getStoreList("""
                                                select Miktar from UretimTB where SiparisAciklama=? and UrunKartID=?
                                            
            
                                            """,(data['siparisno'],data['urunkartid']))
            siparisMiktari = self.data.getStoreList("""
                                                        select Miktar from SiparisUrunTB where SiparisNo=? and UrunKartID=?
                                                    
                                                    """,(data['siparisno'],data['urunkartid']))[0].Miktar
            
            
            
            uretimMiktari = 0
            for item in uretim:
                uretimMiktari += item.Miktar
                
                
            uretimMiktari += float(data['miktar']) * int(data['kasaadet'])
            
            if(uretimMiktari > siparisMiktari):
                return True
            else:
                return False
            
            
                
                
        except Exception as e:
            print('getProductCrateControl hata',str(e))
            return False
    
    def getPoProductList(self,po):
        try:
            result = self.data.getStoreList("""
                                    select 

                                        su.ID,
                                        su.UrunKartID,
                                        (select KategoriAdi from KategoriTB k where k.ID = uk.KategoriID) as KategoriAdi,
                                        (select UrunAdi from UrunlerTB ur where ur.ID = uk.UrunID) as UrunAdi,
                                        (select YuzeyIslemAdi from YuzeyKenarTB yk where yk.ID = uk.YuzeyID) as YuzeyIslemAdi,
                                        (select En from OlculerTB o where o.ID = uk.OlcuID) as En,
                                        (select Boy from OlculerTB o where o.ID = uk.OlcuID) as Boy,
                                        (select Kenar from OlculerTB o where o.ID = uk.OlcuID) as Kenar
                                    from SiparisUrunTB su
                                    inner join UrunKartTB uk on uk.ID = su.UrunKartID

                                    where SiparisNo=?
                                   """,(po))
            liste = list()
            for item in result:
                model = PoProductListModel()
                model.id = item.ID
                model.product_id = item.UrunKartID
                model.product_category = item.KategoriAdi
                model.product_name = item.UrunAdi
                model.product_surface = item.YuzeyIslemAdi
                model.product_width = item.En
                model.product_height = item.Boy
                model.product_edge = item.Kenar
                model.product_full_name = item.KategoriAdi + '/' + item.UrunAdi + '/' + item.YuzeyIslemAdi + '/' + item.En + 'x' + item.Boy + 'x' + item.Kenar
                liste.append(model)
                
            schema = PoProductListSchema(many=True)
            return schema.dump(liste)
        
                
            
        except Exception as e:
            print('getPoProductList hata',str(e))
            return False
        
