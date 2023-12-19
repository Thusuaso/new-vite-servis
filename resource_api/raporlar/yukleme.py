from helpers import SqlConnect,TarihIslemler
from models.raporlar import YuklemeAySchema,YuklemeAyModel, YuklemeyilSchema,YuklemeYilModel,YuklemeAylikSchema,YuklemeAylikModel,YuklemeYillikSchema,YuklemeYillikModel,SayimYillikSchema,SayimYillikModel,SayimAylikModel,SayimAylikSchema



class YuklemeListeler:

    def __init__(self):

        self.data = SqlConnect().data
        self.satislarsql = []
        self.masraflarsql = []
        self.satislarDetaySql = []
    
    
    def getYuklemeRaporAylik(self,yil,ay):

        result = self.data.getStoreList(
            """
            select  
            s.YuklemeTarihi,  
            s.SiparisNo,  
            m.FirmaAdi as MusteriAdi,  
            (select Sum(SatisToplam) from SiparisUrunTB su where su.SiparisNo=s.SiparisNo) as Fob,  
            (select Sum(SatisToplam) from SiparisUrunTB su where su.SiparisNo=s.SiparisNo)+  
            dbo.Get_SiparisNavlun(s.SiparisNo) as Dtp,  
            'Konteyner' as Tur,m.Marketing  
            from  
            SiparislerTB s,MusterilerTB m  
            where Year(YuklemeTarihi)=?
            and Month(YuklemeTarihi)=?
            and m.ID=s.MusteriID  
            and m.Marketing not in ('Mekmar Numune','Seleksiyon','Warehouse')  
            and m.Marketing is not null  
             
            union  
            select  
            s.Tarih as YuklemeTarihi,  
            s.CikisNo as SiparisNo,  
            m.FirmaAdi as MusteriAdi,  
            Sum(Toplam) as Fob  
            ,Sum((s.BirimFiyat+7.5)*u.Miktar) as Dtp,  
            'Depo' as Tur,m.Marketing  
            from  
            SevkiyatTB s,MusterilerTB m,UretimTB u  
            where s.MusteriID=m.ID and u.KasaNo=s.KasaNo  
            and Year(s.Tarih)=? and Month(s.Tarih)=?
            and m.Mt_No=1  
            group by  
            s.Tarih,s.CikisNo,m.FirmaAdi,m.Marketing  
            
            """,(yil,ay,yil,ay)
        ) 

        liste = list()

        for item in result:
            model = YuklemeAylikModel()
            model.yukleme_tarihi = item.YuklemeTarihi
            model.siparis_no = item.SiparisNo
            model.musteri_adii = item.MusteriAdi
            model.fob = item.Fob
            model.dtp = item.Dtp
            model.tur = item.Tur
            model.marketing = item.Marketing
            liste.append(model)

        schema = YuklemeAylikSchema(many=True)

        return sorted(schema.dump(liste), key=lambda x:x['dtp'],reverse=True)

    
    def getYuklemeRaporuYillik(self,yil):

        result = self.data.getStoreList(
            """
            select  
            s.YuklemeTarihi,  
            s.SiparisNo,  
            m.FirmaAdi as MusteriAdi,  
            (select Sum(SatisToplam) from SiparisUrunTB su where su.SiparisNo=s.SiparisNo) as Fob,  
            (select Sum(SatisToplam) from SiparisUrunTB su where su.SiparisNo=s.SiparisNo)+  
            dbo.Get_SiparisNavlun(s.SiparisNo) as Dtp,  
            'Konteyner' as Tur,m.Marketing  
            from  
            SiparislerTB s,MusterilerTB m  
            where Year(YuklemeTarihi)=?
            and m.ID=s.MusteriID  
            and m.Marketing not in ('Mekmar Numune','Seleksiyon','Warehouse')  
            and m.Marketing is not null  
             
            union  
            select  
            s.Tarih as YuklemeTarihi,  
            s.CikisNo as SiparisNo,  
            m.FirmaAdi as MusteriAdi,  
            Sum(Toplam) as Fob  
            ,Sum((s.BirimFiyat+7.5)*u.Miktar) as Dtp,  
            'Depo' as Tur,m.Marketing  
            from  
            SevkiyatTB s,MusterilerTB m,UretimTB u  
            where s.MusteriID=m.ID and u.KasaNo=s.KasaNo  
            and Year(s.Tarih)=?
            and m.Mt_No=1  
            group by  
            s.Tarih,s.CikisNo,m.FirmaAdi,m.Marketing 
            
            """,(yil,yil)
        ) 

        liste = list()

        for item in result:
            model = YuklemeAylikModel()
            model.yukleme_tarihi = item.YuklemeTarihi
            model.siparis_no = item.SiparisNo
            model.musteri_adii = item.MusteriAdi
            model.fob = item.Fob
            model.dtp = item.Dtp
            model.tur = item.Tur
            model.marketing = item.Marketing
            liste.append(model)

        schema = YuklemeAylikSchema(many=True)

        return sorted(schema.dump(liste), key=lambda x:x['dtp'],reverse=True)
    
    
    
    
    def getYuklemeRaporAylikMusteriBazinda(self,yil,ay):

        result = self.data.getStoreList(
            """
             select  
                 m.ID as MusteriId,  
                 m.FirmaAdi as MusteriAdi,  
                  m.Marketing, 
				  
				(  
                   Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo  
                   and s.SiparisDurumID=3 and s.MusteriID=m.ID and Year(YuklemeTarihi)=?  and MONTH(YuklemeTarihi) =?  and s.SiparisDurumID=3
                ) 
                    
                as Fob, 
                
                (  
                   Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo  
                   and s.SiparisDurumID=3 and s.MusteriID=m.ID and Year(YuklemeTarihi)=? and MONTH(YuklemeTarihi) =?  and s.SiparisDurumID=3
                )  +  
                (  
                    Select Sum(s.NavlunSatis + s.DetayTutar_1 + s.DetayTutar_2 + s.DetayTutar_3 ) from SiparislerTB s  
                    where s.MusteriID=m.ID and YEAR(s.YuklemeTarihi)=? and MONTH(s.YuklemeTarihi) =?  and s.SiparisDurumID=3
                )  
                    
                as Dtp 
               
                from  
                MusterilerTB m,YeniTeklif_UlkeTB u  
                where 
                u.Id = m.UlkeId  
                order by  m.FirmaAdi asc
            """,(yil,ay,yil,ay,yil,ay)
        ) 

        liste = list()

        for item in result:
            model = YuklemeAylikModel()
           
            if item.Fob != None and item.Fob !=0 :

                model.musteri_adii = item.MusteriAdi
            
                model.fob = item.Fob
                model.dtp = item.Dtp
            
                model.marketing = item.Marketing
                liste.append(model)

        schema = YuklemeAylikSchema(many=True)

        return sorted(schema.dump(liste), key=lambda x:x['dtp'],reverse=True)

    def getYuklemeRaporYillik(self,yil,ay):

        result = self.data.getStoreList(
            """
             select  
                 m.ID as MusteriId,  
                 m.FirmaAdi as MusteriAdi,  
                  m.Marketing, 
				  
				(  
                   Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo  
                   and s.SiparisDurumID=3 and s.MusteriID=m.ID and Year(YuklemeTarihi)=?  and MONTH(YuklemeTarihi) <=?  and s.SiparisDurumID=3
                ) 
                    
                as Fob, 
                
                (  
                   Select Sum(SatisToplam) from SiparislerTB s, SiparisUrunTB u where s.SiparisNo=u.SiparisNo  
                   and s.SiparisDurumID=3 and s.MusteriID=m.ID and Year(YuklemeTarihi)=? and MONTH(YuklemeTarihi) <=?  and s.SiparisDurumID=3
                )  +  
                (  
                    Select Sum(s.NavlunSatis + s.DetayTutar_1 + s.DetayTutar_2 + s.DetayTutar_3 ) from SiparislerTB s  
                    where s.MusteriID=m.ID and YEAR(s.YuklemeTarihi)=? and MONTH(s.YuklemeTarihi) <=?  and s.SiparisDurumID=3
                )  
                    
                as Dtp 
               
                from  
                MusterilerTB m,YeniTeklif_UlkeTB u  
                where 
                u.Id = m.UlkeId  
               
            """,(yil,ay,yil,ay,yil,ay)
        ) 
        
        liste = list()
         
       
        for item in result:
          
            model = YuklemeYillikModel()
           
            if item.Fob != None and item.Fob !=0 :

                model.musteri_adi = item.MusteriAdi
            
                model.fob = item.Fob
                model.dtp = item.Dtp
            
                model.marketing = item.Marketing
                liste.append(model)

        schema = YuklemeYillikSchema(many=True) 

        return sorted(schema.dump(liste), key=lambda x:x['dtp'],reverse=True)

    def __getYuklemeSayimAylik(self,yil,ay):

        result = self.data.getStoreList(
            """
            
            select m.Marketing,count(*) as YuklemeSayisi from   
            MusterilerTB m,SiparislerTB s  
            where   
            m.Marketing is not null  
           and  m.Marketing != 'Seleksiyon'
            and m.ID = s.MusteriID and s.SiparisDurumID=3  
            and Year(s.YuklemeTarihi)=?
            and Month(s.YuklemeTarihi)=?
            group by Marketing  

            """,(yil,ay)
        ) 

        liste = list()

        for item in result:
            model = SayimAylikModel()
            model.marketing = item.Marketing
            model.yukleme_sayisi = item.YuklemeSayisi
            
            liste.append(model)

        schema = SayimAylikSchema(many=True)

        return schema.dump(liste)
           
    def getYuklemeSayimYillik(self,yil,ay):

        result = self.data.getStoreList(
            """
            
          select m.Marketing,count(*) as YuklemeSayisi from   
            MusterilerTB m,SiparislerTB s  
            where   
            m.Marketing is not null  
            and m.Marketing != 'Seleksiyon'  
            and m.ID = s.MusteriID and s.SiparisDurumID=3  
            and Year(s.YuklemeTarihi)=?
            and Month(s.YuklemeTarihi)<=?
            group by Marketing  

            """,(yil,ay)
        ) 

        liste = list()
        aylist = self.__getYuklemeSayimAylik(yil,ay)
        i = 0
        j = len(aylist) -1      
        
        for item in result:
            model = SayimYillikModel()
            model.marketing = item.Marketing
            model.yukleme_sayisi = item.YuklemeSayisi
            i = 0  
            for key in aylist:
              if model.marketing == aylist[i]['marketing']:
                 model.yukleme_sayisiay = aylist[i]['yukleme_sayisi']
              if i <= j :  i +=1
                  
            liste.append(model)
        schema = SayimYillikSchema(many=True)
       
        return schema.dump(liste)

    def getAyListesi(self,yil):

        result = self.data.getStoreList(
            """
         select  
            ROW_NUMBER() over (order by Month(Tarih) desc) as ID,  
            Month(Tarih) as Ay,  
            DATENAME(Month,Tarih) as AyIsim  
            from  
            SevkiyatTB  
            where  
            Year(Tarih)=?
            group by Month(Tarih) ,datename(month,Tarih)
            """,(yil)
        )

        liste = list()
        id = 1
        for item in result:

            model = YuklemeAyModel()
            model.id = id
            model.ay = item.Ay
            model.ay_str = self.__getAyStr(model.ay)

            liste.append(model)
            id += 1

        schema = YuklemeAySchema(many=True)

        return schema.dump(liste)     

    def __getAyStr(self,ay):

        aylar = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']

        return aylar[ay - 1] 

    def getYilListesi(self):

        result = self.data.getList(
            """
            select  
            ROW_NUMBER() over (order by Year(Tarih) desc) as ID,  
            Year(Tarih) as Yil  
            from  
            SevkiyatTB  
            group by Year(Tarih)   
            """
        )

        id = 1

        liste = list()
        for item in result:

            model = YuklemeYilModel()
            model.id = id 
            model.yil = item.Yil

            liste.append(model)

            id += 1

        schema = YuklemeyilSchema(many=True)

        return schema.dump(liste) 

    def getYuklemeRaporMusteriBazindaYillik(self,year):
        try:
            
            self.satislarsql = self.data.getList("""
                                                    select sum(su.SatisToplam) as FOB,s.MusteriID,m.FirmaAdi from SiparislerTB s
                                                    inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                    inner join MusterilerTB m on m.ID = s.MusteriID
                                                    
                                                    group by s.MusteriID,m.FirmaAdi

                                              """)
            self.masraflarsql = self.data.getList("""
                                                select s.MusteriID,m.FirmaAdi,sum(s.NavlunSatis) as Navlun, sum(s.DetayTutar_1) as Detay1, sum(s.DetayTutar_2) as Detay2,sum(s.DetayTutar_3) as Detay3 from SiparislerTB s
                                                inner join MusterilerTB m on m.ID = s.MusteriID
                                                
                                                group by s.MusteriID,m.FirmaAdi
                                              """)
            
            
            
            results = self.data.getStoreList("""
                                                select s.MusteriID,m.FirmaAdi,s.SiparisTarihi,s.YuklemeTarihi from SiparislerTB s
                                                            inner join MusterilerTB m on m.ID = s.MusteriID

                                                            where YEAR(s.SiparisTarihi) = ? and s.SiparisDurumID=3 and m.Marketing='Mekmar' and
                                                            (s.SiparisNo LIKE '%01' or s.SiparisNo LIKE '%01-1')
                                             """,(year))
            
            
            liste = list()
            for item in results:
                if(item.MusteriID == 273 or item.MusteriID == 3446):
                    continue
                else:
                    model = YuklemeYillikModel()
                    model.musteri_adi = item.FirmaAdi
                    model.musteriID = item.MusteriID
                    navlun,detay1,detay2,detay3 = self.__getYuklemeYeniMasraflar(item.MusteriID)
                    model.fob = self.__noneTypeControl(self.__getYuklemeYeniSatis(item.MusteriID))
                    model.dtp = model.fob + self.__noneTypeControl(navlun) + self.__noneTypeControl(detay1) + self.__noneTypeControl(detay2) + self.__noneTypeControl(detay3)
                    liste.append(model)
                    
            
            
            
            schema = YuklemeYillikSchema(many=True)
            return schema.dump(liste)
            
            
        except Exception as e:
            print('getYuklemeRaporMusteriBazindaYillik hata',str(e))
            return False

    
    
    def getYuklemeRaporMusteriBazindaYillikDetail(self,customer_id,year):
        try:
            self.satislarDetaySql = self.data.getStoreList("""
                                                                select 
                                                                    sum(su.SatisToplam) as SatisToplam,
                                                                    s.SiparisNo
                                                                from SiparislerTB s 
                                                                inner join SiparisUrunTB su on su.SiparisNo = s.SiparisNo
                                                                where s.MusteriID=? 
                                                                group by s.SiparisNo
                                                           
                                                           """,(customer_id))
            
            results = self.data.getStoreList("""
                                        select 
                                        s.SiparisNo,
                                        s.NavlunSatis,
                                        s.DetayTutar_1,
                                        s.DetayTutar_2,
                                        s.DetayTutar_3,
                                        s.YuklemeTarihi
                                    from SiparislerTB s 
                                    where s.MusteriID=? 
                                   """,(customer_id))
            
            liste = list()
            for item in results:
                model = YuklemeYillikModel()
                model.siparis_no = item.SiparisNo
                model.navlun = self.__noneTypeControl(item.NavlunSatis)
                model.detay_1 = self.__noneTypeControl(item.DetayTutar_1)
                model.detay_2 = self.__noneTypeControl(item.DetayTutar_2)
                model.detay_3 = self.__noneTypeControl(item.DetayTutar_3)
                model.fob = self.__getYuklemeYeniSiparisDetay(item.SiparisNo)
                model.dtp = model.navlun + model.detay_1 + model.detay_2 + model.detay_3 + model.fob
                model.yukleme_tarihi = item.YuklemeTarihi
                liste.append(model)
            schema = YuklemeYillikSchema(many = True)
            return schema.dump(liste)
    
        except Exception as e:
            print('getYuklemeRaporMusteriBazindaYillikDetail hata',str(e))
            return False
    
    def __getYuklemeYeniSiparisDetay(self,po):
        try:
            for item in self.satislarDetaySql:
                if(item.SiparisNo == po):
                    return self.__noneTypeControl(item.SatisToplam)
        except Exception as e:
            print('__getYuklemeYeniSiparis hata',str(e))
            return False
    
    def __noneTypeControl(self,value):
        if(value == None):
            return 0
        else:
            return float(value)
   
                       
    def __getYuklemeYeniMasraflar(self,musteri_id):
        try:
            control = False
            for item in self.masraflarsql:
                if(item.MusteriID == musteri_id):
                    control = True
                    return self.__noneTypeControl(item.Navlun),self.__noneTypeControl(item.Detay1),self.__noneTypeControl(item.Detay2),self.__noneTypeControl(item.Detay3)
            if(control == False):
                return float(0),float(0),float(0),float(0)
                
        except Exception as e:
            print('__getYuklemeYeniMasraflar',str(e))
            return False
        
    def __getYuklemeYeniSatis(self,musteri_id):
        try:
            control = False
            for item in self.satislarsql:
                if(item.MusteriID == musteri_id):
                    control = True
                    return self.__noneTypeControl(item.FOB)
            if(control == False):
                return float(0)

        except Exception as e:
            print('__getYuklemeYeniSatis hata',str(e))
            return False
    
        
    def __set(self):
        pass