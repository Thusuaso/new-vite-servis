from models.new_sevkiyat import SevkiyatSchema,SevkiyatModel,KasaListesiModel,KasaListesiSchema
from helpers import SqlConnect


class SevkiyatIslem:

    def __init__(self):

        self.data = SqlConnect().data

    def newSevkiyatModel(self):

        item = SevkiyatModel()
        item.kasalistesi = list()
        schema = SevkiyatSchema()
        return schema.dump(item)

    def getKasaListesi(self,siparisno):

        result = self.data.getStoreList(
            """
            select
            u.ID as id,
            u.KasaNo,
            s.SatisFiyati,
            s.SatisToplam,
            dbo.Get_UrunAdi(u.UrunKartID) as urunadi,
            dbo.Get_KenarIslem(u.UrunKartID) as yuzeyislem,
            dbo.Get_Ebat(u.UrunKartID) as ebat,
            u.Miktar,
            u.UrunKartID,
            (select ub.BirimAdi from UrunBirimTB ub where ub.ID=u.UrunBirimID) as Birim,
            u.TedarikciID
            from
            UretimTB u,SiparisUrunTB s
            where 
            u.UrunDurumID=1            
			and s.SiparisNo=u.SiparisAciklama
			and s.UrunKartID=u.UrunKartID
			and s.TedarikciID=u.TedarikciID
            and s.SiparisNo=?
            """,(siparisno)
        )

        liste = list() 

        for item in result:

            model = KasaListesiModel() 
            model.id = item.UrunKartID 
            model.kasano = item.KasaNo 
            model.birimfiyat = item.SatisFiyati 
            model.toplam = item.SatisToplam 
            model.urunadi =item.urunadi 
            model.yuzeyislem = item.yuzeyislem 
            model.ebat = item.ebat 
            model.miktar = item.Miktar
            model.birimadi = item.Birim 
            model.tedarikci_id = item.TedarikciID
             

            liste.append(model)

        schema = KasaListesiSchema(many=True)

        return schema.dump(liste)

    
