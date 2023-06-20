from helpers import SqlConnect,MailService,DegisiklikMain


class FinansPesinatIslem:

    def __init__(self):

        self.data = SqlConnect().data 

    
    def pesinat_kaydet(self,_item):
        try:
            item = _item['pesinat_model']
            item['tarih'] = _item['tarih']
            
            self.data.update_insert(
               """
                insert into OdemelerTB (
                    Tarih,MusteriID,SiparisNo,FinansOdemeTurID,
                    Aciklama,Tutar,Masraf,Kur,KullaniciID
                )
                values
                (?,?,?,?,?,?,?,?,?)
                """,
               (
                    item['tarih'],item['musteri_id'],item['siparis_no'],
                    1,item['aciklama'],item['tutar'],item['masraf'],item['kur'],item['kullanici_id']
                )
            )

            self.__siparisKontrol(item)
        
            mail_konu = f""" 
            {item['musteri_adi']} {item['siparis_no']}  ${item['tutar']} / ${item['masraf']}       
            
            {_item['kullaniciadi']} tarafından işlendi . 
             """
           
            info =_item['kullaniciadi'].capitalize() + ', ' + item['siparis_no'] + ' $' + str(item['tutar']) + ' Peşinat Girişi Yaptı'
            yukleme_tarihi=""
            DegisiklikMain().setMaliyetDegisiklik(info,_item['kullaniciadi'].capitalize(),item['siparis_no'],yukleme_tarihi)
            MailService('Peşinat Tahsilat Bildirimi ',"huseyin@mekmarmarble.com",mail_konu)
            MailService('Peşinat Tahsilat Bildirimi ',"mehmet@mekmer.com",mail_konu)
          
            MailService('Peşinat Tahsilat Bildirimi  ',item['temsilci_mail'],mail_konu)
            if item['marketing'] == 'Mekmar' :
                MailService('Peşinat Tahsilat Bildirimi ',"info@mekmar.com",mail_konu)
            return True

        except Exception as e:
            print('PesinatIslem pesinat_kaydet Hata :',str(e))
            return False

    
    def __siparisKontrol(self,item):

        result = self.data.getStoreList(
            """
            select
            s.SiparisNo,
            m.FirmaAdi,
            s.MusteriID,
            Sum(s.Pesinat) as Pesinat,
            (Select Sum(o.Tutar) from OdemelerTB o where o.SiparisNo=s.SiparisNo) as Odenen,
             (Select Sum(o.Masraf) from OdemelerTB o where o.SiparisNo=s.SiparisNo) as Masraf,
			(select k.MailAdres from KullaniciTB k where s.SiparisSahibi = k.ID) as Mail,
			 m.Marketing
            from
            SiparislerTB s,MusterilerTB m
            where
            s.SiparisDurumID in (1,2)
            and s.Pesinat >0
            and m.ID = s.MusteriID
            and s.SiparisNo=?
            group by s.SiparisNo,s.MusteriID,m.FirmaAdi,s.SiparisSahibi, m.Marketing
            """,(item['siparis_no'])
        )[0]

        pesinat = float(result.Pesinat)
        odenen = float(result.Odenen)
       
        
        kalan = pesinat - odenen

        if kalan <=0:
            self.__siparisDurumGuncelle(item['siparis_no'])
           

    def __siparisDurumGuncelle(self,siparis_no):

        try:

            self.data.update_insert(

                """
                update SiparislerTB set SiparisDurumID=2 where SiparisNo=?
                """,(siparis_no)
            )
            
           
            self.mailGonderInsert(siparis_no)
            return True 

        except Exception as e:

            print('PesinatIslem __siparisDurumGuncelle Hata : ',str(e))
            return False
   
    def mailGonderInsert(self,siparis_no):

        result = self.data.getStoreList(
            """
            select 
            s.SiparisTarihi ,
		    s.SiparisDurumID,
            s.ID,
            s.SiparisNo,
            u.Miktar, 
            
            (select BirimAdi from UrunBirimTB t  where t.ID=u.UrunBirimID) as UrunBirimi,
            (select k.FirmaAdi from TedarikciTB k where k.ID=u.TedarikciID) as Tedarikci,
             u.UretimAciklama ,
            (select m.UrunAdi from UrunlerTB m where m.ID = n.UrunID) as urunadi,
            (select y.YuzeyIslemAdi from YuzeyKenarTB y where y.ID=n.YuzeyID) as yuzeyadi ,
            (select o.En  from OlculerTB o where o.ID=n.OlcuID) as En,
            (select o.Boy from OlculerTB o where o.ID=n.OlcuID) as Boy,
            (select o.Kenar  from OlculerTB o where o.ID=n.OlcuID) as Kenar,
		    (select p.KullaniciAdi  from KullaniciTB p where p.ID=s.SiparisSahibi) as SiparisSahibi
           
            from
            SiparisUrunTB u ,SiparislerTB s ,UrunKartTB n 
            
            where 
            s.SiparisNo= u.SiparisNo 
            and u.UrunKartID = n.ID
		    and (s.SiparisDurumID=2)
            and s.SiparisNo=?
            order by s.SiparisTarihi desc
            """,(siparis_no)
        )
        
        body = """
        <table >
            <tr style ="background-color: #f2f2f2;">
                <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                Sipariş Numarası
                </th>
                <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tedarikçi
                </th>
                <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Ürün Bilgisi 
                </th>
                 <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Üretim Açıklama 
                </th>
                 <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Ürün Miktarı
                </th>
                <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                 Sipariş Temsilcisi
                </th>
            </tr>
        """
         

        for item in result:
          
            body += f"""
           
            <tr style ="background-color: #ddd;">
                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                   {item.SiparisNo}
                </td>
                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                  {item.Tedarikci}
                </td>
                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                  {item.urunadi} {item.yuzeyadi} {item.En}x{item.Boy}x{item.Kenar}
                </td>
                 <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 150px;">
                  {item.UretimAciklama}
                </td>
                 <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                  {item.Miktar} {item.UrunBirimi} 
                </td>
                 <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                  {item.SiparisSahibi} 
                </td>
                
            </tr>
           
          
              """
         
        body = body + "</table>"
        mekmer = 0
        mekmoz = 0
        diger = 0
        
           
        
        for item in result:
            if item.Tedarikci == "Mekmer":
                
               mekmer +=1
                
            if item.Tedarikci == "Mek-Moz":
                
                mekmoz +=1

            if item.Tedarikci != "Mek-Moz" and item.Tedarikci != "Mekmer":
                
                diger +=1    

        if  (mekmer >=1 ) and item.SiparisDurumID ==2:

             MailService("Üretilecek Sipariş Bilgi Bildirimi", "muhsin@mekmer.com", body) #muhsin
            
        
            

        if  (mekmoz + mekmer >=1) and item.SiparisDurumID ==2:
              MailService("Üretilecek Sipariş Bilgi Bildirimi", "mehmet@mekmer.com", body) #Mehmet 
            
        if  (diger >=1 ) and item.SiparisDurumID ==2:
              MailService("Üretilecek Sipariş Bilgi Bildirimi", "info@mekmar.com", body) #gizem
                  