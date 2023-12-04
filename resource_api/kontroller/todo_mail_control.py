from helpers import MailService,SqlConnect,TarihIslemler
import datetime
from flask import jsonify,request
from flask_restful import Resource
from helpers.sqlConnect import SqlConnect


class TodoMailControlApi(Resource):
    def get(self):
        islem = TodoMailControl()
        islem.getToDoMailControl()
        return {'status':True}

class TodoMailControl():
    def __init__(self):
        self.data = SqlConnect().data
        
    def getToDoMailControl(self):
        try:
            x = datetime.datetime.now()
            day = x.strftime('%A')
            isMailSend = self.data.getList("""
                                            select MailControl from YapilacaklarMailKontrol where ID= 1
                                           """)
            if(day == 'Monday' or day == 'Thursday'):
                pass
            else:
                self.data.update_insert("""update YapilacaklarMailKontrol SET MailControl = ? where ID=?""",(0,1))
                
                
            if(isMailSend[0][0] == False):
                if(day == 'Monday' or day == 'Thursday'):
                    
                    self.data.update_insert("""
                                        update YapilacaklarMailKontrol SET MailControl = ? where ID=?
                                      """,(1,1))
                    result = self.data.getList("""
                                                    select y.GorevSahibiAdi,y.Yapilacak,k.MailAdres from Yapilacaklar y 
                                                    inner join KullaniciTB k on k.ID = y.GorevSahibiId

                                                    where y.Yapildi=0 and y.YapilacakOncelik='C'

                                            """)
                    subject = 'Haftalık Sabit Yapılacaklar...'
                    for item in result:
                        MailService(subject,item.MailAdres,item.Yapilacak)
                    
                    
            
        except Exception as e:
            print('getToDoMailControl hata',str(e))


