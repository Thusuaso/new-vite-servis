from helpers import SqlConnect
from models.tedarikci_form import TedarikciFormSchema,TedarikciFormModel,TedarikciTeslimvFaturaTurModel,TedarikciTeslimvFaturaTurSchema


class TedarikciIcSiparisListe:
    def __init__(self):
        self.data = SqlConnect().data
    def getTedariciFaturaTurList(self):
        result = self.data.getList(
            """
            Select * from TedarikciSiparisFaturaTurTB
            """
        )
        liste = list()
        for item in result:
            model = TedarikciTeslimvFaturaTurModel()
            model.id = item.ID
            model.tur = item.FaturaTanim
            liste.append(model)
        schema = TedarikciTeslimvFaturaTurSchema(many=True)
        return schema.dump(liste)

    def getTedarikciTeslimTurList(self):  #firma ? liman

        result = self.data.getList(
            """
            select * from Tedarikci_Teslim_TurTB
            """
        )

        liste = list()
        for item in result:
            model = TedarikciTeslimvFaturaTurModel()
            model.id = item.ID
            model.tur = item.TeslimAdi
            liste.append(model)
        schema = TedarikciTeslimvFaturaTurSchema(many=True)
            
        return schema.dump(liste)


   