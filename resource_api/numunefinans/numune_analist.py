from helpers import SqlConnect
from models.numuneler.numune_finans import *


class NumuneFinansAnaListe:

    def __init__(self):

        self.data = SqlConnect().data
      
        self.dtOdenenList = self.data.getList(

            """
         select
            o.NumuneNo , 
             o.Tutar as odenen ,
             n.MusteriID as Id,
		     o.Masraf as masraf,
			o.Aciklama
			 
            from NumuneOdemelerTB o  , NumunelerTB n 
            where n.NumuneNo =o.NumuneNo
           
			group by    o.NumuneNo ,    n.MusteriID , o.Aciklama, o.Tutar, o.Masraf

            """
        )
    #numune finans listesini gösteren method
    def getNumuneList(self,yil):

        result = self.data.getStoreList(

            """
          select
			m.MusteriAdi , 

			  m.Id,
			  sum(n.KuryeAlis) as kuryeAlis,
			  sum(n.KuryeSatis) as kuryeSatis,
              sum(n.TL_Alis) as TL_Alis,
			  sum(n.TL_Satis) as TL_Satis,
              sum(n.Euro_Alis) as Euro_Alis,
			  sum(n.Euro_Satis) as Euro_Satis
          		   
			from NumunelerTB n ,  YeniTeklif_MusterilerTB m 
			where m.Id = n.MusteriID and year(n.NumuneTarihi)= ?
			group by m.MusteriAdi ,  m.Id 

			order by m.MusteriAdi asc

            """,(yil)
        )

        liste = list()
        
        for item in result:

            model = NumuneFinansAnaListeModel()
         
            model.id = item.Id
            model.kuryeSatis = item.kuryeSatis
            model.kuryeAlis = item.kuryeAlis  

            model.TL_Alis = item.TL_Alis
            model.TL_Satis = item.TL_Satis  

            model.Euro_Alis = item.Euro_Alis
            model.Euro_Satis = item.Euro_Satis     
           
            model.musteriadi = item.MusteriAdi
            
         
          
           
           
            liste.append(model)

        schema = NumuneFinansAnaListeSchema(many=True)

        return sorted(schema.dump(liste), key=lambda x:x['kuryeSatis'],reverse=True)

    def getNumuneBankaList(self,yil):

        result = self.data.getStoreList(

            """
                select 

                    sum(nod.Tutar) as bedel,
                    nod.Banka,
                    sum(nod.Euro_Tutar) as bedel_Euro,
                    sum(nod.TL_Tutar) as bedel_TL


                from NumunelerTB n
                inner join NumuneOdemelerTB nod on nod.NumuneNo = n.NumuneNo

                where YEAR(nod.Tarih) = ?
                group by nod.Banka

            """,(yil)
        )

        liste = list()
      
        for item in result:

            model = NumuneFinansBankaModel()
         
            model.bedel = item.bedel
            model.bedel_tl = item.bedel_TL
            model.bedel_euro = item.bedel_Euro
            model.banka = item.Banka
                
            liste.append(model)

        schema = NumuneFinansBankaSchema(many=True)

        return sorted(schema.dump(liste), key=lambda x:x['bedel'],reverse=True)


    def getYilListesi(self):

        result = self.data.getList(
            """
            select
            Year(Tarih) as Yil
            from
            NumuneOdemelerTB
            group by Year(Tarih)
            order by Year(Tarih) desc

            """
        )

        id = 1

        liste = list()

        for item in result:

            model = NumuneYilModel()
            model.id = id 
            model.yil = item.Yil

            liste.append(model)

            id += 1

        schema = NumuneYilSchema(many=True)

        return schema.dump(liste)

    def getTakipYilListesi(self):

        result = self.data.getList(
            """
           

            select
            Year(NumuneTarihi) as Yil
            from
            NumunelerTB
            group by Year(NumuneTarihi)
            order by Year(NumuneTarihi) desc

            """
        )

        id = 1

        liste = list()

        for item in result:

            model = NumuneYilModel()
            model.id = id 
            model.yil = item.Yil

            liste.append(model)

            id += 1

        schema = NumuneYilSchema(many=True)

        return schema.dump(liste)
 

    def getBankayaGelenOdemelerAyrinti(self,banka,yil):
        try:
            result = self.data.getStoreList("""
                                                 select 
                                                    nod.ID,
                                                    nod.Tutar as bedel,
													nod.Tarih as BankayaGelenTarih,
                                                    nod.Banka,
                                                    nod.Euro_Tutar as bedel_Euro,
                                                    nod.TL_Tutar as bedel_TL,
                                                    nod.NumuneNo,
                                                    (select ym.MusteriAdi from YeniTeklif_MusterilerTB ym where ym.Id = n.MusteriID) as Musteri,
                                                    n.NumuneTarihi


                                                from NumunelerTB n
                                                inner join NumuneOdemelerTB nod on nod.NumuneNo = n.NumuneNo

                                                where YEAR(nod.Tarih) = ? and nod.Banka=?
                                            
                                            """,(yil,banka))
            
            liste = list()
            for item in result:
                model = NumuneBankayaGelenAyrintiModel()
                model.id = item.ID
                model.bedel_dolar = self.__getNone(item.bedel)
                model.bedel_euro = self.__getNone(item.bedel_Euro)
                model.bedel_tl = self.__getNone(item.bedel_TL)
                model.banka_adi = item.Banka
                model.musteri_adi = item.Musteri
                model.numune_no = item.NumuneNo
                model.numune_tarihi = item.NumuneTarihi
                model.bankaya_gelen_tarih = item.BankayaGelenTarih
                liste.append(model)
            schema = NumuneBankayaGelenAyrintiSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print('getBankayaGelenOdemelerAyrinti hata',str(e))
            return False
        
    def __getNone(self,value):
        if(value == None):
            return 0
        else:
            return float(value)

   
