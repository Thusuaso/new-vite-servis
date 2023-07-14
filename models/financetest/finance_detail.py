from marshmallow import Schema,fields

class FinanceDetailSchema(Schema):
    customer_id = fields.Int()
    po = fields.String()
    cost = fields.Float()
    paid = fields.Float()
    balance = fields.Float()
    status = fields.String()
    advanced_payment = fields.Float()
    product_date = fields.String()
    forwarding_date = fields.String()
    maya_control = fields.Boolean()
    
class FinanceDetailModel:
    customer_id = 0
    po = ""
    cost = 0
    paid = 0
    balance = 0
    status = ""
    advanced_payment = 0
    product_date = ""
    forwarding_date = ""
    maya_control = False
    
class ByDatePaidsSchema(Schema):
    date = fields.String()
    paid = fields.Float()
    
class ByDatePaidsModel:
    date = ""
    paid = 0
    