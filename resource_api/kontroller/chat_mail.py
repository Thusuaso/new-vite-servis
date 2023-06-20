
from helpers import SqlConnect,TarihIslemler
from helpers import MailService
import datetime
from models.chat import *

class ChatGiris:
    
    def __init__(self):
        self.data = SqlConnect().data
        
    def mailGonderInsert(self,item):
       
        
        try:
            #item = _item['pesinat_model']
          
            self.data.update_insert(
                """
                insert into ChatTB (
                  SiparisNo,Gonderen,Alici,Mesaj,Tarih
                )
                values
                (?,?,?,?,?)
                """,
                (
                item['po'], item['gonderen'] ,item['alici'] , item['metin'] , item['bugun']
                )
            )

           

            MailService( item['po']+ ' - '+ item['gonderen'] +' dan mesajınız var (!)', item['alici'], item['metin']) #mesaj 
           
            
            return True

        except Exception as e:
            print('Chat  Hata :',str(e))
            return False

    def getChatList(self,siparisNo):

        result = self.data.getStoreList(
           """   
             
             select  *  from ChatTB where SiparisNo=? order by Tarih  , ID asc 

        
           """
             , (siparisNo))
        liste = list()
        
        for item in result: 

            model = ChatModel()
   
            model.mesaj = item.Mesaj
            model.alici = item.Alici
            model.po = item.SiparisNo
            model.gonderen = item.Gonderen
            liste.append(model)
           

        schema = ChatSchema(many=True)

        return schema.dump(liste)
            
    