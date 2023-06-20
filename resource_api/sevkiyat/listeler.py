from models.new_sevkiyat import SiparisListeModel,SiparisListeSchema,SiparisKalemModel,SiparisKalemSchema
from helpers import SqlConnect


class Listeler:

    def __init__(self):

        self.data = SqlConnect().data

    
    def getSiparisListe(self):

        result = self.data.getList(
            """
            select
            ID,
            SiparisNo,
            MusteriID
            from
            SiparislerTB
            where SiparisDurumID=2

            """
        )

        liste = list()

        for item in result: 

            model = SiparisListeModel()
            model.id = item.ID 
            model.siparisno = item.SiparisNo
            model.musteriid = item.MusteriID

            liste.append(model)

        schema = SiparisListeSchema(many=True)

        return schema.dump(liste)

    def getSiparisKalemList(self,siparisNo):

        result = self.data.getStoreList(
            """
            select
            u.ID,
            u.UrunKartID,
            u.Miktar as SiparisMiktar,
            t.FirmaAdi as Tedarikci,
            u.TedarikciID,
            dbo.Get_KategoriAdi(u.UrunKartID) as Kategori,
            dbo.Get_UrunAdi(u.UrunKartID) as UrunAdi,
            dbo.Get_KenarIslem(u.UrunKartID) as KenarIslem,
            dbo.Get_Ebat(u.UrunKartID) as Ebat,
			(select s.NavlunSatis from SiparislerTB s WHERE s.SiparisNo = u.SiparisNo) as NavlunSatis,
			(select st.TeslimTur from SiparislerTB s,SiparisTeslimTurTB st WHERE s.SiparisNo = u.SiparisNo and s.TeslimTurID = st.ID ) as TeslimTuru,
            (select sum(Miktar) from UretimTB ur where ur.SiparisAciklama = u.SiparisNo and ur.UrunKartID = u.UrunKartID) as Uretim
            from
            SiparisUrunTB u,TedarikciTB t
            where
            u.TedarikciID=t.ID and u.SiparisNo=?
                    """,(siparisNo)
        )
        liste = list()
        indeks = 1
        for item in result:

            model = SiparisKalemModel()
            model.id = item.ID 
            model.siparis = self.__getNoneControl(item.SiparisMiktar) 
            model.tedarikciadi = item.Tedarikci 
            model.tedarikciid = item.TedarikciID 
            model.uretim = self.__getNoneControl(item.Uretim)
            model.urunkartid = item.UrunKartID 
            model.icerik = f" {indeks} - {model.tedarikciadi}/{item.Kategori}/{item.UrunAdi}/{item.KenarIslem}/{item.Ebat} "
            model.navlunsatis = item.NavlunSatis
            model.teslimturu = item.TeslimTuru
            liste.append(model)
            indeks += 1

        
        schema = SiparisKalemSchema(many=True)
        
        return schema.dump(liste)

    def __getNoneControl(self,value):
        if(value == None):
            return 0
        else:
            return value


