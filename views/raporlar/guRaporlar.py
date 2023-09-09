import datetime
from helpers import SqlConnect
from openpyxl import *
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from models.raporlar.guRaporlari import * 
import shutil
from resource_api.maliyet_raporlar.siparisler import *

class GuRaporlari:
    def __init__(self):
        self.sql = SqlConnect().data
        self.siparisler = []
        self.forwardingPo = self.sql.getList("""
                                        select 
                                        MONTH(s.YuklemeTarihi) as Month,
                                        sum(s.NavlunSatis) as Navlun,
                                        sum(s.DetayTutar_1) as Detail1, 
                                        sum(s.DetayTutar_2) as Detail2,
                                        sum(s.DetayTutar_3) as Detail3 
                                        from SiparislerTB s 
                                        inner join MusterilerTB m on m.ID=s.MusteriID

                                        where YEAR(s.YuklemeTarihi) >= YEAR(GETDATE())-10 and
                                        m.Marketing='Mekmar'

                                        group by
                                        MONTH(s.YuklemeTarihi)

                                        order by
                                            Month(s.YuklemeTarihi)
                                      """) 
        self.forwardingOrders = self.sql.getList("""
                                                    select 
                                                    MONTH(s.YuklemeTarihi) as Month,
                                                    sum(su.SatisToplam) as Total
                                                    from SiparislerTB s 
                                                    inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                    inner join MusterilerTB m on m.ID = s.MusteriID

                                                    where 
                                                    YEAR(s.YuklemeTarihi) >= YEAR(GETDate()) - 10 and
                                                    m.Marketing='Mekmar'

                                                    group by
                                                    MONTH(s.YuklemeTarihi)

                                                    order by
                                                        Month(s.YuklemeTarihi)
                                      """)
    
    def getMaliyetListesiKar(self,year):
        try:
            self.__getMaliyetListesi(year)
            liste = []
            
            siparisler_musteri = self.sql.getStoreList("""
                                                            select 
                                                                s.MusteriID,
                                                                m.FirmaAdi
                                                            from SiparislerTB s
                                                                inner join MusterilerTB m on m.ID = s.MusteriID

                                                            where
                                                                YEAR(s.YuklemeTarihi) = ? and
                                                                s.SiparisDurumID=3 and
                                                                m.Marketing = 'Mekmar'
                                                            group by
                                                                s.MusteriID,
                                                                m.FirmaAdi
                                                        
                                                        """,(year))
            
            liste = list()
            for item in siparisler_musteri:
                model = OzelMaliyetListeKarModel()
                model.musteri_id = item.MusteriID
                model.musteri_adi = item.FirmaAdi
                toplam_bedel,masraf_toplam,odenen_usd_tutar,odenen_try_tutar,kar_zarar,kar_zarar_tl = self.__getSiparisler(item.MusteriID)
                model.toplam_bedel = toplam_bedel
                model.masraf_toplam = masraf_toplam
                model.odenen_usd_tutar = odenen_usd_tutar
                model.odenen_try_tutar = odenen_try_tutar
                model.kar_zarar =kar_zarar
                model.kar_zarar_tl = kar_zarar_tl
                model.kalan_bedel = model.toplam_bedel - model.odenen_usd_tutar
                if(odenen_usd_tutar != 0):
                    model.kar_zarar_orani = round((kar_zarar / odenen_usd_tutar * 100),2)
                else:
                    model.kar_zarar_orani = 0
                liste.append(model)
                
            schema = OzelMaliyetListeKarSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getMaliyetListesiKar hata',str(e))
            return False
    def __getMaliyetListesi(self,year):
        self.siparisler = SiparislerKar(year).siparis_listesi
    def __getSiparisler(self,musteri_id):
        toplam_bedel = 0
        masraf_toplam= 0
        odenen_usd_tutar= 0
        odenen_try_tutar= 0
        kar_zarar= 0
        kar_zarar_tl= 0

        for item in self.siparisler:
            if(item.musteri_id == musteri_id):
                toplam_bedel += self.__noneControl(item.toplam_bedel)
                masraf_toplam+= self.__noneControl(item.masraf_toplam)
                odenen_usd_tutar += self.__noneControl(item.odenen_usd_tutar)
                odenen_try_tutar += self.__noneControl(item.odenen_try_tutar)
                kar_zarar += self.__noneControl(item.kar_zarar)
                kar_zarar_tl += self.__noneControl(item.kar_zarar_tl)
                
        return toplam_bedel,masraf_toplam,odenen_usd_tutar,odenen_try_tutar,kar_zarar,kar_zarar_tl
    def __noneControl(self,value):
        if(value == None):
            return 0
        else:
            return float(value)
    
    #Konteynır Ülke
    def getUlkeRaporlari(self,year):
        try:
            result = self.sql.getStoreList("""
                                        select 
										count(m.UlkeId) as SipSayisi,
										yu.UlkeAdi,
										sum(s.KonteynirSayisi) as KonteynirSayisi,
										m.UlkeId

                                    from MusterilerTB m
                                    inner join SiparislerTB s on s.MusteriID = m.ID
                                    inner join YeniTeklif_UlkeTB yu on yu.Id = m.UlkeId

                                    where YEAR(s.YuklemeTarihi) = ? and m.Marketing = 'Mekmar'
									group by m.UlkeId,yu.UlkeAdi
                                   """,(year))
            
            liste = list()
            for item in result:
                model = UlkeyeGoreModel()
                model.sip_sayisi = item.SipSayisi
                model.ulke_adi = item.UlkeAdi
                model.ulke_id = item.UlkeId
                model.konteynir_sayisi = self.__noneControl(item.KonteynirSayisi)
                liste.append(model)
            schema = UlkeyeGoreSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getUlkeRaporlari hata',str(e))
            return False
    def getMusteriRaporlari(self,year):
        try:
            result = self.sql.getStoreList("""
                                                select 


                                                    count(m.ID) as YukMusSayisi,
                                                    m.ID,
                                                    m.FirmaAdi,
                                                    yu.UlkeAdi,
                                                    sum(s.KonteynirSayisi) as KonteynirSayisi


                                                from MusterilerTB m
                                                inner join SiparislerTB s on s.MusteriID = m.ID
                                                inner join YeniTeklif_UlkeTB yu on yu.Id = m.UlkeId

                                                where m.Marketing = 'Mekmar' and YEAR(s.YuklemeTarihi) = ?
                                                group by
                                                    m.ID,m.FirmaAdi,yu.UlkeAdi
                                            
                                            
                                            """,(year))
            
            liste = list()
            for item in result:
                model = MusteriyeGoreModel()
                model.id = item.ID
                model.firma_adi = item.FirmaAdi
                model.yuk_mus_sayisi = self.__noneControl(item.YukMusSayisi)
                model.ulke_adi = item.UlkeAdi
                model.konteynir_sayisi = self.__noneControl(item.KonteynirSayisi)
                liste.append(model)
            schema = MusteriyeGoreSchema(many = True)
            return schema.dump(liste)
        except Exception as e:
            print(' getMusteriRaporlari , hata',str(e))
            return False
    def getTedarikciRaporlari(self,year):
        try:
            result = self.sql.getStoreList("""
                                    select 


                                        t.ID,
                                        t.FirmaAdi,
                                        sum(su.AlisFiyati * su.Miktar) as Total,
                                        count(t.ID) as YuklenenTedarikci

                                    from TedarikciTB t
                                    inner join SiparisUrunTB su on su.TedarikciID = t.ID
                                    inner join SiparislerTB s on s.SiparisNo= su.SiparisNo
                                    inner join MusterilerTB m on m.ID = s.MusteriID
                                    where YEAR(s.YuklemeTarihi) = ? and m.Marketing = 'Mekmar'

                                    group by 
                                        t.ID,t.FirmaAdi
                                    order by 
                                        Total desc
                                   
                                   """,(year))
            liste=  list()
            for item in result:
                model = TedarikciyeGoreModel()
                model.tedarikci_id = item.ID
                model.firma_adi = item.FirmaAdi
                model.total_alis = self.__noneControl(item.Total)
                model.yuklenen_tedarikci_sayisi = self.__noneControl(item.YuklenenTedarikci)
                liste.append(model)
            schema = TedarikciyeGoreSchema(many= True)
            return schema.dump(liste)
            
        except Exception as e:
            print("getTedarikciRaporlari,hata",str(e))
            return False
    #Mekus
    def getMekusMasraflar(self,year):
        try:
            result = self.sql.getStoreList("""
                                                select 


                                                    sum(s.DetayTutar_4) as Mekus,
                                                    s.SiparisNo as SiparisNo


                                                from SiparislerTB s
                                                where s.depo_yukleme=1 and YEAR(s.YuklemeTarihi)=?
                                                group by

                                                    s.MusteriID,s.SiparisNo
                                                order by Mekus desc
                                            """,year)

            liste = list()
            for item in result:
                model = MekusMasraflarModel()
                model.siparisNo = item.SiparisNo
                model.mekusMasraf = item.Mekus
                liste.append(model)
                
            schema = MekusMasraflarSchema(many=True)
            return schema.dump(liste)
                
        except Exception as e:
            print('getMekusMasraflar Hata',str(e))
    
    #Logs
    def getLogsMaliyet(self,year):
        try:
            result = self.sql.getStoreList("""
                                                select 


                                                *,
                                                YEAR(DegisiklikTarihi) as Year,
                                                Month(DegisiklikTarihi) as Month,
                                                Day(DegisiklikTarihi) as Day


                                            from MaliyetAnaliziDegisikliklerTB
                                            where YEAR(DegisiklikTarihi) = ?
											order by DegisiklikTarihi desc
                                       
                                       """,(year))
            
            liste = list()
            for item in result:
                model = LogsMaliyetModel()
                model.id = item.ID
                model.kayit_tarihi = item.DegisiklikTarihi
                model.siparis_no = item.SiparisNo
                model.yukleme_tarihi = item.YuklemeTarihi
                model.info = item.IslemAdi
                model.kayit_kisi = item.DegisiklikYapan
                model.yil = item.Year
                model.ay = item.Month
                model.gun = item.Day
                model.renk = item.Renk
                liste.append(model)
            schema = LogsMaliyetSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getLogsMaliyet',str(e))
            return False

    def getForwardingSummary(self):
        try:
            liste = list()
            for item in self.forwardingPo:
                model = ForwardingSummaryModel()
                model.month = item.Month
                model.month_str = self.__getMonth(item.Month)
                model.fob = self.__getFobTotal(item.Month)
                model.ddp = float(model.fob) + float(item.Navlun) + float(item.Detail1) + float(item.Detail2) + float(item.Detail3)
                liste.append(model)
            schema = ForwardingSummarySchema(many=True)
            return schema.dump(liste)
        
        
        except Exception as e:
            print('getForwardingSummary hata',str(e))
            return False
        
    def __getMonth(self,month_id):
        month = {1:'Ocak',2:'Şubat',3:'Mart',4:'Nisan',5:'Mayıs',6:'Haziran',7:'Temmuz',8:'Ağustos',9:'Eylül',10:'Ekim',11:'Kasım',12:'Aralık'}
        return month[month_id]
    
    def __getFobTotal(self,month):
        for item in self.forwardingOrders:
            if(item.Month == month):
                return item.Total
        
        
        