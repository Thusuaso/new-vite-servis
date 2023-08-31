from helpers import SqlConnect
from models.operasyon import NakliyeListeSchema,NakliyeListeModel

class Listeler:

    def __init__(self):

        self.data = SqlConnect().data

   
    def getNakliyeFirmaListe(self):

        result = self.data.getList(
            """ 
           select 
            s.SiparisNo,
            n.FaturaNo,
            (select f.FirmaAdi from FirmalarTB f where f.ID=n.FirmaID ) as firma_adi,
            (select f.ID from FirmalarTB f where f.ID=n.FirmaID ) as firma_id,
            s.Tutar,
            n.Kur,
            s.Tarih
            
            from SiparisFaturaKayitTB s ,NakliyeFaturaKayitTB n where 
            s.YuklemeEvrakID=13 and s.SiparisFaturaTurID=11  and Year(s.Tarih) in (2023,2022,2021)  and n.FaturaNo+'.pdf' = s.EvrakAdi and n.ID = s.FaturaKayitID
          
            group by s.ID ,s.SiparisNo , n.FaturaNo , n.FirmaID ,s.Tutar,n.Kur,s.Tarih

            order by s.Tarih desc

            """
        )

        liste = list()
        
        for item in result: 

            model = NakliyeListeModel()
            
            model.firma_adi = item.firma_adi
            model.faturaNo = item.FaturaNo
            model.Tutar_tl =item.Tutar *  item.Kur
            model.Tutar_dolar = item.Tutar
            model.siparis_no = item.SiparisNo
            model.kur = item.Kur
         
            model.tarih = item.Tarih
            model.Firma_id = item.firma_id
            model.link = f"https://file-service.mekmar.com/file/download/customer/{item.firma_id}/{item.FaturaNo}.pdf "

            liste.append(model)

        schema = NakliyeListeSchema(many=True)

        return schema.dump(liste)


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       