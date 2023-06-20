from helpers import SqlConnect
from datetime import datetime

class Notification:
    def __init__(self):
        self.data = SqlConnect().data
        self.notificationSubList = self.data.getList("""
                                                        select 

                                                            abg.ID,
                                                            abg.Tarih,
                                                            abg.NotificationId,
                                                            abg.Queue,
                                                            abg.Message,
                                                            abg.Follow,
                                                            abg.WhoSendId,
                                                            abg.WhoSendName,
                                                            abg.ReceiverName,
                                                            abg.ReceiverId,
															(select Image from KullaniciTB k where k.ID = abg.WhoSendId) as WhoSendImage,
															(select Image from KullaniciTB k where k.ID = abg.ReceiverId) as ReceiverImage


                                                        from AnlikBildirimGeriDonusTB abg
                                                        order by Tarih desc
                                                     
                                                     
                                                     """)
    def save(self,data):
        try:
            datetime.now()
            self.data.update_insert("""
                                    insert into 
                                    AnlikBildirimTB(
                                        Tarih,
                                        UserId,
                                        UserName,
                                        Message,
                                        Follow,
                                        WhoSendId,
                                        WhoSendName) 
                                    VALUES(?,?,?,?,?,?,?)
                                
                                """,(datetime.now(),
                                     data['userId'],
                                     data['userName'],
                                     data['message'],
                                     1,
                                     data['whoSendId'],
                                     data['whoSendName']
                                     )
                                )
            return True
        except Exception as e:
            print('Notification save hata',str(e))
            return False
    def update(self,data):
        pass
    def getList(self,id):
        try:
            result = self.data.getStoreList("""
                                                select 

                                                    ab.ID,
                                                    ab.Tarih,
                                                    ab.UserId,
                                                    ab.UserName,
                                                    ab.Message,
                                                    ab.Follow,
                                                    ab.WhoSendId,
                                                    ab.WhoSendName,
													(select k.Image from KullaniciTB k where k.ID = ab.UserId) as UserImage,
													(select k.Image from KullaniciTB k where k.ID = ab.WhoSendId) as WhoSendImage



                                                from AnlikBildirimTB ab
                                                where ab.UserId =? or ab.WhoSendId=?
                                                order by ID desc
                                            
                                            """,(id,id))
            liste = list()
            key = 0
            for item in result:
                liste.append({
                    'key':str(key),
                    'data':{
                        'id':item.ID,
                        'tarih':item.Tarih,
                        'user_id':item.UserId,
                        'user_name':item.UserName,
                        'user_image':'https://cdn.mekmarimage.com/personel/' + item.UserImage,
                        'message':item.Message,
                        'follow':item.Follow,
                        'who_send_id':item.WhoSendId,
                        'who_send_name':item.WhoSendName,
                        'who_send_image':'https://cdn.mekmarimage.com/personel/' + item.WhoSendImage
                    },
                    'children':self.__getNotificationSubList(item.ID,key)
                })

                key += 1
            return liste
        except Exception as e:
            print('notification getList hata',str(e))  
            return False
    def __getNotificationSubList(self,notification_id,key):
        
        liste = list()
        key2 = 0
        for item in self.notificationSubList:

            if(item.NotificationId == notification_id):
                liste.append({
                    'key':str(key) + '-' + str(key2),
                    'data':{
                        'table_id':item.ID,
                        'id':item.NotificationId,
                        'notificationId':item.NotificationId,
                        'tarih':item.Tarih,
                        'follow':item.Follow,
                        'message':item.Message,
                        'who_send_id':item.WhoSendId,
                        'who_send_name':item.WhoSendName,
                        'who_send_image':'https://cdn.mekmarimage.com/personel/' + item.WhoSendImage,
                        'receiver_name':item.ReceiverName,
                        'receiver_id':item.ReceiverId,
                        'receiver_image':'https://cdn.mekmarimage.com/personel/' + item.ReceiverImage
                    }
                })
                
                key2 += 1
        return liste
    def setFollow(self,data):
        try:
            self.data.update_insert("""
                                        Update AnlikBildirimTB SET Follow = ? WHERE ID=?
                                    """,(0,data['id']))
            return True
        except Exception as e:
            print('setFollow hata',str(e))
            return False
    def setFollowAnswered(self,data):
        try:
            self.data.update_insert("""
                                        Update AnlikBildirimGeriDonusTB SET Follow = ? WHERE ID=?
                                    """,(0,data['table_id']))
            return True
        except Exception as e:
            print('setFollow hata',str(e))
            return False
    
    
    def answeredsave(self,data):
        try:
            newDate = datetime.now()
            self.data.update_insert("""
                                        Insert Into 
                                        AnlikBildirimGeriDonusTB(
                                            Tarih,
                                            NotificationId,
                                            Message,
                                            Follow,
                                            WhoSendId,
                                            WhoSendName,
                                            ReceiverName,
                                            ReceiverId
                                            ) VALUES(?,?,?,?,?,?,?,?)

                                    """,(newDate,data['id'],data['newMessage'],1,data['user_id'],data['user_name'],data['receiver_name'],data['receiver_id']))
            return True
        except Exception as e:
            print('answeredsave hata',str(e))
            return False
