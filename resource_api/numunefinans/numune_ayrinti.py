from models.numuneler.numune_finans import *
from helpers import SqlConnect,TarihIslemler
from openpyxl import *
import shutil


class NumuneFinansAyrinti:

    def __init__(self):

        self.data = SqlConnect().data
        self.dtOdenenList = self.data.getList(

            """
           
            select
             o.NumuneNo , 
             o.Tutar as odenen ,
             n.MusteriID as Id,
		     o.Masraf as masraf,
			o.Aciklama as aciklama,
			o.Tarih,
            o.Banka
            from NumuneOdemelerTB o  , NumunelerTB n 
            where n.NumuneNo =o.NumuneNo
          
			group by    o.NumuneNo ,    n.MusteriID , o.Aciklama, o.Tutar, o.Masraf , o.Tarih , Banka
            """
        )

    def getAyrintiList(self,musteriid,yil):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(
            """
            select
			n.NumuneNo , 
            m.Id,
			n.YuklemeTarihi,
			n.NumuneTarihi,
			sum(n.KuryeAlis) as KuryeAlis,
			sum(n.KuryeSatis) as KuryeSatis,
            sum(n.TL_Alis) as TL_Alis,
			  sum(n.TL_Satis) as TL_Satis,
              sum(n.Euro_Alis) as Euro_Alis,
			  sum(n.Euro_Satis) as Euro_Satis,
			(select g.GonderiAdi from NumuneGonderiTipi g where g.ID=n.GonderiTipi) as odeme,
			(select b.BankaAdi from NumuneBankaSecim b where b.ID = n.BankaSecim) as banka
			from NumunelerTB n ,  YeniTeklif_MusterilerTB m 
			where m.Id = n.MusteriID  and m.Id=? and YEAR(n.YuklemeTarihi) = ?
			group by n.NumuneNo ,  m.Id ,n.YuklemeTarihi , n.KuryeAlis,n.GonderiTipi,
			n.KuryeSatis,TL_Alis,TL_Satis,Euro_Alis,Euro_Satis,n.BankaSecim,n.NumuneTarihi

			order by  n.NumuneNo asc

            """,(musteriid,yil)
        )

        liste = list()
        id = 1
     
        for item in result:
            model = NumuneFinansAyrintiModel()
            model.id = id
            model.orderno = item.NumuneNo
            model.musteri_id = item.Id
            model.kuryeAlis = item.KuryeAlis
            model.kuryeSatis = item.KuryeSatis
            model.TL_Alis = item.TL_Alis
            model.TL_Satis = item.TL_Satis  

            model.Euro_Alis = item.Euro_Alis
            model.Euro_Satis = item.Euro_Satis 
            model.banka = item.banka
            model.numune_tarihi = tarihIslem.getDate(item.NumuneTarihi).strftime("%d-%m-%Y")
            model.odeme = item.odeme
            if item.YuklemeTarihi != None:
                model.sevktarihi = tarihIslem.getDate(item.YuklemeTarihi).strftime("%d-%m-%Y")
            
            liste.append(model)

        schema = NumuneFinansAyrintiSchema(many=True)
      

        return sorted(schema.dump(liste), key=lambda x:x['orderno'],reverse=True)


       
   
		
		