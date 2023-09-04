from marshmallow import Schema,fields

class ProjectListSchema(Schema):
    id = fields.Int()
    project_name = fields.String()
    project_country_id = fields.Int()
    project_country_name = fields.String()
    project_image = fields.String()
    queue = fields.Int()
    
class ProjectListModel:
    id = 0
    project_name = ""
    project_country_id = 0
    project_country_name = ""
    project_image = ""
    queue=0
    
class ProjectListDetailSchema(Schema):
    id = fields.Int()
    project_id = fields.Int()
    project_name = fields.String()
    image_link = fields.String()
    video_link = fields.String()
    image_status = fields.Boolean()
    video_status = fields.Boolean()
    queue = fields.Int()
    image_name = fields.String()
    
class ProjectListDetailModel:
    id = 0
    project_id = 0
    project_name = ""
    image_link = ""
    video_link = ""
    image_status = 0
    video_status = 0
    queue = 0
    image_name = ""
    
class ProjectInformationListDetailSchema(Schema):
    id = fields.Int()
    project_id = fields.Int()
    information = fields.String()
    project_product_name = fields.String()
    
class ProjectInformationListDetailModel:
    id = 0
    project_id = 0
    information = ""
    project_product_name = ""
