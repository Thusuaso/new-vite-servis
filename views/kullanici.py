from models import KullaniciModel,KullaniciSchema
from helpers import SqlConnect


class Kullanici:

    def __init__(self):
        self.data = SqlConnect().data 

    def getKullaniciList(self):

        result = self.data.getList("Select * from KullaniciTB where Aktif=1 And TemsilciSira!=0 order by TemsilciSira asc ")

        kullaniciList = list()

        for item in result:

            model = KullaniciModel()

            model.id = item.ID 
            model.kullaniciAdi = item.KullaniciAdi 
            model.kullaniciSoyAd = item.KullaniciSoyAd 
            model.mailAdres = item.MailAdres 

            kullaniciList.append(model)

        schema = KullaniciSchema(many=True)

        return schema.dump(kullaniciList)

    def getChatKullaniciList(self):
        result = self.data.getList("select * from KullaniciTB where Aktif=1 and Satisci=1 and VersiyonDegisim=1")
        kullaniciList = list()

        for item in result:

            model = KullaniciModel()

            model.id = item.ID 
            model.kullaniciAdi = item.KullaniciAdi 
            model.kullaniciSoyAd = item.KullaniciSoyAd 
            model.mailAdres = item.MailAdres
            model.image = 'https://cdn.mekmarimage.com/personel/' + item.Image

            kullaniciList.append(model)

        schema = KullaniciSchema(many=True)

        return schema.dump(kullaniciList)

    def getOperasyonKullaniciList(self):

        result = self.data.getList("Select * from KullaniciTB where Aktif=1 And OperasyonSira!=0 order by OperasyonSira asc ")

        kullaniciList = list()

        for item in result:

            model = KullaniciModel()

            model.id = item.ID 
            model.kullaniciAdi = item.KullaniciAdi 
            model.kullaniciSoyAd = item.KullaniciSoyAd 
            model.mailAdres = item.MailAdres 

            kullaniciList.append(model)

        schema = KullaniciSchema(many=True)

        return schema.dump(kullaniciList)