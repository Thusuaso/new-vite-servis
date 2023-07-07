from helpers import SqlConnect
from models.finans import DepoAnaListeModel,DepoAnaListeSchema


class DepoAnaListe:

    def __init__(self):

        self.data = SqlConnect().data
        self.dtOdenenList = self.data.getList(

            """
            select
            m.Id,
            m.CustomersName,
            Sum(u.Total) as odenen
            from
            YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id and s.OrderNo=u.OrderNo
            and s.PaymentDate is not null
            and  s.KalanBorc is  null
          
            group by m.Id,m.CustomersName
            """
        )
        self.dtKalan = self.data.getList(

          """
            select
            m.Id,
            m.CustomersName,
            Sum(u.Total) as odenen

            from
            YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id and s.OrderNo=u.OrderNo
            and s.PaymentDate is  null
            and s.KalanBorc is null
             
            
            group by m.Id,m.CustomersName
            """

        )
        
        self.dtKalanisNull = self.data.getList("""
                                                    select
                                                m.Id,
                                                m.CustomersName,
                                                Sum(u.Total) as odenen

                                                from
                                                YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
                                                where s.CustomersId=m.Id and s.OrderNo=u.OrderNo
                                                and s.PaymentDate is  null
                                                group by m.Id,m.CustomersName
                                               
                                               """)
        
        self.dtYarimOdemeler = self.data.getList(

        """
            select
            m.Id,
            m.CustomersName,
             sum( s.KalanBorc) as odenen 
			
            from
            YeniDepoSatisTB s, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id 
			and s.KalanBorc is not null
           
            group by m.Id,m.CustomersName
        
        """

        )
        
    #depo finans listesini gösteren method
    def getDepoList(self):

        result = self.data.getList(

            """
            select
            m.Id,
            m.CustomersName,
            Sum(u.Total) as ciro
            from
            YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id and s.OrderNo=u.OrderNo

       
            group by m.Id,m.CustomersName
            """
        )

        liste = list()
        total = 0
        kalan = 0 
        odenen = 0
        for item in result:

            model = DepoAnaListeModel()
            model.id = item.Id
            total , kalan = self.__getKonteynerOdenen(item.Id)
            
            odenen = total - kalan
            model.musteriadi = item.CustomersName

            model.ciro = item.ciro + total
            model.odenen = self.__getOdenen(model.id)  + odenen
            
            
            model.bakiye = self.__getKalan(model.id) + kalan + self.__getYarimOdemeler(model.id) + self.__getKalanisNotNull(model.id) - self.__getKonteynirNullShippment(item.Id)
            
            
            
            total = 0
            kalan = 0 
            odenen = 0
            liste.append(model)

        schema = DepoAnaListeSchema(many=True)

        return schema.dump(liste)

    def __getOdenen(self,musteri_id):

        odenen = 0

        for item in self.dtOdenenList:

            if item.Id == musteri_id:
                odenen = item.odenen

        return odenen

    def __getYarimOdemeler(self,musteri_id):    

         kalan = 0

         for item in self.dtYarimOdemeler:

            if item.Id == musteri_id:
                kalan = item.odenen
         
         return kalan

    def __getKalan(self,musteri_id):

        odenen = 0

        for item in self.dtKalan:

            if item.Id == musteri_id:
                odenen = item.odenen     
        
        return odenen
    
    def __getKalanisNotNull(self,musteri_id):
        notNullKalan = 0
        for item in self.dtKalanisNull:
            if item.Id == musteri_id:
                notNullKalan = item.odenen
                
        return notNullKalan
                
                
                

    def __getKonteynerOdenen(self ,musteriid):
         
         if musteriid == 1 : 
             musteriid = 3446

         elif musteriid == 3 : 
             musteriid = 2400
         elif musteriid == 4 : 
             musteriid = 1373 
        
         result = self.data.getStoreList(

         """
          select 
               s.SiparisNo,
			   s.SiparisTarihi,
			   s.YuklemeTarihi,
			   (select top 1 o.Tarih from OdemelerTB o where o.SiparisNo = s.SiparisNo  order by  o.Tarih desc) odenmeTarihi,
               dbo.Get_Siparis_Bakiye_Tutar(s.SiparisNo) as kalan,
			   (select Sum(SatisToplam) from SiparisUrunTB su where su.SiparisNo=s.SiparisNo)+  
               dbo.Get_SiparisNavlun(s.SiparisNo) as Dtp
		   from
                SiparislerTB s 
            where
                s.MusteriID=? and s.YuklemeTarihi is not null
              
		  	    
                order by  s.YuklemeTarihi desc

         """,(musteriid)
         ) 
         total = 0
         kalan = 0  
         for item in result :
             total += item.Dtp
             kalan += item.kalan
             
         return total , kalan

    
    
    def __getKonteynirNullShippment(self,musteriid):
        nullShipment = 0
        result = self.data.getStoreList("""
                                                select 


                                                        su.OrderNo,
                                                        sum(su.Total) as Total


                                                    from YeniDepoSatisTB s
                                                        inner join YeniDepoSatisUrunlerTB su on su.OrderNo = s.OrderNo
                                                        where YEAR(s.Date)>=2023 and s.PaymentDate is null and s.ShippingDate is null and s.CustomersId = ?
                                                        group by su.OrderNo
                                            
                                            
                                            
                                            
                                        """,(musteriid))
        
        for item in  result:
            nullShipment += item.Total
            
        return nullShipment

