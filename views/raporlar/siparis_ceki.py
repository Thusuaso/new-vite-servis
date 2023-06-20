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
            model.adet = item.Adet 
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
            model.tonaj = self.__getTonaj(item.KategoriAdi,item.BirimAdi,item.Adet,item.Miktar,item.En,item.Boy,item.Kenar)
            cekiList.append(model)

            sira += 1

        schema = SiparisCekiSchema(many=True)

        return schema.dump(cekiList)

    def __getTonaj(self,kategori,birim,adet,miktar,en,boy,kenar):
        tonaj = 0
        if(birim == 'M2'):
            tonaj = self.__getKategoriKatsayisi(kategori) * float(str(kenar).replace(',','.')) * float(str(miktar).replace(',','.')) * 10
        elif (birim == 'Adet'):
            if(en == 'VAR' or en == 'Var' or boy=='Free' or boy == 'FREE' or en == 'Various' or en == 'VARIOUS' or en == 'SLAB' or en == 'Slab' or en=='Other' or boy== 'Other'):
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
    
