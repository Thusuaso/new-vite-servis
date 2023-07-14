
from models.raporlar import yukleme
from models.siparisler_model import SiparisGirisSchema,SiparisGirisModel
from models.siparisler_model.siparisGirisUrun import SiparisGirisUrunModel
from models import SiparislerModel
from helpers import SqlConnect,TarihIslemler
from helpers import MailService
import datetime
from resource_api.finans.caprazkur import DovizListem

class SiparisBolme:
    def __init__(self,sipDatas):
        self.data = SqlConnect().data
        self.siparisBilgileri = sipDatas['siparis']
        self.siparisUrunBilgileri = sipDatas['siparisUrunler']
    
    
    def siparisBolme(self):
        self.__setSiparisInsert()
    
    
    def __setSiparisInsert(self):
        
        try:
            self.__setSiparisUpdate()
            result = self.data.getStoreList("""
                                                select * from SiparislerTB where SiparisNo=?
                                        """,(self.siparisBilgileri['siparisNo']))
            if result:
                return False
            else:
                
                s_tarihi = self.__dateConvert(self.siparisBilgileri['siparisTarihi'])
                t_yukleme_tarihi = self.__dateConvert(self.siparisBilgileri['TahminiyuklemeTarihi'])
                vade = None 
                if self.siparisBilgileri['vade'] != None:
                    vade = self.__dateConvert(self.siparisBilgileri['vade'])

                self.data.update_insert("""
                                    insert into SiparislerTB (
                                        SiparisNo,SiparisTarihi,OdemeTurID,TeslimTurID,MusteriID,Pesinat,NavlunFirma,NavlunMekmarNot,NavlunAlis,
                                        NavlunSatis,KullaniciID,SiparisDurumID,UretimAciklama,SevkiyatAciklama,FinansAciklama,OdemeAciklama,TahminiYuklemeTarihi,
                                        Vade,Ulke,UlkeId,Komisyon,DetayAciklama_1,DetayMekmarNot_1,DetayTutar_1,DetayAlis_1,DetayAciklama_2,DetayMekmarNot_2,
                                        DetayTutar_2,DetayAlis_2,DetayAciklama_3,DetayMekmarNot_3,DetayTutar_3,DetayTutar_4,DetayAciklama_4,DetayAlis_3,SiparisSahibi,EvrakGideri,Eta,
                                        KonteynerAyrinti,KonteynerNo,TeslimYeri,FaturaKesimTurID,AktarmaLimanAdi,depo_yukleme,sigorta_id,sigorta_Tutar,Operasyon ,Finansman
                                    )
                                    values
                                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    """,(
                                        self.siparisBilgileri['gidenSiparisNo'],s_tarihi,self.siparisBilgileri['odemeTurId'],self.siparisBilgileri['teslimTurId'],self.siparisBilgileri['musteriId'],
                                        self.siparisBilgileri['pesinat'],self.siparisBilgileri['navlunFirma'],self.siparisBilgileri['navlunMekmarNot'],self.siparisBilgileri['navlunAlis'],self.siparisBilgileri['navlunSatis'],
                                        self.siparisBilgileri['kullaniciId'],self.siparisBilgileri['siparisDurumId'],self.siparisBilgileri['uretimAciklama'],self.siparisBilgileri['sevkiyatAciklama'],
                                        self.siparisBilgileri['finansAciklama'],self.siparisBilgileri['odemeAciklama'],t_yukleme_tarihi,vade,self.siparisBilgileri['ulke'],self.siparisBilgileri['ulkeId'],self.siparisBilgileri['komisyon'],
                                        self.siparisBilgileri['detayAciklama_1'],self.siparisBilgileri['detayMekmarNot_1'],self.siparisBilgileri['detayTutar_1'],self.siparisBilgileri['detayAlis_1'],
                                        self.siparisBilgileri['detayAciklama_2'],self.siparisBilgileri['detayMekmarNot_2'],self.siparisBilgileri['detayTutar_2'],self.siparisBilgileri['detayAlis_2'],
                                        self.siparisBilgileri['detayAciklama_3'],self.siparisBilgileri['detayMekmarNot_3'],self.siparisBilgileri['detayTutar_3'],self.siparisBilgileri['detayTutar_4'],self.siparisBilgileri['detayAciklama_4'],self.siparisBilgileri['detayAlis_3'],self.siparisBilgileri['siparisSahibi'],
                                        self.siparisBilgileri['evrakGideri'],self.siparisBilgileri['eta'],self.siparisBilgileri['konteynerAyrinti'],self.siparisBilgileri['konteynerNo'],self.siparisBilgileri['teslimYeri'],self.siparisBilgileri['faturaKesimTurId'],self.siparisBilgileri['liman'],self.siparisBilgileri['depo'], self.siparisBilgileri['sigorta_id'],self.siparisBilgileri['sigorta_tutar'],self.siparisBilgileri['operasyon'],self.siparisBilgileri['finansman']
                                    ))
            
            
            
            self.mailGonderUpdate(self.siparisBilgileri)
            print('Sipariş Bölme Yeni Sipariş Girişi Başarılı')
            return True
            
        except Exception as e:
            print('Sipariş Bölme Yeni Sipariş Girişi Hatası',str(e))
            return False
        
    
    def __setSiparisUpdate(self):
        try:
            siparisNo = self.siparisBilgileri['siparisNo']
            gidenSiparisNo = self.siparisBilgileri['gidenSiparisNo']
            kalanSiparisNo = self.siparisBilgileri['kalanSiparisNo']
            newPesinat = self.siparisBilgileri['newPesinat']
            pesinat = self.siparisBilgileri['pesinat']
            resultOdemeler = self.data.getStoreList("""
                                                        select * from OdemelerTB where SiparisNo=?
                                                    """,(siparisNo))
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            # if len(resultOdemeler)>0:
            #     if len(siparisNo.split('-'))>0:
            #         self.__odemelerUpdate(siparisNo,pesinat,kalanSiparisNo)
            #         self.__odemelerInsert(gidenSiparisNo,pesinat,resultOdemeler)
            #     else:
            #         self.__odemelerInsert(gidenSiparisNo,pesinat,resultOdemeler)
            #         self.__odemelerUpdate(siparisNo,pesinat,kalanSiparisNo)
            
                
                
            self.__setSiparisUrunInsert()
            for item in self.siparisUrunBilgileri:
                if item['isChange'] == True:
                    satisToplam = item['newAmountmiktar'] * item['satisFiyati']
                    kasaAdet = 0
                    if item['newAmountmiktar'] == 0:
                        self.__setSiparisUrunDelete(item['id'])
                    else:
                        self.__setSiparisUrunUpdate(kalanSiparisNo,item['newAmountmiktar'],satisToplam,kasaAdet,item['id'])
                    
                    
                else:
                    
                    self.__setSiparisUrunDegismeyenUpdate(kalanSiparisNo,item['id'])
                    self.__setSiparisUrunDeleteKalan(item['urunKartId'],gidenSiparisNo)
                    
                    
                    
            
            
            self.data.update_insert("""
                                        update SiparislerTB SET SiparisNo=?,Pesinat=?  where SiparisNo=?
                                    """,(kalanSiparisNo,newPesinat,siparisNo))
            
            print('Sipariş Bölme Güncellendi.')
            return True
        except Exception as e:
            print('Siparis Bölme Güncelleme Hatası' + str(e))
            return False

    
    def __setSiparisUrunDeleteKalan(self,urunKartId,gidenSiparisNo):
        try:
            self.data.update_insert("""
                                        delete SiparisUrunTB where UrunKartId=? and SiparisNo=?

                                    """,(urunKartId,gidenSiparisNo))
            print('SiparisUrunDeleteKalan Başarılı')
        except Exception as e:
            print('__setSiparisUrunDeleteKalan',str(e))
            return False
    
    
    def __setSiparisUrunInsert(self):
        
        try:
            for item in self.siparisUrunBilgileri:
                item['satisToplam'] = item['satisFiyati'] * item['miktar']
                self.data.update_insert("""
                                    insert into SiparisUrunTB(SiparisNo,
                                    TedarikciID,
                                    UrunKartID,
                                    UrunBirimID,
                                    Miktar,
                                    OzelMiktar,
                                    KasaAdet,
                                    SatisFiyati,
                                    SatisToplam,
                                    UretimAciklama,
                                    MusteriAciklama,
                                    AlisFiyati,
                                    AlisFiyati_TL,
                                    SiraNo,
                                    Ton,
                                    musteriID) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                    

                                
                                """,(self.siparisBilgileri['gidenSiparisNo'],item['tedarikciId'],item['urunKartId'],item['urunBirimId'],item['miktar'],
                                     item['ozelMiktar'],item['kasaAdet'],item['satisFiyati'],item['satisToplam'],item['uretimAciklama'],
                                     item['musteriAciklama'],item['alisFiyati'],item['alisFiyati_Tl'],item['siraNo'],item['ton'],self.siparisBilgileri['musteriId']
                                     
                                     
                                     ))

            
            
            print('Siparis Bölme ürün Kaydı Yapıldı')
            return True
        except Exception as e:
            print('Siparis Bölme Ürün Kaydı Yapılamadı',str(e))
            return False
    
    def __setSiparisUrunUpdate(self,kalanSiparisNo,miktar,satisToplam,kasaAdet,id):
        try:
            
            self.data.update_insert("""
                                    update SiparisUrunTB SET SiparisNo=?,Miktar=?,SatisToplam=?,KasaAdet=? where ID=?
                                
                                
                                """,(kalanSiparisNo,miktar,satisToplam,kasaAdet,id))
            print('Ürün Bölme Güncelleştirmesi Başarılı',str(e))
            return True
        except Exception as e:
            print('Urun Bölme Güncelleştirmesi Hata',str(e))
            return False
    
    
    def __setSiparisUrunDegismeyenUpdate(self,kalanSiparisNo,id):
        try:
            
            self.data.update_insert("""
                                    update SiparisUrunTB SET SiparisNo=? where ID=?
                                
                                
                                """,(kalanSiparisNo,id))
            print('Ürün Bölme Güncelleştirmesi Başarılı',str(e))
            return True
        except Exception as e:
            print('Urun Bölme Güncelleştirmesi Hata',str(e))
            return False
    
    
    
    def __setSiparisUrunDelete(self,id):
        try:
            self.data.update_insert("""
                                    
                                        delete from SiparisUrunTB where ID=?
                                    
                                    """,(id))
            print('Siparis Bölme Ürün Bilgisi Silindi')
            return True
        except Exception as e:
            print('Siparis Bölme Ürün Bilgisi Silme Hata',str(e))
            return False
        
    
    
    def __dateConvert(self,date_v):
        if (date_v) : 
            forMat = '%d-%m-%Y'
            date_v = datetime.datetime.strptime(date_v, forMat)
            return date_v.date()
        else:
            return None
    
    
    def __odemelerUpdate(self,siparisNo,pesinat,kalanSiparisNo):
        try:
            
            result = self.data.getStoreList("""
                                        select * from OdemelerTB where SiparisNo=?
                                   
                                   """,(siparisNo))
            
            
            if len(result)==1:
                pesinat = float(result[0][7]) - float(pesinat)
                self.data.update_insert("""
                                        update OdemelerTB SET Tutar=?,SiparisNo=? where ID=?
                                    
                                    
                                    """,(float(pesinat),kalanSiparisNo,result[0][0]))
            print('Odemeler Tablosu Güncellendi')
            return True
        except Exception as e:
            print('Odemeler Tablosu Güncelleme Hatası',str(e))
            return False
        
        
    def __odemelerInsert(self,gidenSiparisNo,pesinat,resultOdemeler):
        try:
            self.data.update_insert("""
                                
                                    insert into OdemelerTB(Tarih,MusteriID,SiparisNo,FinansOdemeTurID,Aciklama,Tutar,KullaniciID,Kur) VALUES(?,?,?,?,?,?,?,?)
                                
                                """,(resultOdemeler[0][1],
                                     int(resultOdemeler[0][2]),
                                     gidenSiparisNo,
                                     int(resultOdemeler[0][5]),
                                     resultOdemeler[0][6],
                                     float(pesinat),
                                     int(resultOdemeler[0][10]),
                                     float(resultOdemeler[0][12])))
            
            print('Odemeler Tablosuna Yeni Giriş Yapıldı')
            return True
        except Exception as e:
            print('Odemeler Insert Hata',str(e))
            return False
        
    def mailGonderUpdate(self,siparis,degisen,siparis_no):
        degismeyen = list()
        if len(degisen)==1:
            
            degismeyen = self.data.getStoreList("""
                                                select 

                                                    s.ID,
                                                    s.SiparisNo,
                                                    s.AlisFiyati,
                                                    s.SatisFiyati,
                                                    s.Miktar,
                                                    s.UretimAciklama,
                                                    s.MusteriAciklama,
                                                    ur.BirimAdi,
                                                    t.FirmaAdi


                                                from 
                                                    SiparisUrunTB s,
                                                    UrunBirimTB ur,
                                                    TedarikciTB t 
                                                where 
                                                    s.ID=? and 
                                                    s.UrunBirimID = ur.ID and 
                                                    s.TedarikciID = t.ID
                                            
                                            """,(degisen[0]['id']) )
        else:
            for i in range(0,len(degisen)):
                degismeyen.append( self.data.getStoreList("""
                                                select 

                                                    s.ID,
                                                    s.SiparisNo,
                                                    s.AlisFiyati,
                                                    s.SatisFiyati,
                                                    s.Miktar,
                                                    s.UretimAciklama,
                                                    s.MusteriAciklama,
                                                    ur.BirimAdi,
                                                    t.FirmaAdi


                                                from 
                                                    SiparisUrunTB s,
                                                    UrunBirimTB ur,
                                                    TedarikciTB t 
                                                where 
                                                    s.ID=? and 
                                                    s.UrunBirimID = ur.ID and 
                                                    s.TedarikciID = t.ID
                                            
                                """,(degisen[i]['id']) ))
        
        
        baslik =  siparis['kayit_kisi'] + " tarafından işlendi ."
        
        body = """
        <table >
            <tr style ="background-color: orange;">
                <th style ="color: white;background-color: orange;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Durum
                </th>
                <th style ="color: white;background-color: orange;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Sipariş Numarası
                </th>
                <th style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tedarikçi
                </th>
                <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Ürün Bilgisi 
                </th>
                 <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Üretim Açıklama 
                </th>
                 <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Miktarı
                </th>
                <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Alış Fiyatı
                </th>
                <th  style ="color: white;background-color: orange ;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Satış Fiyatı
                </th>
            </tr>
        """
        
                
            


        
        
        if siparis['siparisDurumId'] == 2:
            if len(degisen)==1:
                body += f"""
                        <tr style ="background-color: #ddd;">
                            <td style ="border: 1px solid #ddd;background-color:red;color:white;padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞTİRİLEN ↓↓↓
                                    
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][1]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][8]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][6]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                                {degismeyen[0][5]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][4]} {degismeyen[0][7]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[0][2]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {float(degismeyen[0][3])}
                            </td>
                        </tr>
                
                
                        """
            else:
                for i in range(0,len(degisen)):
                    body += f"""
                        <tr style ="background-color: #ddd;">
                            <td style ="border: 1px solid #ddd;background-color:red;color:white;padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞTİRİLEN ↓↓↓
                                    
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][1]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {degismeyen[i][0][8]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {degismeyen[i][0][6]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                            {degismeyen[i][0][5]}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {float(degismeyen[i][0][4])} {degismeyen[i][0][7]} 
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {float(degismeyen[i][0][2])}
                            </td>
                            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                            {float(degismeyen[i][0][3])}
                            </td>
                        </tr>
                
                
                        """
            sayac = 0
            for item in degisen:
                body += f"""
                    <tr style ="background-color: #ddd;">
                        <td style ="border: 1px solid #ddd;background-color:#2fc289;color:white; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                DEĞİŞEN
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:#ddd;">
                            {siparis_no}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['tedarikciAdi'],sayac,degismeyen,1)}">
                            {item['tedarikciAdi']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['musteriAciklama'],sayac,degismeyen,7)};">
                            {item['musteriAciklama']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;background-color:{self.__kontrol(item['uretimAciklama'],sayac,degismeyen,2)}">
                            {item['uretimAciklama']}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['miktar'],sayac,degismeyen,3)}">
                            {float(item['miktar'])} {item['urunbirimAdi']} 
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['alisFiyati'],sayac,degismeyen,5)}">
                            {float(item['alisFiyati'])}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;background-color:{self.__kontrol(item['satisFiyati'],sayac,degismeyen,6)}">
                            {float(item['satisFiyati'])}
                        </td>
                    </tr>
            
            
                """
                sayac += 1
                
            
            body = body + "</table>"
            mekmer = 0
            mekmoz = 0
            diger = 0
        
    
       
        
            for item in degisen:
               
                if item['tedarikciAdi'] == "Mekmer":
                    
                 mekmer +=1
                    
                if item['tedarikciAdi'] == "Mek-Moz":
                    
                    mekmoz +=1

                if item['tedarikciAdi'] != "Mek-Moz" and item['tedarikciAdi'] != "Mekmer":
                    
                    diger +=1    


            if  (mekmer >=1 ) and siparis['siparisDurumId'] == 2 :

              MailService(siparis_no +" Düzenlenen Kalemler ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
                
            elif (mekmoz>1) and siparis['siparisDurumId'] == 2:
                MailService(siparis_no +" Düzenlenen Kalemler ", "muhsin@mekmer.com"," "+ baslik + body) #muhsin
                


            if  (mekmoz + mekmer >=1) and siparis['siparisDurumId'] ==2 :
                 MailService(siparis_no +" Düzenlenen Kalemler ", "mehmet@mekmer.com",  " "+ baslik + body) #Mehmet
                 

            if  (diger >=1 ) and  siparis['siparisDurumId'] ==2:
                   MailService(siparis_no +" Düzenlenen Kalemler ", "info@mekmar.com",  " " +baslik + body) #gizem
                    
            sahibi , maili = self.__siparisDetayi(siparis_no)     
            if sahibi != 'Mehmet'  or sahibi != 'Gizem' : 
                  MailService(siparis_no +" Düzenlenen Kalemler ", maili  , " "+ baslik + body) #satıs temsilcisi(self,siparis,siparis_no):
      