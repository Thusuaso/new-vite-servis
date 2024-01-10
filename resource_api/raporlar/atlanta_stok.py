from helpers import SqlConnect,TarihIslemler
from models.raporlar.atlanta_stok import *
from models.operasyon import *
import datetime


class DepoStokListesi:

    def __init__(self):

        self.data = SqlConnect().data
       

  

    def getAtlantaStok(self):
        liste = list()

        result = self.data.getList(
            """
          
            select  
             k.ID,
            k.SkuNo,
            k.MekmarKod,
            k.UrunTanim,
			k.KasaKutu,
			k.KasaAdet,
			k.KutuAdet,
			k.KasaSqft,
			k.KasaM2,
            k.keys,
			(select top 1  u.OrderNo from YeniDepoGirisUrunlerTB u where u.UrunId=k.ID order by u.Id desc) atl,
			dbo.MekmarUsaYeni_StockSqft(k.SkuNo) as StokSqft,
			dbo.MekmarUsaYeni_StockBox(k.SkuNo) as StokBox,

		    k.mekmar_fiyat,
			k.bd_fiyat,
			k.maya_fiyat,
			k.villo_fiyat,
            k.Kategori,
            k.DepoEbat,
            k.DepoUreticiFiyat,
            k.MaxPayload,
            k.DepoTransport
            from
            DepoUrunKartTB k 
            where k.Aktif =  1 and k.MekmarKod !='SPO'
            order by dbo.get_YeniDepoStok(k.ID,k.Devir) * k.KutuM2  desc
 
               """
          )

        liste = list()
        for item in result:
                model = AtlantaStokModel()

                model.id = item.ID
                model.po = item.atl
                model.sku = item.SkuNo
                model.kod = item.MekmarKod
                model.tanim = item.UrunTanim
                if(item.StokBox == None):
                    
                    model.stok_kutu =0
                else:
                    model.stok_kutu = item.StokBox

                model.kasa_adet = item.KasaAdet
                model.kutu_adet = item.KutuAdet
                model.kasa_kutu = item.KasaKutu
                model.kasa_Sqft = item.KasaSqft
                model.kasa_m2 = item.KasaM2
                if(item.StokSqft == None):
                    
                    model.stok_sqft = 0
                else:
                    model.stok_sqft = item.StokSqft
                
                if item.DepoTransport != None and item.MaxPayload != None and item.DepoUreticiFiyat != None:
                    model.mekmar_fiyat = ( ( (float(item.DepoTransport) / float (item.MaxPayload)) + 5.5 + float(item.DepoUreticiFiyat) ) * 1.35 ) / 10.76
                    
                model.maya_fiyat = item.maya_fiyat
                model.bd_fiyat = item.bd_fiyat
                model.villo_fiyat = item.villo_fiyat
                model.keys = item.keys
                model.kategori = item.Kategori
                model.ebat = item.DepoEbat
                if(self.__noneTypeControl(item.KasaSqft) ==0 or self.__noneTypeControl(item.KasaKutu) == 0):
                    model.kutu_sqft = 0
                else:
                    
                    model.kutu_sqft = self.__noneTypeControl(item.KasaSqft) / self.__noneTypeControl(item.KasaKutu)

                
                
                
                if item.DepoTransport != None and item.MaxPayload != None and item.DepoUreticiFiyat != None:
                    model.toplam_mekus = ( ( float(item.DepoTransport) / float (item.MaxPayload)) + 6 + float(item.DepoUreticiFiyat) ) / 10.76
              
           
           

                liste.append(model)

           

        schema = AtlantaStokSchema(many=True)

        return schema.dump(liste)    

    def __noneTypeControl(self,value):
        if(value == None):
            return 0 
        else:
            return value

    def getStokList(self,skuNo):
      
        liste = list()

        result = self.data.getStoreList(
            """
           select
            g.Id,
            g.Date as YuklemeTarihi,
            g.OrderNo,           
            u.Box,
            (u.Box * k.KutuSqft) as Sqft,
            (u.Box * k.KutuM2) as M2,
			g.Eta,
			g.KonteynerNo,
			g.InboundDate,
			g.Depo_Masraf
            from
            YeniDepoGirisTB g,YeniDepoGirisUrunlerTB u,DepoUrunKartTB k
            where
            g.OrderNo=u.OrderNo and k.ID=u.UrunId and g.Status='stock'
            and k.SkuNo=?
			order by YuklemeTarihi desc
            """,(skuNo)
        )
           
        
        for item in result:

            model = Stok_SuModel()

            model.id = item.Id
            
            model.yukleme_tarihi = item.YuklemeTarihi
            model.order_no = item.OrderNo
            model.box = item.Box
            model.sqft = item.Sqft
            model.m2 = item.M2
            model.eta = item.Eta
            model.konteyner_no = item.KonteynerNo
            model.inbound_date= item.InboundDate
            model.masraf = item.Depo_Masraf
              
           
           

            liste.append(model)

           

        schema = Stok_SuSchema(many=True)

        return schema.dump(liste)  


    def getSuList(self,skuNo):
      
        liste = list()

        result = self.data.getStoreList(
            """
           select
            g.Id,
            g.Date as YuklemeTarihi,
            g.OrderNo,           
            u.Box,
            (u.Box * k.KutuSqft) as Sqft,
            (u.Box * k.KutuM2) as M2,
			g.Eta,
			g.KonteynerNo,
			g.InboundDate,
			g.Depo_Masraf
            from
            YeniDepoGirisTB g,YeniDepoGirisUrunlerTB u,DepoUrunKartTB k
            where
            g.OrderNo=u.OrderNo and k.ID=u.UrunId and g.Status='water'
            and k.SkuNo=?
			order by YuklemeTarihi desc
            """,(skuNo)
        )
           
        
        for item in result:

            model = Stok_SuModel()

            model.id = item.Id
            
            model.yukleme_tarihi = item.YuklemeTarihi
            model.order_no = item.OrderNo
            model.box = item.Box
            model.sqft = item.Sqft
            model.m2 = item.M2
            model.eta = item.Eta
            model.konteyner_no = item.KonteynerNo
            model.inbound_date= item.InboundDate
            model.masraf = item.Depo_Masraf
              
           
           

            liste.append(model)

           

        schema = Stok_SuSchema(many=True)

        return schema.dump(liste)   


    def getSatisList(self,skuNo):

            tarihIslem = TarihIslemler()
            satisListe = list()

            result = self.data.getStoreList(
                """
                select
                u.Id,
                m.CustomersName,
                s.OrderNo,
                s.Date as SatisTarihi,
                s.ShippingDate,
                s.PaymentDate,
                u.Box,
                u.Box * k.KutuSqft as Sqft,
                u.Box * k.KutuM2 as M2,
                u.Price,
                u.Total,
                s.ShippedNo
				
                from
                YeniDepoSatisTB s,YeniDepoSatisUrunlerTB u,DepoUrunKartTB k
                ,YeniDepoMusterilerTB m
                where
                s.OrderNo=u.OrderNo and u.UrunId=k.ID
                and s.CustomersId=m.Id and k.SkuNo=? and yEAR(s.Date) !=2019
                order by s.Date desc
                """,(skuNo)
            )

            for item in result:

                model = DepoUrunSatisModel()

                model.id = item.Id 
                model.musteriAdi = item.CustomersName 
                model.orderNo = item.OrderNo 
                if item.SatisTarihi != None:
                    model.satisTarihi = tarihIslem.getDate(item.SatisTarihi).strftime("%d-%m-%Y")
                if item.ShippingDate != None:
                    model.sevkTarihi = tarihIslem.getDate(item.ShippingDate).strftime("%d-%m-%Y")
                if item.PaymentDate != None:
                    model.odemeTarihi = tarihIslem.getDate(item.PaymentDate).strftime("%d-%m-%Y")
                model.kutu = item.Box 
                model.sqft = item.Sqft 
                model.m2 = item.M2 
                model.rof = item.ShippedNo
                model.birimFiyat = item.Price 
                model.toplamFiyat = item.Total 

                satisListe.append(model)

            schema = DepoUrunSatisSchema(many=True)

            return schema.dump(satisListe)


    def getMaliyetList(self,skuNo):

            liste = list()

            result = self.data.getStoreList(
                """
                select * from DepoUrunKartTB where  SkuNo=?
                
                """,(skuNo)
            )

            for item in result:

                model = DepoMaliyetModel()

                model.id = item.ID
                model.uretici = item.DepoUretici
                model.uretici_fiyat = item.DepoUreticiFiyat
                model.transport = item.DepoTransport
                model.max_payload = item.MaxPayload
                model.mekus_kira = item.Depo_Kira
               
               

                liste.append(model)

            schema = DepoMaliyetSchema(many=True)

            return schema.dump(liste)       

 
       
        
  