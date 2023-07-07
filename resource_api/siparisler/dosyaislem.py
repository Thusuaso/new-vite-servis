from helpers import SqlConnect,TarihIslemler
from models.yeniTeklifler import *
from models.shared import GenelListModel,GenelListSchema
from flask_restful import Resource
from flask import jsonify,request
import datetime


class IcSiparisKaydet(Resource):

    def post(self):

        tedarikci = request.get_json()
        
        Islem = TedarikciIslem()
        result = Islem.IcSiparisKaydet(tedarikci)

        return jsonify({'Status' : result})


class TedarikciIslem:
    def __init__(self):
        self.data = SqlConnect().data
    
    def IcSiparisKaydet(self,tedarikci):
        try:
            
            self.data.update_insert(
                """
                    insert into SiparisUrunTedarikciFormTB (
                    SiparisNo,TedarikciID,TedarikciSiparisFaturaTurID,TedarikciTeslimTurID,TeslimTarihi
                    )
                    values
                    (?,?,?,?,?)
                """,(
                    tedarikci[14]['siparisNo'],tedarikci[14]['tedarikciId'],tedarikci[14]['id'],tedarikci[2][0]['id'],tedarikci[1]
                )
            )
            return True
        except Exception as e:
            print('IcSiparisKaydet Hata : ',str(e))
            return False

  