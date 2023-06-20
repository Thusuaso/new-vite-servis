from helpers import SqlConnect
from models import UrunKartSchema,UrunKartModel

class UrunKartMenu:
    def __init__(self):
        self.data =SqlConnect().data

    def getUrunKartListe(self):
        result = self.data.getList(
            """
            select
            ID as Id,
            dbo.Get_KategoriAdi(ID) as KategoriAdi,
            dbo.Get_UrunAdi(ID) as UrunAdi,
            dbo.Get_KenarIslem(ID) as YuzeyIslem,
            dbo.Get_Olcu_En(ID) as En,
            dbo.Get_Olcu_Boy(ID) as Boy,
            dbo.Get_Olcu_Kenar(ID) as Kenar
            from
            UrunKartTB
            """
        )

        kartList = list()
        sira = 1
        for urun in result:
            model = UrunKartModel() 
            model.id = urun.Id
            model.kategoriAdi = urun.KategoriAdi 
            model.en = urun.En
            model.boy = urun.Boy
            model.kenar = urun.Kenar
            model.urunAdi = urun.UrunAdi
            model.sira = sira
            olculer = str(urun.YuzeyIslem).split('&')

            yuzey_1,yuzey_2,yuzey_3 =  self.__getYuzeyIslem(olculer)
            model.yuzey_1 = yuzey_1
            model.yuzey_2 = yuzey_2
            model.yuzey_3 = yuzey_3
            model.yuzeyIslem = urun.YuzeyIslem
            if len(urun.En) > 0:
                model.ebat = urun.En
            if len(urun.Boy) > 0:
                model.ebat += 'X' + urun.Boy
            if len(urun.Kenar) > 0:
                model.ebat += 'X' + urun.Kenar
            kartList.append(model)
            sira += 1

        schema = UrunKartSchema(many=True)

        return schema.dump(kartList)

    
    def __getYuzeyIslem(self,olculer):

        yuzey_1 = ""
        yuzey_2 = ""
        yuzey_3 = ""

        if len(olculer) == 1:
            yuzey_1 = olculer[0]
        if len(olculer) == 2:
            yuzey_1 = olculer[0]
            yuzey_2 = olculer[1]
        if len(olculer) == 3:
            yuzey_1 = olculer[0]
            yuzey_2 = olculer[1]
            yuzey_3 = olculer[2]


        return yuzey_1,yuzey_2,yuzey_3