from helpers import MailService,SqlConnect,TarihIslemler
import datetime
from datetime import date

class MusteriEta:

    def __init__(self):

        self.data = SqlConnect().data

    
    def etaKontrol(self):

        tarihIslem = TarihIslemler()
        result = self.data.getList(
            """
            select
            s.ID,
            s.SiparisNo,
            m.FirmaAdi as MusteriAdi,
            (select k.MailAdres from KullaniciTB k where k.ID=s.SiparisSahibi ) as MailAdres,           
            (select k.KullaniciAdi from KullaniciTB k where k.ID=s.SiparisSahibi ) as Sorumlu,
            s.Eta,
            s.KonteynerNo,
            s.YuklemeTarihi,
            s.KonsimentoDurum
            from
            SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID
            and s.SiparisDurumID=3 and Takip=1
			and s.Eta is not null
            order by s.ID desc
            """
        )

        
        body = ""        
        subject = "ETA Yaklaşan Konteyner Bildirimi"
        for item in result:
            eta = tarihIslem.getDate(item.Eta).strftime("%d-%m-%Y")
            bugun = datetime.date.today()
            sontarih_str = eta.split('-')
            
            sontarih = datetime.date(int(sontarih_str[2]),int(sontarih_str[1]),int(sontarih_str[0]))
            kalan_sure = (sontarih - bugun).days
           
            if kalan_sure ==10  or kalan_sure ==5 or kalan_sure ==1 :
               
                body = f"""
                        <ul>
                            <li> {item.MusteriAdi} / {item.SiparisNo} / {eta} </li>
                        </ul>
                       """
                if self.__mailKontrol(item.Sorumlu,item.SiparisNo,bugun) == True:
                    MailService(subject,item.MailAdres,body)
                    MailService(subject,"huseyin@mekmarmarble.com",body)


        self.etaBosKontrol()

    def etaBosKontrol(self):

        tarihIslem = TarihIslemler()
        result = self.data.getList(
            """
            select
            s.ID,
            s.SiparisNo,
            m.FirmaAdi as MusteriAdi,
            (select k.MailAdres from KullaniciTB k where k.ID=s.SiparisSahibi ) as MailAdres,           
            (select k.KullaniciAdi from KullaniciTB k where k.ID=s.SiparisSahibi ) as Sorumlu,
            s.Eta,
            s.KonteynerNo,
            s.YuklemeTarihi,
            s.KonsimentoDurum
            from
            SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID
            and s.SiparisDurumID=3 and Takip=1
			and s.Eta is null
            order by s.ID desc
            """
        )

        
        body = ""        
        subject = "ETA Girilmeyen Konteyner Bildirimi"
        for item in result:
            yuklemeTarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")
            bugun = datetime.date.today()
            sontarih_str = yuklemeTarihi.split('-')
            print(sontarih_str[2])
            sontarih = datetime.date(int(sontarih_str[2]),int(sontarih_str[1]),int(sontarih_str[0]))
            kalan_sure = (bugun - sontarih).days

            if kalan_sure <=3 :
                
                body = f"""
                        <ul>
                            <li> {item.MusteriAdi} / {item.SiparisNo}  </li>
                        </ul>
                       """
                if self.__mailBosEtaKontrol(item.Sorumlu,item.SiparisNo,bugun) == True:
                    MailService(subject,item.MailAdres,body)
                 
                    MailService(subject,"huseyin@mekmarmarble.com",body)
                   


    def __mailKontrol(self,kullaniciadi,siparisno,tarih):

        bugun = datetime.date.today()
        durum = self.data.getStoreList(
            """
            select count(*) as durum from MusteriEtaTakipTB where 
            KullaniciAdi=? and SiparisNo=? and Tarih=?
            """,
            (kullaniciadi,siparisno,bugun)
        )[0].durum

        if durum > 0:
            return False 
        else:
            #daha önce kayıt varsa silinmesi
            self.data.update_insert(
                """
                delete from MusteriEtaTakipTB where SiparisNo=?
                """,
                (siparisno)
            )
            self.data.update_insert(
                """
                insert into MusteriEtaTakipTB (KullaniciAdi,Tarih,SiparisNo)
                values
                (?,?,?) 
                """,
                (kullaniciadi,tarih,siparisno)
            )

            return True

    def __mailBosEtaKontrol(self,kullaniciadi,siparisno,tarih):

        bugun = datetime.date.today()
        durum = self.data.getStoreList(
            """
            select count(*) as durum from MusteriEtaBosTakipTB where 
            KullaniciAdi=? and SiparisNo=? and Tarih=?
            """,
            (kullaniciadi,siparisno,bugun)
        )[0].durum

        if durum > 0:
            return False 
        else:
            #daha önce kayıt varsa silinmesi
            self.data.update_insert(
                """
                delete from MusteriEtaBosTakipTB where SiparisNo=?
                """,
                (siparisno)
            )
            self.data.update_insert(
                """
                insert into MusteriEtaBosTakipTB (KullaniciAdi,Tarih,SiparisNo)
                values
                (?,?,?) 
                """,
                (kullaniciadi,tarih,siparisno)
            )

            return True

    def finansBolmeKontrol(self):
        try:
            resultSiparisler = self.data.getList("""
                                                    select SiparisNo,Pesinat,MusteriID from SiparislerTB s where s.Pesinat > 0 and YEAR(s.SiparisTarihi) >=2021 and s.SiparisDurumID in (2,3)

                                                 """)
            for item in resultSiparisler:
                
                if self.finansOdemelerKontrol(item[0]) == False:
                    if self.pesinatMailGonderildiMi(item[0]) == 0:
                        
                        MailService('' +"Ödemeler Tablosu Kontrol Edilmeli!", "bilgiislem@mekmar.com"," "+ 'Peşinat Girildi.' + " "+f'{item[0]} Siparişi için ödemeler tablosunu kontrol et')
                        MailService('' +"Ödemeler Tablosu Kontrol Edilmeli!", "info@mekmar.com"," "+ 'Peşinat Girildi.' + " "+f'{item[0]} Siparişi için ödemeler tablosunu kontrol et')
                        MailService('' +"Ödemeler Tablosu Kontrol Edilmeli!", "huseyin@mekmer.com"," "+ 'Peşinat Girildi.' + " "+f'{item[0]} Siparişi için ödemeler tablosunu kontrol et')
                        self.pesinatMailGonderildiMiUpdate(item[0])
                        
            return True
            
        except Exception as e:
            print('__odemelerKontrolMail : Hata : ', str(e))
            return False
        
        
        
        
        #MailService('' +" Düzenlenen Kalemler ", "bilgiislem@mekmar.com"," "+ 'baslik' + 'body')
        
    def finansOdemelerKontrol(self,siparisNo):
        result = self.data.getStoreList("""
                                            select * from OdemelerTB where SiparisNo=? and YEAR(Tarih) >=2021
                                        
                                        
                                        """,(siparisNo))
        if len(result) == 0:
            return False
        else:
            return True

    def pesinatMailGonderildiMi(self,siparisNo):
        result = self.data.getStoreList("""
                                            select PesinatKontrol from SiparislerTB where SiparisNo=?
                                        """,(siparisNo))
        
        if result[0][0] == None:
            return 0
        else:
            return result[0][0]
    
    def pesinatMailGonderildiMiUpdate(self,siparisNo):
        self.data.update_insert("""
                                    update SiparislerTB SET PesinatKontrol = 1 where SiparisNo = ?
                                
                                """,(siparisNo))


    def getEtaControl(self):
        try:
            result = self.data.getList("""
                                        select
            s.ID,
            s.SiparisNo,
            m.FirmaAdi as MusteriAdi,
            (select k.ID from KullaniciTB k where k.ID=s.Operasyon ) as Operasyon,           
            (select k.ID from KullaniciTB k where k.ID=s.SiparisSahibi ) as SiparisSahibi,
            s.Eta,
            s.KonteynerNo,
            s.YuklemeTarihi,
            s.KonsimentoDurum,
			s.EtaYaklasanSureOn,
			s.EtaYaklasanSureBes,
			s.EtaYaklasanSureBir,
			s.EtaUlasti,
			(select sum(su.SatisToplam) from SiparisUrunTB su where su.SiparisNo = s.SiparisNo) as SatisToplam
            from
            SiparislerTB s,MusterilerTB m
            where s.MusteriID=m.ID
            and s.SiparisDurumID=3 and s.Takip=1
			and s.Eta is not null
            order by s.ID desc

                                       """)
            day,month,year = self.getToday()
            if len(result)>0:
                for item in result:
                    eta = str(item.Eta)
                    eta = eta.split("-")
                    etaYear = int(eta[0])
                    etaMonth = int(eta[1])
                    etaDay = int(eta[2])
                    eta1 = date(etaYear,etaMonth,etaDay)
                    eta2 = date(year,month,day)
                    if (eta1 - eta2).days == 12:
                        if item.EtaYaklasanSureOn != True:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                if(kalanOdeme >0):
                                    self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            else:
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                                self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                                
                            self.sendMailEta(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerBilgisi,odemelerTop)
                            self.data.update_insert("""
                                                    update SiparislerTB SET EtaYaklasanSureOn = 1 where SiparisNo=?
                                                
                                                """,(item.SiparisNo))
                    elif (eta1 - eta2).days == 6:
                        if item.EtaYaklasanSureBes != True:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                if(kalanOdeme >0):
                                    self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            else:
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                                self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            self.sendMailEta(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'6',item.SatisToplam,kalanOdeme,odemelerBilgisi,odemelerTop)
                            self.data.update_insert("""
                                                    update SiparislerTB SET EtaYaklasanSureBes = 1 where SiparisNo=?
                                                """,(item.SiparisNo))
                    elif (eta1 - eta2).days == 3:
                        if item.EtaYaklasanSureBir != True:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                if(kalanOdeme >0):
                                    self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            else:
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                                self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            self.sendMailEta(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'3',item.SatisToplam,kalanOdeme,odemelerBilgisi,odemelerTop)
                            self.data.update_insert("""
                                                    update SiparislerTB SET EtaYaklasanSureBir = 1 where SiparisNo=?
                                                """,(item.SiparisNo))
                    elif (eta1 - eta2).days == 0:
                        if item.EtaUlasti != True:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                if(kalanOdeme >0):
                                    self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            else:
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                                self.sendMailEtaSpecial(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'12',item.SatisToplam,kalanOdeme,odemelerTop)
                            self.sendMailEta(item.SiparisNo,item.SiparisSahibi,item.Operasyon,item.Eta,'Eta Başarıyla Ulaştı',item.SatisToplam,kalanOdeme,odemelerBilgisi,odemelerTop)
                            self.data.update_insert("""
                                                    update SiparislerTB SET EtaUlasti = 1 where SiparisNo=?
                                                """,(item.SiparisNo))


                    else:
                        pass
            else:
                pass
            
            
        except Exception as e:
            print("getEtaControl Hata",str(e))
            return False
        
    def sendMailEtaSpecial(self,siparisno,siparisSahibi,operasyon,eta,etaKalanSure,satisToplam,kalanOdeme,odemelerTop):
        try:
            siparisSahibiName = self.data.getStoreList("""
                                                            select KullaniciAdi from KullaniciTB where ID=?
                                                       
                                                       """,(siparisSahibi))
            operasyonName = self.data.getStoreList("""
                                                            select KullaniciAdi from KullaniciTB where ID=?
                                                       
                                                       """,(operasyon))
            


            body = """
                <table >
                <tr style ="background-color: #f2f2f2;">
                    <th style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                    Sipariş Numarası
                    </th>
                    <th style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                    Sipariş Sahibi
                    </th>
                    <th  style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                    Operasyon
                    </th>
                    <th  style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                    Eta Tarihi
                    </th>
                    <th  style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                    Eta Kalan Süresi
                    </th>
                    <th  style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Sipariş Toplam Bedeli
                    </th>
                    <th  style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Yapılan Ödeme
                    </th>
                    <th  style ="color: white;background-color: #00b4ff;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Kalan Ödeme
                    </th>
                    
                </tr>
                """
                    
            body += f"""
                        <tr style ="background-color: #ddd;">
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {siparisno}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {siparisSahibiName[0].KullaniciAdi}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {operasyonName[0].KullaniciAdi}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                        {eta}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {etaKalanSure}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        $ {satisToplam}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        $ {odemelerTop}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;color:red;">
                        
                        $ {kalanOdeme}
                        </td>

                    </tr>
                    """
            
            
            
            body += "</table>"
            
            baslik = "Acil! Yaklaşan Eta Özel Maili"
            
            MailService(baslik,'mehmet@mekmer.com',body)
            
                
            return True
        except Exception as e:
            print("sendMailEta Hata",str(e))
            return False
        
    def getToday(self):
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year
        return day,month,year
    
    def sendMailEta(self,siparisno,siparisSahibi,operasyon,eta,etaKalanSure,satisToplam,kalanOdeme,odemelerBilgisi,odemelerTop):
        try:
            siparisSahibiMail = self.data.getStoreList("""
                                                select MailAdres as SiparisSahibi from KullaniciTB where ID=?
                                        
                                            """,(siparisSahibi))
            operasyonMail = self.data.getStoreList("""
                                                select MailAdres as SiparisSahibi from KullaniciTB where ID=?
                                        
                                            """,(operasyon))
            siparisSahibiName = self.data.getStoreList("""
                                                            select KullaniciAdi from KullaniciTB where ID=?
                                                       
                                                       """,(siparisSahibi))
            operasyonName = self.data.getStoreList("""
                                                            select KullaniciAdi from KullaniciTB where ID=?
                                                       
                                                       """,(operasyon))
            
            if len(odemelerBilgisi) >0:
                body = """
                    <table >
                    <tr style ="background-color: #f2f2f2;">
                        <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                        Sipariş Numarası
                        </th>
                        <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Sipariş Sahibi
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Operasyon
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Eta Tarihi
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Eta Kalan Süresi
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Sipariş Toplam Bedeli
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Sipariş Ödeme Bilgisi
                        </th>
                        
                        
                    </tr>
                    """
                    
                body += f"""
                        <tr style ="background-color: #ddd;">
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {siparisno}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {siparisSahibiName[0].KullaniciAdi}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {operasyonName[0].KullaniciAdi}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                        {eta}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {etaKalanSure}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {odemelerBilgisi}
                        </td>
                        

                    </tr>
                    """
            
            else:
                
                body = """
                    <table >
                    <tr style ="background-color: #f2f2f2;">
                        <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                        Sipariş Numarası
                        </th>
                        <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Sipariş Sahibi
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Operasyon
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Eta Tarihi
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                        Eta Kalan Süresi
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Sipariş Toplam Bedeli
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Yapılan Ödeme
                        </th>
                        <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Kalan Ödeme
                        </th>
                        
                    </tr>
                    """
                    
                body += f"""
                        <tr style ="background-color: #ddd;">
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {siparisno}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {siparisSahibiName[0].KullaniciAdi}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {operasyonName[0].KullaniciAdi}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                        {eta}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        {etaKalanSure}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        $ {satisToplam}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        $ {odemelerTop}
                        </td>
                        <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                        
                        $ {kalanOdeme}
                        </td>

                    </tr>
                    """
            
            
            
            body += "</table>"
            if( siparisSahibiMail[0].SiparisSahibi == operasyonMail[0].SiparisSahibi):
                MailService(siparisno + "Po'ya Ait Eta Yaklaşan Süre",siparisSahibiMail[0].SiparisSahibi,body)
                MailService(siparisno + "Po'ya Ait Eta Yaklaşan Süre",siparisSahibiMail[0].SiparisSahibi,body)
            else:
                MailService(siparisno + "Po'ya Ait Eta Yaklaşan Süre",siparisSahibiMail[0].SiparisSahibi,body)
                MailService(siparisno + "Po'ya Ait Eta Yaklaşan Süre",siparisSahibiMail[0].SiparisSahibi,body)
                MailService(siparisno + "Po'ya Ait Eta Yaklaşan Süre",operasyonMail[0].SiparisSahibi,body)
                
            return True
        except Exception as e:
            print("sendMailEta Hata",str(e))
            return False
    
    def getOdemeler(self,siparisno):
        try:
            odemeler = self.data.getStoreList("""
                                                 select Tutar from OdemelerTB where SiparisNo=?
                                              
                                             """,(siparisno))
            odemelerToplam = 0
            if len(odemeler)>0:
                
                for item in odemeler:
                    odemelerToplam += item.Tutar
                return odemelerToplam,True
            else:
                return odemelerToplam,False
        except Exception as e:
            print("Eta Bilgilendirme Odemeleri Hata",str(e))
            return False 


    def getEtaControlNotification(self):
        try:
            result = self.data.getList("""
                                        select
                                            s.ID,
                                            s.SiparisNo,
                                            m.FirmaAdi as MusteriAdi,
                                            (select k.ID from KullaniciTB k where k.ID=s.Operasyon ) as Operasyon,           
                                            (select k.ID from KullaniciTB k where k.ID=s.SiparisSahibi ) as SiparisSahibi,
                                            (select k.KullaniciAdi from KullaniciTB k where k.ID=s.Operasyon ) as OperasyonAdi,           
                                            (select k.KullaniciAdi from KullaniciTB k where k.ID=s.SiparisSahibi ) as SiparisSahibiAdi,
                                            s.Eta,
                                            s.KonteynerNo,
                                            s.YuklemeTarihi,
                                            s.KonsimentoDurum,
                                            s.EtaYaklasanSureOn,
                                            s.EtaYaklasanSureBes,
                                            s.EtaYaklasanSureBir,
                                            s.EtaUlasti,
                                            (select sum(su.SatisToplam) from SiparisUrunTB su where su.SiparisNo = s.SiparisNo) as SatisToplam,
                                            s.EtaHControlOn,
                                            s.EtaHControlBes,
                                            s.EtaHControlBir,
                                            s.EtaHControlUlasti

                                            from
                                            SiparislerTB s,MusterilerTB m
                                            where s.MusteriID=m.ID
                                            and s.SiparisDurumID=3 and s.Takip=1
                                            and s.Eta is not null 
                                            order by s.ID desc

                                       """)
            day,month,year = self.getToday()
            liste = list()
            
            if len(result)>0:
                for item in result:
                    eta = str(item.Eta)
                    eta = eta.split("-")
                    etaYear = int(eta[0])
                    etaMonth = int(eta[1])
                    etaDay = int(eta[2])
                    eta1 = date(etaYear,etaMonth,etaDay)
                    eta2 = date(year,month,day)
                    if (eta1 - eta2).days == 12:
                        if(item.EtaHControlOn == True):
                            continue
                        else:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                odemelerBilgisi = "Ödemesi Gelmiştir."
                                
                            else:
                                kalanOdeme = item.SatisToplam
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                            data = {
                                    'po':item.SiparisNo,
                                    'musteri':item.MusteriAdi,
                                    'operasyon':item.OperasyonAdi,
                                    'siparisci':item.SiparisSahibiAdi,
                                    'etaSure':(eta1 - eta2).days,
                                    'yuklemeTarihi':item.YuklemeTarihi,
                                    'etaTarihi':item.Eta,
                                    'satisBedel':item.SatisToplam,
                                    'odenen':odemelerTop,
                                    'kalan':kalanOdeme,
                                    'odemelerBilgisi':odemelerBilgisi
                                   }
                            liste.append(data)
                        
                    elif (eta1 - eta2).days == 6:
                        if(item.EtaHControlBes == True):
                            continue
                        else:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                odemelerBilgisi = "Ödemesi Gelmiştir."
                                
                            else:
                                kalanOdeme = item.SatisToplam
                                
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                            data = {
                                'po':item.SiparisNo,
                                'musteri':item.MusteriAdi,
                                'operasyon':item.OperasyonAdi,
                                'siparisci':item.SiparisSahibiAdi,
                                'etaSure':(eta1 - eta2).days,
                                'yuklemeTarihi':item.YuklemeTarihi,
                                'etaTarihi':item.Eta,
                                'satisBedel':item.SatisToplam,
                                'odenen':odemelerTop,
                                'kalan':kalanOdeme,
                                'odemelerBilgisi':odemelerBilgisi
                            }
                            liste.append(data)
                    elif (eta1 - eta2).days == 3:
                        if(item.EtaHControlBir == True):
                            continue
                        else:
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                odemelerBilgisi = "Ödemesi Gelmiştir."
                                
                            else:
                                kalanOdeme = item.SatisToplam
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                            data = {
                                'po':item.SiparisNo,
                                'musteri':item.MusteriAdi,
                                'operasyon':item.OperasyonAdi,
                                'siparisci':item.SiparisSahibiAdi,
                                'etaSure':(eta1 - eta2).days,
                                'yuklemeTarihi':item.YuklemeTarihi,
                                'etaTarihi':item.Eta,
                                'satisBedel':item.SatisToplam,
                                'odenen':odemelerTop,
                                'kalan':kalanOdeme,
                                'odemelerBilgisi':odemelerBilgisi
                            }
                            liste.append(data)
                    elif (eta1 - eta2).days == 0:
                        if(item.EtaHControlUlasti == True):
                            odemelerTop,isOdemeler = self.getOdemeler(item.SiparisNo)
                            kalanOdeme = 0
                            odemelerBilgisi = ""
                            if isOdemeler:
                                kalanOdeme = item.SatisToplam - odemelerTop
                                odemelerBilgisi = "Ödemesi Gelmiştir."
                                
                            else:
                                kalanOdeme = item.SatisToplam
                                
                                odemelerBilgisi = "Henüz ödenmiş bedel bulunmamaktadır."
                            data = {
                                'po':item.SiparisNo,
                                'musteri':item.MusteriAdi,
                                'operasyon':item.OperasyonAdi,
                                'siparisci':item.SiparisSahibiAdi,
                                'etaSure':(eta1 - eta2).days,
                                'yuklemeTarihi':item.YuklemeTarihi,
                                'etaTarihi':item.Eta,
                                'satisBedel':item.SatisToplam,
                                'odenen':odemelerTop,
                                'kalan':kalanOdeme,
                                'odemelerBilgisi':odemelerBilgisi
                            }
                            liste.append(data)
                    
                    else:
                        pass
            else:
                pass
            return liste

        except Exception as e:
            print('getEtaControlNotification hata',str(e))
            return False
    def setEtaControlNotificationStatus(self,po,etaSure):
        if(etaSure == '12'):
            self.data.update_insert("""
                                        update SiparislerTB SET EtaHControlOn = 1 where SiparisNo=?
                                    
                                    """,(po))
        elif(etaSure == '6'):
            self.data.update_insert("""
                                        update SiparislerTB SET EtaHControlBes = 1 where SiparisNo=?
                                    
                                    """,(po))
        elif(etaSure == '3'):
            self.data.update_insert("""
                                        update SiparislerTB SET EtaHControlBir = 1 where SiparisNo=?
                                    
                                    """,(po))
        elif(etaSure == '0'):
            self.data.update_insert("""
                                        update SiparislerTB SET EtaHControlUlasti = 1 where SiparisNo=?
                                    
                                    """,(po))
        return True     


    
class EtaTarihiYaklasan:
    def __init__(self):
        self.data = SqlConnect().data
        
      

      

     
       


