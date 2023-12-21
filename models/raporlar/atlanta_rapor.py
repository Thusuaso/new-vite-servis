from marshmallow import Schema,fields,validate


class YuklemeAylikSchema(Schema):

   yukleme_tarihi = fields.String()
   siparis_no = fields.String()
   musteri_adii = fields.String()
   fob = fields.Float()
   dtp = fields.Float()
   tur = fields.String()
   marketing = fields.String()
   musteriID = fields.Int()
   navlun = fields.Float()
   detay_1 = fields.Float()
   detay_2 = fields.Float()
   detay_3 = fields.Float()

class YuklemeAylikModel:

    yukleme_tarihi = ""
    siparis_no = "" 
    musteri_adii = ""
    fob = 0
    dtp = 0
    tur = ""
    marketing = ""
    musteriID=0


class YuklemeYillikSchema(Schema):
   siparis_tarihi = fields.String()
   yukleme_tarihi = fields.String()
   siparis_no = fields.String()
   musteri_adi = fields.String()
   fob = fields.Float()
   dtp = fields.Float()
   tur = fields.String()
   marketing = fields.String()
   musteriID = fields.Int()
   navlun = fields.Float()
   detay_1 = fields.Float()
   detay_2 = fields.Float()
   detay_3 = fields.Float()
   musteri_yeri = fields.String()

class YuklemeYillikModel:
    siparis_tarihi = ""
    yukleme_tarihi = ""
    siparis_no = "" 
    musteri_adi = ""
    fob = 0
    dtp = 0
    tur = ""
    marketing = ""
    musteriID = 0  
    navlun = 0
    detay_1 = 0
    detay_2 = 0
    detay_3 = 0
    musteri_yeri = ""
    


class YuklemeAySchema(Schema):
    id = fields.Int()
    ay = fields.Int()
    ay_str = fields.String()

class YuklemeAyModel:
    id = None
    ay = 0
    ay_str = ""        
     
class YuklemeyilSchema(Schema):
    id = fields.Int()
    yil = fields.Int()
    

class YuklemeYilModel:

    id = None
    yil = 0    


    
