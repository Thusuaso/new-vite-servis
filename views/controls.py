from helpers import SqlConnect
class Controls:
    def __init__(self):
        self.data = SqlConnect().data
        
    def getProformaControl(self,siparisNo):
        try:
            
            result = self.data.getStoreList("""
                                                select * from SiparisFaturaKayitTB where YuklemeEvrakID=2 and SiparisNo=?
                                            """,(siparisNo))
            if(len(result)):
                return True
            else:
                return False
            
        except Exception as e:
            print('getProformaControl hata',str(e))
            return True
            
