from marshmallow import Schema,fields

class YapilacaklarSchema(Schema):
    id = fields.Int()
    gorev_sahibi_adi = fields.String()
    gorev_sahibi_id = fields.Int()
    yapilacak = fields.String()
    yapildi = fields.Boolean()
    gorev_veren_id = fields.Int()
    gorev_veren_adi = fields.String()
    girisTarihi = fields.String()
    yapildiTarihi = fields.String()
    oncelik = fields.String()
    userStatus = fields.Boolean()
    aciliyet = fields.Boolean()
    ortak_gorev = fields.String()
    
class YapilacaklarModel:
    id = 0
    gorev_sahibi_adi = ""
    gorev_sahibi_id = 0
    yapilacak = ""
    yapildi = False
    gorev_veren_id = 0
    gorev_veren_adi = ""
    girisTarihi = ""
    yapildiTarihi = ""
    oncelik = ""
    userStatus = False
    aciliyet = False
    ortak_gorev = ''

class YapilacaklarKullanicilarSchema(Schema):
    
    id = fields.Int()
    username = fields.String()
    email = fields.String()
    
class YapilacaklarKullanicilarModel:
    
    id = 0
    username = ""
    email = ""

