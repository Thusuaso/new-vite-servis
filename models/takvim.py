from marshmallow import Schema,fields



class TakvimSchema(Schema):
    id = fields.Int()
    title = fields.String()
    start = fields.String()
    end = fields.String()
    url = fields.String()
    color = fields.String()
    source = fields.String()
    description = fields.String()
    allDay = fields.Boolean()
    hatirlatmaAciklama = fields.String()
    hatirlatmaDurum = fields.String()
    


class TakvimModel:
    id = None
    title = ""
    start = ""
    end = ""
    url = ""
    color = ""
    source = "python"
    description = "Pazarlama"
    allDay = True
    hatirlatmaAciklama = ""
    hatirlatmaDurum = False
    
    
    
class TeklifUlkeSchema(Schema):
    id = fields.Int()
    country = fields.String()
    countryTop = fields.Int()
    
class TeklifUlkeModel:
    id = 0
    country = ""
    countryTop = 0