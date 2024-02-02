from helpers.sqlConnect import SqlConnect
from models.mekmar_com.project import ProjectListSchema,ProjectListModel,ProjectListDetailSchema,ProjectListDetailModel,ProjectInformationListDetailModel,ProjectInformationListDetailSchema
import boto3
from boto3 import session
from botocore.client import Config
from boto3.s3.transfer import S3Transfer
class Project:
    def __init__(self):
        self.sql = SqlConnect().data
        session = boto3.session.Session()

        self.client = session.client(
            's3',
            region_name='fra1',
            endpoint_url='https://fra1.digitaloceanspaces.com',
            aws_access_key_id = 'B7POIPPYM44Y374P23KS',
            aws_secret_access_key='01CMWBcNKtFgKG6XhP+q0PlajTb2yvELaJ1igo7xsyA'
        )
    def getProjectList(self):
        result = self.sql.getList("""
                                    select 
                                        ID,
                                        ProjectName,
                                        CountryId,
                                        CountryName,
                                        Image,
                                        Queue
                                    from MekmarCom_Projects order by Queue
                                  """)
        liste = list()
        for item in result:
            model = ProjectListModel()
            model.id = item.ID
            model.project_name = item.ProjectName
            model.project_country_id = item.CountryId
            model.project_country_name = item.CountryName
            model.project_image = item.Image
            model.queue = item.Queue
            liste.append(model)
        schema = ProjectListSchema(many = True)
        return schema.dump(liste)
    
    def getProjectDetailList(self,id):
        result = self.sql.getStoreList("""
                                            select 
                                                ID,
                                                ProjectId,
                                                ProjectName,
                                                ImageLink,
                                                VideosLink,
                                                ImageStatus,
                                                VideosStatus,
                                                Queue,
                                                ImageName,
                                                ProductName,
                                                ProductName_Fr,
                                                ProductName_Es,
                                                ProductName_Ru
                                            from MekmarCom_Project_Detail
                                            where ProjectId=? and ImageStatus=1
                                       """,(id))
        
        liste = list()
        for item in result:
            model = ProjectListDetailModel()
            model.id = item.ID
            model.project_id = item.ProjectId
            model.project_name = item.ProjectName
            model.image_link = item.ImageLink
            model.video_link = item.VideosLink
            model.image_status = item.ImageStatus
            model.video_status = item.VideosStatus
            model.queue = item.Queue
            model.image_name = item.ImageName
            model.product_name = item.ProductName
            model.product_name_fr = item.ProductName_Fr
            model.product_name_es = item.ProductName_Es
            model.product_name_ru = item.ProductName_Ru
            liste.append(model)
        schema = ProjectListDetailSchema(many=True)
        return schema.dump(liste)  
    
    
    def getProjectDetailVideoList(self,id):
        result = self.sql.getStoreList("""
                                            select 
                                                ID,
                                                ProjectId,
                                                ProjectName,
                                                ImageLink,
                                                VideosLink,
                                                ImageStatus,
                                                VideosStatus,
                                                Queue 
                                            from MekmarCom_Project_Detail 
                                            where ProjectId=? and VideosStatus=1
                                       """,(id))
        if(len(result)>0):
        
            liste = list()
            for item in result:
                model = ProjectListDetailModel()
                model.id = item.ID
                model.project_id = item.ProjectId
                model.project_name = item.ProjectName
                model.image_link = item.ImageLink
                model.video_link = item.VideosLink
                model.image_status = item.ImageStatus
                model.video_status = item.VideosStatus
                model.queue = item.Queue
                liste.append(model)
            schema = ProjectListDetailSchema(many=True)
            return schema.dump(liste)
        else:
            liste = list()
            model = ProjectListDetailModel()
            liste.append(model)
            schema = ProjectListDetailSchema(many=True)
            return schema.dump(liste)
            
    
    def getProjectDetailInformation(self,id):
        result = self.sql.getStoreList("""
                                        select ID,ProjectId,ProjectInformation,ProjectProductName,ProjectInformation_Fr,ProjectInformation_Es,ProjectInformation_Ru from MekmarCom_Projects_Information where ProjectId=?
                                       """,(id))
        if(len(result)>0):
            liste = list()
            for item in result:
                model = ProjectInformationListDetailModel()
                model.id = item.ID
                model.project_id = item.ProjectId
                if(item.ProjectInformation == None):
                    model.information = ""
                else:
                    model.information = item.ProjectInformation

                if(item.ProjectInformation_Fr == None):
                    model.information_fr = ""
                else:
                    model.information_fr = item.ProjectInformation_Fr
                    
                if(item.ProjectInformation_Es == None):
                    model.information_es = ""
                else:
                    model.information_es = item.ProjectInformation_Es

                if(item.ProjectInformation_Ru == None):
                    model.information_ru = ""
                else:
                    model.information_ru = item.ProjectInformation_Ru
            
            
                model.project_product_name = item.ProjectProductName
                liste.append(model)
            schema = ProjectInformationListDetailSchema(many = True)
            return schema.dump(liste)
        else:
            liste = list()
            model = ProjectInformationListDetailModel()
            liste.append(model)
            schema = ProjectInformationListDetailSchema(many = True)
            return schema.dump(liste)
            
    
    def setNewProject(self,data):
        try:
            self.sql.update_insert("""
                                    insert into MekmarCom_Projects
                                        (ProjectName,CountryName,CountryId,Image,Queue) 
                                    VALUES(?,?,?,?,?) 
                                   """,(data['project_name'],data['project_country_name'],data['project_country_id'],data['project_image'],self.findQueueProject()))
            return True
        except Exception as e:
            print('setNewProject hata',str(e))
            return False
        
    def deletePhotos(self,data):
        try:
            print(data)
            for item in data:
                self.sql.update_insert("""
                                        delete MekmarCom_Project_Detail where ID = ?
                                      """,(item['id']))
                
                self.client.delete_object(
                    Bucket='mekmar-image',
                    Key= 'galleria-project_photos/photos/' +  item['image_name'] + '.jpg'
                )
                
                
                
                
            return True
        except Exception as e:
            print('deletePhotos hata',str(e))
            return False
        
    def addPhotos(self,photos):
        try:
            for item in photos:
                self.sql.update_insert("""
                                            insert into MekmarCom_Project_Detail(ProjectId,ProjectName,ImageLink,ImageStatus,VideosStatus,Queue,ImageName) VALUES(?,?,?,?,?,?,?)

                                       """,(item['id'],item['name'],item['image_link'],item['image_status'],item['video_status'],self.findQueue(item['id']),item['image_name']))
            return True
        except Exception as e:
            print('addPhotos hata',str(e))
            return False
        
    def findQueue(self,id):
        queue = self.sql.getStoreList("""
                                select Queue from  MekmarCom_Project_Detail where ProjectId=? and ImageStatus=1 order by Queue desc
                              """,(id))
        if(len(queue)>0):
            return int(queue[0].Queue) + 1
        else:
            return 1
    
    def findQueueProject(self):
        queue = self.sql.getList("""
                                    select Queue from MekmarCom_Projects where Queue != 30 order by Queue desc
                                  """)
        return int(queue[0].Queue) + 1
    
    
    def addVideo(self,data):
        try:
            self.sql.update_insert("""
                                        insert into MekmarCom_Project_Detail(ProjectId,ProjectName,ImageStatus,VideosStatus,VideosLink) VALUES(?,?,?,?,?)
                                   """,(data['id'],data['project_name'],data['image_status'],data['videos_status'],data['videos_link']))
            return True
        except Exception as e:
            print('addVideo hata',str(e))
            return False
        
    def addInformation(self,data):
        print(data)
        try:
            self.sql.update_insert("""
                                    insert into MekmarCom_Projects_Information(ProjectId,ProjectInformation,ProjectInformation_Fr,ProjectInformation_Es,ProjectInformation_Ru) VALUES(?,?,?,?,?)

                                   """,(data['project_id'],data['project_information'],data['project_information_fr'],data['project_information_es'],data['project_information_ru']))
            return True
        except Exception as e:
            print('',str(e))
            return False
        
    def updateInformation(self,data):
        
        try:
            self.sql.update_insert("""
                                   
                                        Update MekmarCom_Projects_Information SET ProjectInformation=?,ProjectInformation_Fr=?,ProjectInformation_Es=?,ProjectInformation_Ru=? WHERE ID=?
                                   """,(data['information'],data['information_fr'],data['information_es'],data['information_ru'],data['id']))
            return True
        except Exception as e:
            print('updateInformation hata',str(e))
            return False
        
    def getNotSuggested(self,id):
        try:
            result = self.sql.getStoreList("""
                                            select mp.ID,mp.ProjectName,mp.Image,mp.Queue from MekmarCom_Projects mp where  mp.ID not in (

                                                        select mps.SuggestedId from MekmarCom_Projects_Suggested mps where mps.ProjectId=?
														
														)
									order by mp.Queue 
                                           """,(id))
            liste = list()
            for item in result:
                if(item.ID == id):
                    continue
                else:
                    model = ProjectListModel()
                    model.id = item.ID
                    model.project_name = item.ProjectName
                    model.project_image = item.Image
                    liste.append(model)
            schema = ProjectListSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print('getProjectListSuggested hata',str(e))
            return False
        
    def getSuggested(self,id):
        try:
            result = self.sql.getStoreList("""
                                            select mp.ID,mp.ProjectName,mp.Image from MekmarCom_Projects mp where  mp.ID in (

                                                        select mps.SuggestedId from MekmarCom_Projects_Suggested mps where mps.ProjectId=?
                                                    )
                                           """,(id))
            liste = list()
            for item in result:
                model = ProjectListModel()
                model.id = item.ID
                model.project_name = item.ProjectName
                model.project_image = item.Image
                liste.append(model)
            schema = ProjectListSchema(many=True)
            return schema.dump(liste)
        
        except Exception as e:
            print('getProjectListSuggested hata',str(e))
            return False
    
    def setSuggested(self,data):
        try:
            for item in data:
                result = self.sql.getStoreList("""
                                            select * from MekmarCom_Projects_Suggested where ProjectId=? and SuggestedId=?
                                      
                                      """,(item['project_id'],item['id']))
                if(len(result)>0):
                    continue
                else:
                
                    self.sql.update_insert("""
                                        insert into MekmarCom_Projects_Suggested(ProjectId,SuggestedId) VALUES(?,?)

                                        """,(item['project_id'],item['id']))
            
            return True
        except Exception as e:
            print('setSuggested hata',str(e))
            return False
    
    
    def deleteSuggested(self,data):
        try:
            result = None
            for item in data:
                result = self.sql.getStoreList("""
                                            select * from MekmarCom_Projects_Suggested where ProjectId=? and SuggestedId=?
                                      """,(item['project_id'],item['id']))
            if(result):
                self.sql.update_insert("""
                                            delete MekmarCom_Projects_Suggested WHERE ID=?
                                        """,(result[0][0]))
                
        except Exception as e:
            print('e',str(e))
            return False
    
    
    def setProjectQueue(self,data):
        try:
            for item in data:
                self.sql.update_insert("""
                                        update MekmarCom_Projects SET Queue = ? where ID=?
                                   """,(item['queue'],item['id']))
            return True
        except Exception as e:
            print('setProjectQueue,hata',str(e))
            return False
        
    def setChangeMainPhotos(self,data):
        try:
            image = 'https://mekmar-image.fra1.cdn.digitaloceanspaces.com/galleria-project_photos/' + data['newFileName']
            self.sql.update_insert("""
                                        update MekmarCom_Projects SET Image=? where ID=? 
                                   """,(image,data['project_id'])
                                    )
            return True
        except Exception as e:
            print('setChangeMainPhotos',(str(e)))
            return False
    def setChangeMainPhotosData(self,data):
        try:
            projectOldMainImage = self.sql.getStoreList("""
                                select Image from MekmarCom_Projects where ID=?

                             """,(data['project_id']))[0][0]
            self.sql.update_insert("""
                                        update MekmarCom_Projects SET Image = ? where ID=?
                                   """,(data['image_link'],data['project_id']))
            self.sql.update_insert("""
                                        update MekmarCom_Project_Detail SET ImageLink=? where ID=?
                                   """,(projectOldMainImage,data['id']))
            
            print('Ana Fotoğraf Değiştirildi...')
            return True
            
        except Exception as e:
            print('setChangeMainPhotosData hata')
            return False
        
    def setChangePhotosQueue(self,data):
        try:
            for item in data:
                
                self.sql.update_insert("""
                                        update MekmarCom_Project_Detail SET Queue =? where ID=?
                                   
                                   """,(item['queue'],item['id']))
            return True
        except Exception as e:
            print('setChangePhotosQueue hata',str(e))
            return False
        
    def setChangeProductsName(self,data):
        try:
            self.sql.update_insert("""
                                    update MekmarCom_Project_Detail SET ProductName=?,ProductName_Fr=?,ProductName_Es=?,ProductName_Ru=? where ID=?
                                   """,(data['product_name'],data['product_name_fr'],data['product_name_es'],data['product_name_ru'],data['id']))
            return True
        except Exception as e:
            print('setChangeProductsName hata',str(e))
            return False