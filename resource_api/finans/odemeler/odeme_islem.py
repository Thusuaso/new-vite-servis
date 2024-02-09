from models.finans.odemeler import *
from helpers import SqlConnect,TarihIslemler


class OdemeIslem:

    def __init__(self):

        self.data = SqlConnect().data


    def getOdemeListesi(self,yil,ay):

        odeme_list = self.__tumfinans(yil,ay)
        
        for item in self.__tumnumune(yil,ay):

            odeme_list.append(item)

        schema = OdemeListeSchema(many=True)
       
        return schema.dump(odeme_list)

    def __tumfinans(self,yil,ay):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select          
            o.Tarih,
            m.FirmaAdi,
            sum(o.Tutar) as Tutar,
            o.SiparisNo
            from
            OdemelerTB o,MusterilerTB m
            where
            o.MusteriID=m.ID
            and Year(o.Tarih)=? and Month(o.Tarih)=?
            group by o.Tarih,m.FirmaAdi,o.SiparisNo
            order by  o.Tarih desc
            """,(yil,ay)
        )

        liste = list()
        id = 1
        for item in result:

            model = OdemeListeModel()

            model.id = id
            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            
            model.musteriadi = item.FirmaAdi
            model.po = item.SiparisNo
            model.tutar = item.Tutar
            model.status = "Sipariş"
            liste.append(model)

            id += 1

        schema = OdemeListeSchema(many=True)

        return schema.dump(liste)

    def __tumnumune(self,yil,ay):

        tarihIslem = TarihIslemler()
        result = self.data.getStoreList(

            """
            select          
            o.Tarih,
            m.MusteriAdi as FirmaAdi,
            sum(o.Tutar) as Tutar,
            o.NumuneNo as SiparisNo
            from
            NumuneOdemelerTB o,YeniTeklif_MusterilerTB m
            where
            o.MusteriID=m.ID
            and Year(o.Tarih)=? and Month(o.Tarih)=?
            group by o.Tarih,m.MusteriAdi,o.NumuneNo
            order by  o.Tarih desc
            """,(yil,ay)
        )

        liste = list()
        id = 1
        for item in result:

            model = OdemeListeModel()

            model.id = id
            if item.Tarih != None:
                model.tarih = tarihIslem.getDate(item.Tarih).strftime("%d-%m-%Y")
            
            model.musteriadi = item.FirmaAdi
            model.po = item.SiparisNo
            model.tutar = item.Tutar
            model.status = "Numune"

            liste.append(model)

            id += 1

        schema = OdemeListeSchema(many=True)

        return schema.dump(liste)    

    def getYilListesi(self):

        result = self.data.getList(
            """
            select
            Year(Tarih) as Yil
            from
            OdemelerTB
            group by Year(Tarih)
            order by Year(Tarih) desc
            """
        )

        id = 1

        liste = list()

        for item in result:

            model = OdemeYilModel()
            model.id = id 
            model.yil = item.Yil

            liste.append(model)

            id += 1

        schema = OdemeYilSchema(many=True)

        return schema.dump(liste)

    def getAyListesi(self,yil):

        result = self.data.getStoreList(
            """
            select
            Month(Tarih) as Ay
            from
            OdemelerTB
            where Year(Tarih)=?
            group by Month(Tarih)
            order by Month(Tarih) desc
            """,(yil)
        )

        liste = list()

        id = 1

        for item in result:

            model = OdemeAyModel()
            model.id = id
            model.ay = item.Ay
            model.ay_str = self.__getAyStr(model.ay)

            liste.append(model)

        schema = OdemeAySchema(many=True)

        return schema.dump(liste)

     
    def __getAyStr(self,ay):

        aylar = ['January','February','March','April','May','June','July','August','September','October','November','December']

        return aylar[ay - 1]

 



