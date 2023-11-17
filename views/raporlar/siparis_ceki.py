from models.raporlar import SiparisCekiModel,SiparisCekiSchema
from helpers import SqlConnect


class SiparisCeki:

    def __init__(self):
        self.data = SqlConnect().data

    def getCekiList(self,siparisNo):

        cekiList = list()
        result = self.data.getStoreList("{call PytService_Siparis_CekiListesi3(?)}",(siparisNo))
      
        sira = 1
        for item in result:

            model = SiparisCekiModel()
            model.id = item.ID
            model.sira = sira 
             
            model.birimAdi = item.BirimAdi 
            model.boy = item.Boy 
            model.en = item.En 
            model.kasaNo = item.KasaNo 
            model.kategoriAdi = item.KategoriAdi 
            model.kenar = item.Kenar 
            model.kutuAdet =  item.KutuAdet 
            model.miktar = item.Miktar 
            model.tedarikciAdi = item.TedarikciAdi 
            model.urunAdi = item.UrunAdi 
            model.yuzeyIslem = item.YuzeyIslem
            model.urunKart = item.UrunKartID
            model.adet = item.Adet
            # if(item.BirimAdi == 'M2'):
            #     model.kasaAdet= self.__getAdetHesaplama(item.En,item.Boy,item.Miktar)
            #     model.kasaMt = 0
            #     model.kasaM2 = item.Miktar
            #     model.adet = model.kasaAdet
            # elif(item.BirimAdi == 'Adet'):
            #     if(model.kutuAdet != None or model.kutuAdet != 0):
            #         model.kasaAdet = item.Adet
            #         model.kutuAdet = item.Adet
            #     else:
            #         model.kasaAdet = item.Miktar
            #         model.kasaMt = 0
            #         model.kasaM2 = self.__getM2Hesaplama(item.En,item.Boy,item.Miktar)
            #         model.adet = item.Adet
            #         model.miktar = model.kasaM2
            # elif(item.BirimAdi == 'Mt'):
            #     model.kasaAdet = 0
            #     model.kasaMt = item.Miktar
            #     model.kasaM2 = 0
            if(item.BirimAdi == 'M2'):
                model.kasaM2 = item.Miktar
                if(model.adet == None or model.adet == 0):
                    model.adet = self.__getAdetHesaplama(item.En,item.Boy,item.Miktar)
            
            if(item.BirimAdi == 'Adet'):
                model.adet = item.Miktar
                model.miktar = self.__getM2Hesaplama(item.En,item.Boy,item.Miktar)
                model.kasaM2 = model.miktar
            
            model.tonaj = self.__getTonaj(item.KategoriAdi,item.BirimAdi,item.Adet,item.Miktar,item.En,item.Boy,item.Kenar)
            cekiList.append(model)

            sira += 1

        schema = SiparisCekiSchema(many=True)

        return schema.dump(cekiList)

    def __getTonaj(self,kategori,birim,adet,miktar,en,boy,kenar):
        tonaj = 0
        
        if(birim == 'M2'):
            if(en == 'VAR' or en == 'Var' or boy=='Free' or boy == 'FREE' or en == 'Various' or en == 'VARIOUS' or en == 'SLAB' or en == 'Slab' or en=='Other' or boy== 'Other' or en == 'OZEL' or boy == 'OZEL' or boy == 'Various' or en =='1 LT' or boy=='VAR' or boy=='Var' or en == 'özel' or en  =='ozel' or en == None or boy == None or kenar == None or kenar == 'özel' or kenar == 'ozel'):
                pass
            else:
                
                tonaj = self.__getKategoriKatsayisi(kategori) * float(str(kenar).replace(',','.')) * float(str(miktar).replace(',','.')) * 10
        elif (birim == 'Adet'):
            if(en=='1 LT' or en == None or en == 'VAR' or en == 'Var' or boy=='Free' or boy == 'FREE' or en == 'Various' or en == 'VARIOUS' or en == 'SLAB' or en == 'Slab' or en=='Other' or boy== 'Other' or en == 'OZEL' or boy == 'OZEL' or boy == 'Various' or kenar =='Various' or en=='1 LT' or boy=='VAR' or boy=='Var' or en == 'özel' or en  =='ozel' or en == None or boy == None or kenar == 'özel' or kenar == 'ozel'):
                pass
            else:
                m2 = (float(str(en).replace(',','.')) * float(str(boy).replace(',','.')) * float(str(adet).replace(',','.'))) / 10000
                tonaj = self.__getKategoriKatsayisi(kategori) * float(str(kenar).replace(',','.')) * m2 * 10
        else:
            tonaj = 0
            
            
            
        return tonaj
            
            
    def __getKategoriKatsayisi(self,kategori):
        kategori1 = kategori.split(' ')[0]
        if(kategori1 == 'Travertine'):
            return 2.4
        elif (kategori1 == 'Marble'):
            return 2.75
        elif (kategori1 == 'Limestone'):
            return 2.5
        else:
            return 0
        
    def __getAdetHesaplama(self,en,boy,miktar):
        if(
            en=='VAR' or
            en == 'Var' or
            en == 'Various' or
            en == 'VARIOUS' or
            en == 'ANT' or
            en =='Free' or
            en =='FREE' or
            en == 'Slabs' or
            en == 'Slab' or
            en == 'SLAB' or
            en == 'SLABS' or
            en == '1 LT' or
            en == 'Crazy' or
            boy == 'Free' or
            boy == 'FREE' or
            boy == 'Set' or
            boy == 'SET'  or
            boy == 'VAR' or
            en == 'Fr' or
            en == 'FR' or
            boy == 'Fr' or
            boy == 'FR' or
            en == 'özel' or
            en == 'ozel' or 
            en == 'Mini' or
            boy == 'Mini'
        ):
            return 0
        else:
            return int(float(str(miktar).replace(',','.')) / (float(str(en).replace(',','.'))/100) / (float(str(boy).replace(',','.'))/100))
    
    def __getM2Hesaplama(self,en,boy,miktar):
        if(
            en=='VAR' or
            en == 'Var' or
            en == 'Various' or
            en == 'VARIOUS' or
            en == 'ANT' or
            en =='Free' or
            en =='FREE' or
            en == 'Slabs' or
            en == 'Slab' or
            en == 'SLAB' or
            en == 'SLABS' or
            en == '1 LT' or
            en == 'Crazy' or
            boy == 'Free' or
            boy == 'FREE' or
            boy == 'Set' or
            boy == 'SET' or
            boy == 'VAR' or
            boy=='Various' or
            boy =='Var' or
            boy =='VARIOUS' or
            boy=='Other' or
            boy =='OTHER' or
            en =='Other' or
            en =='OTHER' or
            en == None or
            boy == None or
            miktar == None or
            en == 'Fr' or
            en == 'FR' or
            boy == 'Fr' or
            boy == 'FR' or
            en == 'özel' or
            en == 'ozel'
        ):
            return 0
        else:
            return round(float(float(str(miktar).replace(',','.')) * (float(str(en).replace(',','.'))/100) * (float(str(boy).replace(',','.'))/100)),2)
    
    
