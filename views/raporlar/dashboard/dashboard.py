from helpers import SqlConnect
import datetime
from models.dashboard.gelenSiparis import *
from models.raporlar.anaSayfaDegisiklik import *
import locale
class DashboardNew:
    def __init__(self):
        self.data = SqlConnect().data
        self.now = datetime.datetime.now()
        self.month = self.now.month
        self.year = self.now.year
        self.grafikMekmarNavlunBuYil = self.data.getList("""
                                                        select 

                                                            sum(s.NavlunSatis) + sum(s.DetayTutar_1) + sum(s.DetayTutar_2) + sum(s.DetayTutar_3) as NavlunSatis,
                                                            Month(s.YuklemeTarihi) as Ay

                                                        from 
                                                            SiparislerTB s
															inner join MusterilerTB m on m.ID = s.MusteriID
                                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) and m.Marketing='Mekmar'
                                                        group by 
                                                            MONTH(s.YuklemeTarihi)
                                                        order by
                                                            MONTH(s.YuklemeTarihi)
                                                    
                                                    """)
        self.grafikMekmarNavlunGecenYil = self.data.getList("""
                                                                select 

                                                            sum(s.NavlunSatis) + sum(s.DetayTutar_1) + sum(s.DetayTutar_2) + sum(s.DetayTutar_3) as NavlunSatis,
                                                            Month(s.YuklemeTarihi) as Ay

                                                        from 
                                                            SiparislerTB s
															inner join MusterilerTB m on m.ID = s.MusteriID
                                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) - 1 and m.Marketing='Mekmar'
                                                        group by 
                                                            MONTH(s.YuklemeTarihi)
                                                        order by
                                                            MONTH(s.YuklemeTarihi)
                                                            
                                                            
                                                            
                                                            """)
        self.grafikHepsiNavlunBuYil = self.data.getList("""
                                                            select 

                                                            sum(s.NavlunSatis) as NavlunSatis,
                                                            Month(s.YuklemeTarihi) as Ay

                                                        from 
                                                            SiparislerTB s
                                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi) = YEAR(GETDATE())
                                                        group by 
                                                            MONTH(s.YuklemeTarihi)
                                                        """)
        self.grafikHepsiNavlunGecenYil = self.data.getList("""
                                                            select 

                                                                    sum(s.NavlunSatis) as NavlunSatis,
                                                                    Month(s.YuklemeTarihi) as Ay

                                                                from 
                                                                    SiparislerTB s
                                                                where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) -  1 and  s.FaturaKesimTurID=1 and MONTH(s.YuklemeTarihi) <= MONTH(GETDATE())
                                                                group by 
                                                                    MONTH(s.YuklemeTarihi)
                                                        """)
        self.odemeler = self.data.getList("""
                                            select 

                                                sum(o.Tutar) as OdenenTutar,
                                                o.SiparisNo as SiparisNo



                                            from OdemelerTB o group by o.SiparisNo
                                          
                                          """)
        self.navlun = self.data.getList("""
                                            select 

                                            sum(s.NavlunSatis) as Navlun,
											sum(s.DetayTutar_1) as Detay1,
											sum(s.DetayTutar_2) as Detay2,
											sum(s.DetayTutar_3) as Detay3,
                                            s.SiparisNo as SiparisNo



                                        from SiparislerTB s group by s.SiparisNo
                                        
                                        """)
    def getDashboardGelenSiparis(self):
        try:
            result = self.data.getList("""
                                                select 


                                                    sum(su.SatisToplam) as SatisToplami,
                                                    MONTH(s.SiparisTarihi) as Ay

                                                from SiparislerTB s
                                                inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                inner join MusterilerTB m on m.ID = s.MusteriID

                                                where YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and MONTH(s.SiparisTarihi) = MONTH(GETDATE()) and m.Marketing='Mekmar'

                                                group by YEAR(s.SiparisTarihi),MONTH(s.SiparisTarihi)
                                            
                                            
                                            """)
            liste = list()
            if len(result) >0:
                
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = self.getMonth(self.month)
                model.gelenSiparisFob = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparis hata",str(e))
            return False
    def getDashboardGelenSiparisYuklenen(self):
        try:
            result = self.data.getList("""
                                                select 


                                                    sum(su.SatisToplam) as SatisToplami,
                                                    MONTH(s.YuklemeTarihi) as Ay
                                                    


                                                from SiparislerTB s
                                                inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                inner join MusterilerTB m on m.ID = s.MusteriId

                                                where  YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) and m.Marketing='Mekmar' and s.SiparisDurumID=3 and MONTH(s.YuklemeTarihi) = MONTH(GETDATE())

                                                group by MONTH(s.YuklemeTarihi)
                                            
                                            
                                            """)
            
            
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami + self.__mekmarYuklenenNavlun()
                    liste.append(model)
                    
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = self.getMonth(self.month)
                model.gelenSiparisFob = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparis hata",str(e))
            return False
    
    ################################################################
    
    def getDashboardGelenSiparisSatisci(self,satisci):
        try:
            result = self.data.getStoreList("""
                                    select 
                                        sum(su.SatisToplam) as SatisToplami,
                                        MONTH(s.SiparisTarihi) as Ay,
                                        s.SiparisSahibi as SiparisSahibi
                                    from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo
                                    where MONTH(s.SiparisTarihi) = ? and YEAR(s.SiparisTarihi)=? and s.SiparisDurumID=2 and (s.FaturaKesimTurID=1 or s.FaturaKesimTurID=3) and s.SiparisSahibi=?
                                    group by
                                        MONTH(s.SiparisTarihi),s.SiparisSahibi
                                   
                                   """,(self.month,self.year,satisci))
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.siparisSahibi = i.SiparisSahibi
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami
                    liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisSatisci hata",str(e))
            return False
    
    #########################################
    def getDashboardGelenSiparisAll(self):
        try:
            result = self.data.getList("""
                                                select 


                                                    sum(su.SatisToplam) as SatisToplami,
                                                    MONTH(s.SiparisTarihi) as Ay

                                                from SiparislerTB s
                                                inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                
                                                where YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and MONTH(s.SiparisTarihi) = MONTH(GETDATE()) 

                                                group by YEAR(s.SiparisTarihi),MONTH(s.SiparisTarihi)
                                            
                                            
                                            """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = self.getMonth(self.month)
                model.gelenSiparisFob = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisAll hata",str(e))
            return False
    
    def getDashboardGelenSiparisAllYuklenen(self):
        try:
            result = self.data.getList("""
                                                select 


                                                    sum(su.SatisToplam) as SatisToplami,
                                                    MONTH(s.YuklemeTarihi) as Ay
                                                    


                                                from SiparislerTB s
                                                inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                                where YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and s.SiparisDurumID=3 and MONTH(s.YuklemeTarihi) = MONTH(GETDATE())

                                                group by YEAR(s.SiparisTarihi),MONTH(s.YuklemeTarihi)
                                            
                                            
                                            """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami + self.__allYuklenenNavlun()
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = self.getMonth(self.month)
                model.gelenSiparisFob = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisAll hata",str(e))
            return False
    
    
    
    
    ################################################################
    def getDashboardGelenSiparisYillikMekmar(self):
        try:
            result = self.data.getList("""
                                    select 
                                            sum(su.SatisToplam) as SatisToplam
                                        from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                        inner join MusterilerTB m on m.ID = s.MusteriID
                                        where YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and MONTH(s.SiparisTarihi) <= MONTH(GETDATE()) - 1 and m.Marketing='Mekmar'

                                        group by YEAR(s.SiparisTarihi)
                                   """)
            liste = list()
            if len(result) >0:
                for i in result:
                    
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = str(self.month) + '/' + '12'
                    model.gelenSiparisFob = i.SatisToplam
                    model.gelenSiparisYil = self.year
                    model.gelenSiparisAylikOrtalama = (float(i.SatisToplam) + float(self.getDashboardGelenSiparis()[0]['gelenSiparisFob'])) / (self.month)
                    model.gelenSiparisYilSonuTahmini = model.gelenSiparisAylikOrtalama * 12
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = 0
                model.gelenSiparisYil = self.year
                model.gelenSiparisAylikOrtalama = 0
                model.gelenSiparisYilSonuTahmini = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisYillikMekmar hata",str(e))
            return False
    def getDashboardGelenSiparisYillikAll(self):
        try:
            result = self.data.getList("""
                                    select 


                                            sum(su.SatisToplam) as SatisToplam
                                            


                                        from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and MONTH(s.SiparisTarihi)<= MONTH(GETDATE()) - 1

                                        group by YEAR(s.SiparisTarihi)
                                   """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = str(self.month ) + '/' + '12'
                    model.gelenSiparisFob = i.SatisToplam
                    model.gelenSiparisYil = self.year
                    model.gelenSiparisAylikOrtalama = (float(i.SatisToplam) + float(self.getDashboardGelenSiparisAll()[0]['gelenSiparisFob'])) / (self.month)
                    model.gelenSiparisYilSonuTahmini = model.gelenSiparisAylikOrtalama * 12
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = 0
                model.gelenSiparisYil = self.year
                model.gelenSiparisAylikOrtalama = 0
                model.gelenSiparisYilSonuTahmini = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisYillikAll hata",str(e))
            return False
    ################################################################
    
    ################################################################
    def getDashboardYuklenenSiparisYillikMekmar(self):
        try:
            result = self.data.getList("""
                                    select 


                                            sum(su.SatisToplam) as SatisToplam
                                            


                                        from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                        inner join MusterilerTB m on m.ID = s.MusteriID

                                        where  YEAR(s.YuklemeTarihi)=YEAR(GETDATE()) and s.SiparisDurumID=3 and MONTH(s.YuklemeTarihi)<=MONTH(GETDATE()) -1 and m.Marketing='Mekmar'

                                        group by YEAR(s.YuklemeTarihi)
                                   """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = str(self.month) + '/' + '12'
                    navlun,detay1,detay2,detay3 = self.__mekmarYuklenenYillikNavlun()
                    model.gelenSiparisFob = i.SatisToplam + self.__noneControl(navlun) + self.__noneControl(detay1) + self.__noneControl(detay2) + self.__noneControl(detay3)
                    model.gelenSiparisYil = self.year
                    model.gelenSiparisAylikOrtalama = (float(model.gelenSiparisFob) + float(self.getDashboardGelenSiparisYuklenen()[0]['gelenSiparisFob'])) / (self.month)
                    model.gelenSiparisYilSonuTahmini = model.gelenSiparisAylikOrtalama * 12
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = 0
                model.gelenSiparisYil = self.year
                model.gelenSiparisAylikOrtalama = 0
                model.gelenSiparisYilSonuTahmini = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardYuklenenSiparisYillikMekmar hata",str(e))
            return False
    
    
    def __noneControl(self,value):
        if(value == None):
            return 0
        else:
            return value
    
    
    def getDashboardYuklenenSiparisYillikAll(self):
        try:
            result = self.data.getList("""
                                    select 
                                            sum(su.SatisToplam) as SatisToplam
                                            
                                        from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where YEAR(s.YuklemeTarihi)=YEAR(GETDATE() - 1) and s.SiparisDurumID=3 and MONTH(s.YuklemeTarihi) <= MONTH(GETDATE())-1

                                        group by YEAR(s.YuklemeTarihi)
                                   """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = str(self.month) + '/' + '12'
                    model.gelenSiparisFob = i.SatisToplam + self.__allYuklenenYillikNavlun()
                    model.gelenSiparisYil = self.year
                    model.gelenSiparisAylikOrtalama = float(model.gelenSiparisFob / (self.month - 1))
                    model.gelenSiparisYilSonuTahmini = model.gelenSiparisAylikOrtalama * 12
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = 0
                model.gelenSiparisYil = self.year
                model.gelenSiparisAylikOrtalama = 0
                model.gelenSiparisYilSonuTahmini = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardYuklenenSiparisYillikAll hata",str(e))
            return False
    ################################################################
    
    def __mekmarYuklenenNavlun(self):
        result = self.data.getList("""
                                        select 

                                            sum(s.NavlunSatis) + sum(s.DetayTutar_1) + sum(s.DetayTutar_2) + sum(s.DetayTutar_3) as NavlunSatis

                                        from
                                        SiparislerTB s
                                        inner join MusterilerTB m on m.Id = s.MusteriID

                                        where YEAR(s.YuklemeTarihi) =YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) = MONTH(GETDATE()) and m.Marketing='Mekmar'

                                        group by MONTH(s.YuklemeTarihi)
                                   
                                   """)
        return result[0].NavlunSatis
    
    def __allYuklenenNavlun(self):
        result = self.data.getList("""
                                        select 

                                            sum(s.NavlunSatis) as NavlunSatis

                                        from
                                        SiparislerTB s

                                        where YEAR(s.YuklemeTarihi) =YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) = MONTH(GETDATE())

                                        group by MONTH(s.YuklemeTarihi)
                                   
                                   """)
        return result[0].NavlunSatis
    
    
    def __mekmarYuklenenYillikNavlun(self):
        result = self.data.getList("""
                                        select 

                                        sum(s.NavlunSatis) as NavlunSatis,
										sum(s.DetayTutar_1) as Detay1,
										sum(s.DetayTutar_2) as Detay2,
										sum(s.DetayTutar_3) as Detay3

                                        from
                                        SiparislerTB s
                                        inner join MusterilerTB m on m.ID = s.MusteriID

                                        where YEAR(s.YuklemeTarihi) =YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) <= MONTH(GETDATE()) - 1 and m.Marketing='Mekmar'

                                        group by YEAR(s.YuklemeTarihi)
                                   
                                   """)
        return result[0].NavlunSatis,result[0].Detay1,result[0].Detay2,result[0].Detay3
    
    def __allYuklenenYillikNavlun(self):
        result = self.data.getList("""
                                        select 

                                        sum(s.NavlunSatis) as NavlunSatis

                                        from
                                        SiparislerTB s

                                        where YEAR(s.YuklemeTarihi) =YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) <= MONTH(GETDATE()) - 1

                                        group by YEAR(s.YuklemeTarihi)
                                   
                                   """)
        return result[0].NavlunSatis

    def getDashboardGelenSiparisYillik(self):
        try:
            result = self.data.getList("""
                                    select 

                                        sum(su.SatisToplam) as SatisToplam
                                    from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo

                                    where YEAR(s.SiparisTarihi)=YEAR(GETDATE())  and MONTH(s.SiparisTarihi) <= (MONTH(GETDATE()) - 1)

                                    group by 
                                        YEAR(s.SiparisTarihi)


                                   
                                   """)
            liste = list()
            for i in result:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = i.SatisToplam
                model.gelenSiparisYil = self.year
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisYillik hata",str(e))
            return False
    
    ###########EFES###############
    
    def getDashboardGelenSiparisEfes(self):
        try:
            result = self.data.getStoreList("""
                                                select 

                                                    sum(su.SatisToplam) as SatisToplami,
                                                    MONTH(s.SiparisTarihi) Ay

                                                from SiparislerTB s
                                                    inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo

                                                where MONTH(s.SiparisTarihi) = ? and YEAR(s.SiparisTarihi)=? and s.SiparisDurumID=2 and (s.FaturaKesimTurID=2)

                                                group by
                                                    MONTH(s.SiparisTarihi)
                                            
                                            
                                            """,(self.month,self.year))
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = self.getMonth(self.month)
                model.gelenSiparisFob = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparis hata",str(e))
            return False
    def getDashboardGelenSiparisYillikEfes(self):
        try:
            result = self.data.getList("""
                                    select 
                                        sum(su.SatisToplam) as SatisToplam
                                    from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo

                                    where YEAR(s.SiparisTarihi)=YEAR(GETDATE())  and MONTH(s.SiparisTarihi) <= (MONTH(GETDATE()) - 1) and (s.FaturaKesimTurID=2)

                                    group by 
                                        YEAR(s.SiparisTarihi)
                                   """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = str(self.month) + '/' + '12'
                    model.gelenSiparisFob = i.SatisToplam
                    model.gelenSiparisYil = self.year
                    model.gelenSiparisAylikOrtalama = float(i.SatisToplam / self.month)
                    model.gelenSiparisYilSonuTahmini = model.gelenSiparisAylikOrtalama * 12
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = 0
                model.gelenSiparisYil = self.year
                model.gelenSiparisAylikOrtalama = 0
                model.gelenSiparisYilSonuTahmini = 0
                liste.append(model)

            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisYillikEfes hata",str(e))
            return False
    
    
    def getDashboardGelenSiparisEfesYuklenen(self):
        try:
            result = self.data.getStoreList("""
                                                select 

                                                    sum(su.SatisToplam) as SatisToplami,
                                                    MONTH(s.SiparisTarihi) Ay

                                                from SiparislerTB s
                                                    inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo

                                                where MONTH(s.SiparisTarihi) = ? and YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and s.SiparisDurumID=3 and (s.FaturaKesimTurID=2)

                                                group by
                                                    MONTH(s.SiparisTarihi)
                                            
                                            
                                            """,(self.month))
            liste = list()
            if len(result)==0:
                model = GelenSiparisModel()
                model.gelenSiparisAy = self.getMonth(self.month)
                model.gelenSiparisFob = 0
                liste.append(model)
            else:
                
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = self.getMonth(i.Ay)
                    model.gelenSiparisFob = i.SatisToplami + self.__efesYuklenenNavlun()
                    liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisEfesYuklenen hata",str(e))
            return False
    def getDashboardGelenSiparisYillikEfesYuklenen(self):
        try:
            result = self.data.getList("""
                                    select 
                                        sum(su.SatisToplam) as SatisToplam
                                    from SiparislerTB s
                                        inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo

                                    where YEAR(s.SiparisTarihi)=YEAR(GETDATE())  and MONTH(s.SiparisTarihi) <= (MONTH(GETDATE()) - 1) and s.SiparisDurumID=3 and (s.FaturaKesimTurID=2)

                                    group by 
                                        YEAR(s.SiparisTarihi)
                                   """)
            liste = list()
            if len(result) >0:
                for i in result:
                    model = GelenSiparisModel()
                    model.gelenSiparisAy = str(self.month) + '/' + '12'
                    model.gelenSiparisFob = i.SatisToplam + self.__efesYuklenenYillikNavlun()
                    model.gelenSiparisYil = self.year
                    model.gelenSiparisAylikOrtalama = float(model.gelenSiparisFob / self.month)
                    model.gelenSiparisYilSonuTahmini = model.gelenSiparisAylikOrtalama * 12
                    liste.append(model)
            else:
                model = GelenSiparisModel()
                model.gelenSiparisAy = str(self.month) + '/' + '12'
                model.gelenSiparisFob = 0
                model.gelenSiparisYil = self.year
                model.gelenSiparisAylikOrtalama = 0
                model.gelenSiparisYilSonuTahmini = 0
                liste.append(model)
            schema = GelenSiparisSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print("getDashboardGelenSiparisYillikEfesYuklenen hata",str(e))
            return False
    
    
    def __efesYuklenenNavlun(self):
        result = self.data.getList("""
                                        select 

                                            sum(s.NavlunSatis) as NavlunSatis

                                        from
                                        SiparislerTB s

                                        where YEAR(s.YuklemeTarihi) =YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) = MONTH(GETDATE()) and s.FaturaKesimTurID = 2

                                        group by MONTH(s.YuklemeTarihi)
                                   
                                   
                                   """)
        if len(result) ==0:
            return 0
        else:
            return result[0].NavlunSatis
    def __efesYuklenenYillikNavlun(self):
        result = self.data.getList("""
                                        select 

                                        sum(s.NavlunSatis) as NavlunSatis

                                    from
                                    SiparislerTB s

                                    where YEAR(s.YuklemeTarihi) =YEAR(GETDATE()) and MONTH(s.YuklemeTarihi) <= MONTH(GETDATE() - 1) and s.FaturaKesimTurID = 2

                                    group by YEAR(s.YuklemeTarihi)
                                   
                                   """)
        
        if len(result) == 0:
            return 0
        else:
            return result[0].NavlunSatis
    
    
    
    ##########Grafikler#########
    def getsiparisGrafikRapor(self):

        try:
            result = self.data.getList("""
                                        select 
                                            sum(su.SatisToplam) as SatisToplam,
                                            MONTH(s.YuklemeTarihi) as Ay
                                        from SiparislerTB s
                                            inner join MusterilerTB m on m.ID = s.MusteriID
                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi)=YEAR(GETDATE())  and m.Marketing='Mekmar'

                                        group by
                                            MONTH(s.YuklemeTarihi)
                                        order by
                                            MONTH(s.YuklemeTarihi)
                                       
                                       """)
            result2 = self.data.getList("""
                                        select 
                                            sum(su.SatisToplam) as SatisToplam,
                                            MONTH(s.YuklemeTarihi) as Ay
                                        from SiparislerTB s
                                            inner join MusterilerTB m on m.ID = s.MusteriID
                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi)=(YEAR(GETDATE()) -1) and MONTH(s.YuklemeTarihi)<= MONTH(GETDATE()) and m.Marketing='Mekmar'

                                        group by
                                            MONTH(s.YuklemeTarihi)
                                        order by
                                            MONTH(s.YuklemeTarihi)
                                       
                                       """)
            
            dataset = [
                
            ]
            data1 = [
                
            ]
            data2 = [
                
            ]

            if len(result)>0:
                for item in result:
                    r = int(item.SatisToplam) + self.__getGrafikMekmarBuYilNavlun(item.Ay)
                    data1.append(r)
            else:
                r = 0
                data1.append(r)
            if len(result2)>0:
                for item2 in result2:
                    l = int(item2.SatisToplam)+ self.__getGrafikMekmarGecenYilNavlun(item2.Ay)
                    data2.append(l)
            else:
                r = 0
                data1.append(r)
            dataset.append({
                'label':'Shipped 2024 (DDP)',
                'backgroundColor': '#2f4860',
                'data':data1,
                'fiil' : False,
                'borderColor': '#2f4860'
            },)
            dataset.append({
                'label':'Shipped 2023 (DDP)',
                'backgroundColor': '#00bb7e',
                'data':data2,
                'fiil' : False,
                'borderColor': '#00bb7e'
            })
            
            basicDatas = {
                
                'labels':['January','February','March','April','May','June','July','August','September','October','November','December'],
                'datasets':dataset
            }
            return basicDatas
                
        except Exception as e:
            print('getsiparisGrafikRapor hata',str(e))
            return False
    def getsiparisGrafikRaporHepsi(self):
        try:
            result = self.data.getList("""
                                        select 
                                            sum(su.SatisToplam) as SatisToplam,
                                            MONTH(s.YuklemeTarihi) as Ay
                                        from SiparislerTB s

                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi)=YEAR(GETDATE())

                                        group by
                                            MONTH(s.YuklemeTarihi)
                                       
                                       """)
            result2 = self.data.getList("""
                                        select 
                                            sum(su.SatisToplam) as SatisToplam,
                                            MONTH(s.YuklemeTarihi) as Ay
                                        from SiparislerTB s

                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi)=(YEAR(GETDATE()) - 1) and MONTH(s.YuklemeTarihi)<= MONTH(GETDATE()) 

                                        group by
                                            MONTH(s.YuklemeTarihi)
                                       
                                       """)
            
            dataset = [
                
            ]
            data1 = [
                
            ]
            data2 = [
                
            ]
            if len(result)>0:
                
                for item in result:
                    data1.append(int(item.SatisToplam) + self.__getGrafikAllBuYilNavlun(item.Ay))
            else:
                data1.append(0)
            if len(result2)>0:
                for item2 in result2:
                    data2.append(int(item2.SatisToplam) + self.__getGrafikAllGecenYilNavlun(item2.Ay))
                    
            else:
                data1.append(0)
            dataset.append({
                'label':'Yüklenen 2024',
                'backgroundColor': '#2f4860',
                'data':data1,
                'fiil' : False,
                'borderColor': '#2f4860'
            },)
            dataset.append({
                'label':'Yüklenen 2023',
                'backgroundColor': '#00bb7e',
                'data':data2,
                'fiil' : False,
                'borderColor': '#00bb7e'
            })
            
            basicDatas = {
                
                'labels':['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'],
                'datasets':dataset
            }
            return basicDatas
                
        except Exception as e:
            print('getsiparisGrafikRapor2 hata',str(e))
            return False

    def getSiparisGrafikYuklenenvSiparis(self):
        buyilsiparis = self.data.getList("""
                                        select 
                                            sum(su.SatisToplam) as SatisToplam
                                        from SiparislerTB s

                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                            inner join MusterilerTB m on m.ID = s.MusteriID

                                        where YEAR(s.SiparisTarihi)=YEAR(GETDATE()) and m.Marketing='Mekmar'

                                        group by
                                            YEAR(s.SiparisTarihi)
                                   """)
        buyilyuklenen = self.data.getList("""
                                            select 
                                            sum(su.SatisToplam) as SatisToplam
                                        from SiparislerTB s

                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                            inner join MusterilerTB m on m.ID = s.MusteriID

                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi)=YEAR(GETDATE()) and m.Marketing='Mekmar'

                                        group by
                                            YEAR(s.YuklemeTarihi)
                                        
                                        """)
        buyilyuklenenNavlun = self.data.getList("""
                                                    select 
                                                    sum(s.NavlunSatis) + sum(s.DetayTutar_1) + sum(s.DetayTutar_2) + sum(s.DetayTutar_3)  as NavlunSatis
                                                    from 
                                                    SiparislerTB s
													inner join MusterilerTB m on m.ID = s.MusteriID
                                                    where YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) and m.Marketing='Mekmar' and s.SiparisDurumID=3
                                                    group by 
                                                        YEAR(s.YuklemeTarihi)
                                                """)
        
        gecenyilsiparis = self.data.getList("""
                                        select 
                                            sum(su.SatisToplam) as SatisToplam
                                            from 
                                            SiparislerTB s
                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                            inner join MusterilerTB m on m.ID = s.MusteriID
                                            where YEAR(s.SiparisTarihi) = YEAR(GETDATE()) - 1 and m.Marketing='Mekmar'
                                            group by 
                                                YEAR(s.SiparisTarihi)
                                   """)

        gecenyilyuklenen = self.data.getList("""
                                            select 
                                            sum(su.SatisToplam) as SatisToplam
                                        from SiparislerTB s

                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                            inner join MusterilerTB m on m.ID = s.MusteriID

                                        where s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi)=YEAR(GETDATE()) - 1 and m.Marketing='Mekmar'

                                        group by
                                            YEAR(s.YuklemeTarihi)
                                        
                                        """)
        
        gecenyilyuklenenNavlun = self.data.getList("""
                                                    select 
                                                    sum(s.NavlunSatis) + sum(s.DetayTutar_1) + sum(s.DetayTutar_2) + sum(s.DetayTutar_3) + sum(s.DetayTutar_4)  as NavlunSatis
                                                    from 
                                                    SiparislerTB s
                                                    inner join MusterilerTB m on m.ID = s.MusteriID
                                                    where YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) - 1 and m.Marketing='Mekmar' and s.SiparisDurumID=3
                                                    group by 
                                                        YEAR(s.YuklemeTarihi)
                                                """)

        if len(buyilsiparis) == 0:
            buYilSipTop = 0
        else:
            buYilSipTop = float(buyilsiparis[0].SatisToplam)
        if len(buyilyuklenen) <= 0:
            
            buYilYukTop = 0
        else:
            buYilYukTop = float(buyilyuklenen[0].SatisToplam) + float(buyilyuklenenNavlun[0].NavlunSatis)
            
        gecenYilSipTop = float(gecenyilsiparis[0].SatisToplam)
        gecenYilYukTop = float(gecenyilyuklenen[0].SatisToplam) + float(gecenyilyuklenenNavlun[0].NavlunSatis)
        return buYilSipTop,buYilYukTop,gecenYilSipTop,gecenYilYukTop

    def __getGrafikMekmarBuYilNavlun(self,ay):
        for i in self.grafikMekmarNavlunBuYil:
            if i.Ay == ay:
                return int(i.NavlunSatis)
    def __getGrafikMekmarGecenYilNavlun(self,ay):
        for i in self.grafikMekmarNavlunGecenYil:
            if i.Ay == ay:
                return int(i.NavlunSatis)
    def __getGrafikAllBuYilNavlun(self,ay):
        for i in self.grafikHepsiNavlunBuYil:
            if i.Ay == ay:
                return int(i.NavlunSatis)

    def __getGrafikAllGecenYilNavlun(self,ay):
        for i in self.grafikHepsiNavlunGecenYil:
            if i.Ay == ay:
                return int(i.NavlunSatis)
    def getMonth(self,monthId):
        data = {
            1:'January',
            2:'February',
            3:'March',
            4:'April',
            5:'May',
            6:'June',
            7:'July',
            8:'August',
            9:'September',
            10:'October',
            11:'November',
            12:'December'
        }
        return data[monthId]
    
    def getDashboardKonteynir(self):
        try:
            result = self.data.getList("""
                                            select 
                                                s.SiparisNo as SiparisNo,
                                                m.FirmaAdi as FirmaAdi,
                                                s.Line as Line,
                                                s.YuklemeTarihi as YuklemeTarihi,
                                                s.SiparisTarihi as SiparisTarihi,
                                                s.KonteynerNo as KonteynirNo,
                                                s.Eta as Eta,
                                                s.NavlunFirma as NavlunFirma,
                                                ((select sum(su.SatisToplam) from SiparisUrunTB su where su.SiparisNo = s.SiparisNo) + s.NavlunSatis + s.DetayTutar_1 + s.DetayTutar_2 + s.DetayTutar_3) as DDP,
                                                (select sum(o.Tutar) from OdemelerTB o where o.SiparisNo = s.SiparisNo) as Odenen
                                            from 
                                                SiparislerTB s
                                                inner join MusterilerTB m on m.ID = s.MusteriID 
                                            where 
                                                    m.Marketing in ('Mekmar')  and s.SiparisDurumID=3 and YEAR(s.YuklemeTarihi) in (YEAR(GETDATE()),YEAR(GETDATE()) -1)
                                            order by s.YuklemeTarihi desc
                                       """)
            
            liste = list()
            for item in result:
                if item.FirmaAdi =='BD-2019 ve Oncesi' or item.FirmaAdi=='BSAD - Ghana' or item.FirmaAdi=='BD-AMES' or item.FirmaAdi=='Tamer ($)' or item.FirmaAdi=='Balogun - Nigeria' or item.FirmaAdi=='Mantej - Australia':
                    continue
                else:
                    if item.Odenen != None:
                        if (item.DDP - item.Odenen) > 10:      
                            model = SiparislerKonteynirModel()
                            model.firmaAdi = item.FirmaAdi
                            model.siparisNo = item.SiparisNo
                            model.line = item.Line
                            model.yuklemeTarihi = item.YuklemeTarihi
                            model.siparisTarihi = item.SiparisTarihi
                            model.konteynirNo = item.KonteynirNo
                            if item.Eta != None:
                                model.etaTarihi = item.Eta
                            else:
                                model.etaTarihi = ""
                            model.navlunFirma = item.NavlunFirma
                            model.kalan = item.DDP - item.Odenen
                            liste.append(model)
                        else:
                            continue
                    else:
                        if item.SiparisNo == '22KET01 - 3':
                            continue
                        else:
                            
                            if item.DDP >10 :
                                model = SiparislerKonteynirModel()
                                model.firmaAdi = item.FirmaAdi
                                model.siparisNo = item.SiparisNo
                                model.line = item.Line
                                model.yuklemeTarihi = item.YuklemeTarihi
                                model.siparisTarihi = item.SiparisTarihi
                                model.konteynirNo = item.KonteynirNo
                                if item.Eta != None:
                                    model.etaTarihi = item.Eta
                                else:
                                    model.etaTarihi = ""
                                model.navlunFirma = item.NavlunFirma
                                model.kalan = item.DDP
                                liste.append(model)
                            else:
                                continue
                
            schema = SiparislerKonteynirSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardKonteynir',str(e))
            return False
    
    def getDashboardFinans(self):
        try:
            result = self.data.getList("""
                                            select 

                                                sum(su.SatisToplam) as SatisToplam,
                                                s.SiparisNo as SiparisNo,
                                                m.FirmaAdi as Musteri,
                                                s.SiparisDurumID as SiparisDurum,
                                                k.KullaniciAdi as SiparisSahibi,
                                                kt.KullaniciAdi as Operasyon
                                            from 
                                                SiparislerTB s
                                                inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                inner join MusterilerTB m on m.ID = s.MusteriID
                                                inner join KullaniciTB k on k.ID = s.SiparisSahibi
                                                inner join KullaniciTB kt on kt.ID = s.Operasyon
                                            where m.Marketing='Mekmar' and s.SiparisDurumID=3
                                            
                                            group by
                                                su.SiparisNo,s.SiparisNo,m.FirmaAdi,s.SiparisDurumID,k.KullaniciAdi,kt.KullaniciAdi 
                                            order by 
                                                s.SiparisDurumID desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = FinansTakipListesiModel()
                model.musteriAdi = item.Musteri
                model.siparisNo = item.SiparisNo
                model.siparisDurum = self.__getSiparisDurum(item.SiparisDurum)
                model.odenen = self.__getSiparisOdenenTutar(item.SiparisNo)
                model.satisToplami = float(item.SatisToplam) + self.__getNavlun(item.SiparisNo)
                model.siparisSahibi = item.SiparisSahibi
                model.operasyon = item.Operasyon
                if model.odenen == None:
                    model.kalanBedel = self.__kalan(model.satisToplami, 0)
                else:
                    model.kalanBedel = self.__kalan(model.satisToplami, model.odenen)
                liste.append(model)
            schema = FinansTakipListesiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardFinans',str(e))
    def getDashboardTedarikci(self):
        try:
            result = self.data.getList("""
                                            select 

                                                sum(su.SatisToplam) as SatisToplami,
                                                t.FirmaAdi as Tedarikci,
                                                sum(su.Miktar) as Miktar,
                                                t.ID as TedarikciID
                                            from SiparislerTB s
                                            inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo
                                            inner join TedarikciTB t on t.ID = su.TedarikciID
											inner join MusterilerTB m on m.ID = s.MusteriID
                                            where YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) and m.Marketing='Mekmar'
                                            group by 
                                                YEAR(su.TedarikciID),t.FirmaAdi,t.ID

                                            order by SatisToplami desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = TedarikciListesiModel()
                model.tedarikci = item.Tedarikci
                model.satisToplam = item.SatisToplami
                model.satisMiktar = item.Miktar
                model.tedarikci_id = item.TedarikciID
                liste.append(model)
            schema = TedarikciListesiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardTedarikci',str(e))
            
    def getDashboardTedarikciSiparisler(self):
        try:
            result = self.data.getList("""
                                            select 

                                                sum(su.SatisToplam) as SatisToplami,
                                                t.FirmaAdi as Tedarikci,
                                                sum(su.Miktar) as Miktar,
                                                t.ID as TedarikciID
                                            from SiparislerTB s
                                            inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo
                                            inner join TedarikciTB t on t.ID = su.TedarikciID
                                            inner join MusterilerTB m on m.ID = s.MusteriID
                                            where YEAR(s.SiparisTarihi) = YEAR(GETDATE()) and m.Marketing='Mekmar'
                                            group by 
                                                YEAR(su.TedarikciID),t.FirmaAdi,t.ID

                                            order by SatisToplami desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = TedarikciListesiModel()
                model.tedarikci = item.Tedarikci
                model.satisToplam = item.SatisToplami
                model.satisMiktar = item.Miktar
                model.tedarikci_id = item.TedarikciID
                liste.append(model)
            schema = TedarikciListesiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardTedarikciSiparisler',str(e))

    def getDashboardMusteriSiparisleri(self):
        try:
            result = self.data.getList("""
                                            select 

                                            sum(su.SatisToplam) as SatisToplami,
                                            sum(su.Miktar) as Miktar,
                                            m.FirmaAdi as Musteri,
                                            m.ID as MusteriID   

                                            from SiparislerTB s
                                            inner join SiparisUrunTB su on su.SiparisNo=s.SiparisNo
                                            inner join MusterilerTB m on m.ID = s.MusteriID
                                            where YEAR(s.SiparisTarihi) = YEAR(GETDATE()) and m.Marketing='Mekmar'
                                            group by 
                                            s.MusteriID,m.FirmaAdi,m.ID

                                            order by SatisToplami desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = TedarikciListesiModel()
                model.tedarikci = item.Musteri
                model.satisToplam = item.SatisToplami
                model.satisMiktar = item.Miktar
                model.firmaId = item.MusteriID
                liste.append(model)
            schema = TedarikciListesiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardTedarikciSiparisler',str(e))
    
    def getDashboardTeklifler(self):
        try:
            result = self.data.getList("""
                                            select


                                            count(t.KullaniciID) as TeklifSayisi,
                                            k.KullaniciAdi as TeklifSahibi,
											k.ID as TeklifSahibiId


                                        from YeniTeklifTB t
                                        inner join KullaniciTB k on k.ID = t.KullaniciID
                                        where YEAR(t.Tarih) = YEAR(GETDATE()) and MONTH(t.Tarih)= MONTH(GETDATE()) and t.TakipEt=1
                                        group by t.KullaniciID,k.KullaniciAdi,k.ID
                                        order by TeklifSayisi desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = TeklifListesiModel()
                model.teklifSayisi = item.TeklifSayisi
                model.teklifSahibi = item.TeklifSahibi
                model.teklifSahibiId = item.TeklifSahibiId
                liste.append(model)
            schema = TeklifListesiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardTeklifler',str(e))
    def getDashboardTekliflerYillik(self):
        try:
            result = self.data.getList("""
                                            select


                                            count(t.KullaniciID) as TeklifSayisi,
                                            k.KullaniciAdi as TeklifSahibi,
                                            k.ID as TeklifSahibiId


                                        from YeniTeklifTB t
                                        inner join KullaniciTB k on k.ID = t.KullaniciID
                                        where YEAR(t.Tarih) = YEAR(GETDATE()) 
                                        group by t.KullaniciID,k.KullaniciAdi,k.ID
                                        order by TeklifSayisi desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = TeklifListesiModel()
                model.teklifSayisi = item.TeklifSayisi
                model.teklifSahibi = item.TeklifSahibi
                model.teklifSahibiId = item.TeklifSahibiId
                liste.append(model)
            schema = TeklifListesiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardTekliflerYillik',str(e))

    def getDashboardSonSiparisler(self):
        try:
            result = self.data.getList("""
                                            select
                                                sum(su.SatisToplam) as SatisToplami,
                                                s.SiparisNo as SiparisNo,
                                                k.KullaniciAdi as Satisci,
                                                (select COUNT(*) from SiparisFaturaKayitTB  f where f.SiparisNo=s.SiparisNo and YuklemeEvrakID=2 ) as Evrak
                                            from
                                            SiparislerTB s
                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                            inner join KullaniciTB k on k.ID = s.SiparisSahibi
                                            where YEAR(s.SiparisTarihi) = YEAR(GETDATE()) and MONTH(s.SiparisTarihi) = MONTH(GETDATE()) and s.SiparisDurumID=2
                                            group by
                                                s.SiparisNo,s.SiparisNo,DAY(s.SiparisTarihi),k.KullaniciAdi
                                            order by DAY(s.SiparisTarihi) desc
                                       
                                       
                                       """)  
            liste = list()
            for item in result:
                model = SonEklenenSiparislerModel()
                model.siparisNo = item.SiparisNo
                model.satisci = item.Satisci
                model.satisToplami = item.SatisToplami
                model.link =  f"https://file-service.mekmar.com/file/download/2/{item.SiparisNo}"
                model.evrakDurum = item.Evrak
                liste.append(model)
            schema = SonEklenenSiparislerSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getDashboardSonSiparisler',str(e))
    
    
    
    
    def __getSiparisDurum(self,sipDurum):
        if sipDurum == 1:
            return 'Bekleyen'
        elif sipDurum == 2:
            return 'Üretim'
        elif sipDurum ==3:
            return 'Sevk'
        
    def __getSiparisOdenenTutar(self,siparisNo):
        for item in self.odemeler:
            if item.SiparisNo == siparisNo:
                return float(item.OdenenTutar)     
    def __getNavlun(self,siparisNo):
        for item in self.navlun:
            if item.SiparisNo == siparisNo:
                val = float(item.Navlun) + float(item.Detay1) + float(item.Detay2) + float(item.Detay3)
                return val      
    
    def __kalan(self,sipToplami,odenen):
        return float(sipToplami) - float(odenen)
    
    #############################Dashboard Ayrıntı Bölmesi###################################
    
    def getTedarikciAyrinti(self,tedarikciId):
        try:
            result = self.data.getStoreList("""
                                                select 

                                                    sum(su.SatisToplam) as Toplam,
                                                    m.FirmaAdi as Musteri,
                                                    s.SiparisNo as SiparisNo,
                                                    sum(su.Miktar) as Miktar
                                                from 
                                                    SiparislerTB s 
                                                    inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                    inner join MusterilerTB m on m.ID = s.MusteriID

                                                where
                                                    YEAR(s.YuklemeTarihi) = YEAR(GETDATE()) and su.TedarikciID=? and m.Marketing='Mekmar'

                                                group by
                                                    s.SiparisNo,m.FirmaAdi
                                            
                                            
                                            """,(tedarikciId))
            liste = list()
            for item in result:
                model = TedarikciAyrintiModel()
                model.siparisNo = item.SiparisNo
                model.firmaAdi = item.Musteri
                model.satisMiktari = item.Miktar
                model.satisToplami = item.Toplam
                liste.append(model)
            schema = TedarikciAyrintiSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getTedarikciAyrinti hata',str(e))
            return False
        
    def getTedarikciAyrintiAll(self,tedarikciId):
        try:
            result = self.data.getStoreList("""
                                                select 

                                                    sum(su.SatisToplam) as Toplam,
                                                    m.FirmaAdi as Musteri,
                                                    s.SiparisNo as SiparisNo,
                                                    sum(su.Miktar) as Miktar
                                                from 
                                                    SiparislerTB s 
                                                    inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                    inner join MusterilerTB m on m.ID = s.MusteriID

                                                where
                                                    YEAR(s.SiparisTarihi) = YEAR(GETDATE()) and su.TedarikciID=? and m.Marketing='Mekmar'

                                                group by
                                                    s.SiparisNo,m.FirmaAdi
                                            
                                            
                                            """,(tedarikciId))
            liste = list()
            for item in result:
                model = TedarikciAyrintiModel()
                model.siparisNo = item.SiparisNo
                model.firmaAdi = item.Musteri
                model.satisMiktari = item.Miktar
                model.satisToplami = item.Toplam
                liste.append(model)
            schema = TedarikciAyrintiSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getTedarikciAyrintiAll hata',str(e))
            return False
        
        
    def getFirmaBazindaAyrintiSiparis(self,firmaId):
        try:
            result = self.data.getStoreList("""
                                        select
	
                                            sum(su.SatisToplam) as SatisToplami,
                                            sum(su.Miktar) as SatisMiktari,
                                            s.SiparisNo as SiparisNo
                                            
                                        from
                                            SiparislerTB s
                                            inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo

                                        where YEAR(s.SiparisTarihi) = YEAR(GETDATE()) and s.MusteriID=? 

                                        group by s.MusteriID,s.SiparisNo
                                   
                                   """,(firmaId))
            liste = list()
            for item in result:
                model = FirmaBazindaAyrintiModel()
                model.siparisNo = item.SiparisNo
                model.satisToplami = item.SatisToplami
                model.satisMiktari = item.SatisMiktari
                liste.append(model)
            schema = FirmaBazindaAyrintiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getFirmaBazindaAyrintiSiparis hata',str(e))
            return False
        
    def getTeklifAyrintiAylik(self,satisciId):
        try:
            result = self.data.getStoreList("""
                                                select 
                                                t.Tarih as Tarih,
                                                ym.MusteriAdi as Musteri,
                                                t.KaynakYeri as KaynakYeri,
                                                t.Aciklama as Aciklama
                                                from 
                                                YeniTeklifTB t 
                                                inner join YeniTeklif_MusterilerTB ym on ym.Id = t.MusteriId
                                                where t.KullaniciId=? and YEAR(t.Tarih) = YEAR(GETDATE()) and MONTH(t.Tarih) = MONTH(GETDATE()) and t.TakipEt=1
                                            """,(satisciId))
            liste = list()
            for item in result:
                model = TeklifAyrintiModel()
                model.tarih = item.Tarih
                model.musteri = item.Musteri
                model.kaynakYeri = item.KaynakYeri
                model.aciklama = item.Aciklama
                liste.append(model)
            schema = TeklifAyrintiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getTeklifAyrintiAylik hata',str(e))
            return False
        
    def getTeklifAyrintiYillik(self,satisciId):
        try:
            result = self.data.getStoreList("""
                                                select 
                                                t.Tarih as Tarih,
                                                ym.MusteriAdi as Musteri,
                                                t.KaynakYeri as KaynakYeri,
                                                t.Aciklama as Aciklama
                                                from 
                                                YeniTeklifTB t 
                                                inner join YeniTeklif_MusterilerTB ym on ym.Id = t.MusteriId
                                                where t.KullaniciId=? and YEAR(t.Tarih) = YEAR(GETDATE())
                                            """,(satisciId))
            liste = list()
            for item in result:
                model = TeklifAyrintiModel()
                model.tarih = item.Tarih
                model.musteri = item.Musteri
                model.kaynakYeri = item.KaynakYeri
                model.aciklama = item.Aciklama
                liste.append(model)
            schema = TeklifAyrintiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getTeklifAyrintiAylik hata',str(e))
            return False
    
    def getUlkeTeklifler(self,year):
        try:
            result  = self.data.getStoreList("""
                                                select 

                                                    count(yu.Id) as ToplamTeklif,
                                                    yu.UlkeAdi as UlkeAdi,
													yu.Id as UlkeID


                                                from YeniTeklifTB yt
                                                    inner join YeniTeklif_MusterilerTB ym on ym.Id = yt.MusteriId
                                                    inner join YeniTeklif_UlkeTB yu on yu.Id = ym.UlkeId
                                                where YEAR(yt.Tarih)=?
                                                group by 
                                                    yu.Id,yu.UlkeAdi
                                             
                                             """,(year))
            liste = list()
            for item in result:
                model = TeklifUlkeyeGoreModel()
                model.ulkeAdi = item.UlkeAdi
                model.topTeklif = item.ToplamTeklif
                model.ulkeId = item.UlkeID
                liste.append(model)
            schema = TeklifUlkeyeGoreSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print('getUlkeTeklifler',str(e))
            return False
    
    
    def getUlkeTekliflerAyrinti(self,year,ulkeId):
        try:
            result  = self.data.getStoreList("""
                                                select

                                                yt.Id as TeklifId,
                                                k.KullaniciAdi as TeklifSahibi,
                                                ym.MusteriAdi as MusteriAdi,
                                                yu.UlkeAdi as Ulke,
                                                yt.Sira as TeklifNo,
                                                yt.Tarih as TeklifTarihi
                                                from
                                                YeniTeklifTB yt 
                                                inner join YeniTeklif_MusterilerTB ym on ym.Id = yt.MusteriId
                                                inner join YeniTeklif_UlkeTB yu on yu.Id = ym.UlkeId
                                                inner join KullaniciTB k on k.ID = yt.KullaniciId

                                                where 
                                                YEAR(yt.Tarih) = ? and yu.Id=?
                                             
                                             """,(year,ulkeId))
            liste = list()
            for item in result:
                model = TeklifUlkeyeGoreAyrintiModel()
                model.teklifId = item.TeklifId
                model.teklifNo = item.TeklifNo
                model.tarih = item.TeklifTarihi
                model.kullaniciAdi = item.TeklifSahibi
                model.musteriAdi = item.MusteriAdi
                liste.append(model)
            schema = TeklifUlkeyeGoreAyrintiSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print('getUlkeTekliflerAyrinti',str(e))
            return False
    