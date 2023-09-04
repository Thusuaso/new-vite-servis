from helpers import SqlConnect,DegisiklikMain,MailService
from models.operasyon.nakliyelistesi import *
import datetime

class NakliyeIslem:

    def __init__(self):

        self.data = SqlConnect().data

    
    def getNakliyeList(self):

        result = self.data.getList(

            """
            select* from FirmalarTB
            """
        )

        liste = list()

        for item in result:
            model = NakliyeIslemModel()
            
            model.firma_adi = item.FirmaAdi
            model.Firma_id = item.ID
           

            liste.append(model)

        schema = NakliyeIslemSchema(many=True)

        return schema.dump(liste)

    def getSiparisList(self):

        result = self.data.getList(

            """
            select SiparisNo from SiparislerTB where YEAR(SiparisTarihi) in (2023,2022,2021,2020) order by SiparisTarihi desc
            """
        )

        liste = list()

        for item in result:
            model = NakliyeIslemModel()
            
            model.siparisno = item.SiparisNo
          
           

            liste.append(model)

        schema = NakliyeIslemSchema(many=True)

        return schema.dump(liste)   
    
    def getTNakliyeUrunModel(self):
        model = NakliyeIslemModel()
        schema = NakliyeIslemSchema()
        return schema.dump(model)
            
    def getNakliyeModel(self,urunId):
        result = self.data.getStoreList(

            """
            Select ID from NakliyeFaturaKayitTB where  FaturaNo=?
            """,(urunId)
        )

        liste = list()

        for item in result:
            model = NakliyeIslemModel()
            
            model.id = item.ID
            liste.append(model)
       
        schema = NakliyeIslemSchema(many=True)
      

        return schema.dump(liste)

    def nakliyeKaydet(self,item):
        try:
            invoice_id = 0
            invoice_name=""
            for key in item : 
                    forMat = '%d-%m-%Y'
                    key['tarih'] = datetime.datetime.strptime(key['tarih'], forMat)
                    key['tarih'] = key['tarih'].date()
                    self.data.update_insert(
                        """
                        INSERT INTO NakliyeFaturaKayitTB (FirmaID, Tarih, FaturaNo, Tutar,Kur,KayitTarihi)    values
                        (?,?,?,?,?,?)
                        """,(key['Firma_id'],key['tarih'],key['faturaNo'],key['Tutar_tl'],key['kur'],key['tarih'])
                    )
                    self.__urunId(key)
                    self.__evrakId(key)
                    invoice = self.data.getStoreList("""
                                                select ID,FaturaNo from NakliyeFaturaKayitTB where FaturaNo=?
                                           """,(key['faturaNo']))[0]
                    invoice_name = invoice.FaturaNo
                    invoice_id = invoice.ID
                    result = self.data.getStoreList("""
                                            select FaturaKesimTurID,YuklemeTarihi from SiparislerTB where SiparisNo=?
                                       """,(key['siparisno']))
                    info = key['siparisno'] + ' po ya ' + key['faturaNo'] + ' fatura no ile ' + ' Nakliye faturası $ ' + key['Tutar_dolar'] + ' ve $ ' +  key['kur'] + ' kur girilmiştir.'
                    renk = '#ffec31'
                    DegisiklikMain().setMaliyetDegisiklik(info,'Huseyin',key['siparisno'],result[0][1],renk)
                
            info = "Huseyin Nakliye Faturası Girişi Yaptı"
            DegisiklikMain().setYapilanDegisiklikBilgisi('Huseyin',info)
            data = {
                'status':True,
                'invoice_id':invoice_id,
                'invoice_name':invoice_name
            }
            return data
        except Exception as e:
            print('nakliyeKaydet  Hata : ')
            return False
    def masraflarSendMail(self,item,siparisNo,nowDate,y_tarihi):
        body = """
        <table >
       
            <tr style ="background-color: #f2f2f2;">
                <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Sipariş No
                </th>
                <th style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Fatura No
                </th>
                <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 100px;">
                Tutar ($)
                </th>
                 <th  style ="color: white;background-color: #4CAF50;text-align: left;  padding-bottom: 12px; padding-top: 12px; padding-top: 12px;padding: 8px; font-family: Arial, Helvetica, sans-serif; border-collapse: collapse;width: 150px;">
                Kur
                </th>
            </tr>
        """
            
        body += f"""
    
        <tr style ="background-color: #ddd;">
            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
            {siparisNo}
            </td>
            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
            {item['faturaNo']}
            </td>
            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
            {item['Tutar_dolar']}
            </td>
            <td style ="border: 1px solid #ddd; padding: 8px;  font-family: Arial, Helvetica, sans-serif;border-collapse: collapse; width: 100px;">
            {item['kur']} 
            </td>
            
        </tr>
    
    
        """
            
        body = body + "</table>"
        
        
        MailService(str(y_tarihi) + ' Yükleme Tarihli ' + siparisNo + ' ' +  str(nowDate) + ' Tarihinde Nakliye Fatura Girişi', "bilgiislem@mekmar.com",body)
        MailService(str(y_tarihi) + ' Yükleme Tarihli ' + siparisNo +' ' + str(nowDate) + ' Tarihinde Nakliye Fatura Girişi', "info@mekmar.com",body)

        
    
    def __evrakIdKontrol(self,item):

           kontrol = self.data.getStoreList("Select count(*) as durum from YeniNakliyeFaturalarıTB where SiparisNo=?   ",item['siparisno'])[0].durum 
           print("__evrakIdKontrol",kontrol)
           return kontrol

    def __evrakId(self,item):

        try:
            id = 201
            kontrol = self.data.getStoreList("Select count(*) as durum from YeniNakliyeFaturalarıTB where SiparisNo=?",item['siparisno'])[0].durum 
            
            if kontrol == 0:
                id = 201
            else : 
                id = kontrol + 201   
            self.data.update_insert(
                """
                INSERT INTO YeniNakliyeFaturalarıTB (EvrakID, SiparisNo, EvrakAdi)    values
                (?,?,?)
                """,( id ,item['siparisno'],item['faturaNo'])
            )
            
            return True
        except Exception as e:
            print('__evrakId Hata : ',str(e))
            return False  


    def __urunId(self,item):
       
        kontrol = self.data.getStoreList("select count(*) as durum from NakliyeFaturaKayitTB where FaturaNo=?",item['faturaNo'])[0].durum
      
        urunId = None 
        if kontrol > 0:
            urunId = self.data.getStoreList("Select ID from NakliyeFaturaKayitTB where  FaturaNo=?",item['faturaNo'])[0].ID 
            
         
          
        else:
           
         print('urun id çalıştı')
         
        
        return urunId 


    def NakliyeDosyaKaydet(self,item):
      
             print(item)
             for key in item :  
                
                 urun =  self.__urunId(key)
                 evrak_id = self.__evrakIdKontrol(key)
                 forMat = '%d-%m-%Y'
                 key['tarih'] = datetime.datetime.strptime(key['tarih'], forMat)
                 key['tarih'] = key['tarih'].date()
                 self.data.update_insert(
                    """
                    INSERT INTO SiparisFaturaKayitTB (
                        Tarih,
                        FaturaKayitID,
                        SiparisFaturaTurID, 
                        SiparisNo,
                        Tutar,
                        EvrakDurum,
                        YuklemeEvrakID,
                        YeniEvrakID,
                        YuklemeEvrakDurumID,
                        EvrakYuklemeTarihi,
                        EvrakAdi  ,KullaniciID
                    )   
                        values
                        (?,?,?, ?,?,?,?,?,?,?,?,?)
                    """,(key['tarih'],urun,11,key['siparisno'],key['Tutar_dolar'],1,13,evrak_id+201,2,key['tarih'],key['faturaNo']+'.pdf',key['kullaniciId'])
                )
             info = "Huseyin Nakliye Faturası Evrağı Yükledi"
             DegisiklikMain().setYapilanDegisiklikBilgisi('Huseyin',info)
             return True    

    def getNakliyeDosyaSil(self,siparisNo,evrakAdi):
        try:
            
            self.data.update_insert("""
                                        delete SiparisFaturaKayitTB where SiparisNo=? and EvrakAdi=?
                                    
                                    
                                    """,(siparisNo,evrakAdi + '.pdf'))
            self.data.update_insert("""
                                        delete YeniNakliyeFaturalarıTB where SiparisNo=? and EvrakAdi=?
                                    """,(siparisNo,evrakAdi))
            
            return True
        except Exception as e:
            print('getNakliyeDosyaSil hata',str(e))
            return False

    def getFormIslem(self,firmaId,evrakAdi,siparisNo):
        result = self.data.getStoreList(
            """ 
           select 

            nk.FaturaNo as FaturaNo,
            nk.Tutar as TL,
            nk.Kur as Kur,
            sf.Tutar as Dolar,
            sf.SiparisNo as SiparisNo


            from NakliyeFaturaKayitTB nk,SiparisFaturaKayitTB sf 
            where nk.FaturaNo +'.pdf' = sf.EvrakAdi and nk.FirmaID=? and nk.FaturaNo=? and sf.SiparisNo=?

            """,(firmaId,evrakAdi,siparisNo)
        )

        liste = list()
        
        for item in result: 

            model = NakliyeListeModel()
            
            model.faturaNo = item.FaturaNo
            model.Tutar_dolar = item.Dolar
            model.siparis_no = item.SiparisNo
            model.kur = item.Kur

            liste.append(model)

        schema = NakliyeListeSchema(many=True)

        return schema.dump(liste)

    def setChangeNakliye(self,data):
        try:
            self.data.update_insert("""
                                    update SiparisFaturaKayitTB SET Tutar=? where SiparisNo=? and EvrakAdi=?

                                """,(float(data['Tutar_dolar']),data['siparis_no'],data['faturaNo'] + '.pdf'))
        
            self.data.update_insert("""
                                    update NakliyeFaturaKayitTB SET Kur=? where FaturaNo=?

                                """,(float(data['kur']),data['faturaNo']))
            
 
            
            return True
        except Exception as e:
            print('setChangeNakliye hata',str(e))
            return False
   
