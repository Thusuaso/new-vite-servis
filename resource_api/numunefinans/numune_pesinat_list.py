from helpers import SqlConnect,TarihIslemler,MailService,DegisiklikMain
from models.numuneler.numune_tahsilat import *


class TahsilatIslem:

    def __init__(self): 

        self.data = SqlConnect().data
        self.musteriadi = ""


    def getTahsilatList(self,musteriid,siparisNo):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            Select
            o.ID,
            o.NumuneNo,
            o.Tarih,
            o.Tutar,
            o.Masraf,
            m.MusteriAdi as FirmaAdi,
            o.MusteriID,
            o.Aciklama, 
            o.Banka
            from NumuneOdemelerTB o,YeniTeklif_MusterilerTB m
            where
            m.ID = o.MusteriID and 
            o.NumuneNo=? and o.MusteriID=?
            """,(siparisNo,musteriid)
        )

        liste = list()

        self.musteriadi = self.data.getStoreList(
            """
           Select MusteriAdi  as FirmaAdi  from YeniTeklif_MusterilerTB
            where ID=?
            """,(musteriid)
        )[0].FirmaAdi

        for item in result:

            model = NumuneTahsilatModel()
            model.id = item.ID
            model.siparisno = item.NumuneNo
            model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            model.tutar = item.Tutar
            model.masraf = item.Masraf
            model.musteriadi = item.FirmaAdi
            model.musteri_id = item.MusteriID
            model.aciklama = item.Aciklama
            model.banka = item.Banka
           
            liste.append(model)

        schema = NumuneTahsilatSchema(many=True)

        return schema.dump(liste)

    def getTahsilatModel(self,musteriid,siparisNo):

        model = NumuneTahsilatModel()
        model.siparisno = siparisNo
        model.musteri_id = musteriid
        model.musteriadi = self.musteriadi

        schema = NumuneTahsilatSchema()

        return schema.dump(model)

    def tahsilatKaydet(self,item):
       
        try:
            self.data.update_insert(
                """
                    insert into NumuneOdemelerTB (
                        Tarih,MusteriID,NumuneNo,
                        Tutar,Kullanici,Banka
                        )
                    values
                    (?,?,?,?,?,?)
                """,
                (
                    item['tarih'],item['musteri_id'],item['siparisno'],item['tutar'],item['kullaniciid'],item['banka']
                )
            )
            self.mailGonder(item['siparisno'],'Yeni Numune Tahsilat Girişi',item['tutar'],item['tarih'],item['kullaniciadi'])
            info = item['kullaniciadi'] + ',' + item['siparisno'] + ' Numunesi Için Tahsilat Girdi.'
            DegisiklikMain().setYapilanDegisiklikBilgisi(item['kullaniciadi'],info)
            return True
        except Exception as e:
            print('Numune Kaydet Hata : ',str(e))
            return False

    def tahsilatGuncelle(self,item):
        try:
            kullaniciid = self.data.getStoreList(
                """
                Select ID from KullaniciTB
                where KullaniciAdi=?
                """,(item['kullaniciadi'])
            )[0].ID

            self.data.update_insert(

                """
                update NumuneOdemelerTB set Tarih=?,Tutar=?,
                Kullanici =?,Banka=?
                where ID=?
                """,(
                    item['tarih'],item['tutar']
                ,kullaniciid,item['banka'],item['id']
                )
            )
 
         
            self.mailGonder(item['siparisno'],'Numune Tahsilat Değiştirme',item['tutar'],item['tarih'],item['kullaniciadi'])
            item['kullaniciadi'] = item['kullaniciadi'].capitalize()
            info = item['kullaniciadi'] + ',' + item['siparisno'] + ' Numunesi Için Tahsilatı Güncelledi.'
            DegisiklikMain().setYapilanDegisiklikBilgisi(item['kullaniciadi'],info)
            return True
        except Exception as e:
            print('Numune Güncelleme Hata : ',str(e))
            return False

    def tahsilatSilme(self,id):
       
        try:
            result = self.data.getStoreList(

                """
                select * from NumuneOdemelerTB where ID=?
                """,(id)
            )
            self.data.update_insert(
                """
                delete from NumuneOdemelerTB where ID=?
                """,(id)
            )
            for item in result:
                
            
               self.mailGonder(item.NumuneNo,' Numune Tahsilat Silme İşlemi',item.Tutar , item.Kullanici)
            return True
        except Exception as e:
            print('Numune Silme Hata : ',str(e))
            return False

   
    def mailGonder(self,siparis_no,islem_aciklamasi,tutar,tarih,kullanici):

        result = self.data.getStoreList(
            """
            select 
            k.MailAdres,
			m.MusteriAdi
            from 
            NumunelerTB s,KullaniciTB k,YeniTeklif_MusterilerTB m
            where  s.NumuneNo=?
            and  k.ID=s.NumuneTemsilci
			and m.ID=s.MusteriID
            """,(siparis_no)
        )[0]

        ilgili_mail_adres = result.MailAdres

        musteri_adi = result.MusteriAdi

        mail_konu = f""" 
        {musteri_adi}  - {siparis_no} - {tarih}  -  ${tutar}  
        
        {kullanici} tarafından işlendi.
        
        """

        MailService(islem_aciklamasi,"huseyin@mekmarmarble.com",mail_konu)
        # MailService(islem_aciklamasi,"mehmet@mekmer.com",mail_konu)
       
        MailService(islem_aciklamasi,ilgili_mail_adres,mail_konu)
     