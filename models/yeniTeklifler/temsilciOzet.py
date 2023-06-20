from marshmallow import Schema,fields


class TemsilciOzetSchema(Schema):
    id = fields.Int()
    temsilci_id = fields.Int()
    adi = fields.String()
    teklifSayisi = fields.Int()
    proformaSayisi = fields.Int()

class TemsilciOzetModel:
    id = None 
    temsilci_id = 0
    adi = ""
    teklifSayisi = 0 
    proformaSayisi = 0