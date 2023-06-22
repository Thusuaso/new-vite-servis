from helpers import SqlConnect,DegisiklikMain
from helpers.mail_service import MailService

class SevkiyatKayit:

    def __init__(self):

        self.data = SqlConnect().data

    
    def siparisKayitIslemi(self,item):
        islem_durum = False

        islem_durum = self.__siparisGuncelle(item)
        """
        if self.__siparisMusteri(item) == 37 or self.__siparisMusteri(item) ==273 or self.__siparisMusteri(item) ==169:
           self.__siparisTarihGuncelle(item)
        """
        if islem_durum == False:
            self.__iptal_siparisGuncelle(item['siparisno'])
        else:
            siparis_item = {

                'sevk_tarihi' : item['sevk_tarihi'],
                'musteriid' : item['musteriid'],
                'siparisno' : item['siparisno']

            }
            for kasa_item in item['kasalistesi']:
              islem_durum =  self.__sevkKasaKaydetme(siparis_item,kasa_item)
              if islem_durum == False:
                  self.__iptal_siparisGuncelle(item['siparisno'])
                  self.__iptal_sevkKasaKaydetme(item['siparisno'])
                  return islem_durum
            
            for kasa_item in item['kasalistesi']:
                islem_durum = self.__uretimKasaGuncelleme(kasa_item['kasano'])

                if islem_durum == False:
                    self.__iptal_sevkKasaKaydetme(item['siparisno'])
                    self.__iptal_siparisGuncelle(item['siparisno'])
                    for iptal_item in item['kasalistesi']:
                        self.__iptal_uretimKasaGuncelleme(iptal_item['kasano'])
                    return islem_durum
            toplamKasaM2 = 0
            
            body = f"""
                    <h3>Sevk Eden : </h3><span>{item['sevkEden']}</span>
                    <h3>Sipariş No : </h3> <span>{item['siparisno']}</span>
                    <h3>Sevk Tarihi : </h3> <span>{siparis_item['sevk_tarihi']}</span>
                    <h3>Fatura No : </h3> <span>{item['faturano']}</span>
                    
                    <table >

                        <tr style ="background-color: #f2f2f2;">
                            <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 50px;">
                            Kasa No
                            </th>
                            <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Ürün Renk
                            </th>
                            <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Ürün Yüzey İşlem
                            </th>
                            <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                            Ürün Ebat
                            </th>
                            <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Ürün Birim
                            </th>
                            <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Ürün Miktarı
                            </th>
                            <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                            Ürün Satış Fiyatı
                            </th>
                        </tr>
                    """
            
            
            for kasa_item in item['kasalistesi']:
                toplamKasaM2 += float(kasa_item['miktar'])
                body += f"""                         
                            <tr style ="background-color: #ddd;">
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['kasano']}
                                </td>
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['urunadi']}
                                </td>
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['yuzeyislem']}
                                </td>
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['ebat']}
                                </td>
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['birimadi']}
                                </td>
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['miktar']}
                                </td>
                                <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {kasa_item['birimfiyat']}
                                </td>
                            </tr>
                         """
                   
                         
            body += f"""
                        <tr style ="background-color: #FFE438;">
                            <td style ="border: 1px solid#f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                    Toplam
                                </td>
                                <td style ="border: 1px solid #f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                    {len(item['kasalistesi'])}
                                </td>
                                <td style ="border: 1px solid #f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                </td>
                                <td style ="border: 1px solid #f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                </td>
                                <td style ="border: 1px solid #f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                </td>
                                <td style ="border: 1px solid #f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                {round(toplamKasaM2,2)}
                                </td>
                                <td style ="border: 1px solid #f5756c; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
                                </td>
                        
                        </tr>
                 
                     """             
            body = body + "</table>"
            
            
            MailService('Sevkiyat Bilgi','bilgiislem@mekmar.com',body)
            MailService('Sevkiyat Bilgi','info@mekmar.com',body)
            MailService('Sevkiyat Bilgi','muhsin@mekmer.com',body)
            item['sevkEden'] = item['sevkEden'].capitalize()
            info = item['sevkEden'] + ', ' + item['siparisno'] + ' Siparişini Sevk Etti'
            DegisiklikMain().setYapilanDegisiklikBilgisi(item['sevkEden'],info)
            
            return islem_durum

                

    def __siparisGuncelle(self,item):
        try:
        
            self.data.update_insert(
                """
                update SiparislerTB set YuklemeTarihi=?,
                SiparisFaturaNo=?,Takip=?,HizliSevk=?,
                NormalSevk=?,Hatirlatma_Sure=?,SiparisDurumID=3, 
                Eta=NULL where SiparisNo=?
                """,
                (
                    item['sevk_tarihi'],item['faturano'],item['takip'],
                    item['hizli_sevk'],item['normal_sevk'],item['hatirlatma_sure'],
                    item['siparisno']
                )
            )

            return True 
        except Exception as e:
            print('Sevkiyat İşlem Hata Sipariş Güncelleme : ', str(e))
            return False
    def __siparisTarihGuncelle(self,item):

        try:
            self.data.update_insert(
                """
                update SiparislerTB set YuklemeTarihi=?,SiparisTarihi=? where SiparisNo=?
                """,
                (
                    item['sevk_tarihi'],
                    item['sevk_tarihi'],
                    item['siparisno']
                )
            )

            return True 
        except Exception as e:
            print('Sevkiyat İşlem Hata Tarih Güncelleme : ', str(e))
            return False

    def __siparisMusteri(self,item):
        musteriID=self.data.getStoreList(
            """" 
                select MusteriID from SiparislerTB where SiparisNo=?
            """,(item['siparisno'])
        )
        return musteriID[0]

    def __dateChange(self,date):
        date = date.split('-')
        year = date[2]
        month = date[1]
        day = date[0]
        return year + '-' + month + '-' + day

    def __iptal_siparisGuncelle(self,siparisno):

        self.data.update_insert(
            """
            update SiparislerTB set YuklemeTarihi=NULL,
            SiparisFaturaNo='',Takip=0,HizliSevk=0,
            NormalSevk=0,Hatirlatma_Sure=0 where SiparisNo=?
            """,
            (siparisno)
        )


    def __sevkKasaKaydetme(self,siparis_item,kasa_item):

        try:
            self.data.update_insert(
                """
                insert into SevkiyatTB (
                    Tarih,KasaNo,MusteriID,BirimFiyat,
                    Toplam,CikisNo,RaporDurum,KullaniciID
                )
                values
                (
                    ?,?,?,?,?,?,?,?
                )
                """,
                (
                    siparis_item['sevk_tarihi'],kasa_item['kasano'],
                    siparis_item['musteriid'],kasa_item['birimfiyat'],
                    kasa_item['toplam'],siparis_item['siparisno'],1,7
                )
            )

            return True
        except Exception as e:
            print('Sevkiyat İşlem Sevkiyat Kasa Kaydı Hata : ', str(e))
            return False

    def __iptal_sevkKasaKaydetme(self,siparisno):
        self.data.update_insert(
            """
            delete from SevkiyatTB where CikisNo=?
            """,
            (siparisno)
        )
    
    def __uretimKasaGuncelleme(self,kasano):

        try:
            self.data.update_insert(
                """
                update UretimTB set UrunDurumID=0 where KasaNo=?
                """,
                (kasano)
            )
            return True 

        except Exception as e:
            print("Sevkiyat İşlem Uretim Kasa Güncelleme Hata : ",str(e))

            return False

    def __iptal_uretimKasaGuncelleme(self,kasano):

        try:
            self.data.update_insert(
                """
                update UretimTB set UrunDurumID=1 where KasaNo=?
                """,
                (kasano)
            )
            return True 

        except Exception as e:
            print("Sevkiyat İşlem Uretim Kasa Güncelleme Hata : ",str(e))

            return False

