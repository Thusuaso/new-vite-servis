from models.siparisler_model import IscilikModel,IscilikSchema
from helpers import SqlConnect,TarihIslemler,DegisiklikMain

class Iscilik:
    def __init__(self):
        self.data = SqlConnect().data
    
    def getIscilikList(self,siparisNo,urunKartId):
        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(
            """
            Select 
            s.ID,
            s.Tarih,
            t.FirmaAdi,
            s.Aciklama,
            s.Tutar,
            s.TedarikciID,
            s.UrunKartID,
            s.SiparisEkstraGiderTurID
            from SiparisEkstraGiderlerTB s,TedarikciTB t
            where t.ID=s.TedarikciID and s.SiparisNo=? and
            s.UrunKartID=?
            """,(siparisNo,urunKartId)
        )

        liste = list()

        for item in result:
            model = IscilikModel()
            model.id = item.ID
            model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            model.tedarikciAdi = item.FirmaAdi 
            model.aciklama = item.Aciklama 
            model.tutar = item.Tutar
            model.tedarikciId = item.TedarikciID 
            model.urunKartId = item.UrunKartID 
            model.siparisEkstraGiderTurId = item.SiparisEkstraGiderTurID 

            liste.append(model)

        schema = IscilikSchema(many=True)

        return schema.dump(liste)

    def getIscilikModel(self):

        model = IscilikModel()

        schema = IscilikSchema()

        return schema.dump(model)

    def kaydet(self,data):
        self.data.update_insert(
            """
            insert into SiparisEkstraGiderlerTB (
                Tarih,siparisNo,UrunKartID,TedarikciID,
                SiparisEkstraGiderTurID,Aciklama,Tutar
            )
            values
            (?,?,?,?,?,?,?)
            """,(
                
                data['tarih'],data['siparisNo'],data['urunKartId'],
                data['tedarikciId'],data['siparisEkstraGiderTurId'],
                data['aciklama'],data['tutar']
            )
        )


    def guncelle(self,data):
        print(data)
        self.data.update_insert(
            """
            update SiparisEkstraGiderlerTB set Tarih=?,TedarikciID=?,
            SiparisEkstraGiderTurID=?,Aciklama=?,Tutar=?
            where ID=?
            """,(
                data['tarih'],data['tedarikciId'],data['siparisEkstraGiderTurId'],
                data['aciklama'],data['tutar'],data['id']
            )
        )

    def sil(self,id):
        
        self.data.update_insert(
            """
            delete from SiparisEkstraGiderlerTB where ID=?
            """,(id)
        )