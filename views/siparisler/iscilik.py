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
        try:
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
            iscilik = self.data.getStoreList("""
                                        select * from SiparisEkstraGiderlerTB where SiparisNo=?
                                    """,(data['siparisNo']))
            liste = list()
            for item in iscilik:
                model = IscilikModel()
                model.tutar = item.Tutar
                liste.append(model)
                
            schema  = IscilikSchema(many = True)
            
            data = {
                'status':True,
                'iscilik':schema.dump(liste)
            }
            
        
            return data
        except Exception as e:
            print('iscilik kaydet hata',str(e))
            data = {
                'status':False
            }
            return data

    def guncelle(self,data):
        try:
            print(data['siparisNo'])
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

            iscilik = self.data.getStoreList("""
                                    select * from SiparisEkstraGiderlerTB where SiparisNo=?
                                """,(data['siparisNo']))
            print(iscilik)
            liste = list()
            for item in iscilik:
                model = IscilikModel()
                model.tutar = item.Tutar
                liste.append(model)
                
            schema  = IscilikSchema(many = True)
            
            data = {
                'status':True,
                'iscilik':schema.dump(liste)
            }
            
            
            return data
        except Exception as e:
            print('iscilik güncelle hata',str(e))
            data = {
                'status':False
            }
            return data
            
        
    def sil(self,id):
    
        
        try:
            
            siparisNo = self.data.getStoreList("""
                                                    select SiparisNo from SiparisEkstraGiderlerTB where ID=?
                                               """,(id))
            
            self.data.update_insert(
            """
                delete from SiparisEkstraGiderlerTB where ID=?
                """,(id)
            )

            iscilik = self.data.getStoreList("""
                                    select * from SiparisEkstraGiderlerTB where SiparisNo=?
                                """,(siparisNo[0][0]))
            liste = list()
            for item in iscilik:
                model = IscilikModel()
                model.tutar = item.Tutar
                liste.append(model)
                
            schema  = IscilikSchema(many = True)
            
            data = {
                'status':True,
                'iscilik':schema.dump(liste)
            }
            
            
            return data
        except Exception as e:
            print('iscilik sil hata',str(e))
            data = {
                'status':False
            }
            return data