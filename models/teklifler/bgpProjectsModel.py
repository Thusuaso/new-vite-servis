from marshmallow import Schema,fields

class BgpProjectsListSchema(Schema):
    id = fields.Int()
    projectName = fields.String()
    dateOfRegistiration = fields.String()
    temsilci = fields.Int()
    ulkeAdi = fields.String()
    ulkeLogo = fields.String()
    borderColor = fields.String()
    filelink = fields.String()
    fileCloud = fields.Boolean()
    temsilciAdi = fields.String()
class BgpProjectsListModel:

    id = 0
    projectName = ""
    dateOfRegistiration = ""
    temsilci = 0
    ulkeAdi=""
    ulkeLogo=""
    borderColor=""
    filelink = ""
    fileCloud = False
    temsilciAdi = ""
    

class BgpProjectsAyrintiSchema(Schema):
    id = fields.Int()
    projectName = fields.String()
    firmaAdi = fields.String()
    kayitTarihi = fields.String()
    baslik = fields.String()
    aciklama = fields.String()
    hatirlatmaTarihi = fields.String()
    hatirlatmaAciklama = fields.String()
    temsilci = fields.Int()
    email = fields.String()
    phoneNumber = fields.String()
    wrongNumber = fields.Boolean()
    notResponse = fields.Boolean()
    notInterested = fields.Boolean()
    interested = fields.Boolean()
    unvan = fields.String()
    unvanColor = fields.String()
    temsilciAdi = fields.String()
    ulkeAdi = fields.String()

class BgpProjectsAyrintiModel:
    id = 0
    projectName = ""
    firmaAdi = ""
    kayitTarihi = ""
    baslik = ""
    aciklama = ""
    hatirlatmaTarihi = ""
    hatirlatmaAciklama = ""
    temsilci = 0
    email = ""
    phoneNumber = ""
    wrongNumber = False
    notResponse = False
    notInterested = False
    interested = False
    unvan = ""
    unvanColor = ""
    temsilciAdi =""
    ulkeAdi = ""

    
class BgpProjectsUlkeSchema(Schema):
    id= fields.Int()
    ulke_adi = fields.String()
    logo = fields.String()
    
class BgpProjectsUlkeModel(Schema):
    id= 0
    ulke_adi = ""
    logo = ""
    
class BgpProjectsStatisticsSchema(Schema):
    ulkeAdi = fields.String()
    wrongNumber = fields.Int()
    notResponse = fields.Int()
    notInterested = fields.Int()
    interested = fields.Int()
    
class BgpProjectsStatisticsModel:
    ulkeAdi = ""
    wrongNumber = 0
    notResponse = 0
    notInterested = 0
    interested = 0
    
    
class BgpProjectsCompanyDetailListSchema(Schema):
    firmaAdi = fields.String()
    
class BgpProjectsCompanyDetailListModel:
    firmaAdi =""
    
    
class BgpProjectsCountryandReseptationSchema(Schema):
    temsilci = fields.String()
    temsilciId = fields.Int()
    ulkeAdi = fields.String()
    projectSum = fields.Int()
    
    
class BgpProjectsCountryandReseptationModel:
    temsilci = ""
    temsilciId = 0
    ulkeAdi = ""
    projectSum = 0
    
    
class BgpProjectsCountryListSchema(Schema):
    ulkeAdi = fields.String()
    toplamProje = fields.Int()
class BgpProjectsCountryListModel:
    ulkeAdi = ""
    toplamProje = ""
    