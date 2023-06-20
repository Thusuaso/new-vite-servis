from marshmallow import Schema,fields


class TedarikciFormSchema(Schema):
    id = fields.Int() 
    siparis_no = fields.String()
    fatura_tur_id = fields.Int()
    teslim_id = fields.Int()
    siparis_tarihi = fields.String() 
    teslim_tarihi = fields.String()
    madde4 = fields.String()
    madde5 = fields.String()
    kullanici_id = fields.Int()
    kullanici_adi = fields.String()
    tedarikci_id = fields.Int()

class TedarikciFormModel:
    id = None 
    siparis_no = ""
    fatura_tur_id = None
    teslim_id = None
    siparis_tarihi = ""
    teslim_tarihi = ""
    madde4 = ""
    madde5 = ""
    kullanici_id = None
    kullanici_adi = ""
    tedarikci_id = None
    
class TedarikciTeslimvFaturaTurSchema(Schema):
    id = fields.Int()
    tur = fields.String()
    
    
class TedarikciTeslimvFaturaTurModel:
    id = 0
    tur = ""