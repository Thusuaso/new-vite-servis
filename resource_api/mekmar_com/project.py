from flask import jsonify,request
from flask_restful import Resource
from views.islemler.project import Project
from views.teklifler import Ulke
from models.mekmar_com.project import *

class ProjectApi(Resource):
    def get(self):
        project = Project()
        project_list = project.getProjectList()
        return jsonify(project_list)
    
class ProjectDetailApi(Resource):
    def get(self,id):
        project= Project()
        project_detail_list = project.getProjectDetailList(id)
        project_detail_video_list = project.getProjectDetailVideoList(id)
        project_detail_information_list = project.getProjectDetailInformation(id)
        data = {
            'project_detail_list':project_detail_list,
            'project_detail_video_list':project_detail_video_list,
            'project_detail_information_list':project_detail_information_list
            
        }
        return jsonify(data)
    
class ProjectModelApi(Resource):
    def get(self):
        model = ProjectListModel()
        schema = ProjectListSchema()
        country = Ulke()
        countryList = country.getUlkeList()
        data = {
            'model':schema.dump(model),
            'countryList':countryList,
            
        }
        return jsonify(data)

class ProjectSaveApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.setNewProject(data)
        return {'status':status}
    
class ProjectDeletePhotosApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.deletePhotos(data)
        return {'status':status}
    
class ProjectAddPhotosApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.addPhotos(data)
        return {'status':status}
    
class ProjectAddVideoApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.addVideo(data)
        return {'status':status}
    
    
class ProjectInformationApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.addInformation(data)
        return {'status':status}
    
    def put(self):
        data = request.get_json()
        project = Project()
        status = project.updateInformation(data)
        return {'status':status}
    
class ProjectListSuggestedApi(Resource):
    def get(self,id):
        project = Project()
        not_suggested = project.getNotSuggested(id)
        suggested = project.getSuggested(id)
        data = {
            'not_suggested':not_suggested,
            'suggested':suggested
        }
        return jsonify(data)
    
class ProjectSuggestedApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        project.deleteSuggested(data[0])
        status = project.setSuggested(data[1])
        return {'status':status}
    
class ProjectQueueApi(Resource):
    def post(self):
        
        data = request.get_json()
        project = Project()
        status = project.setProjectQueue(data)
        return {'status':status}
    
class ProjectMainPhotosChaneApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.setChangeMainPhotos(data)
        return {'status':status}
    
    
class ProjectMainPhotosChangeApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.setChangeMainPhotosData(data)
        return {'status':status}

class ProjectPhotosQueueChangeApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.setChangePhotosQueue(data)
        return {'status':status}
    
class ProjectProductsNameChangeApi(Resource):
    def post(self):
        data = request.get_json()
        project = Project()
        status = project.setChangeProductsName(data)
        
        return {'status':status}
