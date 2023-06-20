from helpers.sqlConnect import SqlConnect
import datetime
from models.teklifler.bgpProjectsModel import *
class BgpProjects():
    def __init__(self):
        self.data = SqlConnect().data
        
    def setBgpProjectsName(self,data):
        try:
            now = datetime.datetime.now()
            day = now.strftime("%d")
            month = now.strftime("%m")
            year = now.strftime("%Y")
            nowDate = year + '-' + month + '-' + day
            result = self.data.getStoreList("""
                                                select * from BgpNetworkProjects where ProjectName=?
                                            
                                            """,(data['name']))
            
            if len(result) > 0:
                return False
            else:
                self.data.update_insert("""

                                            insert BgpNetworkProjects(ProjectName,DateofRegistiration,Temsilci,UlkeAdi,UlkeLogo) VALUES(?,?,?,?,?)
                                        
                                        """,(data['name'],nowDate,data['representive'],data['country'],data['countryLogo']))
                return True
            
        except Exception as e:
            print('setBgpProjectsName',str(e))
            return False
    
    
    
    def setBgpProjectsNameChange(self,projectName,temsilci,bgpUlkeAdi,ulkeLogo,projectId):
        try:
            self.data.update_insert("""

                                        update BgpNetworkProjects set ProjectName=?,Temsilci=?,UlkeAdi=?,UlkeLogo=? where ID=?
                                    
                                    """,(projectName,temsilci,bgpUlkeAdi,ulkeLogo,projectId))

            result = self.getBgpProjectList(temsilci)
            return True,result
            
        except Exception as e:
            print('setBgpProjectsNameChange',str(e))
            result = self.getBgpProjectList(temsilci)
            return False,result
      
    
    
    def getBgpProjectList(self,temsilci):
        try:
            if temsilci == 19 or temsilci == 44:
                result = self.data.getStoreList("""
                                                    select 
                                                        bgp.*,
                                                        (select k.KullaniciAdi from KullaniciTB k where k.ID=bgp.Temsilci) as TemsilciAdi
                                                    from BgpNetworkProjects bgp where bgp.Temsilci=?
                                                
                                                """,(temsilci))
                liste = list()
                for item in result:
                    model = BgpProjectsListModel()
                    model.id = item.ID
                    model.projectName = item.ProjectName
                    model.dateOfRegistiration = item.DateofRegistiration
                    model.temsilci = item.Temsilci
                    if(item.Temsilci == 19):
                        model.borderColor = 'red'
                    elif item.Temsilci == 44:
                        model.borderColor = 'blue'
                    model.ulkeAdi = item.UlkeAdi
                    model.ulkeLogo = item.UlkeLogo
                    model.filelink = item.Filelink
                    model.fileCloud = item.FileCloud
                    model.temsilciAdi = item.TemsilciAdi
                    liste.append(model)
                schema = BgpProjectsListSchema(many=True)
                return schema.dump(liste)
            else:
                result = self.data.getList("""
                                                    select 
                                                        bgp.*,
                                                        (select k.KullaniciAdi from KullaniciTB k where k.ID=bgp.Temsilci) as TemsilciAdi
                                                    from BgpNetworkProjects bgp
                                                
                                                """)
                liste = list()
                for item in result:
                    model = BgpProjectsListModel()
                    model.id = item.ID
                    model.projectName = item.ProjectName
                    model.dateOfRegistiration = item.DateofRegistiration
                    model.temsilci = item.Temsilci
                    if(item.Temsilci == 19):
                        model.borderColor = 'red'
                    elif item.Temsilci == 44:
                        model.borderColor = 'blue'
                    model.ulkeAdi = item.UlkeAdi
                    model.ulkeLogo = item.UlkeLogo
                    model.filelink = item.Filelink
                    model.fileCloud = item.FileCloud
                    model.temsilciAdi = item.TemsilciAdi
                    liste.append(model)
                schema = BgpProjectsListSchema(many=True)
                return schema.dump(liste)
            
        except Exception as e:
            print('getBgpProjectList',str(e))
            return False
        
    def getBgpProjectListAyrinti(self,projectName):
        try:
            result =  self.data.getStoreList("""
                                        select * from BgpProjectDetailList where ProjectName = ?
                                   """,(projectName))
            
            liste = list()
            for item in result:
               model = BgpProjectsAyrintiModel()
               model.id = item.ID
               model.projectName = item.ProjectName
               model.firmaAdi = item.FirmaAdi
               model.kayitTarihi = item.KayitTarihi
               model.baslik = item.Baslik
               model.aciklama = item.Aciklama
               model.hatirlatmaAciklama = item.HatirlatmaAciklama
               model.hatirlatmaTarihi = item.HatirlatmaTarihi
               model.temsilci = item.Temsilci
               model.email = item.Email
               model.phoneNumber = item.PhoneNumber
               model.wrongNumber = item.WrongNumber
               model.notResponse = item.NotResponse
               model.notInterested = item.NotInterested
               model.interested = item.Interested,
               if item.Unvan == 'contractor':
                   model.unvanColor = 'red'
               elif item.Unvan == 'architect':
                   model.unvanColor = 'Yellow'
               else:
                   model.unvanColor = 'white'
               model.unvan = item.Unvan
               liste.append(model)
            schema = BgpProjectsAyrintiSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getBgpProjectList hata',str(e))
            return False
        
    def getBgpDetailModel(self):
        model = BgpProjectsAyrintiModel()
        schema = BgpProjectsAyrintiSchema()
        return schema.dump(model)

         
    def setBgpProjectListDetail(self,datas):
        try:
            self.data.update_insert("""
                                             
                                                insert into BgpProjectDetailList
                                                (
                                                    ProjectName,
                                                    FirmaAdi,
                                                    KayitTarihi,
                                                    Baslik,
                                                    Aciklama,
                                                    HatirlatmaTarihi,
                                                    HatirlatmaAciklama,
                                                    Temsilci,
                                                    Email,
                                                    PhoneNumber,
                                                    WrongNumber,
                                                    NotResponse,
                                                    NotInterested,
                                                    Interested,
                                                    Unvan,
                                                    UlkeAdi
                                                    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                             
                                             
                                             """,(datas['projectName'],
                                                  datas['firmaAdi'],
                                                  datas['kayitTarihi'],
                                                  datas['baslik'],
                                                  datas['aciklama'],
                                                  datas['hatirlatmaTarihi'],
                                                  datas['hatirlatmaAciklama'],
                                                  datas['temsilci'],
                                                  datas['email'],
                                                  datas['phoneNumber'],
                                                  datas['wrongNumber'],
                                                  datas['notResponse'],
                                                  datas['notInterested'],
                                                  datas['interested'],datas['unvan'],datas['ulkeAdi']
                                                  
                                                  
                                                  
                                                  ))
            return True
        except Exception as e:
            print('setBgpProjectListDetail',str(e))
            return False
            
            
    def getBgpProjectDetailForm(self,id):
        try:
            result = self.data.getStoreList("""
                                                select * from BgpProjectDetailList where ID=?
                                            
                                            """,(id))
            liste = list()
            for item in result:
               model = BgpProjectsAyrintiModel()
               model.id = item.ID
               model.projectName = item.ProjectName
               model.firmaAdi = item.FirmaAdi
               model.kayitTarihi = item.KayitTarihi
               model.baslik = item.Baslik
               model.aciklama = item.Aciklama
               model.hatirlatmaAciklama = item.HatirlatmaAciklama
               model.hatirlatmaTarihi = item.HatirlatmaTarihi
               model.temsilci = item.Temsilci
               model.email = item.Email
               model.phoneNumber = item.PhoneNumber
               model.wrongNumber = item.WrongNumber
               model.notResponse = item.NotResponse
               model.notInterested = item.NotInterested
               model.interested = item.Interested
               if item.Unvan == 'contractor':
                   model.unvanColor = 'red'
               elif item.Unvan == 'architect':
                   model.unvanColor = 'Yellow'
               else:
                   model.unvanColor = 'white'
               model.unvan = item.Unvan
               liste.append(model)
            schema = BgpProjectsAyrintiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getBgpProjectDetailForm',str(e))
            return False
        
        
    def setBgpProjectDetailFormChange(self,datas):
        try:
            self.data.update_insert("""
                                    update BgpProjectDetailList
                                        SET
                                          
                                        FirmaAdi =?,
                                        KayitTarihi =?,
                                        Baslik =?,
                                        Aciklama =?,
                                        HatirlatmaTarihi =?,
                                        HatirlatmaAciklama =?,
                                        Email=?,
                                        PhoneNumber=?,
                                        WrongNumber=?,
                                        NotResponse=?,
                                        NotInterested=?,
                                        Interested=?,
                                        Unvan=?
                                        
                                        WHERE ID=?
                                    
                                    """,(datas['firmaAdi'],
                                         datas['kayitTarihi'],
                                         datas['baslik'],
                                         datas['aciklama'],
                                         datas['hatirlatmaTarihi'],
                                         datas['hatirlatmaAciklama'],
                                         datas['email'],
                                         datas['phoneNumber'],
                                         datas['wrongNumber'],
                                         datas['notResponse'],
                                         datas['notInterested'],
                                         datas['interested'],
                                         datas['unvan'],
                                         datas['id']))
            return True
        except Exception as e:
            print('getBgpProjectDetailFormChange',str(e))
            return False
        
        
    def setBgpProjectDetailFormDelete(self,id):
        try:
            self.data.update_insert("""
                                        delete BgpProjectDetailList where ID=?
                                   
                                   """,(id))
            return True
        except Exception as e:
            print('setBgpProjectDetailFormDelete',str(e))
            return False
        
    def setBgpProjectDelete(self,projectName):
        try:
            self.data.update_insert("""
                                        delete BgpNetworkProjects where ProjectName=?
                                    
                                    """,(projectName))
            result2 = self.data.getStoreList("""
                                        select * from BgpProjectDetailList where ProjectName=?
                                   
                                   """,(projectName))
            if len(result2)>0:
                self.data.update_insert("""
                                            delete BgpProjectDetailList where ProjectName=?
                                        
                                        """,(projectName))
            
            
            
            return True
        except Exception as e:
            print('setBgpProjectDelete hata',str(e))
            return False
    
    def getUlkeList(self,id):
        if id == 10:
            result = self.data.getList(
            """
            select 


                        UlkeAdi 


                    from 


                    BgpProjectDetailList 



                    group by
                        UlkeAdi
            """
            )

            liste = list()
            for item in result:
                model = BgpProjectsCountryListModel()
                model.ulkeAdi = item.UlkeAdi
                liste.append(model)
            schema = BgpProjectsCountryListSchema(many=True)
            return schema.dump(liste)
        else:
            result = self.data.getStoreList(
                """
                select 


                            UlkeAdi 


                        from 


                        BgpProjectDetailList 


                        where Temsilci=?

                        group by
                            UlkeAdi
                """,(id)
                )

            liste = list()
            for item in result:
                model = BgpProjectsCountryListModel()
                model.ulkeAdi = item.UlkeAdi
                liste.append(model)
            schema = BgpProjectsCountryListSchema(many=True)
            return schema.dump(liste)
    
    def getBgpProjectsHatirlatmaList(self,userId):
        
        try:
            result = self.data.getStoreList("""
                                            select * from 
                                            BgpProjectDetailList 
                                            where YEAR(HatirlatmaTarihi) = YEAR(GETDATE()) and
                                            MONTH(HatirlatmaTarihi) >= MONTH(GETDATE()) and
                                            DAY(HatirlatmaTarihi) >= DAY(GETDATE()) and
                                            Temsilci=?
                                       """,(userId))
            liste = list()
            for item in result:
                model = BgpProjectsAyrintiModel()
                model.id = item.ID
                model.projectName = item.ProjectName
                model.firmaAdi = item.FirmaAdi
                model.kayitTarihi = item.KayitTarihi
                model.baslik = item.Baslik
                model.aciklama = item.Aciklama
                model.hatirlatmaAciklama = item.HatirlatmaAciklama
                model.hatirlatmaTarihi = item.HatirlatmaTarihi
                model.temsilci = item.Temsilci
                model.email = item.Email
                model.phoneNumber = item.PhoneNumber
                liste.append(model)

            schema = BgpProjectsAyrintiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getBgpProjectsHatirlatmaList',str(e))
            return False
        
    def getBgpProjectCompanyList(self):
        try:
            result = self.data.getList("""
                                                select * from BgpProjectDetailList
                                            
                                            """)
            liste = list()
            for item in result:
               model = BgpProjectsAyrintiModel()
               model.id = item.ID
               model.projectName = item.ProjectName
               model.firmaAdi = item.FirmaAdi
               model.kayitTarihi = item.KayitTarihi
               model.baslik = item.Baslik
               model.aciklama = item.Aciklama
               model.hatirlatmaAciklama = item.HatirlatmaAciklama
               model.hatirlatmaTarihi = item.HatirlatmaTarihi
               model.temsilci = item.Temsilci
               model.email = item.Email
               model.phoneNumber = item.PhoneNumber
               model.wrongNumber = item.WrongNumber
               model.notResponse = item.NotResponse
               model.notInterested = item.NotInterested
               model.interested = item.Interested
               model.unvan = item.Unvan
               
               liste.append(model)
            schema = BgpProjectsAyrintiSchema(many=True)
            return schema.dump(liste)
        except Exception as e:
            print('getBgpProjectCompanyList',str(e))
            return False
        
    def getBgpProjectCompanyStatus(self,username):
        
        if username == 19 or username == 44:
                ulkeler = self.data.getStoreList("""
                            select 
                                bgp.UlkeAdi as UlkeAdi
                            from
                                BgpProjectDetailList bgp
                            where bgp.Temsilci=?
                            
                            group by 
                                bgp.UlkeAdi
                          """,(username))
                ayrintiList = self.data.getStoreList("""
                                                    select bgp.WrongNumber,
                                                    bgp.NotResponse,
                                                    bgp.NotInterested,
                                                    bgp.Interested,
                                                    bgp.UlkeAdi 
                                                    from  BgpProjectDetailList bgp
                                                    where  (bgp.WrongNumber=1 or bgp.NotResponse=1 or bgp.Interested = 1 or bgp.NotInterested=1) and bgp.Temsilci = ?

                                                """,(username))
                liste = list()
                wrongNumber= 0
                notResponse = 0
                notInterested = 0
                interested = 0
                sumWrongNumber = 0
                sumNotResponse = 0
                sumNotInterested = 0
                sumInterested = 0
                for item in ulkeler:
                    for item2 in ayrintiList:
                        if item.UlkeAdi == item2.UlkeAdi:
                            if item2.WrongNumber == True:
                                wrongNumber += 1
                            elif item2.NotResponse == True:
                                notResponse += 1
                            elif item2.NotInterested == True:
                                notInterested += 1
                            elif item2.Interested == True:
                                interested += 1
                            else:
                                continue
                        else:
                             continue
                        
                    liste.append({'ulkeAdi':item.UlkeAdi,'wrongNumber':wrongNumber,'notResponse':notResponse,'notInterested':notInterested,'interested':interested})
                    wrongNumber= 0
                    notResponse = 0
                    notInterested = 0
                    interested = 0
                    
                
                
                
                for item2 in ayrintiList:
                        if item2.WrongNumber == True:
                            sumWrongNumber += 1
                        elif item2.NotResponse == True:
                            sumNotResponse += 1
                        elif item2.NotInterested == True:
                            sumNotInterested += 1
                        elif item2.Interested == True:
                            sumInterested += 1
                        else:
                            continue
                    

                   
            
                
                
                
                return liste
            
        else:
            ulkeler = self.data.getList("""
                            select 
                                bgp.UlkeAdi as UlkeAdi
                            from
                                BgpProjectDetailList bgp
                            
                            group by 
                                bgp.UlkeAdi
                          """)
            ayrintiList = self.data.getList("""
                                                    select bgp.WrongNumber,
                                                        bgp.NotResponse,
                                                        bgp.NotInterested,
                                                        bgp.Interested,
                                                        bgp.UlkeAdi 
                                                        from  BgpProjectDetailList bgp

                                                    where (bgp.WrongNumber=1 or bgp.NotResponse=1 or bgp.Interested = 1 or bgp.NotInterested=1)

                                                """)
            liste = list()
            wrongNumber= 0
            notResponse = 0
            notInterested = 0
            interested = 0
            sumWrongNumber = 0
            sumNotResponse = 0
            sumNotInterested = 0
            sumInterested = 0
            for item in ulkeler:
                for item2 in ayrintiList:
                    if item.UlkeAdi == item2.UlkeAdi:
                        if item2.WrongNumber == True:
                            wrongNumber += 1
                        elif item2.NotResponse == True:
                            notResponse += 1
                        elif item2.NotInterested == True:
                            notInterested += 1
                        elif item2.Interested == True:
                            interested += 1
                        else:
                            continue
                    else:
                        continue

                liste.append({'ulkeAdi':item.UlkeAdi,'wrongNumber':wrongNumber,'notResponse':notResponse,'notInterested':notInterested,'interested':interested})
                wrongNumber= 0
                notResponse = 0
                notInterested = 0
                interested = 0
                
            
            for item2 in ayrintiList:
                if item2.WrongNumber == True:
                    sumWrongNumber += 1
                elif item2.NotResponse == True:
                    sumNotResponse += 1
                elif item2.NotInterested == True:
                    sumNotInterested += 1
                elif item2.Interested == True:
                    sumInterested += 1
                else:
                    continue
                
            
            
            return liste
            

    def getBgpProjectCompanyStatusDetail(self,ulkeAdi):
        try:
            result = self.data.getStoreList("""
                                                select 

                                                        *,
														(select k.KullaniciAdi from KullaniciTB k where k.ID=bgp.Temsilci) as TemsilciAdi


                                                    from BgpProjectDetailList bgp

                                                    where bgp.UlkeAdi=? and (bgp.WrongNumber=1 or bgp.NotInterested=1 or bgp.NotResponse = 1 or bgp.Interested=1) 
                                            
                                            """,(ulkeAdi))
            
            liste = list()
            for item in result:
               model = BgpProjectsAyrintiModel()
               model.id = item.ID
               model.projectName = item.ProjectName
               model.firmaAdi = item.FirmaAdi
               model.kayitTarihi = item.KayitTarihi
               model.baslik = item.Baslik
               model.aciklama = item.Aciklama
               model.hatirlatmaAciklama = item.HatirlatmaAciklama
               model.hatirlatmaTarihi = item.HatirlatmaTarihi
               model.temsilci = item.Temsilci
               model.email = item.Email
               model.phoneNumber = item.PhoneNumber
               model.wrongNumber = item.WrongNumber
               model.notResponse = item.NotResponse
               model.notInterested = item.NotInterested
               model.interested = item.Interested
               model.unvan = item.Unvan
               model.temsilciAdi = item.TemsilciAdi
               
               liste.append(model)
            schema = BgpProjectsAyrintiSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getBgpProjectCompanyStatusDetail hata',str(e))
            return False
            
    
    def getBgpProjectsCompanyDetailList(self):
        result = self.data.getList("""
                                        select 

                                            bgp.FirmaAdi 

                                        from BgpProjectDetailList bgp group by bgp.FirmaAdi
                                   
                                   """)
        liste = list()
        for item in result:
            model = BgpProjectsCompanyDetailListModel()
            model.firmaAdi = item.FirmaAdi
            liste.append(model)
        schema = BgpProjectsCompanyDetailListSchema(many=True)
        return schema.dump(liste)
    
    
    
    def getBgpProjectsCompanySelectedDetailList(self,firmaAdi):
        try:
            result =  self.data.getStoreList("""
                                        select * from BgpProjectDetailList where FirmaAdi = ?
                                   """,(firmaAdi))
            
            liste = list()
            for item in result:
               model = BgpProjectsAyrintiModel()
               model.id = item.ID
               model.projectName = item.ProjectName
               model.firmaAdi = item.FirmaAdi
               model.kayitTarihi = item.KayitTarihi
               model.baslik = item.Baslik
               model.aciklama = item.Aciklama
               model.hatirlatmaAciklama = item.HatirlatmaAciklama
               model.hatirlatmaTarihi = item.HatirlatmaTarihi
               model.temsilci = item.Temsilci
               model.email = item.Email
               model.phoneNumber = item.PhoneNumber
               model.wrongNumber = item.WrongNumber
               model.notResponse = item.NotResponse
               model.notInterested = item.NotInterested
               model.interested = item.Interested
               model.unvan = item.Unvan
               liste.append(model)
            schema = BgpProjectsAyrintiSchema(many=True)
            return schema.dump(liste)
            
        except Exception as e:
            print('getBgpProjectsCompanyDetailList hata',str(e))
            return False
        
        
        
        
    def getBgpProjectCountryandReseptation(self):
        result = self.data.getList("""
                            select 

                                count(bgp.UlkeAdi) as SumProject,
                                bgp.Temsilci as TemsilciId,
                                bgp.UlkeAdi as UlkeAdi,
                                (select k.KullaniciAdi from KullaniciTB k where k.ID = bgp.Temsilci) as TemsilciAdi


                            from BgpProjectDetailList bgp

                            group by
                                bgp.Temsilci,bgp.UlkeAdi
                          
                          """)
        liste = list()
        for item in result:
            model = BgpProjectsCountryandReseptationModel()
            model.temsilci = item.TemsilciAdi
            model.temsilciId = item.TemsilciId
            model.ulkeAdi = item.UlkeAdi
            model.projectSum = item.SumProject
            liste.append(model)
            
        schema = BgpProjectsCountryandReseptationSchema(many=True)
        return schema.dump(liste)
    
    
    def getCountryList(self):
        result = self.data.getList("""
                                   select count(bgp.UlkeAdi) as Total,bgp.UlkeAdi as UlkeAdi from BgpProjectDetailList bgp group by bgp.UlkeAdi

                                   """)
        liste = list()
        for item in result:
            model = BgpProjectsCountryListModel()
            model.ulkeAdi = item.UlkeAdi
            model.toplamProje = item.Total
            liste.append(model)
        schema = BgpProjectsCountryListSchema(many=True)
        return schema.dump(liste)
    
    def setFileData(self,data):
        try:
            self.data.update_insert("""
                                        update BgpNetworkProjects SET Filelink=?,FileCloud=? where ID=?

                                    """,(data['link'],True,data['id']))

            return True
        except Exception as e:
            print("setFileData hata",str(e))
            return False