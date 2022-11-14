from models.siparisler_model import FaturaKesimTurSchema,FaturaKesimTurModel
from helpers import SqlConnect

class faturaKesimTur:

    def __init__(self):
        self.data = SqlConnect().data

    def getFaturaKesimTurList(self):
        result = self.data.getList("Select * from FaturaKesilmeTB")

        odemeList = list()

        for item in result:
            model = FaturaKesimTurModel()
            model.id = item.ID
            model.faturaKesimTurAdi = item.FaturaAdi

            odemeList.append(model)

        schema = FaturaKesimTurSchema(many=True)
      
        return schema.dump(odemeList)