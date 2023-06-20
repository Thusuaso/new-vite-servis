from flask_restful import Resource
from views.teklifler.bgpProject import BgpProjects
from flask import jsonify,request
from views.shared import Ulkeler
class BgpProjectApi(Resource):
    def post(self):
        data = request.get_json()
        islem = BgpProjects()
        status = islem.setBgpProjectsName(data)
        
        return {'status':status}
    
class BgpProjectApiList(Resource):
    def get(self,temsilci):
        islem = BgpProjects()
        result = islem.getBgpProjectList(temsilci)
        bgpulkeler = islem.getUlkeList(temsilci)
        statistic = islem.getBgpProjectCompanyStatus(temsilci)
        ulkelerListDrop = islem.getCountryList()
        representiveCountry = islem.getBgpProjectCountryandReseptation()
        return {'result':result,'bgpulkeler':bgpulkeler,'statistic':statistic,'ulkelerListDrop':ulkelerListDrop,'representiveCountry':representiveCountry}
    
class BgpProjectAyrintiApi(Resource):
    def get(self,projectName):
        islem = BgpProjects()
        result = islem.getBgpProjectListAyrinti(projectName)
        return result
    
class BgpDetailModelApi(Resource):
    def get(self):
        islem = BgpProjects()
        result = islem.getBgpDetailModel()
        return result
    
class BgpProjectAyrintiSave(Resource):
    def post(self):
        data = request.get_json()
        islem = BgpProjects()
        status = islem.setBgpProjectListDetail(data)
        return {'status':status}
    def put(self):
        datas = request.get_json()
        islem = BgpProjects()
        status = islem.setBgpProjectDetailFormChange(datas)
        return {'status':status}
    
    
class BgpProjectAyrintiForm(Resource):
    def get(self,id):
        islem = BgpProjects()
        result = islem.getBgpProjectDetailForm(id)
        return result
    



class BgpProjectAyrintiFormDelete(Resource):
    def delete(self,id):
        islem = BgpProjects()
        status = islem.setBgpProjectDetailFormDelete(id)
        return {'status':status}
    
class BgpProjectDelete(Resource):
    def delete(self,projectName):
        islem = BgpProjects()
        status = islem.setBgpProjectDelete(projectName)
        return {'status':status}
        
class BgpProjectHatirlatmaListApi(Resource):
    def get(self,userId):
        islem = BgpProjects()
        result = islem.getBgpProjectsHatirlatmaList(userId)
        return {'result': result}
    
class BgpProjectCompanyListApi(Resource):
    def get(self):
        islem = BgpProjects()
        result = islem.getBgpProjectCompanyList()
        return {'result':result}

class BgpProjectCompanyStatusApi(Resource):
    def get(self,username):
        islem = BgpProjects()
        result,basicData = islem.getBgpProjectCompanyStatus(username)
        return {'result':result,'chartData':basicData}
    
    
    
class BgpProjectByCountryandReseptationApi(Resource):
    def get(self):
        islem = BgpProjects()
        result = islem.getBgpProjectCountryandReseptation()
        return {'result':result}
    
class BgpProjectCompanyStatusDetailApi(Resource):
    def get(self,ulkeAdi):
        islem = BgpProjects()
        result = islem.getBgpProjectCompanyStatusDetail(ulkeAdi)
        return {'result':result}
    
class BgpProjectChangeApi(Resource):
    def get(self,projectName,temsilci,bgpUlkeAdi,ulkeLogo,projectId):
        islem = BgpProjects()
        status,result = islem.setBgpProjectsNameChange(projectName,temsilci,bgpUlkeAdi,ulkeLogo,projectId)
        
        return {'status':status,'result':result}
    
class BgpProjectCompanyDetailListApi(Resource):
    def get(self):
        islem = BgpProjects()
        result = islem.getBgpProjectsCompanyDetailList()
        return result
    
class BgpServiceSelectedCompanyApi(Resource):
    def get(self,firmaAdi):
        islem = BgpProjects()
        result = islem.getBgpProjectsCompanySelectedDetailList(firmaAdi)
        return result
    
class BgpProjectCountryListApi(Resource):
    def get(self):
        islem = BgpProjects()
        result = islem.getCountryList()
        return result
        
class BgpProjectFileSave(Resource):
    def post(self):
        data = request.get_json()
        islem = BgpProjects()
        result = islem.setFileData(data)
        return result