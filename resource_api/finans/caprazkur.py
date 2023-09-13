

import urllib.request,ssl # Websitesinden veri cekmek ve ssl sertifikasini es gecmek
import xml.etree.ElementTree as ET # Xml yapisini ayristirmak


import urllib.request,ssl # Websitesinden veri cekmek ve ssl sertifikasini es gecmek
import xml.etree.ElementTree as ET # Xml yapisini ayristirmak
import datetime
import requests
import json
import datetime
class DovizListem:

    def __init__(self):

        pass

    # def getDovizKurListe(self,yil,ay,gun):
    #     is_day = datetime.datetime(yil,ay,gun)
    #     is_day = is_day.strftime("%a")
    #     now = datetime.datetime.now()
    #     nowgun = now.strftime("%d")
    #     if int(nowgun) == int(gun):
    #         gun = int(gun) - 1
    #         is_day2 = datetime.datetime(yil,ay,gun)
    #         is_day2 = is_day2.strftime("%a")
            
            
    #         if(is_day2 == 'Sun'):
    #             gun = int(gun) - 2
    #         else:
    #             gun = int(gun)
        
        
        
    #     if is_day == 'Sat':
    #         gun = gun - 1
        
        
    #     yil = str(yil)
    #     ay = str(ay)
    #     gun = str(gun)
    #     # SSl sertifikasi hatalarini engellemek
    #     ctx = ssl.create_default_context()
    #     ctx.check_hostname = False
    #     ctx.verify_mode = ssl.CERT_NONE
    #     if len(gun) ==1:
    #         gun = "0"+ gun
    #     if len(ay) ==1:
    #         ay = "0"+ ay
    #    # URL = "https://www.tcmb.gov.tr/kurlar/202111/02112021.xml"
    #     URL = "https://www.tcmb.gov.tr/kurlar/"+yil+ay+"/"+gun+ay+yil+".xml"
       
    #     cross_dolar = 0
    #     # Websitesinden veri cekmek
    #     body = urllib.request.urlopen(URL,context=ctx)
    #     data = body.read().decode()
    #     # Xml dosyasini ayristirmak
    #     xml = ET.fromstring(data)
    #     for currency in xml:
    #      for child in currency:
    #         if (child.tag == 'CrossRateOther' and currency.get("Kod") == "EUR"):
    #             cross_dolar = float(child.text)        
    #         else:
    #          continue
    #     return format(cross_dolar)
    
    def getDovizKurListe(self,yil,ay,gun):
        try:
            api_url = "https://dovizkurlari-l6vtviaacq-uc.a.run.app/api/doviz"
            x = datetime.datetime.now()
            nowDay = x.strftime('%d')
            nowMonth = x.strftime('%m')
            xy = datetime.datetime(int(yil),int(ay),int(gun))
            if(int(nowDay) == int(gun) and int(ay) == int(nowMonth)):
                return 0
            
            tarih = f"/{yil}/{ay}/{gun}"
            api = requests.get(api_url+tarih)
            if(len(json.loads(api.text)) == 1):
                gun = int(gun) - 1
            
            if(int(gun) == int(nowDay) and int(ay) != int(nowMonth)):
                gun = int(gun) -1
                    
            if (xy.strftime("%A") == "Saturday"):
                if int(gun) == 1:
                    gun = str(30)
                    ay = str(int(ay) - 1)
                    
                else:
                    gun = str(int(gun) - 1)
            if(xy.strftime("%A") == 'Sunday'):
                gun = str(int(gun) - 2)
                
            if len(str(gun)) == 1:
                gun = "0" + str(gun)
                        
            if len(str(ay)) == 1:
                ay = "0"+ str(ay)
            
            tarih = f"/{yil}/{ay}/{gun}"
            

            
            usd = requests.get(api_url+tarih+'/USD')
            euro = requests.get(api_url+tarih+'/EUR')            
            usd = json.loads(usd.text)
            euro = json.loads(euro.text)
            return float(euro["BanknoteBuying"]) / float(usd["BanknoteBuying"])
        except Exception as e:
            print('Doviz Kur Hatası',str(e))
            return False


        

        