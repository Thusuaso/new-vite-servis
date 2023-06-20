from views.siparisler.listeler import UrunKartMenu
from flask_restful import Resource

class UrunKartMenuList(Resource):
    def get(self):

        urun = UrunKartMenu()

        result = urun.getUrunKartListe()
        
        return result