class DepoAnaListeYeni:

    def __init__(self):

        self.data = SqlConnect().data
        self.dtOdenenList = self.data.getList(

            """
            select
            m.Id,
            m.CustomersName,
            Sum(u.Total) as odenen
            from
            YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id and s.OrderNo=u.OrderNo
            and s.PaymentDate is not null
            and  s.KalanBorc is  null
          
            group by m.Id,m.CustomersName
            """
        )
        self.dtKalan = self.data.getList(

          """
            select
            m.Id,
            m.CustomersName,
            Sum(u.Total) as odenen

            from
            YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id and s.OrderNo=u.OrderNo
            and s.PaymentDate is  null
            and s.KalanBorc is null
             
            
            group by m.Id,m.CustomersName
            """

        )
        
        self.dtKalanisNull = self.data.getList("""
                                                    select
                                                m.Id,
                                                m.CustomersName,
                                                Sum(u.Total) as odenen

                                                from
                                                YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
                                                where s.CustomersId=m.Id and s.OrderNo=u.OrderNo
                                                and s.PaymentDate is  null
                                                group by m.Id,m.CustomersName
                                               
                                               """)
        
        self.dtYarimOdemeler = self.data.getList(

        """
            select
            m.Id,
            m.CustomersName,
             sum( s.KalanBorc) as odenen 
			
            from
            YeniDepoSatisTB s, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id 
			and s.KalanBorc is not null
           
            group by m.Id,m.CustomersName
        
        """

        )
        
    #depo finans listesini gösteren method
    def getDepoList(self):

        result = self.data.getList(

            """
            select
            m.Id,
            m.CustomersName,
            Sum(u.Total) as ciro
            from
            YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u, YeniDepoMusterilerTB m
            where s.CustomersId=m.Id and s.OrderNo=u.OrderNo

       
            group by m.Id,m.CustomersName
            """
        )

        liste = list()
        total = 0
        kalan = 0 
        odenen = 0
        for item in result:

            model = DepoAnaListeModel()
            model.id = item.Id
            total , kalan = self.__getKonteynerOdenen(item.Id)
            
            odenen = total - kalan
            model.musteriadi = item.CustomersName

            model.ciro = item.ciro + total
            model.odenen = self.__getOdenen(model.id)  + odenen
            
            
            model.bakiye = self.__getKalan(model.id) + kalan + self.__getYarimOdemeler(model.id) + self.__getKalanisNotNull(model.id) - self.__getKonteynirNullShippment(item.Id)
            
            
            
            total = 0
            kalan = 0 
            odenen = 0
            liste.append(model)

        schema = DepoAnaListeSchema(many=True)

        return schema.dump(liste)

    def __getOdenen(self,musteri_id):

        odenen = 0

        for item in self.dtOdenenList:

            if item.Id == musteri_id:
                odenen = item.odenen

        return odenen

    def __getYarimOdemeler(self,musteri_id):    

         kalan = 0

         for item in self.dtYarimOdemeler:

            if item.Id == musteri_id:
                kalan = item.odenen
         
         return kalan

    def __getKalan(self,musteri_id):

        odenen = 0

        for item in self.dtKalan:

            if item.Id == musteri_id:
                odenen = item.odenen     
        
        return odenen
    
    def __getKalanisNotNull(self,musteri_id):
        notNullKalan = 0
        for item in self.dtKalanisNull:
            if item.Id == musteri_id:
                notNullKalan = item.odenen
                
        return notNullKalan
                
                
                

    def __getKonteynerOdenen(self ,musteriid):
         
         if musteriid == 1 : 
             musteriid = 3446

         elif musteriid == 3 : 
             musteriid = 2400
         elif musteriid == 4 : 
             musteriid = 1373 
        
         result = self.data.getStoreList(

         """
          select 
               s.SiparisNo,
			   s.SiparisTarihi,
			   s.YuklemeTarihi,
			   (select top 1 o.Tarih from OdemelerTB o where o.SiparisNo = s.SiparisNo  order by  o.Tarih desc) odenmeTarihi,
               dbo.Get_Siparis_Bakiye_Tutar(s.SiparisNo) as kalan,
			   (select Sum(SatisToplam) from SiparisUrunTB su where su.SiparisNo=s.SiparisNo)+  
               dbo.Get_SiparisNavlun(s.SiparisNo) as Dtp
		   from
                SiparislerTB s 
            where
                s.MusteriID=? and s.YuklemeTarihi is not null
              
		  	    
                order by  s.YuklemeTarihi desc

         """,(musteriid)
         ) 
         total = 0
         kalan = 0  
         for item in result :
             total += item.Dtp
             kalan += item.kalan
             
         return total , kalan

    
    
    def __getKonteynirNullShippment(self,musteriid):
        nullShipment = 0
        result = self.data.getStoreList("""
                                                select 


                                                        su.OrderNo,
                                                        sum(su.Total) as Total


                                                    from YeniDepoSatisTB s
                                                        inner join YeniDepoSatisUrunlerTB su on su.OrderNo = s.OrderNo
                                                        where YEAR(s.Date)>=2023 and s.PaymentDate is null and s.ShippingDate is null and s.CustomersId = ?
                                                        group by su.OrderNo
                                            
                                            
                                            
                                            
                                        """,(musteriid))
        
        for item in  result:
            nullShipment += item.Total
            
        return nullShipment
