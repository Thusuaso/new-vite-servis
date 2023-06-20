from helpers import SqlConnect
from models.operasyon.firmalar import FirmaListeSchema,FirmaListeModel,FirmaSchema,FirmaModel


class Listeler:

    def __init__(self):

        self.data = SqlConnect().data

   
    def getFirmaListe(self):

        result = self.data.getList(
            """ 
             select * from FirmalarTB order by ID DESC

            """
        )

        liste = list()
        
        for item in result: 

            model = FirmaListeModel()
            model.id = item.ID
            model.firma_adi = item.FirmaAdi
            model.mail = item.MailAdresi
            model.telefon = item.Telefon
            model.aciklama = item.Notlar
            liste.append(model)

        schema = FirmaListeSchema(many=True)

        return schema.dump(liste)

    def getFirmaModel(self):

        model = FirmaModel()
        schema = FirmaSchema()

        return schema.dump(model)
       

       


    def firmaKaydet(self,item):
        try:
            self.data.update_insert(
                """
                INSERT INTO FirmalarTB (FirmaAdi, Telefon, MailAdresi, Notlar)    values
                (?,?,?,?)
                """,(item['firma_adi'],item['telefon'],item['mail'],item['aciklama'])
            )
           
            
            return True
        except Exception as e:
            print('firmaKaydet  Hata : ',str(e))
        return False    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       